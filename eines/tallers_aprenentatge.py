"""Comparació, experimentació i retorn formatiu per als dotze quaderns de 1r BAT."""


def pregunta(enunciat, opcions, correcta, retorn):
    return dict(enunciat=enunciat, opcions=opcions, correcta=correcta, retorn=retorn)


TALLERS = {
    "Q_conjunt_dens.ipynb": dict(
        parella=(0, 5), etiquetes='[f"Decisió {k+1}" for k in fotogrames_laboratori]',
        comparacio="Compara la primera i la sisena decisió. A l'esquerra, l'escala és fixa; a la dreta s'amplia cada interval. Calcula la proporció entre les amplades: no la dedueixis de la llargada del segment ampliat.",
        repte="Canvia l'àrea del quadrat de 2 a 3. Abans d'executar, calcula les dues primeres decisions. Després canvia el nombre de passos i explica què representa l'última amplada.",
        codi=r'''
        area = Fraction(3)        # Prova també 2 o 5/2, escrit Fraction(5, 2).
        passos = 6
        a, b = Fraction(1), Fraction(2)  # Volem 1 < area < 4.
        if not a*a < area < b*b:
            raise ValueError("Tria una àrea entre 1 i 4 per a aquest interval inicial.")
        for k in range(1, passos+1):
            m = (a+b)/2
            if m*m == area:
                a = b = m
                print(f"Pas {k}: arrel racional exacta {m}.")
                break
            if m*m < area:
                a = m
            else:
                b = m
            print(f"Pas {k}: [{a}, {b}], amplada = {b-a}")
        print("La comparació dels quadrats usa fraccions exactes.")
        ''',
        preguntes=[
            pregunta("Després de 4 biseccions d'un interval d'amplada 1, quina amplada queda?",
                     ["1/4", "1/16", "0"], 1,
                     ["Cada pas divideix per 2: són quatre divisions, no una divisió per 4.",
                      "Correcte: (1/2)⁴ = 1/16. La longitud encara és positiva.",
                      "Cap nombre finit de biseccions dona amplada zero en aquest procés exacte."]),
            pregunta("Si m² és menor que 2 i l'interval és positiu, quina meitat conservem?",
                     ["[a,m]", "Qualsevol de les dues", "[m,b]"], 2,
                     ["Si m² < 2, el costat buscat és més gran que m.",
                      "La decisió depèn de la comparació; una meitat perdria el valor buscat.",
                      "Correcte: en nombres positius, elevar al quadrat conserva l'ordre."]),
            pregunta("Tots els punts mitjans són racionals. Què podem concloure sobre el límit?",
                     ["Això no determina si el límit és racional", "És racional necessàriament", "És l'últim punt mig"], 0,
                     ["Correcte: els racionals poden aproximar un nombre irracional com √2.",
                      "Confons els termes amb el límit: l'exemple de √2 mostra la diferència.",
                      "En una successió infinita no hi ha un últim terme."]),
        ],
    ),
    "Càlcul_Nombre_pi.ipynb": dict(
        parella=(6, 300), etiquetes='[f"{n} costats" for n in fotogrames_laboratori]',
        comparacio="Compara 6 i 300 costats: anota angle central, base i perímetre. Després compara 100 i 200. La segona aproximació redueix l'error aproximadament a la meitat o a la quarta part?",
        repte="Mantén el radi fix i compara 30, 60, 120 i 240 costats. Prediu el factor de reducció de l'error quan dupliquem n; després contrasta'l amb els resultats. L'error es calcula amb π només per comprovar l'aproximació.",
        codi=r'''
        valors_n = [30, 60, 120, 240]
        radi_taller = 1
        errors_taller = []
        for n in valors_n:
            resultat = dades_poligon(n, radi=radi_taller)
            error = math.pi-resultat["pi_aprox"]
            errors_taller.append(error)
            print(f"n={n:3}; πₙ≈{resultat['pi_aprox']:.9f}; error≈{error:.9f}")
        for k in range(1, len(valors_n)):
            print(f"De {valors_n[k-1]} a {valors_n[k]}: error dividit per {errors_taller[k-1]/errors_taller[k]:.4f}")
        fig, ax = plt.subplots(figsize=(8, 3.5))
        ax.loglog(valors_n, errors_taller, "o-", label="Error observat")
        ax.loglog(valors_n, [errors_taller[0]*(valors_n[0]/n)**2 for n in valors_n],
                  "--", label="Comparació: constant / n²")
        ax.set(xlabel="Costats n (escala logarítmica)", ylabel="Error (escala logarítmica)",
               title="Quanta precisió guanyem en duplicar els costats?")
        ax.legend(); plt.tight_layout(); plt.show()
        ''',
        preguntes=[
            pregunta("Amb 12 costats, quin angle usem per calcular mitja base amb el sinus?",
                     ["30°", "15°", "150°"], 1,
                     ["30° és l'angle central complet. L'altura el divideix en dos.",
                      "Correcte: 360°/12 = 30° i la meitat és 15°.",
                      "150° és l'angle interior del dodecàgon, no el mig angle del triangle central."]),
            pregunta("Si el radi es duplica, què passa amb pₙ/(2r)?",
                     ["Es conserva", "Es duplica", "Es divideix per 2"], 0,
                     ["Correcte: tant el perímetre com el diàmetre es dupliquen.",
                      "El numerador es duplica, però el denominador també.",
                      "El denominador es duplica, però el perímetre no es manté fix."]),
            pregunta("Amb 300 costats, el polígon sembla un cercle. Què significa?",
                     ["Ja hem obtingut π exactament", "L'error és exactament zero", "La resolució del dibuix amaga una diferència petita"], 2,
                     ["Un polígon finit encara té segments: la semblança visual no és una igualtat.",
                      "La taula mostra un error positiu d'aproximadament 0,00005742.",
                      "Correcte: cal llegir l'error o ampliar el gràfic, a més de mirar la forma."]),
        ],
    ),
    "NumeroPi.ipynb": dict(
        parella=(0, 4), etiquetes='[f"{6*2**k} costats" for k in fotogrames_laboratori]',
        comparacio="Compara els intervals de 6 i 96 costats. A la gràfica ampliada poden ocupar un espai semblant: justifica amb nombres per què la precisió és diferent i distingeix amplada i marge del punt mig.",
        repte="Escull una tolerància abans d'executar. Atura el càlcul quan la meitat de l'amplada sigui menor que aquesta tolerància. Després exigeix deu vegades més precisió i compara quants costats necessites.",
        codi=r'''
        tolerancia_taller = Decimal("0.0001")
        if tolerancia_taller <= 0:
            raise ValueError("La tolerància ha de ser positiva.")
        for n, inferior, superior in arquimedes(12):
            marge = (superior-inferior)/2
            if marge < tolerancia_taller:
                print(f"Primer resultat: {n} costats")
                print(f"Punt mig ≈ {(inferior+superior)/2:.12f}")
                print(f"Meitat de l'amplada ≈ {marge:.6E}")
                break
        else:
            print("Calen més passos per assolir aquesta tolerància.")
        print("Aquests decimals tenen arrodoniment; la certificació exacta és a l'ampliació.")
        ''',
        preguntes=[
            pregunta("Si 3,14 < π < 3,15, quin és el marge més ajustat que aquestes cotes garanteixen per al punt mig?",
                     ["Error menor que 0,01", "Error menor que 0,005", "Error zero"], 1,
                     ["És cert però menys precís: el punt mig permet dividir l'amplada per 2.",
                      "Correcte: (3,15−3,14)/2 = 0,005.",
                      "El punt mig és una aproximació; les cotes no afirmen que sigui el nombre buscat."]),
            pregunta("Què necessitem per obtenir error del punt mig menor que ε?",
                     ["U−L < 2ε", "U−L = ε²", "Conèixer tots els decimals de π"], 0,
                     ["Correcte: dividint aquesta desigualtat per 2 obtenim el marge requerit.",
                      "No cal aquesta igualtat: l'error depèn de la meitat de l'amplada.",
                      "Les dues cotes controlen l'error sense conèixer el valor exacte."]),
            pregunta("Una amplada decimal impresa com a zero demostra que π és racional?",
                     ["Sí, perquè el càlcul s'ha acabat", "Sí, si usem prou costats", "No: pot ser arrodoniment numèric"], 2,
                     ["L'aritmètica de l'ordinador té precisió finita; acabar el càlcul no és una prova.",
                      "Cap quantitat finita de costats converteix el polígon en la circumferència.",
                      "Correcte: cal distingir amplada matemàtica i representació decimal finita."]),
        ],
    ),
    "04_Talladures_Dedekind.ipynb": dict(
        parella=(2, 3), etiquetes='[f"q = {candidats_tall[k]}" for k in fotogrames_laboratori]',
        comparacio="Compara 7/5 amb 10/7. Escriu els quadrats com a fraccions exactes i explica per què queden en grups diferents. El decimal del títol serveix per situar-los, però no per decidir la classificació.",
        repte="Construeix ara una regla per a la frontera √3. Conserva el tractament separat dels negatius. Afegeix dues fraccions noves, una a cada costat, i justifica la decisió amb el quadrat.",
        codi=r'''
        nombre_sota_arrel = Fraction(3)
        candidats = [Fraction(-2), Fraction(5, 3), Fraction(7, 4), Fraction(2)]
        for q in candidats:
            if q < 0 or q*q < nombre_sota_arrel:
                grup = "A: inferior"
            elif q*q == nombre_sota_arrel:
                grup = "B: igual a la frontera (quan és racional)"
            else:
                grup = "B: superior"
            print(f"q={q}; q²={q*q}; {grup}")
        ''',
        preguntes=[
            pregunta("On queda −2 respecte de √2?",
                     ["A la dreta, perquè el seu quadrat és 4", "A l'esquerra, perquè és negatiu", "No es pot saber"], 1,
                     ["Elevar al quadrat no conserva l'ordre si comparem negatius amb positius.",
                      "Correcte: √2 és positiu i qualsevol nombre negatiu és inferior.",
                      "No calen decimals: el signe ja permet decidir."]),
            pregunta("En la talladura A={q racional: q<3/2}, el nombre 3/2...",
                     ["És el mínim de B", "És el màxim d'A", "No pertany a cap grup"], 0,
                     ["Correcte: A exclou la frontera i B la inclou.",
                      "La desigualtat que defineix A és estricta: 3/2 no pertany a A.",
                      "Els dos grups han de classificar tots els racionals."]),
            pregunta("Mostrar deu fraccions a cada costat descriu tota la talladura?",
                     ["Sí, si són molt properes", "Sí, perquè el gràfic és continu", "No: la defineix una regla per a tots els racionals"], 2,
                     ["La proximitat no converteix una llista finita en el conjunt complet.",
                      "La línia del dibuix no és una enumeració de tots els racionals.",
                      "Correcte: el dibuix il·lustra la regla, però només en mostra una part finita."]),
        ],
    ),
    "05_Successions_Cauchy.ipynb": dict(
        parella=(4, 128), etiquetes='[f"n = {n}" for n in fotogrames_laboratori]',
        comparacio="Compara n=4 amb n=128. Anota el salt consecutiu i la distància fins a 2n en les dues successions. Identifica quina d'aquestes distàncies continua sent més gran que 1/2.",
        repte="Escull N i compara tres successions. Per a 1/n i Hₙ examinem N i 2N; per a (−1)ⁿ examinem N i N+1 perquè els signes siguin diferents. Explica per què triar només una parella favorable no certifica Cauchy.",
        codi=r'''
        N_taller = 100
        epsilon_taller = 0.1
        for tipus in ["inversa", "harmonica", "alternant"]:
            segon = N_taller+1 if tipus == "alternant" else 2*N_taller
            valors = valors_successio(tipus, segon)
            distancia = abs(valors[segon-1]-valors[N_taller-1])
            print(f"{tipus}: índexs {N_taller} i {segon}; distància={distancia:.6f}; "
                  f"menor que ε: {distancia < epsilon_taller}")
        print("Una parella que falla pot refutar una proposta de N; una que passa no controla tota la cua.")
        ''',
        preguntes=[
            pregunta("Els salts Hₙ₊₁−Hₙ tendeixen a 0. Això demostra que Hₙ és de Cauchy?",
                     ["Sí", "Només si n supera 100", "No: cal controlar totes les parelles prou avançades"], 2,
                     ["Els salts acumulats fins a 2n no es fan petits: són almenys 1/2.",
                      "Cap llindar finit repara el problema dels salts entre n i 2n.",
                      "Correcte: Cauchy és una condició sobre totes les parelles de la cua."]),
            pregunta("La successió (−1)ⁿ és acotada. És de Cauchy?",
                     ["No, perquè termes de paritat diferent disten 2", "Sí, perquè tots els termes estan entre −1 i 1", "Sí, perquè alguns termes coincideixen"], 0,
                     ["Correcte: podem trobar aquestes parelles per molt lluny que avancem.",
                      "L'acotació no implica que tots els termes de la cua s'apropin entre si.",
                      "Cauchy no exigeix només algunes parelles properes, sinó totes."]),
            pregunta("Per a 1/n, quin N és suficient perquè qualsevol parella amb índexs ≥N disti menys de 0,01?",
                     ["N=10", "N=100", "No existeix"], 1,
                     ["Amb N=10 la cota 1/N és 0,1 i no assegura la tolerància demanada.",
                      "Correcte: per a índexs finits m,n≥100, la distància és estrictament menor que 1/100.",
                      "La successió 1/n sí que és de Cauchy: la cota 1/N es pot fer tan petita com calgui."]),
        ],
    ),
    "06_Completesa_R.ipynb": dict(
        parella=(20, 21), etiquetes='[f"{n} termes" for n in fotogrames_laboratori]',
        comparacio="Compara els termes 20 i 21: al primer arribem a 0,95 i al segon el superem. Escriu per què això refuta 0,95 com a cota superior de S, encara que semblés vàlida en una mostra més petita.",
        repte="Escull un candidat racional M entre 0 i 1. Troba directament el primer índex amb 1−1/n>M, sense recórrer tots els termes. Dedueix abans la desigualtat n>1/(1−M).",
        codi=r'''
        candidat_M = Fraction("0.999")  # Evita escriure primer un decimal float.
        if not 0 < candidat_M < 1:
            raise ValueError("Aquest taller demana un candidat M entre 0 i 1.")
        llindar = 1/(1-candidat_M)
        primer_n = llindar.numerator//llindar.denominator+1
        terme = 1-Fraction(1, primer_n)
        anterior = 1-Fraction(1, primer_n-1)
        print(f"Cal n > {llindar}; primer enter: {primer_n}")
        print(f"Terme anterior ≤ M: {anterior <= candidat_M}")
        print(f"Terme trobat > M: {terme > candidat_M}; valor exacte = {terme}")
        ''',
        preguntes=[
            pregunta("El conjunt S={1−1/n: n≥1} té màxim?",
                     ["Sí: 1", "No: qualsevol terme és superat pel següent", "Sí: el terme n=100"], 1,
                     ["1 és el suprem, però no pertany a S.",
                      "Correcte: hi ha termes cada vegada més grans, tots estrictament menors que 1.",
                      "El terme 101 supera el 100: un màxim de la mostra no és màxim del conjunt infinit."]),
            pregunta("Quin és el suprem de l'interval obert (0,1)?",
                     ["1", "No existeix perquè l'interval és obert", "L'últim decimal abans d'1"], 0,
                     ["Correcte: 1 és la cota superior més petita, encara que no pertanyi al conjunt.",
                      "L'obertura impedeix un màxim, però no impedeix el suprem.",
                      "No hi ha un últim nombre real abans d'1: sempre en podem trobar un altre més proper."]),
            pregunta("Si cap dels primers 20 termes supera 0,95, què sabem sobre el conjunt infinit?",
                     ["Que 0,95 n'és cota superior", "Que 0,95 n'és suprem", "Encara no podem generalitzar a tots els termes"], 2,
                     ["El terme 21 ja supera 0,95: has generalitzat una observació finita.",
                      "Ni tan sols és una cota superior de tot S.",
                      "Correcte: cal una justificació per a tots els índexs, no una mostra."]),
        ],
    ),
}

TALLERS.update({
    "07_Limits_Continuitat.ipynb": dict(
        parella=(0, 10), etiquetes='[f"h = {.8*.72**k:.5f}" for k in fotogrames_laboratori]',
        comparacio="Compara una aproximació inicial i una d'avançada. En el forat, les dues altures s'acosten a 2 encara que f(1)=3. En el salt, les altures continuen separades: anota les tres dades, límit esquerre, límit dret i valor al punt.",
        repte="Canvia només el valor assignat f(1). Comprova amb una taula si les aproximacions per l'esquerra i la dreta canvien. Després explica per què f(1)=2 repara la continuïtat i altres valors no.",
        codi=r'''
        valor_en_el_punt = 3  # Torna a executar amb 2 i després amb -1.
        def funcio_amb_forat(x):
            return valor_en_el_punt if x == 1 else x+1
        print("f(1) =", funcio_amb_forat(1))
        for exponent in range(1, 6):
            h = 10.0**(-exponent)
            print(f"h={h:.5f}; f(1−h)={funcio_amb_forat(1-h):.5f}; "
                  f"f(1+h)={funcio_amb_forat(1+h):.5f}")
        print("La fórmula x+1 per a x≠1 justifica el límit 2.")
        print("Contínua a 1:", valor_en_el_punt == 2)
        ''',
        preguntes=[
            pregunta("Si f(x)=x+1 per a x≠1 i f(1)=3, quin és el límit quan x→1?",
                     ["3", "No existeix", "2"], 2,
                     ["3 és el valor al punt, no el valor al qual s'apropen les imatges properes.",
                      "Les dues aproximacions laterals tendeixen a 2; el forat no impedeix el límit.",
                      "Correcte: per a x≠1, f(x)−2=x−1, que tendeix a 0."]),
            pregunta("Canviar només g(0) pot reparar un salt amb límits laterals −1 i 1?",
                     ["No", "Sí, posant g(0)=0", "Sí, posant g(0)=1"], 0,
                     ["Correcte: canviar un punt no canvia els límits laterals diferents.",
                      "Posar el punt al mig del salt no fa que els dos costats arribin a la mateixa altura.",
                      "Coincidir amb el costat dret no resol el desacord amb l'esquerre."]),
            pregunta("Per fer contínua la funció del forat a 1, quin valor hem d'assignar a f(1)?",
                     ["Qualsevol", "2", "3"], 1,
                     ["La continuïtat exigeix igualtat entre el valor al punt i el límit.",
                      "Correcte: el límit és 2, així que f(1) també ha de ser 2.",
                      "Amb f(1)=3, el punt ple continua separat de l'altura límit."]),
        ],
    ),
    "Derivades_BAT.ipynb": dict(
        parella=(0, 10), etiquetes='[f"h = {.9*.76**k:.5f}" for k in fotogrames_laboratori]',
        comparacio="Compara dos triangles de la secant. Calcula Δs/Δt en tots dos: el triangle s'encongeix, però la proporció s'acosta a 2. Contrasta-ho amb les dues pendents de |x| a la dreta.",
        repte="Canvia el punt a de 1 a 2 i després a −1. Prediu la pendent de x² i comprova-la amb quocients pels dos costats. Després prova abs(x) a a=0 i explica què impedeix obtenir una única derivada.",
        codi=r'''
        a_taller = 2.0
        def funcio_taller(x):
            return x*x  # Prova després abs(x), amb a_taller = 0.
        pendents_esquerres, pendents_dretes = [], []
        increments = [1, .5, .1, .05, .01, .005]
        for h in increments:
            dreta = (funcio_taller(a_taller+h)-funcio_taller(a_taller))/h
            esquerra = (funcio_taller(a_taller-h)-funcio_taller(a_taller))/(-h)
            pendents_dretes.append(dreta); pendents_esquerres.append(esquerra)
            print(f"h={h:.3f}; pendent esquerra={esquerra:.6f}; dreta={dreta:.6f}")
        fig, ax = plt.subplots(figsize=(8, 3.5))
        ax.semilogx(increments, pendents_esquerres, "o-", label="Esquerra")
        ax.semilogx(increments, pendents_dretes, "o-", label="Dreta")
        ax.invert_xaxis()
        ax.set(xlabel="h positiu, cada vegada més petit → (escala logarítmica)",
               ylabel="Pendent del quocient incremental", title=f"Les dues pendents s'apropen al mateix valor? a={a_taller}")
        ax.legend(); plt.tight_layout(); plt.show()
        ''',
        preguntes=[
            pregunta("Per a s(t)=t², la velocitat mitjana de t=1 a t=1+h és...",
                     ["2+h, si h≠0", "h", "0, perquè h es fa petit"], 0,
                     ["Correcte: ((1+h)²−1)/h=(2h+h²)/h=2+h.",
                      "En desenvolupar el quadrat també apareix el terme 2h.",
                      "Que numerador i denominador es facin petits no implica que el seu quocient tendeixi a 0."]),
            pregunta("Què fem amb h per trobar la derivada?",
                     ["El substituïm directament per 0 al quocient", "Estudiem el límit amb h≠0", "El deixem fix a 1"], 1,
                     ["El quocient quedaria 0/0; cal estudiar el límit sense dividir per zero.",
                      "Correcte: h s'apropa a 0, però no el substituïm al denominador.",
                      "Amb un interval fix calculem una taxa mitjana, no el límit instantani."]),
            pregunta("La funció |x| a 0 és...",
                     ["Discontínua", "Derivable amb derivada 0", "Contínua però no derivable"], 2,
                     ["Les imatges s'apropen a 0 des dels dos costats: sí que és contínua.",
                      "Fer la mitjana de les pendents −1 i 1 no defineix una derivada.",
                      "Correcte: el valor i el límit coincideixen, però les pendents laterals són diferents."]),
        ],
    ),
    "LaRecta.ipynb": dict(
        parella=(4, 12), etiquetes='[f"Pendent m = {-2+k/4:g}" for k in fotogrames_laboratori]',
        comparacio="Compara m=−1 i m=1 amb la mateixa ordenada b=1. Què es conserva? Què canvia de signe? Després tria m=0 i explica per què és un cas diferent d'una recta vertical.",
        repte="Dues tarifes: A cobra 3 € inicials i 1,50 €/km; B no té cost inicial i cobra 2 €/km. Prediu quan convé cadascuna i troba el punt de tall amb una equació, abans de mirar-lo al gràfic.",
        codi=r'''
        inici_A, preu_A = 3.0, 1.5
        inici_B, preu_B = 0.0, 2.0
        distancia = np.linspace(0, 12, 121)
        fig, ax = plt.subplots(figsize=(8, 3.8))
        ax.plot(distancia, inici_A+preu_A*distancia, label="Tarifa A")
        ax.plot(distancia, inici_B+preu_B*distancia, label="Tarifa B")
        if preu_A != preu_B:
            tall = (inici_B-inici_A)/(preu_A-preu_B)
            print(f"Solució de l'equació: d={tall:g} km; preu={inici_A+preu_A*tall:g} €")
            if 0 <= tall <= 12:
                ax.scatter(tall, inici_A+preu_A*tall, color="#ea580c", s=70, zorder=5)
        elif inici_A == inici_B:
            print("Les dues tarifes coincideixen.")
        else:
            print("Les rectes són paral·leles: no tenen punt de tall.")
        ax.set(xlabel="Distància (km)", ylabel="Preu (€)", title="Cost inicial i cost per quilòmetre")
        ax.legend(); plt.tight_layout(); plt.show()
        ''',
        preguntes=[
            pregunta("Si Δx=3 i Δy=−6, quina és la pendent?",
                     ["−2", "−1/2", "2"], 0,
                     ["Correcte: m=Δy/Δx=−6/3=−2.",
                      "Has invertit el quocient: la pendent és canvi vertical dividit per l'horitzontal.",
                      "El signe negatiu indica que y disminueix quan x augmenta."]),
            pregunta("A P=1,5d+3, què significa el 3?",
                     ["Tres quilòmetres", "Un cost inicial de 3 euros", "La pendent"], 1,
                     ["d és la distància; el terme constant té les unitats de P, euros.",
                      "Correcte: és el preu quan d=0.",
                      "La pendent és 1,5 €/km; 3 és l'ordenada a l'origen."]),
            pregunta("Dues rectes amb pendent igual i ordenades diferents...",
                     ["Sempre es tallen a l'origen", "Coincideixen", "Són paral·leles i no es tallen"], 2,
                     ["Tenen punts de tall amb l'eix y diferents i mantenen la mateixa direcció.",
                      "Per coincidir necessitarien també la mateixa ordenada.",
                      "Correcte: la diferència vertical entre elles és constant i no nul·la."]),
        ],
    ),
    "ComplexNumbers.ipynb": dict(
        parella=(0, 6), etiquetes='[f"Gir de {15*k}°" for k in fotogrames_laboratori]',
        comparacio="Compara z amb iz: contrasta les coordenades i el mòdul. Després compara 90° i 270°. Justifica els signes de les dues components, sense confondre una component negativa amb una distància negativa.",
        repte="Per al mateix z, compara sumar i, multiplicar per i i multiplicar per 2i. Calcula primer els tres resultats amb àlgebra. Després classifica cada transformació com a traslació, gir o gir amb dilatació.",
        codi=r'''
        z_taller = 2+1j  # Prova també 3-2j.
        transformacions = {"z": z_taller, "z+i": z_taller+1j,
                           "i·z": 1j*z_taller, "2i·z": 2j*z_taller}
        fig, ax = plt.subplots(figsize=(6, 5))
        colors = ["#2563eb", "#047857", "#ea580c", "#7c3aed"]
        for (nom, z), color in zip(transformacions.items(), colors):
            print(f"{nom}: {z}; mòdul≈{abs(z):.6f}")
            ax.annotate("", (z.real, z.imag), (0, 0), arrowprops=dict(arrowstyle="->", color=color, lw=2))
            ax.scatter(z.real, z.imag, color=color, label=nom)
        abast = max(abs(z) for z in transformacions.values())+1
        ax.axhline(0, color="0.6"); ax.axvline(0, color="0.6")
        ax.set(aspect="equal", xlim=(-abast, abast), ylim=(-abast, abast),
               xlabel="Part real", ylabel="Part imaginària", title="Sumar i no és multiplicar per i")
        ax.legend(); plt.tight_layout(); plt.show()
        ''',
        preguntes=[
            pregunta("Quin és el resultat d'i(2+i)?",
                     ["2+2i", "1+2i", "−1+2i"], 2,
                     ["Aquest és el resultat de sumar i, no de multiplicar.",
                      "Recorda que i²=−1, no 1.",
                      "Correcte: 2i+i²=−1+2i."]),
            pregunta("Multiplicar per 2i produeix...",
                     ["Un gir de 90° i una duplicació del mòdul", "Una traslació de dues unitats", "Un gir de 180° sense canviar el mòdul"], 0,
                     ["Correcte: el factor 2 dilata i el factor i gira un quart de volta.",
                      "Una traslació correspon a sumar, no a multiplicar.",
                      "El gir de 180° correspondria a multiplicar per −1."]),
            pregunta("Per què el zero no té argument definit?",
                     ["Perquè no té mòdul", "Perquè no determina cap direcció des de l'origen", "Perquè és un nombre negatiu"], 1,
                     ["El seu mòdul sí que està definit i val 0.",
                      "Correcte: qualsevol angle amb radi zero arriba al mateix punt.",
                      "El zero no és negatiu; el problema és l'absència de direcció."]),
        ],
    ),
    "AnálisisUnivariante(I).ipynb": dict(
        parella=(0, 15), etiquetes='[f"Dada modificada: {15+3*k} minuts" for k in fotogrames_laboratori]',
        comparacio="Compara 15 i 60 minuts per a l'única dada que canvia. Els eixos i les classes es mantenen: anota la variació de mitjana i mediana i explica quantes persones han modificat el temps.",
        repte="Representa totes les observacions com a punts, ordenades de menor a major. Canvia el valor extrem i identifica la posició central: és l'11a, perquè hi ha 21 dades. Compara aquesta lectura amb l'histograma.",
        codi=r'''
        valor_extrem_taller = 60
        dades_taller, mitjana_taller, mediana_taller = resum_temps(valor_extrem_taller)
        ordenades = np.sort(dades_taller)
        posicions = np.arange(1, len(ordenades)+1)
        fig, ax = plt.subplots(figsize=(8, 3.8))
        ax.scatter(posicions, ordenades, color="#2563eb", label="Dades ordenades")
        ax.scatter([11], [ordenades[10]], color="#047857", s=90, zorder=5, label="Posició central: 11a")
        ax.axhline(mitjana_taller, color="#ea580c", label=f"Mitjana: {mitjana_taller:.2f}")
        ax.axhline(mediana_taller, color="#047857", ls="--", label=f"Mediana: {mediana_taller:g}")
        ax.set(xlabel="Posició després d'ordenar", ylabel="Temps (minuts)",
               title="La mediana depèn de la posició central; la mitjana depèn de tota la suma")
        ax.legend(); plt.tight_layout(); plt.show()
        ''',
        preguntes=[
            pregunta("Si una sola dada augmenta 21 minuts en una mostra de 21 dades, quant augmenta la mitjana?",
                     ["21 minuts", "1 minut", "No canvia"], 1,
                     ["Cal repartir l'increment de la suma entre les 21 observacions.",
                      "Correcte: l'increment de la mitjana és 21/21=1 minut.",
                      "La mitjana depèn de la suma i per tant canvia quan una dada canvia."]),
            pregunta("Quina posició determina la mediana amb 21 dades ordenades?",
                     ["La 11a", "La 10a", "L'última"], 0,
                     ["Correcte: queden 10 observacions a cada costat.",
                      "La 10a deixaria 9 observacions abans i 11 després.",
                      "L'última és el màxim, no la mediana."]),
            pregunta("Un punt atípic al diagrama de caixa s'ha d'eliminar sempre?",
                     ["Sí, perquè és un error", "Sí, si augmenta la mitjana", "No: cal investigar-ne el context i la qualitat"], 2,
                     ["Un valor poc habitual pot ser real; atípic no vol dir erroni.",
                      "L'efecte sobre la mitjana no justifica esborrar una observació.",
                      "Correcte: revisem unitats, registre i context abans de decidir."]),
        ],
    ),
    "PràcticaBasedeDades.ipynb": dict(
        parella=(2, 11), etiquetes='[f"{k+1} registres visitats" for k in fotogrames_laboratori]',
        comparacio="Compara el tercer i el dotzè registre transformat. Localitza l'ID, l'any i la categoria d'una fila i reconstrueix-ne la cel·la d'origen. Explica per què més files no significa més identificadors.",
        repte="Escull una sola categoria i compara 2025 amb 2026 per a cadascun dels tres identificadors. Abans de calcular mitjanes, indica la unitat de la variable. Prova després l'altra categoria.",
        codi=r'''
        categoria_taller = "Salary"  # Prova també "employees".
        unitats_taller = {"Salary": "euros", "employees": "treballadors"}
        if categoria_taller not in unitats_taller:
            raise ValueError("Tria Salary o employees.")
        seleccio_taller = mini_llarg[mini_llarg["category"] == categoria_taller]
        comparacio_anys = seleccio_taller.pivot(index="rank", columns="year", values="value")
        display(comparacio_anys)
        print("Variació 2026−2025 per ID:")
        display(comparacio_anys[2026]-comparacio_anys[2025])
        ax = comparacio_anys.plot.bar(figsize=(8, 3.8), rot=0)
        ax.set(xlabel="Identificador", ylabel=unitats_taller[categoria_taller],
               title=f"Dades sintètiques: mateixa categoria, dos anys ({categoria_taller})")
        plt.tight_layout(); plt.show()
        ''',
        preguntes=[
            pregunta("Amb 3 ID, 2 anys i 2 categories completes, quantes files hi ha en format llarg?",
                     ["12", "7", "3"], 0,
                     ["Correcte: 3×2×2=12 combinacions d'ID, any i categoria.",
                      "Cal multiplicar les combinacions, no sumar les dimensions.",
                      "Hi ha tres identificadors, però cada un apareix en quatre registres."]),
            pregunta("La taula ampla i la llarga tenen un nombre diferent de files. Això significa que...",
                     ["Hem creat persones noves", "Hem canviat la representació de la mateixa informació", "Hem perdut necessàriament dades"], 1,
                     ["Cada fila llarga és una combinació d'ID, any i categoria, no una persona nova.",
                      "Correcte: cal comprovar la correspondència de cada cel·la i els seus identificadors.",
                      "El canvi de dimensions no implica pèrdua: cal comprovar les correspondències."]),
            pregunta("Podem calcular una única mitjana barrejant Salary i employees?",
                     ["Sí, perquè tots són nombres", "Sí, si són del mateix any", "No: barregem euros i nombre de treballadors"], 2,
                     ["Els nombres representen magnituds diferents: la unitat també importa.",
                      "Compartir any no fa compatibles les unitats.",
                      "Correcte: filtrem la categoria abans d'interpretar un resum numèric."]),
        ],
    ),
})


EINES = r'''
def compara_estats(inicial, final):
    """Dos fotogrames simultanis; els eixos conserven el significat del laboratori."""
    if inicial not in fotogrames_laboratori or final not in fotogrames_laboratori:
        raise ValueError("Tria dos estats de fotogrames_laboratori.")
    fig, axes = plt.subplots(2, 2, figsize=(11.6, 8.8), dpi=90)
    for fila, estat, lletra in [(0, inicial, "A"), (1, final, "B")]:
        dibuixa_laboratori(estat, axes[fila])
        for ax in axes[fila]:
            ax.set_title(lletra + " · " + ax.get_title(), fontsize=10)
    fig.suptitle("Comparació simultània: observa què canvia i què es conserva", fontsize=14, weight="bold")
    fig.tight_layout(rect=(0, 0, 1, .95), h_pad=3)
    plt.show()

def controls_comparacio():
    try:
        import ipywidgets as widgets
    except ImportError:
        print("Canvia els dos arguments de compara_estats(...) per fer una altra comparació.")
        return None
    opcions = list(zip(etiquetes_comparacio, fotogrames_laboratori))
    panell = widgets.interactive(compara_estats, {"manual": True, "manual_name": "Compara els estats"},
        inicial=widgets.Dropdown(options=opcions, value=parella_comparacio[0], description="Estat A:"),
        final=widgets.Dropdown(options=opcions, value=parella_comparacio[1], description="Estat B:"))
    display(panell)
    return panell

def feedback_resposta(numero, lletra):
    """Retorn per opció. Ex.: feedback_resposta(1, 'B'); no desa ni envia respostes."""
    if isinstance(numero, bool) or not isinstance(numero, int) or not 1 <= numero <= len(preguntes_taller):
        raise ValueError("El número de pregunta no és vàlid.")
    q = preguntes_taller[numero-1]
    lletra = str(lletra).strip().upper()
    lletres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:len(q["opcions"])]
    if lletra not in lletres or len(lletra) != 1:
        raise ValueError("Tria una de les lletres de les opcions.")
    index = lletres.index(lletra)
    return {"correcte": index == q["correcta"], "explicacio": q["retorn"][index]}

def mostra_feedback(numero, lletra):
    resultat = feedback_resposta(numero, lletra)
    estat = "Resposta encertada" if resultat["correcte"] else "Revisa el raonament"
    display(Markdown(f"**Pregunta {numero} · {estat}.** {resultat['explicacio']}"))
    return resultat

def crea_autoavaluacio():
    try:
        import ipywidgets as widgets
        from html import escape
    except ImportError:
        print("Respon amb mostra_feedback(1, 'A'), canviant la pregunta i la lletra.")
        return None
    camps, selectors = [], []
    for numero, q in enumerate(preguntes_taller, 1):
        opcions = [("Tria una resposta", None)] + [
            (f"{chr(65+k)}. {text}", chr(65+k)) for k, text in enumerate(q["opcions"])]
        selector = widgets.Dropdown(options=opcions, value=None, layout=widgets.Layout(width="100%"))
        selectors.append(selector)
        camps.append(widgets.VBox([
            widgets.HTML(f"<b>{numero}. {escape(q['enunciat'])}</b>"), selector]))
    sortida = widgets.Output()
    boto = widgets.Button(description="Comprova i raona", button_style="info", layout=widgets.Layout(width="180px"))
    def comprova(_):
        with sortida:
            sortida.clear_output(wait=True)
            for numero, selector in enumerate(selectors, 1):
                if selector.value is None:
                    display(Markdown(f"**Pregunta {numero}:** encara has de triar una resposta."))
                else:
                    mostra_feedback(numero, selector.value)
    def canvi(_):
        sortida.clear_output()
    for selector in selectors:
        selector.observe(canvi, names="value")
    boto.on_click(comprova)
    panell = widgets.VBox(camps+[boto, sortida])
    display(panell)
    return {"panell": panell, "selectors": selectors, "boto": boto, "sortida": sortida}
'''


def celles_taller(filename, md, code):
    t = TALLERS[filename]
    questions_md = []
    for numero, q in enumerate(t["preguntes"], 1):
        questions_md.append(f"**{numero}. {q['enunciat']}**\n\n" + "\n".join(
            f"- {chr(65+k)}. {text}" for k, text in enumerate(q["opcions"])))
    return [
        md("### Compara abans de concloure\n\n" + t["comparacio"] +
           "\n\nTria dos estats amb els controls i prem **Compara els estats**. "
           "Llegeix les escales: algunes ampliacions del laboratori canvien els límits dels eixos. "
           "Justifica la comparació amb els nombres dels títols."),
        code("parella_comparacio = " + repr(t["parella"]) + "\n"
             "etiquetes_comparacio = " + t["etiquetes"] + "\n"
             "preguntes_taller = " + repr(t["preguntes"]) + "\n"),
        code(EINES),
        code("compara_estats(*parella_comparacio)\npanell_comparacio = controls_comparacio()"),
        md("### Taller de Python · canvia una dada i explica l'efecte\n\n" + t["repte"] +
           "\n\n**Fes-ho en tres passos:** escriu una predicció, modifica les dades indicades "
           "i contrasta el resultat. Acaba amb una explicació matemàtica; executar la cel·la és només una part de la tasca."),
        code(t["codi"]),
        md("### Atura't i comprova què has entès\n\nTria una resposta per pregunta i escriu "
           "una justificació abans de comprovar-la. Si t'equivoques, llegeix el retorn i torna al gràfic "
           "per localitzar el malentès.\n\n" + "\n\n".join(questions_md) +
           "\n\nSi no es mostren els controls, executa `mostra_feedback(1, 'B')`, "
           "canviant el número i la lletra. El retorn comprova l'opció; la justificació escrita s'ha de discutir a classe."),
        code("autoavaluacio = crea_autoavaluacio()"),
        md("### Evidència final de l'aprenentatge\n\n"
           "Completa aquestes frases amb un cas concret del taller:\n\n"
           "1. **He canviat…**\n2. **Esperava que… perquè…**\n3. **El resultat ha estat…**\n"
           "4. **Ara ho explico amb aquesta relació o propietat…**\n5. **Un cas en què no puc generalitzar directament és…**\n\n"
           "Torna a una pregunta que hagis corregit i explica què has canviat del teu raonament."),
    ]
