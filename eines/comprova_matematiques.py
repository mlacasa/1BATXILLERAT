"""Proves d'invariants matemàtics i regressions, sense executar les figures."""
import ast
from pathlib import Path
import json
import math
from decimal import Decimal, localcontext
from fractions import Fraction
import re
import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def functions(filename):
    namespace = dict(math=math, np=np, pd=pd, re=re, Fraction=Fraction, Decimal=Decimal, localcontext=localcontext)
    nb = json.loads((ROOT / filename).read_text(encoding="utf-8"))
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            source = cell["source"]
            tree = ast.parse(source if isinstance(source, str) else "".join(source))
            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    exec(compile(ast.Module(body=[node], type_ignores=[]), filename, "exec"), namespace)
    return namespace


def laboratory(filename):
    namespace = functions(filename)
    nb = json.loads((ROOT / filename).read_text(encoding="utf-8"))
    for cell in nb["cells"]:
        source = "".join(cell["source"])
        if cell["cell_type"] == "code" and source.startswith("titol_laboratori ="):
            exec(compile(source, filename, "exec"), namespace)
    return namespace


class Mathematics(unittest.TestCase):
    def test_animated_bisection_preserves_exact_bracket(self):
        ns = laboratory("Q_conjunt_dens.ipynb")
        for step in ns["fotogrames_laboratori"]:
            a, b, m, (c, d) = ns["estat_biseccio"](step)
            self.assertLess(a*a, 2)
            self.assertLess(2, b*b)
            self.assertLess(c*c, 2)
            self.assertLess(2, d*d)
            self.assertEqual(d-c, (b-a)/2)
            self.assertEqual(m, (a+b)/2)

    def test_pi_educational_error_thresholds(self):
        f = functions("Càlcul_Nombre_pi.ipynb")["dades_poligon"]
        self.assertEqual(next(n for n in range(3, 301) if math.pi-f(n)["pi_aprox"] < .001), 72)
        arch = functions("NumeroPi.ipynb")["arquimedes"]
        self.assertEqual(next(n for n, a, b in arch(9) if (b-a)/2 < Decimal(".0001")), 384)

    def test_dedekind_animation_uses_exact_square_comparison(self):
        ns = laboratory("04_Talladures_Dedekind.ipynb")
        for q in ns["candidats_tall"]:
            self.assertNotEqual(q*q, 2)
            self.assertEqual(q*q < 2, ns["pertany_inferior"](q, "arrel2"))

    def test_cauchy_animation_counterexample_persists(self):
        ns = laboratory("05_Successions_Cauchy.ipynb")
        for n in ns["fotogrames_laboratori"]:
            da, block_a, dh, block_h = ns["distancies_cauchy"](n)
            self.assertLessEqual(block_h, 1)
            self.assertGreaterEqual(block_h, .5)
            self.assertAlmostEqual(da, 1/n-1/(n+1))
            self.assertAlmostEqual(block_a, 1/n-1/(2*n))
            self.assertAlmostEqual(dh, 1/(n+1))

    def test_suprem_candidate_is_exceeded_at_21(self):
        f = laboratory("06_Completesa_R.ipynb")["estat_suprem"]
        self.assertFalse(f(20)[2])
        self.assertTrue(f(21)[2])
        for n in (1, 2, 100, 1001):
            m, d, _ = f(n)
            self.assertEqual(m+d, 1)
            self.assertGreater(d, 0)

    def test_limits_frames_keep_distinct_lateral_limits(self):
        ns = laboratory("07_Limits_Continuitat.ipynb")
        for step in ns["fotogrames_laboratori"]:
            h, left, right, jump_left, jump_right = ns["estat_limits"](step)
            self.assertGreater(h, 0)
            self.assertLess(left, 2)
            self.assertGreater(right, 2)
            self.assertEqual((jump_left, jump_right), (-1, 1))

    def test_derivative_slopes_approach_from_both_sides(self):
        ns = laboratory("Derivades_BAT.ipynb")
        for step in ns["fotogrames_laboratori"]:
            h, right, left = ns["estat_derivada"](step)
            self.assertAlmostEqual(right, 2+h, places=11)
            self.assertAlmostEqual(left, 2-h, places=11)

    def test_slope_triangles_preserve_ratio_and_intercept(self):
        f = laboratory("LaRecta.ipynb")["dades_rampa"]
        for m in (-2, -.5, 0, 2/3, 2):
            for dx in (1, 2, 6):
                dy, y = f(m, dx, b=3)
                self.assertAlmostEqual(dy/dx, m)
                self.assertAlmostEqual(y-dy, 3)

    def test_complex_animation_rotation_and_dilation(self):
        f = laboratory("ComplexNumbers.ipynb")["gira_complex"]
        for angle in range(0, 361, 15):
            w, z = f(2+1j, angle)
            self.assertAlmostEqual(abs(w), 1)
            self.assertAlmostEqual(abs(z), math.sqrt(5))
        self.assertAlmostEqual(abs(f(2+1j, 90)[1]-(-1+2j)), 0)
        self.assertAlmostEqual(abs(f(2+1j, 90, 2)[1]-(-2+4j)), 0)

    def test_one_outlier_changes_mean_but_not_median(self):
        ns = laboratory("AnálisisUnivariante(I).ipynb")
        f = ns["resum_temps"]
        initial = f(15)[1]
        for value in (15, 30, 36, 60):
            data, mean, median = f(value)
            self.assertEqual(len(data), 21)
            self.assertAlmostEqual(mean-initial, (value-15)/21)
            self.assertEqual(median, 12)

    def test_data_animation_preserves_each_source_cell(self):
        ns = laboratory("PràcticaBasedeDades.ipynb")
        self.assertEqual(len(ns["mini_llarg"]), 12)
        seen = set()
        for step in ns["fotogrames_laboratori"]:
            pos, column, row = ns["origen_registre"](step)
            self.assertEqual(ns["mini_ample"].iloc[pos][column], row["value"])
            self.assertEqual(ns["mini_ample"].iloc[pos]["ID"], row["rank"])
            seen.add((pos, column))
        self.assertEqual(len(seen), 12)

    def test_pi_all_polygons_to_300(self):
        f = functions("Càlcul_Nombre_pi.ipynb")["dades_poligon"]
        self.assertAlmostEqual(f(3)["base"], math.sqrt(3), places=13)
        self.assertAlmostEqual(f(4)["base"], math.sqrt(2), places=13)
        self.assertAlmostEqual(f(6)["pi_aprox"], 3.0, places=13)
        self.assertAlmostEqual(f(12)["base"], math.sqrt(2-math.sqrt(3)), places=13)
        previous = 0.0
        for n in range(3, 301):
            d = f(n)
            self.assertAlmostEqual(d["pi_aprox"], n*math.sin(math.pi/n), delta=2e-11)
            self.assertGreater(d["pi_aprox"], previous)
            self.assertLess(d["pi_aprox"], math.pi)
            self.assertAlmostEqual(f(n, radi=3)["pi_aprox"], d["pi_aprox"], places=13)
            previous = d["pi_aprox"]
        self.assertLess(math.pi-previous, 0.000058)

    def test_pi_calculation_does_not_use_known_pi(self):
        f = functions("Càlcul_Nombre_pi.ipynb")["dades_poligon"]
        expected = f(300)["pi_aprox"]
        with patch.object(math, "pi", 0.0), patch.object(np, "pi", 0.0), \
             patch.object(math, "sin", side_effect=AssertionError("No sinus predefinit")):
            self.assertEqual(f(300)["pi_aprox"], expected)

    def test_pi_polygon_input_bounds(self):
        f = functions("Càlcul_Nombre_pi.ipynb")["dades_poligon"]
        for n in (2, 301, 6.5, True):
            with self.assertRaises(ValueError):
                f(n)
        for radi in (0, -1, float("inf"), float("nan")):
            with self.assertRaises(ValueError):
                f(6, radi=radi)

    def test_midpoints_are_exact_and_independent(self):
        f = functions("Q_conjunt_dens.ipynb")["punts_mitjans"]
        a = f(passos=80)
        self.assertEqual(a[-1], 1-Fraction(1, 2**80))
        self.assertEqual(f(passos=10), f(passos=10))
        self.assertEqual(f("2/7", "5/9", 3)[-1], Fraction(5, 9)-(Fraction(5, 9)-Fraction(2, 7))/8)
        with self.assertRaises(ValueError): f("1", "0")

    def test_bisection_brackets_and_widths(self):
        f = functions("Q_conjunt_dens.ipynb")["intervals_arrel2"]
        prev = (Fraction(1), Fraction(2))
        for k, (a, b) in enumerate(f(100)):
            self.assertLess(a*a, 2)
            self.assertGreater(b*b, 2)
            self.assertEqual(b-a, Fraction(1, 2**k))
            self.assertLessEqual(prev[0], a)
            self.assertLessEqual(b, prev[1])
            prev = a, b

    def test_archimedes_geometric_values(self):
        f = functions("NumeroPi.ipynb")["arquimedes"]
        prev = None
        for n, a, b in f(16):
            self.assertLess(a, b)
            self.assertAlmostEqual(float(a), n*math.sin(math.pi/n), places=12)
            self.assertAlmostEqual(float(b), n*math.tan(math.pi/n), places=12)
            if prev:
                self.assertLess(prev[0], a)
                self.assertLess(b, prev[1])
                self.assertLess(b-a, (prev[1]-prev[0])/2)
            prev = a, b

    def test_exact_square_root_enclosures(self):
        f = functions("NumeroPi.ipynb")["arrel_racional_acotada"]
        for q in (Fraction(0), Fraction(4), Fraction(3), Fraction(2, 7), Fraction(1234567, 891)):
            for bits in (2, 20, 80):
                a, b = f(q, bits)
                self.assertLessEqual(a*a, q)
                self.assertGreaterEqual(b*b, q)
                self.assertLessEqual(b-a, Fraction(1, 2**bits))

    def test_certified_pi_and_stop(self):
        ns = functions("NumeroPi.ipynb")
        reference = Fraction("3.14159265358979323846264338327950288419716939937510")
        for _, a, b in ns["arquimedes_certificat"](18):
            self.assertLess(a, reference)
            self.assertGreater(b, reference)
        _, a, b = ns["arquimedes_certificat"](4)[-1]
        self.assertLess(Fraction(223, 71), a)
        self.assertLess(b, Fraction(22, 7))
        for tolerance in (Fraction(1, 1000), Fraction(1, 10**6), Fraction(1, 10**9)):
            _, a, b = ns["pi_amb_tolerancia"](tolerance)
            self.assertLess((b-a)/2, tolerance)
        with self.assertRaises(ValueError): ns["pi_amb_tolerancia"](Fraction(1, 10**30), maxim=2)

    def test_dedekind_no_maximum_witness(self):
        ns = functions("04_Talladures_Dedekind.ipynb")
        self.assertTrue(ns["pertany_inferior"](-3))
        self.assertFalse(ns["pertany_inferior"](Fraction(10, 7)))
        for d in range(1, 45):
            for n in range(-5, 2*d):
                q = Fraction(n, d)
                if ns["pertany_inferior"](q):
                    r = ns["mes_gran_dins_A"](q)
                    self.assertGreater(r, q)
                    self.assertTrue(ns["pertany_inferior"](r))

    def test_harmonic_counterexample_exact(self):
        for n in (1, 2, 10, 100):
            block = sum((Fraction(1, k) for k in range(n+1, 2*n+1)), Fraction(0))
            self.assertGreaterEqual(block, Fraction(1, 2))

    def test_derivative_sides_and_stability(self):
        f = functions("Derivades_BAT.ipynb")["pendent_secant"]
        self.assertEqual(f("quadratica", 1, 1e-17), 2)
        self.assertEqual(f("absolut", 0, .001), 1)
        self.assertEqual(f("absolut", 0, -.001), -1)
        self.assertGreater(f("arrel_cubica", 0, 1e-6), f("arrel_cubica", 0, 1e-3))
        with self.assertRaises(ValueError): f("quadratica", 1, 0)

    def test_statistics_maxima_and_constant_data(self):
        f = functions("AnálisisUnivariante(I).ipynb")["taula_frequencies"]
        for data in ([18, 19, 20], [20, 20, 20], [1], [-5, 0, 5, 5]):
            table, edges = f(data, 2)
            self.assertEqual(table["Freqüència"].sum(), len(data))
            np.testing.assert_array_equal(table["Freqüència"], np.histogram(data, edges)[0])
        with self.assertRaises(ValueError): f([])
        with self.assertRaises(ValueError): f([1, float("nan")])

    def test_complex_quadrants_and_zero(self):
        f = functions("ComplexNumbers.ipynb")["dades_complex"]
        self.assertEqual(f(0), (0, None))
        self.assertAlmostEqual(f(-1+1j)[1], 3*math.pi/4)
        self.assertAlmostEqual(f(1j)[1], math.pi/2)

    def test_data_reshape_preserves_meaning_after_shuffle(self):
        ns = functions("PràcticaBasedeDades.ipynb")
        wide = ns["dades_demostracio"](files=10, anys=[2020, 2025])
        expected, _ = ns["format_llarg"](wide)
        actual, _ = ns["format_llarg"](wide[wide.columns[::-1]])
        keys = ["rank", "year", "category"]
        pd.testing.assert_frame_equal(expected.sort_values(keys).reset_index(drop=True),
                                      actual.sort_values(keys).reset_index(drop=True))
        self.assertEqual(len(actual), 60)
        self.assertEqual(expected.query("rank == 1 and year == 2020 and category == 'Salary'")["value"].iloc[0], wide["2020"].iloc[0])
        sample = pd.DataFrame({"ID": [1], "2020": ["1,234"], "2020.3": [9]})
        result, ignored = ns["format_llarg"](sample, True)
        self.assertEqual(result["value"].iloc[0], 1234)
        self.assertEqual(ignored, ["2020.3"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
