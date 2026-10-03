"""Genera els quaderns autònoms. Només biblioteca estàndard; no els executa."""
from pathlib import Path
import json
import textwrap

ROOT = Path(__file__).resolve().parents[1]


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": textwrap.dedent(text).strip() + "\n"}


def code(text):
    return {"cell_type": "code", "metadata": {}, "source": textwrap.dedent(text).strip() + "\n",
            "execution_count": None, "outputs": []}


SETUP = r'''
import math
from fractions import Fraction
from decimal import Decimal, localcontext
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, Markdown

plt.rcParams.update({"figure.figsize": (10, 4), "axes.grid": True,
                     "font.size": 11, "figure.dpi": 100})

def explora(funcio, **rangs):
    """Controls opcionals: la mateixa funció també es pot cridar directament."""
    try:
        import ipywidgets as widgets
    except ImportError:
        print("Sense controls: executem els paràmetres per defecte. Pots canviar-los a la crida.")
        return funcio()
    panell = widgets.interactive(funcio, **rangs)
    display(panell)
    return panell
'''

BISSECTION = r'''
def intervals_arrel2(passos=12):
    """Extrems racionals exactes. No calcula sqrt(2)."""
    if not isinstance(passos, int) or passos < 0:
        raise ValueError("El nombre de passos ha de ser un enter no negatiu.")
    a, b = Fraction(1), Fraction(2)
    intervals = [(a, b)]
    for _ in range(passos):
        m = (a + b) / 2
        if m * m < 2:
            a = m
        else:
            b = m
        intervals.append((a, b))
    return intervals
'''

ARCHIMEDES = r'''
def arquimedes(passos=8, precisio=60):
    """Semiperímetres calculats amb Decimal; les xifres tenen arrodoniment."""
    if not isinstance(passos, int) or passos < 0:
        raise ValueError("El nombre de passos ha de ser un enter no negatiu.")
    if not isinstance(precisio, int) or precisio < 16:
        raise ValueError("Calen almenys 16 xifres de precisió.")
    with localcontext() as ctx:
        ctx.prec = precisio
        n, inferior, superior = 6, Decimal(3), 2 * Decimal(3).sqrt()
        files = [(n, inferior, superior)]
        for _ in range(passos):
            nova_superior = 2 * inferior * superior / (inferior + superior)
            nova_inferior = (inferior * nova_superior).sqrt()
            n, inferior, superior = 2 * n, nova_inferior, nova_superior
            files.append((n, inferior, superior))
    return files
'''

CERTIFICATE = r'''
def arrel_racional_acotada(q, bits=80):
    """Interval diàdic que conté sqrt(q), amb enters i Fraction exclusivament."""
    q = Fraction(q)
    if q < 0 or not isinstance(bits, int) or bits < 1:
        raise ValueError("Cal q >= 0 i un nombre positiu de bits.")
    d = 2 ** bits
    m = math.isqrt(q.numerator * d * d // q.denominator)
    a = Fraction(m, d)
    b = a if a * a == q else Fraction(m + 1, d)
    return a, b

def arquimedes_certificat(passos=8, bits=80):
    """Acota cada operació: els extrems retornats són racionals exactes."""
    if not isinstance(passos, int) or passos < 0:
        raise ValueError("El nombre de passos ha de ser un enter no negatiu.")
    a, b = arrel_racional_acotada(3, bits)
    li = ls = Fraction(3)       # interval que conté el semiperímetre inscrit
    ui, us = 2 * a, 2 * b       # interval que conté el semiperímetre circumscrit
    files = [(6, li, us)]
    for k in range(passos):
        # La mitjana harmònica és creixent en cadascun dels arguments positius.
        vi = 2 * li * ui / (li + ui)
        vs = 2 * ls * us / (ls + us)
        ni = arrel_racional_acotada(li * vi, bits)[0]
        ns = arrel_racional_acotada(ls * vs, bits)[1]
        li, ls, ui, us = ni, ns, vi, vs
        files.append((6 * 2 ** (k + 1), li, us))
    return files
'''


def notebook(filename, title, objective, prior, duration, origin, cells, previous=None, following=None):
    intro = md(f"""
    # {title}

    **Matemàtiques · 1r de batxillerat**  
    **Autoria: Dr. Lacasa-Cazcarra · Any 2026**

    **Objectiu.** {objective}

    **Abans de començar:** {prior}  
    **Temps orientatiu:** {duration}. Hi ha activitats bàsiques i ampliacions opcionals.

    **Funcionament.** Executa les cel·les en ordre, des del començament. Primer fes una predicció,
    després experimenta i escriu una justificació. Els controls són opcionals: també pots
    modificar els arguments de les funcions i executar-les. Les figures representen mostres
    finites; les propietats infinites necessiten una demostració.

    **Procedència.** {origin}
    """)
    tail = md("**Navegació:** " + " · ".join(
        ([f"[Anterior]({previous})"] if previous else []) + ["[Índex i guia](README.md)"] +
        ([f"[Següent]({following})"] if following else [])))
    all_cells = [intro, code(SETUP)] + cells + [tail]
    for i, cell in enumerate(all_cells):
        cell["id"] = f"c{i:03d}"
    data = {"cells": all_cells, "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12"},
        "authors": [{"name": "Dr. Lacasa-Cazcarra"}], "edition_year": 2026,
        "colab": {"provenance": []}}, "nbformat": 4, "nbformat_minor": 5}
    (ROOT / filename).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")


def build():
    notebook("Q_conjunt_dens.ipynb", "01 · Racionals: densitat i nombres que falten",
        "Distingir la densitat de ℚ de la completesa de ℝ i construir aproximacions exactes.",
        "fraccions, desigualtats i potències", "1–2 sessions",
        "Reelaboració de Q_conjunt_dens.ipynb del repositori original.", [
        md(r'''
        ## 1. Predicció: podem esgotar els racionals d'un interval?
        Si $p<q$ són racionals, el punt mig $m=(p+q)/2$ també és racional i satisfà $p<m<q$.
        Repetir aquesta construcció dona infinits racionals entre $p$ i $q$.
        Aquesta és la **densitat** de l'ordre de ℚ. No afirma que tots els punts de la recta siguin racionals.

        Prediu els cinc primers resultats si comencem amb $[0,1]$ i conservem la meitat dreta.
        ''') ,
        code(r'''
        def punts_mitjans(p="0", q="1", passos=10):
            p, q = Fraction(p), Fraction(q)
            if p >= q or not isinstance(passos, int) or passos < 0:
                raise ValueError("Cal p < q i un nombre enter no negatiu de passos.")
            resultat = []
            for _ in range(passos):
                p = (p + q) / 2
                resultat.append(p)
            return resultat

        punts = punts_mitjans()
        for i, valor in enumerate(punts, 1):
            print(f"a_{i} = {valor}; distància a 1 = {1 - valor}")
        ''') ,
        md(r'''
        **Justificació.** Per inducció, $a_n=1-2^{-n}$ per a $n\ge1$. Per tant $a_n<1$ sempre,
        encara que la distància a 1 pugui ser tan petita com vulguem. Aquí el límit sí que és racional.

        Canvia els extrems per `"2/7"` i `"5/9"`. Escriu una fórmula general per a $a_n$.
        Fes servir cadenes o `Fraction(2, 7)`: `Fraction(0.1)` parteix d'un decimal binari ja arrodonit.
        ''') ,
        code(r'''
        def dibuixa_racionals(passos=6):
            punts = punts_mitjans(passos=passos)
            fig, ax = plt.subplots()
            ax.axhline(0, color="0.6")
            ax.scatter([float(p) for p in punts], np.zeros(len(punts)), color="#2563eb")
            ax.scatter([1], [0], facecolors="none", edgecolors="#dc2626", s=100, label="Límit: 1")
            ax.set(xlim=(-.05, 1.08), ylim=(-.1, .1), yticks=[], title="Punts mitjans: sempre queda un interval")
            ax.legend(); plt.show()
        panell = explora(dibuixa_racionals, passos=(1, 15, 1))
        ''') ,
        md(r'''
        ## 2. Busquem un nombre amb quadrat igual a 2
        A l'interval $[1,2]$, comparem $m^2$ amb 2. Si $m^2<2$, conservem $[m,b]$;
        si $m^2>2$, conservem $[a,m]$. **No necessitem conèixer el valor de l'arrel.**
        ''') , code(BISSECTION),
        code(r'''
        def laboratori_biseccio(passos=8):
            intervals = intervals_arrel2(passos)
            a, b = intervals[-1]
            print(f"a = {a}; b = {b}; amplada exacta = {b-a}")
            print(f"Comprovació exacta: a² < 2 < b²: {a*a < 2 < b*b}")
            fig, ax = plt.subplots()
            for k, (a, b) in enumerate(intervals):
                ax.plot([float(a), float(b)], [k, k], "o-", color="#2563eb")
            ax.set(xlabel="Extrems racionals", ylabel="Pas", title="Intervals encaixats per bisecció")
            plt.show()
        panell = explora(laboratori_biseccio, passos=(0, 16, 1))
        ''') ,
        md(r'''
        ## 3. Per què falta un racional?
        Suposem que $(p/q)^2=2$, amb $p,q$ enters primers entre si i $q\ne0$.
        Aleshores $p^2=2q^2$, de manera que $p$ és parell: $p=2r$.
        Substituint, $q^2=2r^2$, i $q$ també és parell. Això contradiu que $p/q$ sigui irreductible.

        Per tant, **cap racional té quadrat igual a 2**. Els intervals construïts tenen
        extrems racionals, però el punt que busquem no és racional. Més endavant justificarem
        l'existència d'aquest punt en ℝ mitjançant la completesa.

        ## Activitats
        1. Demostra que l'amplada després de $n$ biseccions és $2^{-n}$.
        2. Troba un nombre de passos que garanteixi una amplada inferior a $10^{-6}$.
        3. Explica per què executar un milió de passos no demostra la irracionalitat de l'arrel.
        4. **Ampliació:** adapta la bisecció a $x^2=3$ i a $x^2=9$. Quina diferència observes?

        <details><summary>Pistes i comprovació</summary>

        Cada pas divideix l'amplada per 2; 20 passos són suficients perquè $2^{-20}<10^{-6}$.
        A l'equació $x^2=9$ la solució positiva és racional. Cal tractar explícitament el cas
        d'igualtat si generalitzes l'algorisme. Per als punts mitjans,
        $a_n=q-(q-p)/2^n$.
        </details>
        ''')], following="Càlcul_Nombre_pi.ipynb")

    notebook("Càlcul_Nombre_pi.ipynb", "02 · Exhaurir el cercle: aproximacions a π",
        "Interpretar les aproximacions de π com dues cotes geomètriques que s'apropen.",
        "perímetres, Pitàgores i quadern 01", "1 sessió",
        "Reelaboració de Càlcul_Nombre_pi.ipynb; la visualització ja no depèn de GeoGebra.", [
        md(r'''
        ## 1. Una longitud corba entre dues longituds poligonals
        Treballem amb una circumferència de radi 1. Anomenem π la meitat de la seva longitud.
        Un polígon **inscrit** té els vèrtexs sobre la circumferència; un polígon **circumscrit**
        té els costats tangents. La comparació geomètrica dels perímetres dona
        $p_n<2\pi<P_n$. Per tant, els semiperímetres satisfan $L_n<\pi<U_n$.

        Acceptem aquí aquesta comparació geomètrica; no pretenem construir tota la teoria
        de la longitud de corbes. Prediu com canviaran les dues cotes en duplicar els costats.

        Per a l'hexàgon: el costat inscrit és 1, i Pitàgores dona el semiperímetre circumscrit
        $2\sqrt3$. Així, $3<\pi<2\sqrt3$. No cal conèixer cap decimal de π.
        ''') , code(ARCHIMEDES),
        code(r'''
        def poligons(iteracions=2):
            n, inferior, superior = arquimedes(iteracions)[-1]
            fig, (ax, bx) = plt.subplots(1, 2, figsize=(12, 4))
            # np.pi només orienta els punts del DIBUIX. No intervé en les cotes calculades.
            angles = np.linspace(0, 2*np.pi, n+1)
            t = np.linspace(0, 2*np.pi, 500)
            radi_exterior = 1 / np.cos(np.pi/n)
            ax.plot(np.cos(t), np.sin(t), color="0.2", label="Circumferència")
            ax.plot(np.cos(angles), np.sin(angles), color="#2563eb", label="Inscrit")
            ax.plot(radi_exterior*np.cos(angles+np.pi/n),
                    radi_exterior*np.sin(angles+np.pi/n), color="#d97706", label="Circumscrit")
            ax.set_aspect("equal"); ax.set_title(f"{n} costats"); ax.legend(fontsize=9)
            files = arquimedes(iteracions)
            for k, (_, a, b) in enumerate(files):
                bx.plot([float(a), float(b)], [k, k], "o-", color="#7c3aed")
            bx.set(xlabel="Semiperímetre", ylabel="Duplicacions", title="Cotes sobre la recta")
            plt.tight_layout(); plt.show()
            print(f"Cota inferior ≈ {inferior:.12f}; cota superior ≈ {superior:.12f}")
            print(f"Amplada aproximada: {superior-inferior:.4E}")
        panell = explora(poligons, iteracions=(0, 6, 1))
        ''') ,
        md(r'''
        ## 2. Què vol dir exhaurir?
        No acabem fent un polígon amb «infinits costats». Construïm una successió de
        polígons finits que deixa una diferència entre cotes tan petita com es vulgui.
        **En cap pas finit el polígon es converteix en la circumferència.**

        Les cotes anteriors s'han calculat amb una recurrència que estudiarem al quadern 03.
        Les funcions trigonomètriques només s'utilitzen per dibuixar. No serien una manera
        independent de descobrir π si introduíssim `np.pi` dins del càlcul del perímetre.

        ## 3. Del dibuix a una pregunta sobre ℝ
        La pantalla pot fer indistingibles dues corbes diferents. Per decidir si l'aproximació
        és bona, necessitem nombres: l'amplada $U_n-L_n$.
        Què garanteix que tots aquests intervals cada vegada més petits determinen un punt?
        Aquesta pregunta ens conduirà a la **completesa**.

        ## Activitats
        1. Explica la diferència entre «inscrit» i «circumscrit» amb un dibuix propi.
        2. Compara 6, 12, 24 i 96 costats. Es mouen les dues cotes en la mateixa direcció?
        3. Si $a<\pi<b$, justifica que usar $(a+b)/2$ dona un error menor que $(b-a)/2$.
        4. **Ampliació:** què passa si el radi és 3? Quina divisió cal fer als perímetres?

        <details><summary>Comprovació</summary>

        La cota inferior augmenta i la superior disminueix. Per a radi $r$, dividim els
        perímetres per $2r$. La distància del punt mig a qualsevol punt de l'interval
        és com a màxim la meitat de l'amplada.
        </details>
        ''')], previous="Q_conjunt_dens.ipynb", following="NumeroPi.ipynb")

    notebook("NumeroPi.ipynb", "03 · L'algorisme d'Arquimedes",
        "Calcular π mitjançant cotes, justificar la convergència i controlar l'error.",
        "quadern 02, radicals i desigualtats", "2 sessions; certificació opcional",
        "Reconstrucció de NumeroPi.ipynb. La integral es reserva per a un curs posterior.", [
        md(r'''
        ## 1. Duplicar costats sense conèixer π
        Partim de $L_6=3$ i $U_6=2\sqrt3$. En duplicar el nombre de costats:
        $$U_{2n}=\frac{2L_nU_n}{L_n+U_n},\qquad L_{2n}=\sqrt{L_nU_{2n}}.$$
        La primera expressió és la mitjana harmònica; la segona, una mitjana geomètrica.

        **D'on surten?** Si $s$ és mig costat inscrit i $c=\sqrt{1-s^2}$, els triangles
        rectangles donen $L_n=ns$ i $U_n=ns/c$. La bisecció de l'angle dona
        $U_{2n}=2ns/(1+c)$ i $L_{2n}=n\sqrt{2(1-c)}$.
        Substituint $L_n,U_n$ i usant $s^2=1-c^2$ obtenim les dues recurrències.
        No hem necessitat avaluar cap angle amb π.
        ''') , code(ARCHIMEDES),
        code(r'''
        def taula_arquimedes(passos=6):
            files = arquimedes(passos)
            print(f"{'Costats':>9} {'L aproximat':>18} {'U aproximat':>18} {'Amplada aprox.':>16}")
            for n, a, b in files:
                print(f"{n:9d} {a:18.12f} {b:18.12f} {b-a:16.5E}")
            fig, ax = plt.subplots()
            ax.semilogy(range(len(files)), [float(b-a) for _, a, b in files], "o-", color="#2563eb")
            ax.set(xlabel="Duplicacions", ylabel="Amplada (escala logarítmica)", title="Quant es redueix la incertesa?")
            plt.show()
        panell = explora(taula_arquimedes, passos=(0, 15, 1))
        ''') ,
        md(r'''
        ## 2. Una demostració que serveix per a tots els passos
        Escriu $0<a<b$, $v=2ab/(a+b)$ i $u=\sqrt{av}$.
        Comprova que $a<u<v<b$. Així, cada nou interval està dins de l'anterior.
        A més,
        $$0<v-u<v-a=\frac{a(b-a)}{a+b}<\frac{b-a}{2}.$$
        Per tant, després de $k$ duplicacions, l'amplada és menor que
        $(U_6-L_6)/2^k$, que tendeix a zero. Aquesta cota és suficient, encara que
        a la pràctica observem una reducció més ràpida.

        Si **assumim la completesa de ℝ**, els intervals tancats encaixats tenen un únic
        punt comú. La comparació geomètrica identifica aquest punt amb π.
        El quadern 06 justificarà el teorema dels intervals encaixats a partir del suprem.

        ## 3. Error geomètric i error de l'ordinador
        `Decimal` permet augmentar la precisió, però continua arrodonint. Les desigualtats
        matemàtiques exactes no es converteixen automàticament en certificats sobre decimals.
        A prop del límit de precisió, dues cotes poden coincidir a la pantalla.
        ''') ,
        code(r'''
        for precisio in (16, 32, 60):
            _, a, b = arquimedes(35, precisio)[-1]
            with localcontext() as ctx:
                ctx.prec = precisio
                print(f"Precisió {precisio}: amplada calculada = {b-a}")
        print("Una amplada decimal zero no significa que un polígon finit sigui un cercle.")
        ''') ,
        md(r'''
        ## 4. Ampliació: un interval certificat amb fraccions
        Per certificar cotes, acotem també les arrels. Si $d=2^b$ i
        $m=\lfloor d\sqrt q\rfloor$, aleshores $m/d\le\sqrt q\le(m+1)/d$.
        `math.isqrt` permet trobar aquest enter sense usar arrels de coma flotant.

        Propaguem els extrems inferiors i superiors perquè les operacions emprades són
        creixents per a arguments positius. El resultat és un interval racional que
        conté π, amb la justificació geomètrica anterior. La conversió a decimal només és una visualització.
        ''') , code(CERTIFICATE),
        code(r'''
        def pi_amb_tolerancia(tolerancia=Fraction(1, 10**6), maxim=20, bits=80):
            tolerancia = Fraction(tolerancia)
            if tolerancia <= 0:
                raise ValueError("La tolerància ha de ser positiva.")
            for n, a, b in arquimedes_certificat(maxim, bits):
                if (b-a)/2 < tolerancia:
                    return n, a, b
            raise ValueError("No s'ha assolit la tolerància: augmenta els passos i/o els bits.")

        n, a, b = pi_amb_tolerancia()
        print(f"Costats: {n}; punt mig aproximat: {float((a+b)/2):.12f}")
        print("Error < 10⁻⁶ certificat amb fraccions:", (b-a)/2 < Fraction(1, 10**6))
        print("Amplada aproximada:", float(b-a))
        # Comprovació exacta d'un interval racional conegut, sense usar math.pi:
        _, a96, b96 = arquimedes_certificat(4)[-1]
        print("Amb 96 costats: 223/71 < L ≤ π ≤ U < 22/7:",
              Fraction(223, 71) < a96 < b96 < Fraction(22, 7))
        ''') ,
        md(r'''
        ## Activitats
        1. Demostra $a<u<v<b$ i explica què significa al dibuix dels polígons.
        2. Demana errors inferiors a $10^{-3}$, $10^{-6}$ i $10^{-9}$ amb `Fraction`.
        3. Per què comparar amb `math.pi` no seria un criteri de parada independent?
        4. Explica per què aquest experiment no demostra la irracionalitat de π.
        5. **Ampliació:** redueix `bits`. Observa que afegir passos deixa de ser suficient
           per aconseguir qualsevol tolerància: també cal augmentar la precisió de les arrels.

        <details><summary>Pistes</summary>

        $v-a=a(b-a)/(a+b)>0$ i $b-v=b(b-a)/(a+b)>0$; si $a<v$, aleshores
        $a<\sqrt{av}<v$. El criteri de parada usa l'amplada, no el valor desconegut de π.
        Aproximar amb racionals és compatible tant amb un límit racional com amb un d'irracional.
        </details>
        ''')], previous="Càlcul_Nombre_pi.ipynb", following="04_Talladures_Dedekind.ipynb")

    notebook("04_Talladures_Dedekind.ipynb", "04 · Talladures de Dedekind",
        "Descriure un nombre a partir de l'ordre dels racionals i entendre una construcció de ℝ.",
        "quadern 01 i ordre de les fraccions", "1–2 sessions",
        "Quadern nou. Context: Dedekind, Continuïtat i nombres irracionals (1872).", [
        md(r'''
        ## 1. Un nombre pot separar la recta
        La talladura determinada per $3/2$ separa els racionals en
        $A=\{q\in\mathbb Q:q<3/2\}$ i $B=\{q\in\mathbb Q:q\ge3/2\}$.
        En aquesta convenció, la part inferior **no té màxim**. La part superior sí que té
        mínim: $3/2$. Dibuixa alguns elements de cada part abans d'executar.

        Per construir la talladura que representarà $\sqrt2$, no l'hem d'usar com a entrada:
        $$A=\{q\in\mathbb Q:q<0\ \text{o}\ q^2<2\},\qquad B=\mathbb Q\setminus A.$$
        ''') ,
        code(r'''
        def pertany_inferior(q, tall="arrel2"):
            q = Fraction(q)
            if tall == "racional":
                return q < Fraction(3, 2)
            if tall == "arrel2":
                return q < 0 or q*q < 2
            raise ValueError("Tall desconegut.")

        def dibuixa_tall(denominador=12, tall="arrel2"):
            punts = [Fraction(i, denominador) for i in range(-denominador, 2*denominador+1)]
            a = [q for q in punts if pertany_inferior(q, tall)]
            b = [q for q in punts if not pertany_inferior(q, tall)]
            fig, ax = plt.subplots()
            ax.scatter([float(q) for q in a], np.zeros(len(a)), color="#2563eb", label="Part A")
            ax.scatter([float(q) for q in b], np.zeros(len(b)), color="#d97706", marker="x", label="Part B")
            ax.set(yticks=[], xlabel="Mostra finita de racionals", title="La classificació usa fraccions exactes")
            ax.legend(); plt.show()
            print("Màxim d'A dins de la mostra:", max(a))
            print("Això NO és un màxim del conjunt infinit A.")
        panell = explora(dibuixa_tall, denominador=(2, 40, 1), tall=["racional", "arrel2"])
        ''') ,
        md(r'''
        ## 2. Propietats que cal justificar
        Una talladura és una partició $\mathbb Q=A\cup B$, amb $A\cap B=\varnothing$,
        totes dues parts no buides, tot element d'A menor que qualsevol de B, i A sense màxim.

        En el cas de l'arrel de 2: $1\in A$, $2\in B$, i la monotonia del quadrat sobre
        els nombres no negatius justifica l'ordre. Falta demostrar que A no té màxim.
        El programa següent construeix un racional més gran dins d'A per a cada $q\in A$.
        ''') ,
        code(r'''
        def mes_gran_dins_A(q):
            q = Fraction(q)
            if not pertany_inferior(q):
                raise ValueError("Cal començar amb q dins d'A.")
            if q < 0:
                return Fraction(0)
            h = (2-q*q) / (2*(2*q+1))
            return q+h

        for q in [Fraction(-3), Fraction(0), Fraction(7,5), Fraction(1414,1000)]:
            r = mes_gran_dins_A(q)
            print(f"q={q}; r={r}; q<r i r∈A: {q < r and pertany_inferior(r)}")
        ''') ,
        md(r'''
        **Demostració.** Si $0\le q$ i $q^2<2$, prenem
        $h=(2-q^2)/(2(2q+1))$. Tenim $0<h\le1$ i
        $$2qh+h^2\le(2q+1)h=(2-q^2)/2<2-q^2.$$
        Per tant $(q+h)^2<2$ i $q+h\in A$. Si $q<0$, el racional 0 ja és més gran i és dins d'A.

        ## 3. Què estem construint?
        Una talladura racional representa un racional ja conegut. La talladura anterior
        representa un punt que no correspon a cap racional: ni A té màxim ni B té mínim.
        La construcció de Dedekind pren les talladures com a nombres reals i hi defineix
        l'ordre i les operacions. Aquí n'estudiem la idea; no desenvolupem tota la construcció del cos.

        **Ampliació: per què B no té mínim?** Per a $q\in B$ tenim $q>0$ i $q^2>2$.
        Prenent $h=(q^2-2)/(2q)$, el racional $r=q-h$ satisfà $0<r<q$ i
        $r^2=2+h^2>2$. Per tant $r\in B$.

        ## Activitats
        1. Classifica $-2$, $7/5$, $10/7$ i $3/2$ sense decimals.
        2. Explica per què no podem definir A només amb $q^2<2$: què passaria amb $-3$?
        3. Canvia 2 per 9. Quina part de la talladura té un extrem racional?
        4. Relaciona les dues parts amb els extrems dels intervals de bisecció del quadern 01.

        <details><summary>Comprovació</summary>

        $-2$ i $7/5$ són a A; $10/7$ i $3/2$ són a B. El nombre $-3$ ha d'estar
        a l'esquerra de la frontera, encara que el seu quadrat sigui més gran que 2.
        Per a l'arrel de 9, B té mínim 3. A continua sense màxim.
        </details>

        **Lectura:** [Dedekind, Continuidad y números irracionales](https://www.uv.es/jkliment/Documentos/Dedekind.pc.pdf).
        La lectura és complementària; el quadern s'executa sense connexió a aquest document.
        ''')], previous="NumeroPi.ipynb", following="05_Successions_Cauchy.ipynb")

    notebook("05_Successions_Cauchy.ipynb", "05 · Successions i criteri de Cauchy",
        "Distingir convergència, acotació i condició de Cauchy, i precisar els quantificadors.",
        "successions elementals i quadern 01", "2 sessions",
        "Quadern nou del recorregut de fonaments.", [
        md(r'''
        ## 1. Apropar-se a un límit o apropar-se entre si
        $a_n\to L$ significa:
        $$\forall\varepsilon>0\ \exists N\ \forall n\ge N:\ |a_n-L|<\varepsilon.$$
        Una successió és **de Cauchy** si:
        $$\forall\varepsilon>0\ \exists N\ \forall m,n\ge N:\ |a_m-a_n|<\varepsilon.$$
        La segona definició no necessita conèixer L. L'índex N pot dependre d'ε,
        però ha de servir per a **tots dos índexs** m i n de la cua infinita.

        Prediu què passarà amb $1/n$, $(-1)^n$ i les sumes harmòniques.
        ''') ,
        code(r'''
        def valors_successio(tipus, maxim):
            n = np.arange(1, maxim+1)
            if tipus == "inversa":
                return 1/n
            if tipus == "alternant":
                return (-1.0)**n
            if tipus == "harmonica":
                return np.cumsum(1/n)
            raise ValueError("Successió desconeguda.")

        def laboratori_cauchy(tipus="inversa", N=10, finestra=60, epsilon=0.2):
            valors = valors_successio(tipus, N+finestra-1)
            cua = valors[N-1:]
            diametre = float(np.max(cua)-np.min(cua))
            fig, (ax, bx) = plt.subplots(1, 2, figsize=(12, 4))
            ax.plot(np.arange(N, N+finestra), cua, ".", color="#2563eb")
            ax.axhspan(cua[0]-epsilon, cua[0]+epsilon, alpha=.15, color="#16a34a")
            ax.set(xlabel="n", ylabel="aₙ", title="Finestra finita de la cua")
            distancies = np.abs(cua[:, None]-cua[None, :])
            im = bx.imshow(distancies, origin="lower", aspect="auto", cmap="viridis")
            bx.set(xlabel="Índex dins la finestra", ylabel="Índex dins la finestra", title="Distàncies |aₘ − aₙ|")
            fig.colorbar(im, ax=bx); plt.tight_layout(); plt.show()
            print(f"Diàmetre mostrat = {diametre:.6g}; ε = {epsilon}")
            print("Totes les parelles MOSTRADES compleixen la desigualtat:", diametre < epsilon)
            print("Una comprovació finita no certifica una cua infinita.")
        panell = explora(laboratori_cauchy, tipus=["inversa", "alternant", "harmonica"],
                         N=(1, 300, 1), finestra=(10, 150, 10), epsilon=(.01, 2.1, .01))
        ''') ,
        md(r'''
        ## 2. Tres justificacions, no només tres gràfiques
        **$1/n$:** si $m,n\ge N$, $|1/m-1/n|<1/N$. Escollint $N>1/\varepsilon$,
        la successió és de Cauchy i convergeix a 0.

        **$(-1)^n$:** per a qualsevol N hi ha índexs parells i senars més grans que N,
        amb distància 2. Prenent ε=1 refutem la condició de Cauchy. Estar acotada no basta.

        **Harmònica:** els salts consecutius $H_{n+1}-H_n=1/(n+1)$ tendeixen a zero, però
        $$H_{2n}-H_n=\sum_{k=n+1}^{2n}\frac1k\ge n\frac1{2n}=\frac12.$$
        Per a ε=1/2, cap N serveix. Per això «els termes consecutius s'apropen» no és el criteri de Cauchy.
        ''') ,
        code(r'''
        for n in (10, 100, 1000, 10000):
            bloc = np.sum(1 / np.arange(n+1, 2*n+1))
            print(f"n={n:5}: salt consecutiu ≈ {1/(n+1):.7f}; H₂ₙ−Hₙ ≈ {bloc:.7f}")
        ''') , code(BISSECTION),
        code(r'''
        intervals = intervals_arrel2(20)
        aproximacions = [(a+b)/2 for a, b in intervals]
        for n in (2, 5, 10, 20):
            a, b = intervals[n]
            print(f"n={n}: terme racional {aproximacions[n]}; amplada exacta {b-a}")
        ''') ,
        md(r'''
        ## 3. De Cauchy en ℚ, però sense límit en ℚ
        Els punts mitjans $c_n$ dels intervals de bisecció són racionals.
        Si $m,n\ge N$, tots dos són dins $[a_N,b_N]$, de manera que
        $|c_m-c_n|\le2^{-N}$. Escollint $2^{-N}<\varepsilon$, demostrem que són de Cauchy.

        Si tinguessin un límit racional r, les desigualtats $a_n^2<2<b_n^2$ i l'amplada
        que tendeix a zero implicarien $r^2=2$, impossible pel quadern 01.
        En ℝ sí que convergeixen: aquest és el paper de la completesa.

        **Tota successió convergent és de Cauchy:** si a partir de N tots els termes són
        a menys d'ε/2 de L, la desigualtat triangular dona
        $|a_m-a_n|\le|a_m-L|+|L-a_n|<\varepsilon$.

        ## Activitats
        1. Escriu un N que serveixi per a $a_n=1/n$ quan ε=0,001.
        2. A la successió harmònica, augmenta N mantenint una finestra curta. Per què la
           pantalla pot suggerir una conclusió falsa? Torna a comparar n i 2n.
        3. Explica amb paraules pròpies la diferència entre «per a tot» i «existeix» en la definició.
        4. **Ampliació:** demostra que tota successió de Cauchy és acotada.

        <details><summary>Pistes</summary>

        N=1001 és suficient. Per a l'acotació, usa ε=1: tota la cua queda a distància
        menor que 1 d'un terme fix. Els termes anteriors són un conjunt finit, també acotat.
        Una finestra de longitud fixa pot ocultar distàncies grans entre índexs més separats.
        </details>
        ''')], previous="04_Talladures_Dedekind.ipynb", following="06_Completesa_R.ipynb")

    notebook("06_Completesa_R.ipynb", "06 · La completesa de ℝ",
        "Connectar suprem, intervals encaixats i successions de Cauchy sense raonaments circulars.",
        "quaderns 01–05", "2 sessions; demostracions avançades opcionals",
        "Quadern nou. Síntesi dels experiments d'Arquímedes, Dedekind i Cauchy.", [
        md(r'''
        ## 1. Màxim, cota superior i suprem
        Una **cota superior** de S és un nombre M tal que $s\le M$ per a tot $s\in S$.
        El **suprem** és la menor de les cotes superiors. Un **màxim** és un element de S
        que és més gran o igual que tots els altres; el suprem no ha de pertànyer a S.

        Per a $S=\{1-1/n:n\ge1\}$, 1 és el suprem però no és un màxim.
        Qualsevol llista finita dels primers termes sí que té màxim. No confonguis la mostra amb S.
        ''') ,
        code(r'''
        def suprem_mostra(termes=12):
            n = np.arange(1, termes+1)
            valors = 1-1/n
            fig, ax = plt.subplots()
            ax.plot(n, valors, "o", label="Mostra finita")
            ax.axhline(1, color="#dc2626", label="Suprem del conjunt infinit: 1")
            ax.set(xlabel="n", ylabel="1 − 1/n", title="El màxim de la mostra no és el suprem de S")
            ax.legend(); plt.show()
            print("Màxim exacte de la mostra:", 1-Fraction(1, termes))
        panell = explora(suprem_mostra, termes=(2, 100, 1))
        ''') ,
        md(r'''
        ## 2. El punt de partida lògic
        **Axioma de completesa:** tot subconjunt no buit de ℝ acotat superiorment té suprem en ℝ.

        El prenem com a propietat fonamental del sistema dels reals, juntament amb les
        propietats de cos ordenat. No el deduïm d'un gràfic ni d'un càlcul finit de π.
        La construcció per talladures és una altra manera de donar un model d'aquest sistema.

        **Propietat arquimediana.** Els naturals no estan acotats superiorment en ℝ.
        En efecte, si tinguessin suprem s, s−1 no seria cota superior: existiria un natural
        n>s−1, i llavors n+1>s, contradicció. Això justifica que $2^{-n}$ pot ser tan petit
        com vulguem. No confonguis aquesta propietat amb l'algorisme geomètric d'Arquímedes.

        ## 3. Del suprem als intervals encaixats
        Suposem $I_n=[a_n,b_n]$, no buits, tancats, amb $I_{n+1}\subseteq I_n$.
        El conjunt dels extrems inferiors és no buit i està acotat per $b_0$.
        Sigui $x=\sup\{a_n:n\ge0\}$.

        Per a cada n, $a_n\le x$. A més, $b_n$ és cota superior de **tots** els $a_k$:
        si $k\le n$, $a_k\le a_n\le b_n$; si $k\ge n$, $a_k\le b_k\le b_n$.
        Per tant $x\le b_n$ i $x\in I_n$ per a tot n.
        Si $b_n-a_n\to0$, dos punts comuns x,y haurien de satisfer
        $|x-y|\le b_n-a_n$ per a tot n; això obliga $x=y$.

        **Cal mirar les hipòtesis:** els intervals oberts $(0,1/n)$ són encaixats però no tenen
        cap punt comú. Els intervals tancats $[0,1]$ repetits tenen molts punts comuns,
        perquè la seva amplada no tendeix a zero.
        ''') , code(BISSECTION), code(ARCHIMEDES),
        code(r'''
        def compara_intervals(passos=6):
            racional = intervals_arrel2(passos)
            pi_intervals = arquimedes(passos)
            fig, axs = plt.subplots(1, 2, figsize=(12, 4))
            for k, (a, b) in enumerate(racional):
                axs[0].plot([float(a), float(b)], [k, k], "o-", color="#2563eb")
            for k, (_, a, b) in enumerate(pi_intervals):
                axs[1].plot([float(a), float(b)], [k, k], "o-", color="#d97706")
            axs[0].set_title("Bisecció: el punt comú no pertany a ℚ")
            axs[1].set_title("Arquímedes: el punt comú és π")
            for ax in axs: ax.set(xlabel="Extrems", ylabel="Pas")
            plt.tight_layout(); plt.show()
        panell = explora(compara_intervals, passos=(1, 12, 1))
        ''') ,
        md(r'''
        ## 4. Per què tota successió de Cauchy real convergeix? — Ampliació
        Una successió de Cauchy és acotada. Per a cada N considerem
        $$\alpha_N=\inf\{a_n:n\ge N\},\qquad \beta_N=\sup\{a_n:n\ge N\}.$$
        El suprem i l'ínfim existeixen per completesa (l'ínfim es dedueix aplicant el
        suprem als oposats). Els intervals $[\alpha_N,\beta_N]$ són tancats i encaixats.

        Per a cada ε>0, Cauchy dona una cua amb totes les distàncies menors que ε/2;
        per tant $\beta_N-\alpha_N\le\varepsilon/2<\varepsilon$.
        Les amplades tendeixen a zero. El teorema anterior dona un únic punt L i,
        com que tots els termes de la cua són dins l'interval, $a_n\to L$.

        **Esquema de les implicacions justificades aquí:**
        axioma del suprem → intervals encaixats → convergència de les successions de Cauchy.
        En ℝ aquestes són formulacions equivalents de la completesa; en aquest quadern
        hem demostrat les implicacions indicades, no tots els recíprocs.

        ## 5. Tornem al problema inicial
        L'algorisme d'Arquímedes proporciona intervals encaixats d'amplada que tendeix a zero.
        La completesa garanteix un únic real comú. La geometria identifica aquest real amb π.
        El quadern 01 mostra que els intervals racionals poden no contenir cap racional comú.

        ## Activitats
        1. Dona un conjunt que tingui suprem però no màxim, diferent de l'exemple inicial.
        2. Per què cal que els intervals siguin tancats? Justifica el cas $(0,1/n)$.
        3. Explica la funció de cadascuna d'aquestes idees: encaixament, amplada i completesa.
        4. Escriu cinc frases que connectin Arquímedes, Dedekind i Cauchy sense dir que
           un càlcul numèric finit demostra la completesa.

        <details><summary>Pistes</summary>

        $(0,1)$ té suprem 1 i no màxim. Si x>0, existeix n amb $1/n<x$, de manera que
        x no és a tots els $(0,1/n)$; 0 tampoc hi pertany. L'encaixament i la completesa
        proporcionen existència en el cas tancat; l'amplada que tendeix a zero proporciona unicitat.
        </details>
        ''')], previous="05_Successions_Cauchy.ipynb", following="07_Limits_Continuitat.ipynb")

    notebook("07_Limits_Continuitat.ipynb", "07 · De les successions als límits de funcions",
        "Interpretar límits laterals, la definició ε–δ i la continuïtat abans de derivar.",
        "quaderns 05–06 i funcions elementals", "1–2 sessions",
        "Quadern nou de transició al càlcul diferencial.", [
        md(r'''
        ## 1. Apropar-se al punt per camins diferents
        Per a $x\ne1$, $f(x)=(x^2-1)/(x-1)=x+1$. Encara que f no estigui definida a 1,
        els valors s'apropen a 2 quan x s'apropa a 1. El límit descriu el comportament
        **a prop del punt**, no necessàriament el valor en el punt.

        Calcula mentalment què passarà amb les successions $x_n=1+1/n$ i $y_n=1-1/n$.
        ''') ,
        code(r'''
        n = np.array([2, 10, 100, 1000, 10000])
        for k, dreta, esquerra in zip(n, 2+1/n, 2-1/n):
            print(f"n={k:5d}: f(1+1/n)≈{dreta:.6f}; f(1-1/n)≈{esquerra:.6f}")
        print("Hem usat l'expressió simplificada x+1 per evitar cancel·lació numèrica.")
        ''') ,
        md(r'''
        ## 2. La definició ε–δ
        $$\lim_{x\to a}f(x)=L\quad\Longleftrightarrow\quad
        \forall\varepsilon>0\ \exists\delta>0\ \forall x\text{ del domini}:\quad
        0<|x-a|<\delta\Rightarrow|f(x)-L|<\varepsilon.$$
        El 0< exclou el punt a. Per a $f(x)=x+1$, a=1 i L=2,
        $|f(x)-2|=|x-1|$, de manera que δ=ε serveix per a tots els punts del domini.
        ''') ,
        code(r'''
        def bandes(epsilon=.4, delta=.3, valor_punt=2.0):
            fig, ax = plt.subplots()
            x = np.linspace(0, 2, 401)
            ax.plot(x, x+1, color="#2563eb", label="f(x)=x+1 si x≠1")
            ax.axhspan(2-epsilon, 2+epsilon, color="#16a34a", alpha=.15, label="Banda ε")
            ax.axvspan(1-delta, 1+delta, color="#d97706", alpha=.15, label="Banda δ")
            ax.scatter([1], [2], facecolors="white", edgecolors="#2563eb", s=100, zorder=4)
            ax.scatter([1], [valor_punt], color="#dc2626", zorder=5, label="Valor assignat a f(1)")
            ax.set(xlabel="x", ylabel="f(x)", ylim=(-.5, 4.5), title="El límit no depèn del valor aïllat f(1)")
            ax.legend(fontsize=9); plt.show()
            print("La implicació per a TOTS els punts és vàlida si δ≤ε:", delta <= epsilon)
            print("La funció és contínua a 1 si f(1)=2:", valor_punt == 2)
        panell = explora(bandes, epsilon=(.05, 1., .05), delta=(.05, 1., .05), valor_punt=(0., 4., .5))
        ''') ,
        md(r'''
        ## 3. Dos límits laterals diferents impedeixen el límit
        Considerem $g(x)=-1$ si x<0 i $g(x)=1$ si x≥0.
        Les successions $1/n$ i $-1/n$ tendeixen a 0, però les imatges tendeixen a 1 i −1.
        Per tant g no té límit a 0.

        **Criteri seqüencial:** el límit és L si per a **tota** successió $x_n$ del domini,
        amb $x_n\ne a$ i $x_n\to a$, tenim $f(x_n)\to L$.
        Dues successions amb resultats diferents refuten el límit; dues amb el mateix
        resultat, totes soles, no el demostren.
        ''') ,
        code(r'''
        n = np.arange(1, 31)
        fig, ax = plt.subplots()
        ax.scatter(1/n, np.ones_like(n), color="#2563eb", label="xₙ=1/n")
        ax.scatter(-1/n, -np.ones_like(n), color="#d97706", label="yₙ=−1/n")
        ax.axvline(0, color="0.5"); ax.set(xlabel="x", ylabel="g(x)", title="Dos camins, dos límits diferents")
        ax.legend(); plt.show()
        ''') ,
        md(r'''
        ## 4. Continuïtat
        f és contínua a a si està definida a a i $\lim_{x\to a}f(x)=f(a)$.
        A la funció inicial, assignar f(1)=2 omple el forat de manera contínua;
        assignar f(1)=3 no canvia el límit, però produeix una discontinuïtat.

        ## Activitats
        1. Per a ε=0,01, dona un δ vàlid per a $f(x)=x+1$ al punt 1.
        2. **Ampliació:** per a $f(x)=x^2$ al punt 1, prova
           $|x^2-1|=|x-1||x+1|<3|x-1|$ si $|x-1|<1$.
           Justifica δ=min(1, ε/3).
        3. Si f(1)=3 a l'exemple inicial, quin és el límit? És contínua?
        4. Explica per què provar únicament una successió de punts no estableix un límit de funció.

        <details><summary>Comprovació</summary>

        δ=0,01 serveix. Si $|x-1|<1$, tenim $0<x<2$ i $|x+1|<3$.
        El límit continua sent 2 quan f(1)=3, i la funció no és contínua a 1.
        </details>
        ''')], previous="06_Completesa_R.ipynb", following="Derivades_BAT.ipynb")

    notebook("Derivades_BAT.ipynb", "08 · De la secant a la derivada",
        "Entendre la derivada com un límit finit de pendents i distingir tres comportaments locals.",
        "quadern 07 i pendent d'una recta", "2 sessions",
        "Reelaboració de Derivades_BAT.ipynb. Es conserven els originals en un arxiu separat.", [
        md(r'''
        ## 1. La tangent no és simplement una recta que toca una corba
        Prenem $A=(a,f(a))$ i $B=(a+h,f(a+h))$, amb $h\ne0$.
        El pendent de la secant és
        $$m_h=\frac{f(a+h)-f(a)}h.$$
        Si aquest quocient té un límit **real finit**, el denotem $f'(a)$.
        La tangent té equació $y=f(a)+f'(a)(x-a)$.

        Per a $f(x)=x^2$, simplifica el quocient abans d'executar:
        $$m_h=\frac{(a+h)^2-a^2}h=2a+h\longrightarrow2a.$$
        ''') ,
        code(r'''
        def funcio(tipus, x):
            if tipus == "quadratica": return np.asarray(x)**2
            if tipus == "absolut": return np.abs(x)
            if tipus == "arrel_cubica": return np.cbrt(x)
            raise ValueError("Funció desconeguda.")

        def pendent_secant(tipus, a, h):
            if h == 0: raise ValueError("El pas h ha de ser diferent de zero.")
            if tipus == "quadratica": return 2*a+h  # forma algebraica estable
            return float((funcio(tipus, a+h)-funcio(tipus, a))/h)

        def secant(tipus="quadratica", a=0.0, exponent=2, costat=1):
            h = costat * 10.0**(-exponent)
            m = pendent_secant(tipus, a, h)
            x = np.linspace(-2.2, 2.2, 601)
            fa = float(funcio(tipus, a))
            fig, ax = plt.subplots()
            ax.plot(x, funcio(tipus, x), color="#2563eb", label="Funció")
            ax.plot(x, fa+m*(x-a), color="#d97706", label=f"Secant: pendent {m:.5g}")
            ax.scatter([a, a+h], [fa, float(funcio(tipus, a+h))], color="#dc2626")
            if tipus == "quadratica":
                ax.plot(x, fa+2*a*(x-a), "--", color="#16a34a", label=f"Tangent: pendent {2*a:g}")
            ax.set(xlim=(-2.2, 2.2), ylim=(-3, 5), xlabel="x", ylabel="y", title=f"h = {h:g}")
            ax.legend(); plt.show()
            print(f"Quocient incremental = {m:.10g}. Un valor finit de h no és el límit.")
        panell = explora(secant, tipus=["quadratica", "absolut", "arrel_cubica"],
                         a=(-1.5, 1.5, .25), exponent=(0, 6, 1), costat=[-1, 1])
        ''') ,
        md(r'''
        ## 2. Al punt a=0: tres resultats diferents
        * $x^2$: $m_h=h\to0$ pels dos costats. Derivada igual a 0.
        * $|x|$: $m_h=1$ per h>0 i $m_h=-1$ per h<0. No hi ha un únic límit.
        * $\sqrt[3]{x}$: $m_h=|h|^{-2/3}\to+\infty$. Hi ha tangent vertical,
          però no una derivada real finita a 0.

        Les tres funcions són contínues a 0. **Continuïtat no implica derivabilitat.**
        ''') ,
        code(r'''
        for tipus in ("quadratica", "absolut", "arrel_cubica"):
            print("\n", tipus)
            for h in (0.1, 0.001, -0.001, -0.1):
                print(f"h={h:8g}: pendent={pendent_secant(tipus, 0, h):12.6g}")
        ''') ,
        md(r'''
        ## 3. Un pont amb Cauchy, amb una precaució
        Si la derivada existeix, els pendents calculats al llarg de qualsevol successió
        $h_n\to0$, $h_n\ne0$, convergeixen al mateix nombre i són de Cauchy.
        **Una sola successió de pendents de Cauchy no demostra la derivabilitat:**
        per a $|x|$, els passos $h_n=1/n$ donen sempre pendent 1, però els passos negatius donen −1.

        ## 4. Regles i correccions conceptuals
        | Funció | Derivada i condicions |
        |---|---|
        | $x^3$ | $3x^2$ |
        | $\sin x$ | $\cos x$, amb angles en radians |
        | $\cos x$ | $-\sin x$ |
        | $\ln x$ | $1/x$, per a x>0 |
        | $g(h(x))$ | $g'(h(x))h'(x)$, quan les derivades necessàries existeixen |

        La identitat correcta és $\cos^2x-1=-\sin^2x$.
        Si $f'(a)=0$, a no ha de ser un extrem: $f(x)=x^3$ al punt 0 és un contraexemple.
        Si $f''(a)=0$, tampoc podem concloure que la funció sigui una recta en un entorn d'a.
        ''') ,
        code(r'''
        # L'arrodoniment pot malmetre el quocient calculat per una resta de nombres propers.
        a = 1.0
        print("h          quocient directe       expressió 2a+h")
        for h in (1e-2, 1e-6, 1e-10, 1e-14, 1e-17):
            directe = ((a+h)**2-a**2)/h
            print(f"{h:9.1e}  {directe:20.12g}  {2*a+h:20.12g}")
        ''') ,
        md(r'''
        ## Activitats
        1. Troba l'equació de la tangent de $x^2$ al punt a=1 i al punt a=−1.
        2. Explica per què no podem substituir h=0 al quocient incremental.
        3. Per a $|x|$, canvia a de 0 a 1. Què passa amb els pendents quan h és petit?
        4. **Ampliació:** demostra que ser derivable a a implica ser contínua a a,
           escrivint $f(a+h)-f(a)=h\,[f(a+h)-f(a)]/h$.
        5. Escriu una conclusió sobre el recorregut: per què necessitem ℝ abans d'estudiar límits i derivades?

        <details><summary>Comprovació</summary>

        Les tangents són $y=2x-1$ i $y=-2x-1$. A a=1, el valor absolut coincideix localment
        amb x, i la derivada és 1. En la demostració de continuïtat, el quocient té límit
        finit i el factor h tendeix a zero. Els experiments numèrics són evidència;
        les identitats i els arguments de límits proporcionen les justificacions.
        </details>
        ''')], previous="07_Limits_Continuitat.ipynb")


def build_complements():
    notebook("LaRecta.ipynb", "Complement · La recta i el pendent",
        "Interpretar pendent, ordenada a l'origen i rectes verticals.",
        "coordenades cartesianes", "1 sessió",
        "Reelaboració de LaRecta.ipynb, amb controls en lloc d'un vídeo dependent de FFmpeg.", [
        md(r'''
        ## Rectes no verticals
        $y=mx+b$ representa una recta no vertical. m és el pendent i b és l'ordenada
        a l'origen; el punt de tall amb l'eix vertical és $(0,b)$.
        Si m≠0, és una funció polinòmica de primer grau. Si m=0, és constant.
        Les rectes verticals $x=c$ no són gràfiques d'una funció $y=f(x)$.

        Prediu l'efecte de canviar m mantenint b fix. Després fes el contrari.
        ''') ,
        code(r'''
        def recta(pendent=2.0, ordenada=-1.0):
            x = np.linspace(-5, 5, 200)
            fig, ax = plt.subplots()
            ax.plot(x, pendent*x+ordenada, color="#2563eb", label=f"y = {pendent:g}x {ordenada:+g}")
            ax.plot([0, 1], [ordenada, ordenada], "--", color="#16a34a", label="Δx = 1")
            ax.plot([1, 1], [ordenada, ordenada+pendent], "--", color="#d97706", label=f"Δy = {pendent:g}")
            ax.scatter([0, 1], [ordenada, ordenada+pendent], color="#dc2626")
            ax.axhline(0, color="0.5"); ax.axvline(0, color="0.5")
            ax.set(xlim=(-5, 5), ylim=(-12, 12), xlabel="x", ylabel="y", title="Pendent = Δy / Δx")
            ax.legend(); plt.show()
        panell = explora(recta, pendent=(-5., 5., .25), ordenada=(-5., 5., .5))
        ''') ,
        code(r'''
        def pendent_dos_punts(a, b):
            if a[0] == b[0]:
                raise ValueError("No hi ha pendent finit: punts amb la mateixa abscissa.")
            return (b[1]-a[1])/(b[0]-a[0])
        print("Pendent entre (1,1) i (7,4):", pendent_dos_punts((1,1), (7,4)))
        ''') ,
        md(r'''
        ## Activitats
        1. Troba una recta que passi per (0,3) amb pendent −2.
        2. Què representa una recta de pendent zero? I la recta x=2?
        3. Comprova que la recta entre (1,1) i (7,4) té pendent 1/2.
        4. Què necessitarem si el pendent canvia d'un punt a un altre d'una corba?

        <details><summary>Comprovació</summary>

        $y=-2x+3$. El pendent zero dona una funció constant; x=2 és una recta vertical,
        no una funció de x. Per a una corba introduirem la derivada al quadern 08.
        </details>
        ''')], following="Derivades_BAT.ipynb")

    notebook("ComplexNumbers.ipynb", "Complement · Nombres complexos",
        "Operar amb nombres complexos i representar-ne el mòdul i l'argument correctament.",
        "àlgebra i trigonometria", "1–2 sessions",
        "Reelaboració de ComplexNumbers.ipynb. Complement independent de la completesa de ℝ.", [
        md(r'''
        ## 1. Un nou problema d'existència
        Cap nombre real té quadrat −1. Introduïm i amb $i^2=-1$ i escrivim $z=x+iy$.
        Això amplia el sistema per resoldre equacions; és un problema diferent de completar ℚ.
        La part imaginària és el nombre real y, mentre que el terme imaginari és iy.
        En Python s'escriu `1j` per a i.
        ''') ,
        code(r'''
        import cmath
        z1, z2, z3 = 3+4j, 2+5j, -1+2j
        print("Part real:", z1.real, "Part imaginària:", z1.imag)
        print("Commutativa de la suma:", z1+z2 == z2+z1)
        print("Associativa del producte:", (z1*z2)*z3 == z1*(z2*z3))
        print("Distributiva:", z3*(z1+z2) == z3*z1+z3*z2)
        print("Oposat:", -z1, "Conjugat:", z1.conjugate())
        print("Invers:", 1/z1, "Producte pròxim a 1:", cmath.isclose(z1*(1/z1), 1))
        ''') ,
        md(r'''
        ## 2. Mòdul, argument i invers
        Per a z≠0, $|z|=\sqrt{x^2+y^2}$ i
        $$z^{-1}=\frac{x-iy}{x^2+y^2}.$$
        El zero no té invers ni un argument geomètric definit.
        La fórmula $\arctan(y/x)$ sola no distingeix els quadrants i no serveix si x=0.
        Usem `atan2(y,x)` o `cmath.phase(z)` per a z≠0.
        L'argument està definit mòdul $2\pi$; el programa mostra un representant principal.
        ''') ,
        code(r'''
        def dades_complex(z):
            z = complex(z)
            return abs(z), None if z == 0 else math.atan2(z.imag, z.real)

        def pla_complex(real=1.0, imaginaria=1.0):
            z = complex(real, imaginaria)
            modul, argument = dades_complex(z)
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.arrow(0, 0, real, imaginaria, length_includes_head=True,
                     head_width=.12, color="#2563eb")
            ax.scatter([real], [imaginaria], color="#dc2626")
            ax.axhline(0, color="0.5"); ax.axvline(0, color="0.5")
            ax.set(xlim=(-4, 4), ylim=(-4, 4), xlabel="Part real", ylabel="Part imaginària", title=f"z = {z}")
            ax.set_aspect("equal"); plt.show()
            print(f"Mòdul: {modul:.6g}")
            print("Argument no definit" if argument is None else f"Argument: {argument:.6g} radians")
        panell = explora(pla_complex, real=(-3., 3., .5), imaginaria=(-3., 3., .5))
        ''') ,
        code(r'''
        for z in (1+1j, -1+1j, -1-1j, 1-1j, 1j, 0j):
            print(z, "→", dades_complex(z))
        ''') ,
        md(r'''
        ## 3. Fórmula de De Moivre
        Si $z=r(\cos\theta+i\sin\theta)$, per a qualsevol enter n≥0:
        $$z^n=r^n(\cos(n\theta)+i\sin(n\theta)).$$
        Per a enters negatius cal z≠0. Comprovar un exemple numèric no demostra la fórmula
        general; es pot demostrar per inducció amb les identitats de suma d'angles.
        ''') ,
        code(r'''
        z, n = 1+1j, 5
        r, theta = dades_complex(z)
        polar = r**n * complex(math.cos(n*theta), math.sin(n*theta))
        print("Potència directa:", z**n)
        print("Forma trigonomètrica:", polar)
        print("Coincidència dins de l'arrodoniment:", cmath.isclose(z**n, polar, rel_tol=1e-12, abs_tol=1e-12))
        ''') ,
        md(r'''
        ## Activitats
        1. Per què la distributiva no és la propietat associativa?
        2. Compara els arguments de 1+i i −1+i. Què donaria arctan(y/x)?
        3. Troba l'invers de 3+4i a mà i comprova'l.
        4. Explica per què ampliar ℝ a ℂ no significa que a ℝ li faltin límits de successions de Cauchy.

        <details><summary>Comprovació</summary>

        Els arguments són π/4 i 3π/4. L'invers és (3−4i)/25.
        ℝ ja és complet; ℂ permet, entre altres coses, resoldre $z^2=-1$.
        </details>
        ''')])

    notebook("AnálisisUnivariante(I).ipynb", "Complement · Anàlisi univariant",
        "Construir taules i gràfiques coherents i interpretar dades numèriques i ordinals.",
        "freqüències, mitjana i mediana", "1–2 sessions",
        "Reelaboració d'AnálisisUnivariante(I).ipynb; dades simulades amb llavor fixa.", [
        md(r'''
        ## 1. Dades i freqüències
        Una variable discreta pren valors aïllats (no necessàriament enters); una variable
        contínua pot prendre qualsevol valor d'un interval en el model matemàtic.
        Les dades següents són edats enteres **simulades**, no una mostra real d'alumnes.

        Per als intervals usem [a,b), excepte l'últim, que inclou també el màxim.
        La taula i l'histograma han de fer servir exactament les mateixes vores.
        ''') ,
        code(r'''
        import pandas as pd

        rng = np.random.default_rng(2026)
        edats = rng.integers(18, 66, size=100)

        def taula_frequencies(dades, classes=7):
            dades = np.asarray(dades, dtype=float)
            if dades.ndim != 1 or dades.size == 0 or not np.isfinite(dades).all():
                raise ValueError("Cal un vector no buit de nombres finits.")
            if not isinstance(classes, int) or classes < 1:
                raise ValueError("El nombre de classes ha de ser un enter positiu.")
            freq, vores = np.histogram(dades, bins=classes)
            intervals = [f"[{a:.4g}, {b:.4g}{']' if i == len(freq)-1 else ')'}"
                         for i, (a, b) in enumerate(zip(vores[:-1], vores[1:]))]
            taula = pd.DataFrame({"Interval": intervals, "Freqüència": freq,
                                  "Freqüència relativa": freq/len(dades),
                                  "Acumulada": np.cumsum(freq)})
            return taula, vores

        def histograma(classes=7):
            taula, vores = taula_frequencies(edats, classes)
            display(taula)
            fig, ax = plt.subplots()
            ax.hist(edats, bins=vores, edgecolor="white", color="#2563eb")
            ax.set(xlabel="Edat simulada", ylabel="Freqüència", title="Histograma i taula amb els mateixos intervals")
            plt.show()
            print("Total comptat:", int(taula["Freqüència"].sum()), "de", len(edats))
        panell = explora(histograma, classes=(1, 15, 1))
        ''') ,
        md(r'''
        ## 2. Diagrama de caixa i valors atípics
        Separem els conjunts de dades amb noms diferents, perquè executar una activitat
        no substitueixi les dades necessàries per a una altra.
        Per defecte, els bigotis arriben a les dades més extremes dins de les tanques
        $Q_1-1,5\,IQR$ i $Q_3+1,5\,IQR$, amb $IQR=Q_3-Q_1$.
        No cal que acabin exactament a les tanques. Un valor atípic no és necessàriament un error.
        ''') ,
        code(r'''
        rng_caixa = np.random.default_rng(42)
        valors = np.concatenate([rng_caixa.normal(50, 10, 100), [10, 110, 115, 120]])
        df_valors = pd.DataFrame({"Valors": valors})
        df_persones = pd.DataFrame({"Edat": [23, 25, 35, 30, 40], "Salari": [50000, 60000, 80000, 70000, 90000]})
        display(df_persones.describe())
        print("describe() calcula la desviació estàndard mostral (divisor n−1).")
        fig, ax = plt.subplots()
        ax.boxplot(df_valors["Valors"])
        ax.set(ylabel="Valor simulat", title="Caixa del conjunt df_valors")
        plt.show()
        q1, q3 = np.quantile(valors, [.25, .75])
        iqr = q3-q1
        print("Valors fora de les tanques:", valors[(valors < q1-1.5*iqr) | (valors > q3+1.5*iqr)])
        ''') ,
        md(r'''
        ## 3. Categories ordinals
        En una variable ordinal importa conservar l'ordre de les categories.
        Els gràfics han d'utilitzar les dades estudiades, fins i tot si demanem ajuda a una IA
        per escriure el codi. No substituïm les observacions per nombres inventats sense indicar-ho.
        ''') ,
        code(r'''
        ordre = ["Baixa", "Mitjana", "Alta"]
        satisfaccio = pd.Series(pd.Categorical(
            ["Baixa", "Mitjana", "Alta", "Baixa", "Mitjana", "Alta", "Alta", "Mitjana", "Baixa", "Mitjana"],
            categories=ordre, ordered=True))
        recomptes = satisfaccio.value_counts(sort=False).reindex(ordre, fill_value=0)
        fig, ax = plt.subplots()
        ax.barh(ordre, recomptes.to_numpy(), color=["#2563eb", "#16a34a", "#eab308"])
        ax.set(xlabel="Freqüència", title="Satisfacció: les dades originals de l'activitat")
        plt.show()
        ''') ,
        md(r'''
        ## Activitats
        1. Canvia el nombre de classes. Canvien les dades o només l'agrupació?
        2. Executa `taula_frequencies([18,19,20], 2)` i `taula_frequencies([20,20,20], 2)`.
           Comprova que sempre es compten les tres observacions.
        3. Per què no podem concloure que tots els valors atípics són errors de mesura?
        4. Redacta una interpretació del gràfic ordinal que coincideixi amb els recomptes.

        <details><summary>Comprovació</summary>

        Canvia l'agrupació, no les dades. Les freqüències ordinals són 3, 4 i 3.
        Cal investigar el context abans de decidir si un valor atípic és un error.
        </details>
        ''')])

    notebook("PràcticaBasedeDades.ipynb", "Complement · Transformació de dades amb pandas",
        "Transformar dades de format ample a llarg amb una correspondència explícita entre any i categoria.",
        "llistes, bucles i estadística descriptiva", "2 sessions",
        "Reelaboració de PràcticaBasedeDades.ipynb. El CSV original de l'Agència Tributària no era al repositori.", [
        md(r'''
        ## 1. Quines dades utilitzem?
        **Aquest quadern treballa per defecte amb dades sintètiques de demostració.**
        No són dades fiscals reals i no permeten conclusions sobre salaris ni impostos.
        L'arxiu original `data2.csv` no està disponible al repositori i no es pressuposa
        l'accés a cap Drive personal. Si disposes del CSV, pots carregar-lo a la cel·la indicada.

        Reproduïm l'esquema de les columnes: ID, anys per a Salary, anys amb sufix .1 per a tax,
        i anys amb sufix .2 per a employees. Les magnituds simulades no tenen unitats econòmiques assignades.
        ''') ,
        code(r'''
        import pandas as pd
        from pathlib import Path

        def dades_demostracio(files=400, anys=range(2001, 2023), llavor=2026):
            if files < 1: raise ValueError("Cal almenys una fila.")
            rng = np.random.default_rng(llavor)
            dades = {"ID": np.arange(1, files+1)}
            for sufix, escala in (("", 10000), (".1", 2000), (".2", 500)):
                for any_ in anys:
                    dades[f"{any_}{sufix}"] = rng.integers(1, escala, size=files)
            return pd.DataFrame(dades)

        # Opcional: puja el CSV a Colab/Jupyter i escriu-ne la ruta. None usa dades sintètiques.
        ruta_csv = None  # Exemple: "data2.csv"
        if ruta_csv is None:
            dades_amples = dades_demostracio()
            origen_dades = "DADES SINTÈTIQUES DE DEMOSTRACIÓ"
        else:
            dades_amples = pd.read_csv(Path(ruta_csv), dtype=str)
            origen_dades = f"Fitxer proporcionat: {Path(ruta_csv).name}"
        print(origen_dades)
        display(dades_amples.head())
        print("Dimensions:", dades_amples.shape)
        ''') ,
        md(r'''
        ## 2. Append, extend i aplanament
        `append` afegeix un únic element, que pot ser una llista; `extend` afegeix
        cadascun dels elements d'una seqüència. Prediu les longituds abans d'executar.
        ''') ,
        code(r'''
        a, b = [], []
        a.append([1, 2, 3])
        b.extend([1, 2, 3])
        print("append:", a, "longitud:", len(a))
        print("extend:", b, "longitud:", len(b))
        matriu = np.array([[1, 2, 3], [4, 5, 6]])
        print("Ordre de files:", matriu.flatten("C"))
        print("Ordre de columnes:", matriu.flatten("F"))
        ''') ,
        md(r'''
        ## 3. Transformar sense confiar en la posició de les columnes
        La nova taula tindrà les columnes `rank`, `value`, `year`, `category`.
        Extraurem l'any i la categoria dels noms de les columnes. Així no depenem
        de tenir exactament 400 files, 22 anys o un ordre determinat.

        L'opció `comes_milers=True` només és adequada si el fitxer usa comes com a
        separador de milers, com en els exemples guardats al quadern original.
        No l'activis si les comes representen decimals.
        ''') ,
        code(r'''
        import re

        def format_llarg(ample, comes_milers=False):
            if "ID" not in ample.columns or ample["ID"].isna().any() or ample["ID"].duplicated().any():
                raise ValueError("Cal una columna ID sense valors absents ni repetits.")
            if ample.empty: raise ValueError("La taula és buida.")
            categories = {None: "Salary", "1": "tax", "2": "employees"}
            blocs, ignorades = [], []
            for columna in ample.columns:
                if columna == "ID": continue
                patro = re.fullmatch(r"(\d{4})(?:\.(\d+))?", str(columna))
                if patro is None or patro.group(2) not in categories:
                    ignorades.append(str(columna)); continue
                serie = ample[columna]
                if comes_milers:
                    serie = serie.astype(str).str.replace(",", "", regex=False)
                valors = pd.to_numeric(serie, errors="raise")
                if not np.isfinite(valors.to_numpy(dtype=float)).all():
                    raise ValueError(f"Hi ha valors absents o no finits a {columna}.")
                blocs.append(pd.DataFrame({"rank": ample["ID"].to_numpy(), "value": valors.to_numpy(),
                                            "year": int(patro.group(1)), "category": categories[patro.group(2)]}))
            if not blocs: raise ValueError("No s'han trobat columnes d'any i categoria reconegudes.")
            llarg = pd.concat(blocs, ignore_index=True)
            if llarg.duplicated(["rank", "year", "category"]).any():
                raise ValueError("Hi ha registres repetits per identificador, any i categoria.")
            return llarg, ignorades

        dades_llargues, ignorades = format_llarg(dades_amples, comes_milers=ruta_csv is not None)
        print(origen_dades)
        print("Columnes no utilitzades:", ignorades)
        print("Dimensions del format llarg:", dades_llargues.shape)
        display(dades_llargues.head())
        ''') ,
        code(r'''
        def grafic_dades(any_=2001, categoria="Salary"):
            seleccio = dades_llargues[(dades_llargues["year"] == any_) & (dades_llargues["category"] == categoria)]
            fig, ax = plt.subplots()
            ax.bar(np.arange(len(seleccio)), seleccio["value"], color="#2563eb")
            ax.set(xlabel="Posició del registre seleccionat", ylabel="Valor",
                   title=f"{origen_dades}\nAny {any_} · {categoria}")
            plt.tight_layout(); plt.show()
            print("Registres seleccionats:", len(seleccio))
        panell = explora(grafic_dades, any_=sorted(dades_llargues["year"].unique().tolist()),
                         categoria=sorted(dades_llargues["category"].unique().tolist()))
        ''') ,
        md(r'''
        ## 4. Exportació opcional
        La cel·la següent no escriu cap fitxer fins que la descomentis. L'índex tècnic
        del DataFrame no és una variable de les dades i no s'ha d'afegir al CSV.
        ''') ,
        code(r'''
        # dades_llargues.to_csv("dades_format_llarg.csv", index=False)
        ''') ,
        md(r'''
        ## Activitats
        1. Justifica el nombre de registres: 400·22·3=26400 a l'exemple per defecte.
        2. Genera 10 files i només dos anys. Quantes files tindrà el format llarg?
        3. Reordena les columnes de la taula ampla. Comprova que l'associació any–categoria–valor es conserva.
        4. Què caldria documentar abans d'interpretar dades reals: font, any, unitats, població i tractament d'absents?

        <details><summary>Comprovació</summary>

        Amb 10 files, dos anys i tres categories hi ha 60 registres. El nom de cada columna
        conserva el seu significat encara que canviem l'ordre. Les dades sintètiques només
        serveixen per estudiar la transformació, no per extreure conclusions econòmiques.
        </details>
        ''')])


if __name__ == "__main__":
    build()
    build_complements()
    print("Generats vuit quaderns principals i quatre complements.")
