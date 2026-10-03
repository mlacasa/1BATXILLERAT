# De l'exhauriment del cercle a la completesa de ℝ

**Matemàtiques · 1r de batxillerat**  
**Dr. Lacasa-Cazcarra · Any 2026**

Dotze quaderns autònoms en català: un recorregut principal de vuit quaderns i quatre complements.
La pregunta conductora és: **si podem aproximar un nombre cada vegada millor, què garanteix
que existeix el nombre al qual ens apropem?**

L'experimentació amb Python acompanya les definicions, els contraexemples i les demostracions.
Calcular π il·lustra la completesa; no demostra per si sol que ℝ sigui complet.

## Recorregut principal

| Ordre | Quadern | Experiment i objectiu | Sessions orientatives |
|---|---|---|---|
| 01 | [Racionals: densitat i nombres que falten](Q_conjunt_dens.ipynb) | Punts mitjans, bisecció exacta de l'arrel de 2 i irracionalitat | 1–2 |
| 02 | [Exhaurir el cercle](Càlcul_Nombre_pi.ipynb) | Polígons inscrits i circumscrits, perímetres i intervals | 1 |
| 03 | [L'algorisme d'Arquimedes](NumeroPi.ipynb) | Duplicació de costats sense conèixer π; control i certificació de l'error | 2 |
| 04 | [Talladures de Dedekind](04_Talladures_Dedekind.ipynb) | Classificació exacta de racionals; representació d'un nombre per un tall | 1–2 |
| 05 | [Successions i criteri de Cauchy](05_Successions_Cauchy.ipynb) | Distàncies entre termes de cues; contraexemple harmònic | 2 |
| 06 | [La completesa de ℝ](06_Completesa_R.ipynb) | Suprem → intervals encaixats → convergència de Cauchy | 2 |
| 07 | [Límits i continuïtat](07_Limits_Continuitat.ipynb) | Límits laterals, bandes ε–δ i valor al punt | 1–2 |
| 08 | [De la secant a la derivada](Derivades_BAT.ipynb) | Pendents de secants, límits laterals i tangent vertical | 2 |

Els noms dels quatre fitxers principals que ja existien es conserven. El número apareix al títol,
al quadern i a aquesta guia; els quatre quaderns nous porten també el número al nom del fitxer.
Cada quadern inclou objectiu, prerequisits, instruccions, experiments, justificacions,
activitats, pistes desplegables i navegació al següent.

**Obrir directament a Colab:**
[01 · Racionals](https://colab.research.google.com/github/mlacasa/1BATXILLERAT/blob/main/Q_conjunt_dens.ipynb) ·
[02 · Exhauriment](https://colab.research.google.com/github/mlacasa/1BATXILLERAT/blob/main/C%C3%A0lcul_Nombre_pi.ipynb) ·
[03 · Arquímedes](https://colab.research.google.com/github/mlacasa/1BATXILLERAT/blob/main/NumeroPi.ipynb) ·
[04 · Dedekind](https://colab.research.google.com/github/mlacasa/1BATXILLERAT/blob/main/04_Talladures_Dedekind.ipynb) ·
[05 · Cauchy](https://colab.research.google.com/github/mlacasa/1BATXILLERAT/blob/main/05_Successions_Cauchy.ipynb) ·
[06 · Completesa](https://colab.research.google.com/github/mlacasa/1BATXILLERAT/blob/main/06_Completesa_R.ipynb) ·
[07 · Límits](https://colab.research.google.com/github/mlacasa/1BATXILLERAT/blob/main/07_Limits_Continuitat.ipynb) ·
[08 · Derivades](https://colab.research.google.com/github/mlacasa/1BATXILLERAT/blob/main/Derivades_BAT.ipynb).

## Organització de l'aula

Per a cada experiment: **predir → executar → descriure → conjecturar → justificar → aplicar**.
L'alumne ha d'escriure una resposta abans de moure els controls i revisar-la després.
No és necessari comprendre tot el codi per seguir el recorregut matemàtic.

Una ruta inicial curta pot emprar 01, 02, la part bàsica de 03, les definicions de 04 i 05,
i la síntesi de 06. La certificació amb aritmètica racional i la demostració general de
convergència de Cauchy són ampliacions. Els quaderns 07 i 08 fan el pont al càlcul diferencial.

Proposta de lliurament final: una pàgina amb un interval per a π, la cota d'error del seu
punt mig, una explicació del paper de la completesa i una comparació entre les aproximacions
racionals a √2 i una successió racional que convergeix a un racional.
Valoreu separadament el càlcul, la interpretació dels quantificadors i la justificació.

## Rigor matemàtic i numèric

- La densitat de ℚ no implica que ℚ sigui complet. La bisecció de √2 ho fa visible, i la
  demostració d'irracionalitat explica per què falta un límit racional.
- L'algorisme de π parteix de semiperímetres d'hexàgons i usa mitjanes harmòniques i geomètriques.
  `np.pi` només s'utilitza per orientar el dibuix dels polígons; no intervé en el càlcul de les cotes.
- Acceptem la comparació geomètrica entre la circumferència i els perímetres poligonals.
  No desenvolupem una construcció completa de la longitud de corbes.
- La part bàsica usa `Decimal`, amb arrodoniment. L'ampliació certificada usa `Fraction`,
  arrels enteres i propagació d'intervals; les conversions a decimal són només informatives.
- Una mostra finita no demostra una condició sobre tota una cua infinita. El cas harmònic
  mostra que salts consecutius petits no impliquen Cauchy.
- Es pren el suprem com a axioma i es demostren les implicacions indicades; no s'atribueix
  a un experiment la demostració d'un axioma ni es raona circularment.
- La completitud de ℝ no vol dir que totes les successions convergeixin ni que tota funció sigui derivable.

## Complements revisats

| Quadern | Canvis principals |
|---|---|
| [La recta](LaRecta.ipynb) | Triangle de pendent, rectes verticals, controls sense vídeos ni FFmpeg |
| [Nombres complexos](ComplexNumbers.ipynb) | Associativa/distributiva, `atan2`, cas zero i comparacions amb tolerància |
| [Anàlisi univariant](AnálisisUnivariante(I).ipynb) | Freqüències amb màxim inclòs, vores compartides, dades separades, llavor fixa |
| [Transformació de dades](PràcticaBasedeDades.ipynb) | Dades sintètiques explícites, entrada CSV opcional, transformació per noms de columna |

La pràctica de dades **no reprodueix els resultats fiscals originals**: el CSV no formava part del
repositori. El lector ha de proporcionar el fitxer per estudiar dades reals. L'exportació és opcional
i no escriu cap fitxer durant una execució completa per defecte.

## Execució

**Colab:** pugeu el `.ipynb` que voleu obrir i executeu-lo des de la primera cel·la.
Els quaderns no necessiten importar fitxers Python del projecte ni muntar Google Drive.
Si falten paquets, instal·leu `numpy matplotlib pandas ipywidgets` en una cel·la amb `%pip install`.
Els enllaços relatius de navegació són per al repositori o Jupyter; a Colab, obriu el següent fitxer per separat.
Els enllaços de Colab anteriors obren els quaderns de la branca `main` del repositori.

**Jupyter local (Python 3.10 o posterior):**

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m notebook
```

A Linux/macOS, feu servir `.venv/bin/python` en lloc de `.venv/Scripts/python.exe`.
Si els controls interactius no es mostren, executeu directament la funció amb arguments:
`poligons(iteracions=4)`, `laboratori_cauchy(tipus="harmonica", N=100, finestra=100)` o
`secant(tipus="absolut", a=0, exponent=3, costat=-1)`.
Quan `ipywidgets` no està instal·lat, s'executa automàticament l'exemple per defecte.

Els quaderns distribuïts no porten sortides pesades ni animacions de vídeo incrustades.
Les figures i els controls es generen en executar-los. No hi ha logotips.

## Referència de Burgos

Referència provisional: Juan de Burgos, *Cálculo infinitesimal de una variable*, 2a edició,
McGraw-Hill, 2007, ISBN 9788448156343. S'ha verificat l'índex editorial, no el text íntegre.
La correspondència és conceptual; no s'atribueixen a Burgos aquests experiments ni exercicis.

| Apartats de l'índex de Burgos | Desenvolupament en aquest projecte |
|---|---|
| 1.1 Racionals; 1.2 Sistema dels reals | 01 i 04 |
| 1.3–1.4 Límits de successions i propietats | 03 i 05 |
| 1.5 Axiomes de ℝ; 1.6 Propietats de compleció | 06, amb motivació a 02–04 |
| 2.2 Límits; 2.4 Continuïtat en un punt | 07 |
| 3.1 Derivades | 08 |

Fonts: [índex editorial de Burgos](https://www.mheducation.es/calculo-infinitesimal-de-una-variable-9788448156343-spain)
i [Dedekind, Continuidad y números irracionales](https://www.uv.es/jkliment/Documentos/Dedekind.pc.pdf).
Quan es confirmi l'edició utilitzada a classe, es poden ajustar les referències de secció.

## Conservació i manteniment

La font original és [mlacasa/1BATXILLERAT](https://github.com/mlacasa/1BATXILLERAT),
commit `c893563e576273c8da651b94374720e2276defd3`, de 12 de febrer de 2025.
La còpia de treball local conserva els nou fitxers rebuts sense canvis a
`originals/1BATXILLERAT_c893563_original.zip`; aquest arxiu de seguretat no es publica.
Al repositori es poden recuperar des del [commit original](https://github.com/mlacasa/1BATXILLERAT/tree/c893563e576273c8da651b94374720e2276defd3).
`originals/SHA256.json` permet comprovar-ne la integritat. No s'ha afegit una llicència
que alteri els drets dels materials originals.

El fitxer `eines/genera_quaderns.py` conté la font editable de les cel·les. Després de
modificar-la, regenereu i valideu:

```powershell
python eines/genera_quaderns.py
python eines/comprova_matematiques.py
python eines/valida_quaderns.py --figures validacio/figures
```

El generador substitueix els dotze `.ipynb` d'aquesta edició. Si heu editat directament
un quadern, traslladeu primer els canvis al generador. La validació executa cada quadern
amb un nucli nou i comprova també crides explícites als experiments; no desa sortides als originals.
El resum i les versions dels paquets queden a `VALIDACIO.json`.
