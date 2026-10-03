"""Laboratoris didàctics incrustats als quaderns: no cal importar aquest fitxer a classe."""
from tallers_aprenentatge import celles_taller

AJUDANTS = r'''
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

def fotograma_laboratori(pas):
    """Mostra un estat quiet per poder llegir, dibuixar i prendre apunts."""
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.7), dpi=90)
    dibuixa_laboratori(pas, axes)
    fig.suptitle(titol_laboratori, fontsize=14, weight="bold")
    fig.tight_layout(rect=(0, 0, 1, .92))
    plt.show()

def anima_laboratori():
    """Animació HTML amb pausa i desplaçament manual; no necessita FFmpeg."""
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.7), dpi=80)
    def actualitza(pas):
        for ax in axes:
            ax.clear()
        dibuixa_laboratori(pas, axes)
        fig.suptitle(titol_laboratori, fontsize=14, weight="bold")
        fig.tight_layout(rect=(0, 0, 1, .92))
    animacio = FuncAnimation(fig, actualitza, frames=fotogrames_laboratori,
                             interval=700, repeat=False, cache_frame_data=False)
    try:
        contingut = animacio.to_jshtml(fps=1.5, default_mode="once")
    finally:
        plt.close(fig)
    return HTML(contingut)
'''


LABS = {}

LABS["Q_conjunt_dens.ipynb"] = dict(
    abans="## 3. Per què falta un racional?",
    meta="Trobar intervals racionals cada vegada més estrets i explicar per què això no converteix √2 en racional.",
    pregunta="Si trobem deu decimals d'un nombre, ja sabem si és racional?",
    text=r'''
### Un quadrat de superfície 2: quina longitud té el costat?

Un quadrat de costat 1 té àrea 1; un de costat 2 té àrea 4. Busquem un costat entre 1 i 2
amb àrea 2. No premem la tecla √: **provem, comparem i conservem mitja cerca**.

| Pas | Interval abans de provar | Punt mig m | m² | Decisió |
|---|---|---|---|---|
| 1 | [1, 2] | 3/2 | 9/4 > 2 | conservar [1, 3/2] |
| 2 | [1, 3/2] | 5/4 | 25/16 < 2 | conservar [5/4, 3/2] |
| 3 | [5/4, 3/2] | 11/8 | 121/64 < 2 | conservar [11/8, 3/2] |

La comparació $m^2<2$ o $m^2>2$ és exacta amb fraccions. El dibuix només en representa
les posicions aproximades. **Blau:** interval abans de decidir. **Verd:** meitat conservada.
El gràfic dret amplia l'interval actual; comprova les marques de l'eix perquè l'escala canvia.

**Prediu.** Quina serà l'amplada després de 5 passos? Completa primer la tercera fila a mà.
**Durant l'animació.** Pausa al pas 2 i explica per què descartem la meitat esquerra.
''',
    codi=r'''
titol_laboratori = "Buscar √2 sense conèixer-ne els decimals"
fotogrames_laboratori = list(range(10))

def estat_biseccio(pas):
    a, b = intervals_arrel2(pas)[-1]
    m = (a+b)/2
    nou = (m, b) if m*m < 2 else (a, m)
    return a, b, m, nou

def dibuixa_laboratori(pas, axes):
    a, b, m, (c, d) = estat_biseccio(pas)
    ax, bx = axes
    for k, (u, v) in enumerate(intervals_arrel2(pas+1)):
        ax.plot([float(u), float(v)], [k, k], "o-", color="#2563eb", lw=3)
    ax.set(xlim=(.95, 2.05), ylim=(-.7, 10.7), xlabel="Longitud del costat",
           ylabel="Nombre de decisions", title="Escala fixa: l'interval es va estrenyent")
    bx.plot([float(a), float(b)], [1, 1], "o-", lw=6, color="#2563eb", label="Abans")
    bx.plot([float(c), float(d)], [0, 0], "o-", lw=6, color="#047857", label="Després")
    bx.scatter([float(m)], [1], s=65, color="#ea580c", zorder=5)
    marge = float(b-a)*.18
    bx.set(xlim=(float(a)-marge, float(b)+marge), ylim=(-.6, 1.8),
           yticks=[0, 1], yticklabels=["Conservem", "Provem"], xlabel="Longitud (escala ampliada)",
           title=f"Pas {pas+1}: m = {m}\nm² {'<' if m*m < 2 else '>'} 2; amplada nova = {d-c}")
    bx.ticklabel_format(axis="x", style="plain", useOffset=False)
    bx.tick_params(axis="x", labelrotation=20)
    bx.legend(loc="upper right", fontsize=8)
''',
    tasca=r'''
1. Escriu la regla que permet trobar l'amplada després de $k$ passos. Quants passos calen
   perquè sigui menor que $0{,}001$? Justifica-ho amb una potència de 2.
2. Aplica dues decisions a la cerca de √3 dins [1, 2]. Quina comparació has de canviar?
3. Entre $7/5$ i $3/2$, construeix un racional nou amb el punt mig. Per què sempre en podràs construir un altre?
4. Explica la diferència entre «podem aproximar √2 amb racionals» i «√2 és racional».
''',
    resposta=r'''L'amplada és $2^{-k}$; calen 10 passos perquè $2^{-10}<0{,}001$.
Per a √3: [3/2, 2] i després [3/2, 7/4]. El punt mig de 7/5 i 3/2 és 29/20,
estrictament entre els extrems. Una successió de racionals pot tenir un límit irracional;
la prova de la irracionalitat de √2 és una qüestió diferent de l'aproximació.''',
)

LABS["Càlcul_Nombre_pi.ipynb"] = dict(
    abans="## 5. Experimenta:",
    meta="Relacionar el moviment del polígon amb els angles, el costat, el perímetre i l'error de π.",
    pregunta="Si cada costat es fa més curt, per què el perímetre augmenta?",
    text=r'''
### Una pel·lícula del polígon i del seu resultat

L'animació uneix dues representacions del mateix càlcul. A l'esquerra augmenta el nombre
de costats; a la dreta apareix la seva aproximació de π. El punt taronja correspon sempre
al polígon visible. L'eix vertical dret està ampliat: els primers valors queden per sota
de la finestra i entren al gràfic quan l'aproximació és prou propera a π.

**Prediu.** En passar de 6 a 12 costats, l'angle central i el costat es redueixen exactament
a la meitat? Són dues preguntes diferents: comprova-les amb els valors de la taula.
**Pausa** a 6, 12 i 300 costats. Anota $\alpha$, $b$ i $\pi_n$. Explica el factor 2 a $b=2\sin(\alpha/2)$.

La pel·lícula mostra una selecció de nombres de costats per ser llegible;
la corba es calcula per a **tots els enters de 3 a 300**.
''',
    codi=r'''
titol_laboratori = "Del polígon al nombre: aproximar π"
fotogrames_laboratori = [3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 30, 40, 50, 65, 80, 100, 125, 150, 200, 250, 300]

def dibuixa_laboratori(n, axes):
    d = dades_poligon(n)
    ax, bx = axes
    dibuixa_poligon(ax, n)
    ax.set_title(f"n = {n}; α = {d['alpha']:.3f}°; β = {d['beta']:.3f}°\n"
                 f"Base ≈ {d['base']:.6f}; perímetre ≈ {d['perimetre']:.6f}")
    ns = np.arange(3, 301)
    ys = np.array([dades_poligon(int(k))["pi_aprox"] for k in ns])
    bx.plot(ns, ys, color="0.8", label="Recorregut complet")
    bx.plot(ns[ns <= n], ys[ns <= n], color="#2563eb", lw=2)
    bx.axhline(math.pi, color="#b91c1c", ls="--", label="π de referència")
    if d["pi_aprox"] >= 3.12:
        bx.scatter([n], [d["pi_aprox"]], color="#ea580c", s=65, zorder=5)
    else:
        bx.text(.5, .2, "El valor encara és per sota de 3,12", transform=bx.transAxes,
                ha="center", color="#ea580c")
    bx.set(xlim=(3, 305), ylim=(3.12, 3.143), xlabel="Nombre de costats", ylabel="Aproximació (escala ampliada)",
           title=f"πₙ ≈ {d['pi_aprox']:.9f}\nError ≈ {math.pi-d['pi_aprox']:.8f}")
    bx.ticklabel_format(axis="y", style="plain", useOffset=False)
    bx.legend(loc="lower right", fontsize=8)
''',
    tasca=r'''
1. Dibuixa un polígon de 8 costats i un dels seus triangles. Calcula $\alpha$, $\beta$, $b$ i $\pi_8$.
2. Troba a la taula el primer valor **dels que hi apareixen** amb error menor que $0{,}001$.
   Després usa Python per trobar el primer enter entre 3 i 300 que ho compleix.
3. Explica per què una imatge que sembla un cercle no demostra que el polígon sigui un cercle.
4. Canvia el radi a 2: què es duplica i què es conserva?
''',
    resposta=r'''Per a 8 costats: $\alpha=45°$, $\beta=22{,}5°$, $b\approx0{,}76536686$
i $\pi_8\approx3{,}06146746$. La primera fila de la taula que compleix l'error és 96;
examinant tots els enters, és 72. El dibuix té resolució finita. En duplicar el radi,
es dupliquen costat i perímetre, però $p_n/(2r)$ es conserva.''',
)

LABS["NumeroPi.ipynb"] = dict(
    abans="## 2. Una demostració",
    meta="Decidir quan una aproximació és prou bona a partir de dues cotes, sense saber el valor buscat.",
    pregunta="Per afirmar que l'error és petit, necessitem conèixer π exactament?",
    text=r'''
### Una mesura amb marge d'error

Imagina que només sabem que una longitud és entre 3,14 i 3,15. Si diem 3,145,
l'error és menor que 0,005. **El punt mig reparteix la incertesa entre els dos costats.**
Fem el mateix amb $L_n<\pi<U_n$:

$$m_n=\frac{L_n+U_n}{2},\qquad |m_n-\pi|<\frac{U_n-L_n}{2}.$$

No confonguis **amplada** $U_n-L_n$ amb **marge d'error del punt mig** $(U_n-L_n)/2$.
La gràfica esquerra amplia l'interval de cada pas; no compareu-ne la llargada visual
sense llegir els extrems. La dreta manté l'escala i permet veure la reducció del marge.

**Prediu.** Si l'objectiu és error menor que 0,001, quina amplada necessitem?
**Pausa** quan la corba baixi de la línia taronja i anota el nombre de costats.
Les cotes del dibuix estan arrodonides; l'apartat certificat posterior controla també aquest arrodoniment.
''',
    codi=r'''
titol_laboratori = "Saber quan podem aturar el càlcul"
fotogrames_laboratori = list(range(9))

def dibuixa_laboratori(pas, axes):
    files = arquimedes(pas)
    n, a, b = files[-1]
    a, b = float(a), float(b)
    m, marge = (a+b)/2, (b-a)/2
    ax, bx = axes
    ax.plot([a, b], [0, 0], "o-", color="#2563eb", lw=5)
    ax.scatter([m], [0], color="#ea580c", s=70, zorder=5)
    ax.annotate("punt mig", (m, 0), (m, .35), ha="center", arrowprops=dict(arrowstyle="->"))
    ax.set(xlim=(a-marge*.4, b+marge*.4), ylim=(-.55, .7), yticks=[],
           title=f"{n} costats: interval ampliat\nL ≈ {a:.9f}; U ≈ {b:.9f}", xlabel="Valor possible de π")
    ax.ticklabel_format(axis="x", style="plain", useOffset=False)
    ax.tick_params(axis="x", labelrotation=20)
    bx.semilogy(range(len(files)), [float((v-u)/2) for _, u, v in files], "o-", color="#047857")
    bx.axhline(.001, color="#ea580c", ls="--", label="Objectiu: marge < 0,001")
    bx.set(xlim=(-.2, 8.2), ylim=(1e-6, 1), xlabel="Duplicacions", ylabel="Meitat de l'amplada",
           title=f"Marge aproximat: {marge:.3g}\n{'Objectiu assolit' if marge < .001 else 'Encara cal afinar'}")
    bx.legend(fontsize=8, loc="upper right")
''',
    tasca=r'''
1. Si $3{,}1415<\pi<3{,}1417$, calcula el punt mig i el seu marge d'error.
2. Amb `arquimedes`, troba el primer nombre de costats que fa el marge menor que $10^{-4}$.
3. Un company afirma: «el programa imprimeix amplada 0, per tant ja tenim π exacte».
   Explica el problema i proposa una comprovació.
4. Per a l'objectiu $10^{-4}$, contrasta la teva resposta amb `pi_amb_tolerancia`
   després d'executar l'ampliació certificada.
''',
    resposta=r'''El punt mig és 3,1416 i el marge és 0,0001. Duplicant des de 6 costats,
el primer polígon amb marge menor que $10^{-4}$ té 384 costats. Una amplada decimal nul·la
pot venir de l'arrodoniment; augmentar la precisió ajuda a detectar-ho, i l'aritmètica
d'intervals racional de l'ampliació permet certificar les desigualtats.''',
)

LABS["04_Talladures_Dedekind.ipynb"] = dict(
    abans="## 2. Propietats",
    meta="Entendre una talladura com una regla de classificació abans de llegir-ne la definició formal.",
    pregunta="Podem situar un nombre sense disposar d'una fracció que l'expressi?",
    text=r'''
### Un detector: aquest racional queda abans o després de √2?

No necessitem els decimals de √2 per classificar un racional $q$:

- Si $q<0$, queda a l'esquerra perquè √2 és positiu.
- Si $q\ge0$, comparem **exactament** $q^2$ amb 2.
- Si $q^2<2$, posem $q$ al grup A; si $q^2>2$, al grup B.

Per exemple, $(7/5)^2=49/25<2$ i $(10/7)^2=100/49>2$.
El primer és inferior i el segon superior. Cap racional té quadrat 2.
La regla és aplicable a tots els racionals, encara que el gràfic només en mostri uns quants.

**Prediu** la classificació de $-3/2$, $1$, $3/2$ i $7/5$.
**Durant l'animació**, llegeix la fracció i la comparació abans de mirar el color.
La corba dreta mostra per què comparar quadrats funciona per als candidats positius.
''',
    codi=r'''
titol_laboratori = "Separar els racionals amb una regla exacta"
candidats_tall = [Fraction(1), Fraction(3, 2), Fraction(7, 5), Fraction(10, 7),
                  Fraction(41, 29), Fraction(99, 70), Fraction(1414, 1000), Fraction(1415, 1000),
                  Fraction(14142, 10000), Fraction(14143, 10000)]
fotogrames_laboratori = list(range(len(candidats_tall)))

def dibuixa_laboratori(pas, axes):
    ax, bx = axes
    q = candidats_tall[pas]
    inferior = q*q < 2
    color = "#2563eb" if inferior else "#ea580c"
    ax.axhline(0, color="0.6")
    for k, r in enumerate(candidats_tall[:pas+1]):
        ax.scatter(float(r), .06*(k%3), color="#2563eb" if r*r < 2 else "#ea580c", s=45)
    ax.scatter(float(q), -.13, s=90, marker="^", color=color)
    ax.set(xlim=(.96, 1.54), ylim=(-.3, .3), yticks=[], xlabel="Posició del racional",
           title=f"q = {q} ≈ {float(q):.7f}\nGrup {'A: inferior' if inferior else 'B: superior'}")
    x = np.linspace(.95, 1.55, 300)
    bx.plot(x, x*x, color="#7c3aed", label="y = x²")
    bx.axhline(2, color="0.4", ls="--", label="y = 2")
    bx.scatter(float(q), float(q*q), color=color, s=70, zorder=5)
    bx.plot([float(q), float(q)], [0, float(q*q)], ":", color=color)
    bx.set(xlim=(.95, 1.55), ylim=(.85, 2.45), xlabel="q ≥ 0", ylabel="Quadrat de q",
           title=f"q² = {q*q}\nComparació exacta: q² {'<' if inferior else '>'} 2")
    bx.legend(fontsize=8)
''',
    tasca=r'''
1. Classifica $-2$, $0$, $4/3$ i $17/12$ sense usar `sqrt` ni una aproximació de √2.
2. Per què no podem aplicar «$q^2<2$» com a única regla quan $q$ és negatiu?
3. En la talladura que representa 3/2, a quin grup pertany 3/2 si A conté els racionals
   estrictament menors? Té A un màxim? Té B un mínim?
4. Escriu amb paraules què aporta una talladura: un decimal aproximat o una regla que
   determina una frontera? Distingeix la regla completa de la mostra del dibuix.
''',
    resposta=r'''−2, 0 i 4/3 són a A; 17/12 és a B perquè $289/144>2$.
−2 és inferior a √2 tot i tenir quadrat 4. Per a la frontera racional 3/2,
aquest nombre és a B: B té mínim i A no té màxim. La talladura defineix la frontera
a través de tots els racionals; la gràfica només en mostra una part finita.''',
)

LABS["05_Successions_Cauchy.ipynb"] = dict(
    abans="## 2. Tres justificacions",
    meta="Distingir estar a prop del terme següent d'estar a prop de tots els termes prou avançats.",
    pregunta="Si els passos es fan petits, necessàriament ens acabem aturant prop d'un nombre?",
    text=r'''
### Passos petits, recorregut encara gran

Comparem dos recorreguts. En $a_n=1/n$, els valors s'apropen a 0.
En $H_n=1+1/2+\cdots+1/n$, cada increment és petit, però sempre sumem més.

| Pregunta | Successió $1/n$ | Sumes harmòniques $H_n$ |
|---|---|---|
| Distància del terme n al següent | $1/[n(n+1)]$ | $1/(n+1)$ |
| Distància del terme n al terme 2n | $1/(2n)$ | $1/(n+1)+\cdots+1/(2n)$ |

Per a les sumes harmòniques, l'últim bloc conté **n sumands**, cadascun almenys $1/(2n)$.
Per tant $H_{2n}-H_n\ge n\cdot1/(2n)=1/2$. Això continua sent cert per gran que sigui n.

**Prediu.** Quin dels dos gràfics tindrà els punts de n i 2n cada vegada més junts?
**Pausa.** Compara la distància entre n i n+1 amb la distància entre n i 2n. Els eixos
horitzontals mostren cada vegada més termes; els títols indiquen les distàncies numèriques.

La definició de Cauchy exigeix controlar **totes les parelles prou avançades**.
La pel·lícula suggereix el comportament; la desigualtat anterior refuta Cauchy per a $H_n$.
''',
    codi=r'''
titol_laboratori = "Un salt petit no controla tots els salts futurs"
fotogrames_laboratori = [2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192]

def distancies_cauchy(n):
    return 1/(n*(n+1)), 1/(2*n), 1/(n+1), float(np.sum(1/np.arange(n+1, 2*n+1)))

def dibuixa_laboratori(n, axes):
    salt_a, bloc_a, salt_h, bloc_h = distancies_cauchy(n)
    indices = np.arange(1, 2*n+1)
    inversa = 1/indices
    harmonica = np.cumsum(1/indices)
    for ax, dades, color, titol in zip(axes, [inversa, harmonica], ["#2563eb", "#ea580c"],
                                     ["aₙ = 1/n", "Hₙ = 1 + 1/2 + … + 1/n"]):
        ax.plot(indices, dades, color=color)
        ax.scatter([n, 2*n], dades[[n-1, 2*n-1]], color=color, s=65, zorder=5)
        ax.axvspan(n, 2*n, color=color, alpha=.1)
        ax.plot([n, 2*n], [dades[n-1], dades[n-1]], ":", color=color)
        ax.plot([2*n, 2*n], [dades[n-1], dades[-1]], color="#b91c1c", lw=3)
        ax.set(xlim=(0, 2*n*1.12), xlabel="Índex del terme", ylabel="Valor del terme")
    axes[0].set(ylim=(0, 1.05), title=f"1/n: n = {n}\nSalt següent: {salt_a:.5f}; fins a 2n: {bloc_a:.5f}")
    axes[1].set(ylim=(0, 7), title=f"Sumes harmòniques: n = {n}\nSalt següent: {salt_h:.5f}; fins a 2n: {bloc_h:.5f}")
''',
    tasca=r'''
1. Per a $1/n$, si $m,n\ge N$, justifica que $|1/m-1/n|<1/N$.
   Tria un N que asseguri una distància menor que 0,01 entre **qualsevol** parella posterior.
2. A les sumes harmòniques, quin ε fix pots triar per refutar la condició de Cauchy?
   Per què sempre pots trobar una parella d'índexs prou gran que incompleix la condició?
3. Compara amb $(-1)^n$: és acotada? És de Cauchy? Dona una parella d'índexs que ho mostri.
4. Escriu una frase que corregeixi «Cauchy vol dir que dos termes consecutius estan molt junts».
''',
    resposta=r'''N=100 ja serveix perquè la distància és estrictament menor que 1/N; N=101
també serveix. Per a $H_n$, ε=1/2 refuta la condició: tria n tan gran com calgui i m=2n.
La successió alternant és acotada entre −1 i 1, però un índex parell i un d'imparell
sempre donen distància 2. Cauchy exigeix proximitat entre qualsevol parella d'una cua prou avançada.''',
)

LABS["06_Completesa_R.ipynb"] = dict(
    abans="## 2. El punt de partida",
    meta="Distingir el màxim d'una mostra, una cota superior i el suprem del conjunt infinit.",
    pregunta="El valor més gran que es veu a la pantalla és el més gran de tot el conjunt?",
    text=r'''
### Una escala que s'acosta al sostre

Considera $S=\{1-1/n:n=1,2,3,\ldots\}=\{0,1/2,2/3,3/4,\ldots\}$.
Els primers cinc valors tenen màxim $4/5$. Però el següent és $5/6>4/5$:
el màxim de la **mostra** no és un màxim del **conjunt infinit**.

- **Cota superior:** un sostre que cap element supera. 1, 1,1 i 2 són cotes superiors.
- **Suprem:** el més baix dels sostres possibles. Aquí és 1.
- **Màxim:** un element del conjunt que és més gran o igual que tots els altres. Aquí no n'hi ha.

Posem a prova el candidat 0,95. Sembla un sostre si només mirem pocs termes.
Resolem $1-1/n>0{,}95$: equival a $n>20$.

**Prediu.** Què passarà als termes 20 i 21? **Pausa** just abans de 21 i just després.
La dreta mostra la distància al sostre 1; baixar no significa arribar-hi en un pas finit.
''',
    codi=r'''
titol_laboratori = "Màxim visible i suprem: dues idees diferents"
fotogrames_laboratori = [1, 2, 3, 4, 5, 8, 10, 15, 19, 20, 21, 25, 30, 40, 60, 100]

def estat_suprem(n):
    maxim = 1-Fraction(1, n)
    return maxim, Fraction(1, n), maxim > Fraction(19, 20)

def dibuixa_laboratori(n, axes):
    maxim, distancia, supera = estat_suprem(n)
    ax, bx = axes
    indices = np.arange(1, n+1)
    ax.plot(indices, 1-1/indices, "o", ms=4, color="#2563eb", label="Mostra de S")
    ax.scatter(n, float(maxim), color="#ea580c", s=65, zorder=5)
    ax.axhline(1, color="#047857", label="Suprem de S: 1")
    ax.axhline(.95, color="#b91c1c", ls="--", label="Candidat: 0,95")
    ax.set(xlim=(0, 103), ylim=(-.04, 1.07), xlabel="n", ylabel="1 − 1/n",
           title=f"Mostrem {n} termes; màxim = {maxim}\n{'0,95 ja ha estat superat' if supera else 'Encara no hem superat 0,95'}")
    ax.legend(loc="lower right", fontsize=8)
    bx.semilogy(indices, 1/indices, color="#7c3aed")
    bx.scatter(n, float(distancia), color="#7c3aed", s=65)
    bx.set(xlim=(0, 103), ylim=(.008, 1.2), xlabel="n", ylabel="Distància a 1: 1/n",
           title=f"Distància exacta: {distancia}\nÉs positiva en cada pas finit")
''',
    tasca=r'''
1. Troba un element de S més gran que 0,999. Justifica el teu índex sense provar tots els termes.
2. Per als conjunts $\{1,2,3\}$, $(0,1)$ i $[0,1]$, indica una cota superior,
   el suprem i si existeix màxim.
3. Explica per què veure els primers 100 termes no basta per assegurar una propietat de tot S.
4. **Ampliació:** quina diferència hi ha entre l'exemple concret, en què podem demostrar
   que el suprem és 1, i l'axioma que afirma l'existència del suprem de qualsevol conjunt real
   no buit i acotat superiorment?
''',
    resposta=r'''Cal n>1000; per exemple n=1001. Per a {1,2,3}, suprem i màxim són 3
i 4 és una altra cota superior. Per a (0,1), el suprem és 1 però no hi ha màxim.
Per a [0,1], suprem i màxim són 1. L'axioma tracta tots els conjunts amb les hipòtesis
indicades: una animació d'un sol exemple no el demostra.''',
)

LABS["07_Limits_Continuitat.ipynb"] = dict(
    abans="## 2. La definició",
    meta="Llegir límits laterals i separar el valor d'una funció del valor al qual s'apropa.",
    pregunta="Canviar només un punt de la gràfica pot canviar el límit?",
    text=r'''
### Dos viatgers s'acosten al mateix lloc

A l'esquerra definim $f(x)=x+1$ per a $x\ne1$ i $f(1)=3$.
El viatger blau ve de l'esquerra ($x=1-h$) i el taronja de la dreta ($x=1+h$), amb $h>0$.
Les altures són $2-h$ i $2+h$: totes dues s'apropen a 2. El punt ple $(1,3)$ és el valor
assignat a la funció i **no es mou**. El cercle buit $(1,2)$ indica el forat.

A la dreta, $g(x)=-1$ si $x<0$ i $g(x)=1$ si $x\ge0$. Els viatgers s'acosten a 0,
però mantenen altures diferents. Aquest és un salt, no un forat que puguem omplir amb un sol valor.

| h | f(1−h) | f(1+h) | g(−h) | g(h) |
|---|---|---|---|---|
| 0,1 | 1,9 | 2,1 | −1 | 1 |
| 0,01 | 1,99 | 2,01 | −1 | 1 |

**Prediu** la fila h=0,001. **Pausa** i identifica, per separat, el límit esquerre,
el límit dret i el valor en el punt. No els dedueixis només del punt ple.
''',
    codi=r'''
titol_laboratori = "Apropar-se a un punt: un forat i un salt"
fotogrames_laboratori = list(range(18))

def estat_limits(pas):
    h = .8*(.72**pas)
    return h, 2-h, 2+h, -1.0, 1.0

def dibuixa_laboratori(pas, axes):
    h, esquerre, dret, ge, gd = estat_limits(pas)
    ax, bx = axes
    x = np.linspace(0, 2, 300)
    ax.plot(x, x+1, color="0.5")
    ax.scatter([1], [2], facecolor="white", edgecolor="0.2", s=85, zorder=6)
    ax.scatter([1], [3], color="#7c3aed", s=60, label="f(1) = 3", zorder=5)
    for xx, yy, color in [(1-h, esquerre, "#2563eb"), (1+h, dret, "#ea580c")]:
        ax.scatter(xx, yy, color=color, s=65, zorder=5)
        ax.plot([xx, xx], [0, yy], ":", color=color)
    ax.axhline(2, ls="--", color="#047857", label="Límit: 2")
    ax.set(xlim=(0, 2), ylim=(0, 3.5), xlabel="x", ylabel="f(x)",
           title=f"Forat: h = {h:.5f}\nf(1−h) = {esquerre:.5f}; f(1+h) = {dret:.5f}")
    ax.legend(loc="lower right", fontsize=8)
    bx.plot([-1, 0], [-1, -1], color="0.5")
    bx.plot([0, 1], [1, 1], color="0.5")
    bx.scatter([0], [-1], facecolor="white", edgecolor="0.2", s=85, zorder=6)
    bx.scatter([0], [1], color="#7c3aed", s=60, zorder=6)
    bx.scatter([-h, h], [ge, gd], color=["#2563eb", "#ea580c"], s=65, zorder=5)
    bx.set(xlim=(-1, 1), ylim=(-1.5, 1.5), xlabel="x", ylabel="g(x)",
           title="Salt: límit esquerre −1; límit dret 1\nNo existeix el límit bilateral a 0")
''',
    tasca=r'''
1. Si canviem només f(1) de 3 a 2, què canvia: els límits laterals, el límit bilateral o la continuïtat?
2. Podem fer contínua g a 0 canviant només g(0)? Justifica-ho amb els dos costats.
3. Per a f i una tolerància vertical 0,01, quina distància horitzontal al punt 1 és suficient?
   Explica-ho primer amb paraules i després amb $|x-1|$ i $|f(x)-2|$.
4. Trobar dues successions que tendeixen a la mateixa altura prova sempre que existeix el límit?
   Què permeten concloure dues successions amb altures límit diferents?
''',
    resposta=r'''Només canvia la continuïtat: amb f(1)=2, la funció és contínua.
El salt de g no es repara canviant un sol punt. Si $0<|x-1|<0{,}01$, llavors
$|f(x)-2|=|x-1|<0{,}01$. Dues successions concordants no proven el límit per a tots
els camins; dues amb límits diferents sí que el refuten.''',
)

LABS["Derivades_BAT.ipynb"] = dict(
    abans="## 2. Al punt",
    meta="Relacionar la taxa de variació mitjana amb la pendent de la secant i el seu límit.",
    pregunta="Què significa la velocitat en un instant si la fórmula habitual divideix per un interval de temps?",
    text=r'''
### De la velocitat mitjana a la instantània

Un mòbil segueix $s(t)=t^2$ metres, amb t en segons. Entre t=1 i t=1+h, la velocitat mitjana és

$$\frac{s(1+h)-s(1)}{h}=\frac{(1+h)^2-1}{h}=2+h\quad(h\ne0).$$

| h (s) | Increment de posició (m) | Velocitat mitjana (m/s) |
|---|---|---|
| 1 | 3 | 3 |
| 0,1 | 0,21 | 2,1 |
| 0,01 | 0,0201 | 2,01 |

**No substituïm h=0 al quocient.** Estudiem a quin valor s'apropa quan l'interval es fa petit.
El triangle taronja del dibuix mostra $\Delta t=h$ i $\Delta s$. La seva proporció és la pendent.
La recta verda és la tangent de pendent 2 al punt (1,1).

A la dreta repetim la idea amb $|x|$ a 0. Les pendents són −1 per l'esquerra i 1 per la dreta:
els dos costats **no** acorden una única pendent.

**Prediu** la velocitat mitjana entre t=0,9 i t=1. **Pausa** abans del final i explica
què significa cada costat del triangle, incloent les unitats.
''',
    codi=r'''
titol_laboratori = "La secant s'apropa a la tangent; una cantonada no té una sola pendent"
fotogrames_laboratori = list(range(18))

def estat_derivada(pas):
    h = .9*(.76**pas)
    return h, ((1+h)**2-1)/h, (1-(1-h)**2)/h

def dibuixa_laboratori(pas, axes):
    h, dreta, esquerra = estat_derivada(pas)
    ax, bx = axes
    x = np.linspace(-.2, 2.1, 300)
    ax.plot(x, x*x, color="#2563eb", label="s(t) = t²")
    ax.plot(x, 1+dreta*(x-1), color="#ea580c", label="Secant")
    ax.plot(x, 2*x-1, "--", color="#047857", label="Tangent: pendent 2")
    ax.plot([1, 1+h, 1+h], [1, 1, (1+h)**2], color="#ea580c", lw=2)
    ax.scatter([1, 1+h], [1, (1+h)**2], color="#ea580c", zorder=5)
    ax.set(xlim=(-.1, 2.1), ylim=(-.5, 4.5), xlabel="Temps t (s)", ylabel="Posició s (m)",
           title=f"h = {h:.5f} s; pendent = {dreta:.5f} m/s\nPel costat esquerre: {esquerra:.5f} m/s")
    ax.legend(fontsize=8, loc="upper left")
    x = np.linspace(-1, 1, 300)
    bx.plot(x, np.abs(x), color="#7c3aed", lw=2)
    bx.plot(x, x, "--", color="#ea580c", label="Pendent dreta: +1")
    bx.plot(x, -x, "--", color="#2563eb", label="Pendent esquerra: −1")
    bx.scatter([-h, 0, h], [h, 0, h], color=["#2563eb", "0.2", "#ea580c"], s=55, zorder=5)
    bx.set(xlim=(-1, 1), ylim=(-.15, 1.1), xlabel="x", ylabel="|x|",
           title="Contínua a 0, però no derivable\nLes pendents laterals continuen sent diferents")
    bx.legend(fontsize=8, loc="upper center")
''',
    tasca=r'''
1. Desenvolupa $(2+h)^2-4$ i dedueix la derivada de $x^2$ al punt 2 a partir del quocient incremental.
2. Per a $s(t)=3t+2$, calcula dues velocitats mitjanes amb intervals diferents. Quina és la instantània?
3. Per què el triangle del dibuix s'encongeix, però la seva proporció no tendeix a 0?
4. Dona un exemple de funció contínua que no sigui derivable i justifica'l amb pendents laterals.
''',
    resposta=r'''El quocient és $4+h$ i el límit és 4. Per a $s(t)=3t+2$, totes les velocitats
mitjanes i la instantània són 3 m/s. El quocient de dues quantitats que tendeixen a 0
no ha de tendir a 0: aquí tendeix a 2. $|x|$ és contínua a 0 però té pendents laterals −1 i 1.''',
)

LABS["LaRecta.ipynb"] = dict(
    abans="## Activitats",
    meta="Interpretar la pendent com una proporció amb signe i unitats, no com una inclinació aparent a la pantalla.",
    pregunta="Si canviem la mida del triangle de pendent, canvia la pendent de la recta?",
    text=r'''
### Una rampa, dos triangles, una mateixa proporció

Una rampa puja 2 m per cada 3 m de recorregut horitzontal. La pendent és
$m=\Delta y/\Delta x=2/3$. Un triangle amb base 6 m té altura 4 m: $4/6=2/3$.
**La proporció es conserva encara que triem dos punts més allunyats.**

A l'animació, l'ordenada a l'origen es manté en $b=1$ i canviem m.
La recta sempre passa per (0,1). Blau: triangle de base 1. Taronja: triangle de base 2.
Si m és negativa, l'increment vertical també és negatiu: ens desplacem cap avall.

El gràfic dret representa $\Delta y=m\Delta x$: quan dupliquem $\Delta x$, també
dupliquem $\Delta y$. El punt de tall b no intervé en aquesta proporció.

**Prediu.** Amb m=−1,5 i b=1, quina és y quan x=2? **Pausa** a m=0: què tenen d'especial
els triangles? Una recta vertical, en canvi, té $\Delta x=0$ i no té pendent finita.
''',
    codi=r'''
titol_laboratori = "Pendent: canvi vertical dividit pel canvi horitzontal"
fotogrames_laboratori = list(range(17))

def dades_rampa(m, dx, b=1):
    return m*dx, b+m*dx

def dibuixa_laboratori(pas, axes):
    m = -2+pas/4
    ax, bx = axes
    x = np.linspace(-1, 3, 200)
    ax.plot(x, m*x+1, color="#7c3aed", lw=2)
    for dx, color in [(1, "#2563eb"), (2, "#ea580c")]:
        dy, y = dades_rampa(m, dx)
        ax.plot([0, dx, dx], [1, 1, y], color=color, lw=2, label=f"Δx={dx}; Δy={dy:g}")
        ax.scatter([dx], [y], color=color, s=50)
    ax.scatter([0], [1], color="0.2", s=55, zorder=5)
    ax.set(xlim=(-.5, 2.5), ylim=(-4, 6), xlabel="x", ylabel="y", title=f"y = {m:g}x + 1\nTotes passen per (0,1)")
    ax.legend(fontsize=8, loc="upper left")
    dx = np.linspace(0, 3, 100)
    bx.plot(dx, m*dx, color="#047857")
    bx.scatter([1, 2], [m, 2*m], color=["#2563eb", "#ea580c"], s=60)
    bx.axhline(0, color="0.5", lw=.7)
    bx.set(xlim=(0, 3), ylim=(-6.5, 6.5), xlabel="Δx", ylabel="Δy",
           title=f"Proporció constant: Δy / Δx = {m:g}\nLa pendent conserva el signe")
''',
    tasca=r'''
1. Una recta passa per (2,5) i (6,3). Calcula m, després b i comprova l'equació amb els dos punts.
2. Un taxi cobra 3 € inicials i 1,50 €/km. Escriu l'equació, les unitats de m i b i el preu de 4 km.
3. Dues rectes tenen la mateixa pendent però ordenades diferents: què tenen en comú? Es tallen?
4. Per què una recta vertical no es pot escriure en la forma $y=mx+b$ amb m finit?
''',
    resposta=r'''m=−1/2 i b=6, de manera que y=−x/2+6. El taxi segueix P=1,5d+3:
m té unitats €/km i b euros; per a 4 km són 9 €. Les rectes amb pendent igual i ordenades
diferents són paral·leles. En una vertical, Δx=0 i dividir Δy per Δx no està definit.''',
)

LABS["ComplexNumbers.ipynb"] = dict(
    abans="## 3. Fórmula",
    meta="Veure la multiplicació complexa com un gir i una dilatació i connectar-ho amb el càlcul algebraic.",
    pregunta="Multiplicar per i fa el nombre més gran o el fa girar?",
    text=r'''
### Multiplicar per i és fer un quart de volta

Prenem $z=2+i$. Com que $i^2=-1$,

$$i(2+i)=2i+i^2=-1+2i.$$

El punt (2,1) es transforma en (−1,2): un gir de 90° en sentit antihorari.
La distància a l'origen es manté: $\sqrt{2^2+1^2}=\sqrt{(-1)^2+2^2}=\sqrt5$.

| Multiplicació | Resultat | Coordenades |
|---|---|---|
| z | 2+i | (2,1) |
| iz | −1+2i | (−1,2) |
| i²z | −2−i | (−2,−1) |
| i³z | 1−2i | (1,−2) |
| i⁴z | 2+i | (2,1) |

L'animació mostra també els girs intermedis: multipliquem per
$w=\cos\theta+i\sin\theta$, de mòdul 1. L'esquerra mostra el gir; les barres de la dreta
són les parts real i imaginària del resultat, **no** dues distàncies sempre positives.

**Prediu** on serà el punt després de dos quarts de volta. **Pausa** a 90°, 180° i 270°
i comprova el resultat algebraic. La circumferència conserva el radi √5.
''',
    codi=r'''
titol_laboratori = "Multiplicar complexos: veure el gir i comprovar les coordenades"
fotogrames_laboratori = list(range(25))

def gira_complex(z, graus, escala=1):
    angle = math.radians(graus)
    w = escala*complex(math.cos(angle), math.sin(angle))
    return w, w*z

def dibuixa_laboratori(pas, axes):
    graus = 15*pas
    z = 2+1j
    w, producte = gira_complex(z, graus)
    ax, bx = axes
    t = np.linspace(0, 2*np.pi, 250)
    ax.plot(abs(z)*np.cos(t), abs(z)*np.sin(t), ":", color="0.6")
    ax.axhline(0, color="0.5", lw=.7)
    ax.axvline(0, color="0.5", lw=.7)
    for u, color, nom in [(z, "#2563eb", "z = 2+i"), (producte, "#ea580c", "w·z")]:
        ax.annotate("", (u.real, u.imag), (0, 0), arrowprops=dict(arrowstyle="->", color=color, lw=2))
        ax.scatter(u.real, u.imag, color=color, label=nom, s=50)
    ax.set(aspect="equal", xlim=(-2.7, 2.7), ylim=(-2.7, 2.7), xlabel="Part real", ylabel="Part imaginària",
           title=f"Gir: {graus}°; |w| = 1\n|w·z| = |z| ≈ {abs(producte):.5f}")
    ax.legend(loc="lower left", fontsize=8)
    bx.bar([0, 1], [producte.real, producte.imag], color=["#2563eb", "#ea580c"])
    bx.axhline(0, color="0.2")
    bx.set(xticks=[0, 1], xticklabels=["Part real", "Part imaginària"], ylim=(-2.7, 2.7),
           title=f"w ≈ {w.real:.3f} + ({w.imag:.3f})i\nw·z ≈ {producte.real:.3f} + ({producte.imag:.3f})i")
    bx.text(.5, .04, f"a²+b² = {abs(producte)**2:.3f}", transform=bx.transAxes, ha="center")
''',
    tasca=r'''
1. Calcula $i(3-2i)$ i comprova'l amb un gir del punt (3,−2).
2. Compara $z+i$ amb $iz$ per a z=2+i. Quina operació trasllada? Quina gira?
3. Executa `gira_complex(2+1j, 90, escala=2)`. Com canvien el gir i el mòdul si multipliquem per 2i?
4. Per què el nombre 0 té mòdul, però no un argument definit?
''',
    resposta=r'''i(3−2i)=2+3i. Sumar i trasllada una unitat cap amunt; multiplicar per i
gira 90°. Multiplicar per 2i gira 90° i duplica el mòdul: el resultat és −2+4i.
El zero té mòdul 0, però no determina cap direcció des de l'origen.''',
)

LABS["AnálisisUnivariante(I).ipynb"] = dict(
    abans="## 2. Diagrama",
    meta="Interpretar com un valor extrem modifica la mitjana, la mediana i la forma d'una distribució.",
    pregunta="Una mitjana més alta vol dir que gairebé tots els valors han augmentat?",
    text=r'''
### Canviem una sola dada: què explica cada resum?

Treballem amb **21 temps sintètics** de desplaçament a classe, en minuts.
Vint es mantenen fixos; només canviem el més gran, de 15 a 60 minuts.
No són dades recollides d'alumnes reals.

- La **mitjana** reparteix la suma entre totes les observacions: qualsevol canvi hi influeix.
- La **mediana** és el valor central després d'ordenar: amb 21 dades, la posició és l'11a.
- El **diagrama de caixa** situa mediana, quartils i possibles valors atípics.
  El criteri d'1,5 vegades el recorregut interquartílic marca valors per revisar, no errors automàtics.

L'histograma conserva els mateixos intervals, eixos i nombre de dades en tots els fotogrames.
Així els canvis visuals corresponen a les dades, no a un canvi d'escala.

**Prediu.** Si l'única dada modificada augmenta 21 minuts, quant pujarà la mitjana?
**Pausa** i comprova si s'ha mogut la mediana. Quantes persones han canviat el temps de trajecte?
''',
    codi=r'''
titol_laboratori = "Una dada extrema: mitjana i mediana no expliquen el mateix"
from inspect import signature
temps_fixos = np.array([8, 9, 9, 10, 10, 10, 11, 11, 11, 12,
                       12, 12, 12, 13, 13, 13, 14, 14, 14, 15], dtype=float)
fotogrames_laboratori = list(range(16))

def resum_temps(valor):
    dades = np.append(temps_fixos, valor)
    return dades, float(np.mean(dades)), float(np.median(dades))

def dibuixa_laboratori(pas, axes):
    valor = 15+3*pas
    dades, mitjana, mediana = resum_temps(valor)
    ax, bx = axes
    ax.hist(dades, bins=np.arange(5, 66, 5), color="#bfdbfe", edgecolor="#2563eb")
    ax.axvline(mitjana, color="#ea580c", lw=2, label=f"Mitjana: {mitjana:.2f}")
    ax.axvline(mediana, color="#047857", lw=2, ls="--", label=f"Mediana: {mediana:.2f}")
    ax.set(xlim=(5, 65), ylim=(0, 18), xlabel="Temps (minuts)", ylabel="Freqüència absoluta",
           title=f"21 observacions; només en canvia una\nValor modificat: {valor} minuts")
    ax.legend(fontsize=8)
    orientacio = ({"orientation": "horizontal"} if "orientation" in signature(bx.boxplot).parameters
                  else {"vert": False})
    bx.boxplot(dades, **orientacio, widths=.35, patch_artist=True,
               boxprops=dict(facecolor="#ddd6fe"), medianprops=dict(color="#047857", linewidth=2))
    bx.scatter([valor], [.65], color="#ea580c", s=55, label="Dada que modifiquem")
    bx.set(xlim=(5, 65), ylim=(.45, 1.5), yticks=[], xlabel="Temps (minuts)",
           title="Mateixa escala que l'histograma\nEls punts separats són possibles valors atípics")
    bx.legend(fontsize=8, loc="upper right")
''',
    tasca=r'''
1. Calcula quant puja la mitjana quan la dada passa de 15 a 60. Comprova que no necessites tornar a sumar-ho tot.
2. Per a una notícia sobre el trajecte «típic», quin resum destacaries en aquest exemple? Justifica-ho amb les dades.
3. És correcte esborrar una dada només perquè apareix com a atípica? Què comprovaries abans?
4. Canvia el nombre de classes de l'histograma original. Què canvia visualment i què es manté en les dades?
''',
    resposta=r'''La mitjana puja (60−15)/21=15/7≈2,142857 minuts. La mediana es manté en 12.
En aquesta mostra la mediana descriu millor la posició central sense arrossegar-se pel valor extrem,
però convé informar també de la dispersió. Cal revisar unitats, transcripció i context abans
d'eliminar observacions. Canviar classes modifica la representació, no les dades ni la seva mitjana.''',
)

LABS["PràcticaBasedeDades.ipynb"] = dict(
    abans="## 4. Exportació",
    meta="Seguir cada valor des de la taula original fins al format llarg conservant persona, any, categoria i unitats.",
    pregunta="Si una taula té més files després de transformar-la, hem creat més observacions originals?",
    text=r'''
### Segueix una dada: no perdis qui, quan i què

Abans de treballar amb milers de registres, fem-ho amb **3 identificadors i 2 anys**.
Les dades són sintètiques. Les columnes 2025 i 2026 contenen imports salarials en euros;
2025.2 i 2026.2 contenen nombre de treballadors. És el mateix conveni de noms del codi anterior.

Una cel·la com «ID 2, columna 2026, valor 24» es transforma en una fila amb
`rank=2`, `year=2026`, `category=Salary`, `value=24`. El nom de la columna aporta
l'any i la categoria; el valor numèric tot sol no conté aquesta informació.

**Prediu.** Tres identificadors × dos anys × dues categories: quantes files tindrem?
**Pausa.** Localitza la cel·la taronja a la taula ampla i reconstrueix els quatre camps
de la fila taronja del format llarg. Les altres files encara no visitades apareixen buides.
No hem creat persones noves: hem canviat la manera de representar-ne les variables.
''',
    codi=r'''
titol_laboratori = "Una cel·la es converteix en una fila amb significat"
mini_ample = pd.DataFrame({"ID": [1, 2, 3], "2025": [18, 22, 20], "2026": [20, 24, 21],
                           "2025.2": [2, 3, 4], "2026.2": [3, 4, 4]})
mini_llarg, _ = format_llarg(mini_ample)
fotogrames_laboratori = list(range(len(mini_llarg)))

def origen_registre(pas):
    fila = mini_llarg.iloc[pas]
    columna = str(int(fila["year"])) + (".2" if fila["category"] == "employees" else "")
    posicio = int(np.flatnonzero(mini_ample["ID"].to_numpy() == fila["rank"])[0])
    return posicio, columna, fila

def dibuixa_laboratori(pas, axes):
    ax, bx = axes
    posicio, columna, fila = origen_registre(pas)
    for axis in axes:
        axis.axis("off")
    ta = ax.table(cellText=mini_ample.values, colLabels=mini_ample.columns,
                  cellLoc="center", loc="center")
    ta.auto_set_font_size(False)
    ta.set_fontsize(10)
    ta.scale(1, 2)
    ta[(posicio+1, mini_ample.columns.get_loc(columna))].set_facecolor("#fed7aa")
    ta[(posicio+1, 0)].set_facecolor("#dbeafe")
    camps = ["rank", "year", "category", "value"]
    files = [[str(mini_llarg.iloc[k][c]) for c in camps] if k <= pas else ["", "", "", ""]
             for k in range(len(mini_llarg))]
    tb = bx.table(cellText=files, colLabels=["ID", "Any", "Categoria", "Valor"],
                  cellLoc="center", loc="center", colWidths=[.14, .18, .43, .2])
    tb.auto_set_font_size(False)
    tb.set_fontsize(9)
    tb.scale(1, 1.35)
    for j in range(4):
        tb[(pas+1, j)].set_facecolor("#fed7aa")
    unitat = "euros" if fila["category"] == "Salary" else "treballadors"
    ax.set_title(f"Format ample: 3 files\nID {fila['rank']}, columna {columna}: {fila['value']} {unitat}")
    bx.set_title(f"Format llarg: {pas+1} de 12 files\nConservem ID, any, categoria i valor")
''',
    tasca=r'''
1. Filtra només la categoria Salary de 2026 i calcula la mitjana. Quina unitat té?
2. Per què no hem de calcular una única mitjana barrejant Salary i employees?
3. Reordena les columnes de `mini_ample` i torna a aplicar `format_llarg`.
   Comprova el mateix contingut ordenant per ID, any i categoria, sense exigir el mateix ordre de files.
4. Si hi hagués 5 identificadors, 4 anys i 3 categories completes, quantes files tindria el format llarg?
''',
    resposta=r'''Per a Salary de 2026: (20+24+21)/3=65/3≈21,67 euros.
Barrejar euros i nombre de treballadors produeix un resum sense unitat interpretable.
La transformació ha de conservar el significat encara que canviï l'ordre de columnes;
amb 5 identificadors, 4 anys i 3 categories hi hauria 60 files.''',
)


LABS["LaRecta.ipynb"]["mostra"] = 12
LABS["Derivades_BAT.ipynb"]["mostra"] = 3
LABS["ComplexNumbers.ipynb"]["mostra"] = 6
LABS["07_Limits_Continuitat.ipynb"]["mostra"] = 4

AMPLIACIONS = {
    "Q_conjunt_dens.ipynb": ["## 3. Per què falta un racional?"],
    "NumeroPi.ipynb": ["## 2. Una demostració que serveix per a tots els passos"],
    "04_Talladures_Dedekind.ipynb": ["## 2. Propietats que cal justificar", "## 3. Què estem construint?"],
    "05_Successions_Cauchy.ipynb": ["## 2. Tres justificacions, no només tres gràfiques", "## 3. De Cauchy en ℚ, però sense límit en ℚ"],
    "06_Completesa_R.ipynb": ["## 2. El punt de partida lògic", "## 3. Del suprem als intervals encaixats"],
    "07_Limits_Continuitat.ipynb": ["## 2. La definició ε–δ"],
}


def enriqueix(filename, cells, md, code):
    """Insereix cada laboratori després dels seus prerequisits, abans de la formalització."""
    lab = LABS[filename]
    ruta = md(f'''
    ## Ruta guiada per a 1r de batxillerat

    **Pregunta de partida:** {lab['pregunta']}

    **Al final ho has de poder explicar:** {lab['meta']}

    La primera lectura combina l'exemple resolt amb el **laboratori animat** i les preguntes
    que l'acompanyen. Els apartats marcats com a ampliació formal aprofundeixen en el rigor;
    no cal entendre tot el codi per interpretar la matemàtica.

    Dedica 2 minuts a una predicció escrita, 8–10 minuts a experimentar i pausar,
    i 5 minuts a justificar una conclusió amb càlculs. Després resol el repte amb dades noves.
    L'animació té controls de reproducció, pausa i selecció de fotograma.
    Si el visor no mostra HTML interactiu, el fotograma estàtic i la funció
    `fotograma_laboratori(...)` permeten fer la mateixa activitat pas a pas després d'executar el codi.
    ''')
    cells.insert(2, ruta)
    insert_at = next(i for i, cell in enumerate(cells)
                     if cell["cell_type"] == "markdown" and lab["abans"] in cell["source"])
    mostra = str(lab["mostra"]) if "mostra" in lab else "fotogrames_laboratori[len(fotogrames_laboratori)//2]"
    block = [
        md("## Laboratori animat · observa, atura i explica\n\n" + lab["text"]),
        code(AJUDANTS),
        code(lab["codi"]),
        code("# Fotograma visible també quan no es reprodueix l'animació.\n"
             f"fotograma_laboratori({mostra})"),
        md("**Ara reprodueix l'animació.** Fes servir la pausa i el control de fotograma per contrastar "
           "la teva predicció. Els valors numèrics dels títols formen part de l'explicació."),
        code("display(anima_laboratori())"),
        md("### Investiga i transfereix\n\n" + lab["tasca"]),
        md("### El teu raonament\n\nEdita aquesta cel·la per deixar evidència del que has après.\n\n"
           "- **Abans pensava que…**\n- **He provat aquests valors…**\n"
           "- **Al gràfic he observat…**\n- **Ho justifico amb aquest càlcul o propietat…**\n"
           "- **La meva conclusió i el seu límit són…**\n\n"
           "No n'hi ha prou amb una captura: relaciona el dibuix, els nombres i l'explicació."),
        code("# Espai per al teu experiment: canvia l'índex i executa la cel·la.\n"
             "# fotograma_laboratori(fotogrames_laboratori[0])\n"
             "# Escriu aquí els càlculs del repte.\n"),
        md("<details><summary>Comprovació: obre-la després d'intentar els reptes</summary>\n\n"
           + lab["resposta"] + "\n\n</details>\n\n"
           "**Comprova el teu aprenentatge:** has interpretat els eixos i les unitats, "
           "justificat una predicció amb un càlcul i aplicat la idea a un cas nou? "
           "Una observació finita pot suggerir una propietat; una afirmació general necessita una justificació."),
    ]
    block[6:6] = celles_taller(filename, md, code)
    cells[insert_at:insert_at] = block
    for cell in cells:
        if cell["cell_type"] == "markdown":
            for title in AMPLIACIONS.get(filename, []):
                cell["source"] = cell["source"].replace(title, title + " · Ampliació formal")
    return cells
