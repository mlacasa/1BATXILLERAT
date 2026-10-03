"""Executa cada notebook amb un nucli nou; comprova també els callbacks dels controls."""
import argparse
import base64
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import platform
import sys
import tempfile
import time
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

ROOT = Path(__file__).resolve().parents[1]
CALLS = {
    "Q_conjunt_dens.ipynb": "dibuixa_racionals(15)\nlaboratori_biseccio(12)",
    "Càlcul_Nombre_pi.ipynb": "poligons(0)\npoligons(4)\nexplora_aproximacio(3)\nexplora_aproximacio(300)\ndibuixa_triangle(12)",
    "NumeroPi.ipynb": "taula_arquimedes(10)",
    "04_Talladures_Dedekind.ipynb": "dibuixa_tall(20, 'arrel2')\ndibuixa_tall(20, 'racional')",
    "05_Successions_Cauchy.ipynb": "laboratori_cauchy('inversa', 100, 30, .02)\nlaboratori_cauchy('harmonica', 100, 100, .5)\nlaboratori_cauchy('alternant', 20, 30, 1.)",
    "06_Completesa_R.ipynb": "suprem_mostra(80)\ncompara_intervals(8)",
    "07_Limits_Continuitat.ipynb": "bandes(.2, .1, 3.)\nbandes(.1, .3, 2.)",
    "Derivades_BAT.ipynb": "secant('quadratica', 1, 3, 1)\nsecant('absolut', 0, 3, -1)\nsecant('arrel_cubica', 0, 4, 1)",
    "LaRecta.ipynb": "recta(-2, 3)\nrecta(0, 1)",
    "ComplexNumbers.ipynb": "pla_complex(-1, 1)\npla_complex(0, 0)",
    "AnálisisUnivariante(I).ipynb": "histograma(1)\nhistograma(15)",
    "PràcticaBasedeDades.ipynb": "grafic_dades(2022, 'employees')",
}

FORMATIVE_CHECKS = '''
assert len(preguntes_taller) == 3
for numero, q in enumerate(preguntes_taller, 1):
    assert len(q["opcions"]) == len(q["retorn"]) == 3
    for index in range(3):
        resposta = feedback_resposta(numero, chr(65+index))
        assert resposta["correcte"] == (index == q["correcta"])
        assert len(resposta["explicacio"]) > 20
for numero, lletra in [(0, "A"), (4, "A"), (1, ""), (1, "Z"), (True, "A")]:
    try:
        feedback_resposta(numero, lletra)
    except ValueError:
        pass
    else:
        raise AssertionError("Una resposta no vàlida no s'ha rebutjat.")
if panell_comparacio is not None:
    panell_comparacio.update()
if autoavaluacio is not None:
    assert all(control.value is None for control in autoavaluacio["selectors"])
    autoavaluacio["boto"].click()
    for control, pregunta in zip(autoavaluacio["selectors"], preguntes_taller):
        control.value = chr(65+pregunta["correcta"])
    autoavaluacio["boto"].click()
    for control, pregunta in zip(autoavaluacio["selectors"], preguntes_taller):
        control.value = chr(65+(pregunta["correcta"]+1)%3)
    autoavaluacio["boto"].click()
    # L'edició de l'alumne es desa sense respostes preseleccionades ni retorn de prova.
    for control in autoavaluacio["selectors"]:
        control.value = None
    autoavaluacio["sortida"].clear_output()
'''


def hidden_errors(value):
    if isinstance(value, dict):
        if value.get("output_type") == "error":
            yield f"{value.get('ename')}: {value.get('evalue')}"
        for child in value.values(): yield from hidden_errors(child)
    elif isinstance(value, list):
        for child in value: yield from hidden_errors(child)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--figures", type=Path, help="Directori opcional per revisar els PNG de sortida")
    parser.add_argument("--only", help="Valida només aquest fitxer")
    parser.add_argument("--save-outputs", action="store_true",
                        help="Desa les figures i animacions executades al quadern, sense les cel·les de prova")
    args = parser.parse_args()
    if args.figures: args.figures.mkdir(parents=True, exist_ok=True)
    report = {"python": platform.python_version(), "platform": platform.system(),
              "packages": {p: version(p) for p in ("numpy", "matplotlib", "pandas", "ipywidgets", "nbformat", "nbclient", "ipykernel")},
              "method": "Nucli nou per quadern, validació nbformat, execució seqüencial i callbacks explícits; sense navegador Colab.",
              "notebooks": []}
    with tempfile.TemporaryDirectory(prefix="quaderns-kernel-") as tmp:
        kernel_dir = Path(tmp) / "python3"
        kernel_dir.mkdir()
        (kernel_dir / "kernel.json").write_text(json.dumps({
            "argv": [sys.executable, "-m", "ipykernel_launcher", "--log-level=ERROR", "-f", "{connection_file}"],
            "display_name": "Python de validació", "language": "python"}), encoding="utf-8")
        for path in sorted(ROOT.glob("*.ipynb")):
            if args.only and path.name != args.only: continue
            started = time.monotonic()
            nb = nbformat.read(path, as_version=4)
            nbformat.validate(nb)
            # Executa els controls també com a funcions: els errors no poden quedar amagats al widget.
            nb.cells.append(nbformat.v4.new_code_cell(CALLS[path.name] +
                "\nfotograma_laboratori(fotogrames_laboratori[0])" +
                "\nfotograma_laboratori(fotogrames_laboratori[-1])\n" + FORMATIVE_CHECKS + "\nplt.close('all')"))
            manager = KernelManager(kernel_name="python3", kernel_spec_manager=KernelSpecManager(kernel_dirs=[tmp]))
            client = NotebookClient(nb, km=manager, timeout=180,
                                    resources={"metadata": {"path": str(ROOT)}})
            try:
                client.execute()
                errors = list(hidden_errors(nb))
                if errors: raise RuntimeError("; ".join(errors))
                animations = sum("Animation" in output.get("data", {}).get("text/html", "")
                                 for cell in nb.cells[:-1] for output in cell.get("outputs", []))
                if animations < 1: raise RuntimeError("No s'ha generat l'animació HTML del laboratori.")
                pictures = 0
                for i, cell in enumerate(nb.cells):
                    for j, output in enumerate(cell.get("outputs", [])):
                        png = output.get("data", {}).get("image/png")
                        if png:
                            pictures += 1
                            if args.figures:
                                (args.figures / f"{path.stem}_{i:02d}_{j:02d}.png").write_bytes(base64.b64decode(png))
                cell_count = len(nb.cells)-1
                if args.save_outputs:
                    nb.cells.pop()
                    nbformat.validate(nb)
                    nbformat.write(nb, path)
                entry = {"file": path.name, "status": "OK", "cells": cell_count,
                         "animations_html": animations, "outputs_saved": args.save_outputs,
                         "formative_questions": 3, "comparison_and_feedback_callbacks": "OK",
                         "figures_in_cells": pictures, "seconds": round(time.monotonic()-started, 2),
                         "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            except Exception as exc:
                entry = {"file": path.name, "status": "ERROR", "error": str(exc)}
            finally:
                if manager.has_kernel:
                    manager.shutdown_kernel(now=True)
            report["notebooks"].append(entry)
            print(entry["status"], path.name, flush=True)
            if entry["status"] == "ERROR": print(entry["error"], flush=True)
    if not report["notebooks"]: raise SystemExit("No s'ha trobat cap quadern per validar.")
    target = ROOT / ("VALIDACIO_PARCIAL.json" if args.only else "VALIDACIO.json")
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")
    if any(n["status"] != "OK" for n in report["notebooks"]): raise SystemExit(1)


if __name__ == "__main__":
    main()
