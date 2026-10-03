"""Contingut del quadern 02: triangles, perímetres i aproximacions fins a 300 costats."""


def crea_quadern(notebook, md, code, arquimedes):
    notebook(
        "Càlcul_Nombre_pi.ipynb", "02 · Aproximem π: del triangle als 300 costats",
        "Calcular pas a pas el costat d'un polígon regular i veure com el seu perímetre permet aproximar π, de 3 a 300 costats.",
        "perímetres, angles, Pitàgores i sinus d'un angle agut (el repassem aquí)",
        "1 sessió",
        "Reelaboració de Càlcul_Nombre_pi.ipynb amb construccions geomètriques i gràfics propis.",
        [
            md(r'''
            ## 1. La idea: substituir una corba per segments

            Dibuixem un **polígon regular inscrit** en una circumferència de radi $r$:
            tots els costats són iguals i tots els vèrtexs són sobre la circumferència.
            Si $b$ és la longitud d'un costat i $n$ el nombre de costats, el perímetre és
            $p_n=n\,b$. La longitud de la circumferència és $C=2\pi r$.

            Els segments queden per dins dels arcs: $p_n<C$. Quan augmentem $n$, el perímetre
            del polígon s'apropa a la longitud de la circumferència. Per tant,

            $$\boxed{\pi\approx\pi_n=\frac{p_n}{2r}=\frac{n\,b}{2r}}.$$

            **Treballarem amb $r=1$**, de manera que $\pi_n=p_n/2$. El símbol $\pi_n$
            designa la nostra aproximació amb $n$ costats, no el valor exacte de $\pi$.
            Acceptem aquí la comparació geomètrica entre arcs i perímetres.

            **Abans d'executar:** amb més costats, cada costat serà més llarg o més curt?
            I el perímetre total? Escriu una predicció: són dues preguntes diferents.
            '''),
            md(r'''
            ## 2. L'angle superior del triangle isòsceles

            **Pas 1.** Unim el centre $O$ amb dos vèrtexs consecutius $A$ i $B$.
            El triangle $OAB$ és isòsceles perquè $OA=OB=r$: tots dos segments són radis.
            La base $AB=b$ és precisament un costat del polígon.

            **Pas 2.** Al voltant d'$O$ hi ha $n$ triangles iguals que reparteixen una volta completa:

            $$n\alpha=360^\circ\qquad\Longrightarrow\qquad
            \boxed{\alpha=\frac{360^\circ}{n}}.$$

            Aquest és l'**angle superior** del triangle al dibuix, situat al centre del cercle.
            No és l'angle interior del polígon en un vèrtex.

            **Pas 3.** Tracem l'altura des d'$O$ fins al punt mig $M$ de la base.
            En un triangle isòsceles, aquesta altura també parteix l'angle superior per la meitat.
            Obtenim dos triangles rectangles iguals:

            $$\boxed{\beta=\frac{\alpha}{2}=\frac{180^\circ}{n}},\qquad
            AM=MB=\frac b2,\qquad OM\perp AB.$$
            '''),
            md(r'''
            ## 3. Com calculem la base, pas a pas?

            Mirem només el triangle rectangle $OMB$:

            1. La **hipotenusa** és $OB=r$ (el costat oposat a l'angle recte).
            2. El **catet oposat** a $\beta$ és $MB=b/2$.
            3. Per definició del sinus, $\sin\beta=\text{catet oposat}/\text{hipotenusa}$.
            4. Substituïm les longituds: $\sin\beta=(b/2)/r$.
            5. Multipliquem per $r$: $r\sin\beta=b/2$. Encara tenim **mitja base**.
            6. Multipliquem per $2$ per obtenir **tota la base**:

            $$\boxed{b=2r\sin\beta=2r\sin\left(\frac{180^\circ}{n}\right)}.$$

            **Si ho comproves amb calculadora, posa-la en mode DEG (graus).**
            No confonguis $\alpha$ amb $\beta$ ni $b$ amb $b/2$.

            La ruta completa del càlcul és:

            $$n\ \longrightarrow\ \alpha=\frac{360^\circ}{n}
            \ \longrightarrow\ \beta=\frac{\alpha}{2}
            \ \longrightarrow\ b=2r\sin\beta
            \ \longrightarrow\ p_n=n b
            \ \longrightarrow\ \pi_n=\frac{p_n}{2r}.$$
            '''),
            md(r'''
            ### Com ho calcularà l'ordinador sense conèixer π?

            Per trobar la base, el codi aproxima la posició del vèrtex dividint angles
            per la meitat i aplicant Pitàgores. Això permet treballar amb **qualsevol nombre
            enter de costats de 3 a 300**, sense introduir el valor de π en el càlcul.
            Pots seguir els dibuixos i els resultats sense estudiar aquest codi auxiliar.

            <details><summary>Ampliació opcional: bisecció geomètrica d'un angle</summary>

            En un cercle de radi 1, els punts $(1,0)$ i $(0,1)$ delimiten un angle de $90^\circ$.
            El punt mig de la corda està sobre la bisectriu. El dividim per la seva distància
            a l'origen, calculada amb Pitàgores, per tornar-lo a situar sobre el cercle.
            Així obtenim la direcció de $45^\circ$. Conservem la meitat que conté l'angle
            buscat i repetim. La coordenada vertical del punt obtingut aproxima el sinus.

            Fem 50 biseccions. Les operacions tenen arrodoniment: aquests resultats són
            aproximacions numèriques, no intervals certificats. `math.pi` s'utilitzarà
            **només després**, com a referència al gràfic i per comparar l'error.
            La trigonometria de NumPy només serveix per dibuixar les figures.

            </details>
            '''),
            code(r'''
            def sinus_geometric(graus):
                """Aproxima el sinus d'un angle entre 0 i 90 graus sense usar π."""
                if not math.isfinite(graus) or not 0 <= graus <= 90:
                    raise ValueError("Cal un angle entre 0 i 90 graus.")
                if graus == 0:
                    return 0.0
                if graus == 90:
                    return 1.0
                angle_a, angle_b = 0.0, 90.0
                ax, ay, bx, by = 1.0, 0.0, 0.0, 1.0
                for _ in range(50):
                    angle_m = (angle_a + angle_b) / 2
                    mx, my = (ax + bx) / 2, (ay + by) / 2
                    distancia = math.sqrt(mx * mx + my * my)  # Pitàgores
                    mx, my = mx / distancia, my / distancia
                    if angle_m == graus:
                        return my
                    if angle_m < graus:
                        angle_a, ax, ay = angle_m, mx, my
                    else:
                        angle_b, bx, by = angle_m, mx, my
                return (ay + by) / 2

            def dades_poligon(n, radi=1.0):
                """Angles, costat, perímetre i aproximació de π d'un polígon inscrit."""
                if isinstance(n, bool) or not isinstance(n, (int, np.integer)) or not 3 <= n <= 300:
                    raise ValueError("El nombre de costats ha de ser un enter de 3 a 300.")
                if not math.isfinite(radi) or radi <= 0:
                    raise ValueError("El radi ha de ser positiu i finit.")
                alpha = 360.0 / n
                beta = alpha / 2
                mitja_base = radi * sinus_geometric(beta)
                base = 2 * mitja_base
                perimetre = n * base
                pi_aprox = perimetre / (2 * radi)
                altura = math.sqrt(radi**2 - mitja_base**2)
                return dict(n=n, radi=radi, alpha=alpha, beta=beta, base=base,
                            altura=altura, perimetre=perimetre, pi_aprox=pi_aprox)
            '''),
            code(r'''
            from matplotlib.patches import Arc, Polygon

            def dibuixa_poligon(ax, n):
                # π i les funcions trigonomètriques només orienten aquest DIBUIX.
                theta = np.linspace(0, 2*np.pi, 600)
                angles = np.linspace(0, 2*np.pi, n+1) - np.pi/2 - np.pi/n
                x, y = np.cos(angles), np.sin(angles)
                ax.plot(np.cos(theta), np.sin(theta), color="0.55", lw=1.5)
                ax.plot(x, y, color="#2563eb", lw=2)
                if n <= 24:
                    for vx, vy in zip(x[:-1], y[:-1]):
                        ax.plot([0, vx], [0, vy], color="#c4b5fd", lw=.8, zorder=0)
                ax.fill([0, x[0], x[1]], [0, y[0], y[1]], color="#dbeafe")
                ax.plot([x[0], 0, x[1]], [y[0], 0, y[1]], color="#7c3aed", lw=1.5)
                ax.plot(x[:2], y[:2], color="#ea580c", lw=3)
                if n <= 24:
                    ax.text(x[0]-.07, y[0]-.09, "A", ha="right")
                    ax.text(x[1]+.07, y[1]-.09, "B", ha="left")
                ax.text(0, .08, "O", ha="center")
                ax.set(aspect="equal", xlim=(-1.2, 1.2), ylim=(-1.25, 1.2))
                ax.axis("off")

            def dibuixa_triangle(n=6):
                d = dades_poligon(n)
                s, h, beta = d["base"]/2, d["altura"], d["beta"]
                fig, axes = plt.subplots(1, 3, figsize=(13, 4.8))
                dibuixa_poligon(axes[0], n)
                axes[0].set_title(f"1. {n} triangles al voltant d'O")
                for ax in axes[1:]:
                    ax.plot([-s, 0, s], [-h, 0, -h], color="#7c3aed", lw=2.5)
                    ax.plot([-s, s], [-h, -h], color="#ea580c", lw=3)
                    ax.text(0, .06, "O", ha="center", weight="bold")
                    ax.text(-s-.06, -h-.03, "A", ha="right")
                    ax.text(s+.06, -h-.03, "B", ha="left")
                    ax.text(-s/2-.12, -h/2, "r = 1", ha="right", color="#7c3aed")
                    ax.text(s/2+.12, -h/2, "r = 1", ha="left", color="#7c3aed")
                    ax.set(aspect="equal", xlim=(-1.15, 1.15), ylim=(-1.25, .22))
                    ax.axis("off")
                ax = axes[1]
                ax.add_patch(Arc((0, 0), .55, .55, theta1=-90-beta,
                                 theta2=-90+beta, color="#7c3aed", lw=2))
                ax.text(0, -.38, rf"$\alpha={d['alpha']:g}^\circ$", ha="center")
                ax.text(0, -h-.17, "AB = b (base completa)", ha="center", color="#ea580c")
                ax.set_title("2. L'angle superior: 360° / n")
                ax = axes[2]
                ax.add_patch(Polygon([[0, 0], [0, -h], [s, -h]], color="#ffedd5", zorder=0))
                ax.plot([0, 0], [0, -h], "--", color="#047857", lw=2)
                q = min(.06, s/3, h/5)
                ax.plot([0, q, q], [-h+q, -h+q, -h], color="#047857")
                ax.add_patch(Arc((0, 0), .55, .55, theta1=-90,
                                 theta2=-90+beta, color="#047857", lw=2))
                ax.annotate(rf"$\beta={beta:g}^\circ$", xy=(.07, -.22),
                            xytext=(.53, -.13), arrowprops=dict(arrowstyle="->", color="#047857"),
                            color="#047857")
                ax.text(0, -h-.07, "M", ha="center", va="top", color="#047857")
                ax.text(-s/2, -h-.22, "b/2", ha="center", color="#ea580c")
                ax.text(s/2, -h-.22, "b/2", ha="center", color="#ea580c")
                ax.set_title("3. L'altura parteix angle i base")
                fig.suptitle("Del polígon al triangle rectangle", fontsize=16, weight="bold")
                fig.tight_layout()
                plt.show()

            dibuixa_triangle(6)
            '''),
            md(r'''
            ### Exemple complet: primer 6 costats, després 12

            | Pas | Hexàgon: $n=6$, $r=1$ | Dodecàgon: $n=12$, $r=1$ |
            |---|---|---|
            | Angle superior $\alpha=360^\circ/n$ | $60^\circ$ | $30^\circ$ |
            | Mig angle $\beta=\alpha/2$ | $30^\circ$ | $15^\circ$ |
            | Mitja base $b/2=r\sin\beta$ | $\sin30^\circ=0{,}5$ | $\sin15^\circ\approx0{,}258819$ |
            | Base completa $b$ | $1$ | $\approx0{,}517638$ |
            | Perímetre $p_n=n b$ | $6$ | $\approx6{,}211657$ |
            | Aproximació $\pi_n=p_n/2$ | $3$ | $\approx3{,}105829$ |

            **Conclusió:** en passar de 6 a 12 costats, la base disminueix, però el perímetre
            augmenta i l'aproximació s'acosta a π. Conservem tots els decimals durant el
            càlcul i arrodonim només en mostrar el resultat.

            **Una comprovació amb Pitàgores, sense sinus:** l'altura de l'hexàgon és
            $OM=\sqrt{1^2-(1/2)^2}=\sqrt3/2$. Sigui $D$ el punt de la circumferència
            entre $A$ i $B$, sobre la prolongació d'$OM$. Tenim $MD=1-\sqrt3/2$.
            En el triangle rectangle $AMD$,

            $$AD=\sqrt{AM^2+MD^2}
            =\sqrt{(1/2)^2+(1-\sqrt3/2)^2}
            =\sqrt{2-\sqrt3}\approx0{,}517638.$$

            $AD$ és el costat del polígon de 12 costats: coincideix amb el càlcul anterior.
            '''),
            md(r'''
            ## 4. Tots els nombres de costats, de 3 a 300

            Ara repetim **exactament els mateixos passos** per a cada enter $n=3,4,5,\ldots,300$.
            La corba blava mostra $\pi_n=p_n/2$; la línia discontínua és el valor conegut de π,
            utilitzat només com a referència. Els segments uneixen resultats per a nombres
            enters de costats.

            - **Esquerra:** observa que les aproximacions creixen i s'acosten a π des de sota.
            - **Centre:** ampliem la zona de 50 a 300 costats per veure que encara queda una separació.
            - **Dreta:** mostrem l'error $\pi-\pi_n$ en escala logarítmica; baixar una divisió
              principal significa dividir l'error per 10.
            '''),
            code(r'''
            costats = np.arange(3, 301)  # 301 no s'inclou: l'últim polígon té 300 costats.
            aproximacions = np.array([dades_poligon(int(n))["pi_aprox"] for n in costats])
            pi_referencia = math.pi  # Només comparació; no calcula cap costat ni perímetre.
            errors = pi_referencia - aproximacions

            fig, axes = plt.subplots(1, 3, figsize=(15, 4.8))
            for ax in axes[:2]:
                ax.plot(costats, aproximacions, color="#2563eb", lw=2, label=r"$\pi_n=p_n/2$")
                ax.axhline(pi_referencia, color="#b91c1c", ls="--", label="π de referència")
                ax.scatter([300], [aproximacions[-1]], color="#2563eb", zorder=5)
                ax.set(xlabel="Nombre de costats n", ylabel="Aproximació de π")
                ax.ticklabel_format(axis="y", style="plain", useOffset=False)
                ax.legend(loc="lower right", fontsize=9)
            axes[0].set(xlim=(3, 300), title="Cada vegada més a prop de π")
            axes[1].set(xlim=(50, 300), ylim=(3.1393, 3.1418), title="Ampliació: de 50 a 300 costats")
            axes[2].semilogy(costats, errors, color="#047857", lw=2)
            axes[2].scatter([300], [errors[-1]], color="#047857")
            axes[2].set(xlim=(3, 300), xlabel="Nombre de costats n",
                        ylabel=r"Error $\pi-\pi_n$", title="L'error disminueix")
            fig.suptitle(f"Amb 300 costats: π₃₀₀ ≈ {aproximacions[-1]:.9f}   |   Error ≈ {errors[-1]:.8f}",
                         fontsize=14, weight="bold")
            fig.tight_layout()
            plt.show()
            '''),
            code(r'''
            seleccio = [3, 4, 6, 12, 24, 48, 96, 192, 300]
            files = ["| Costats n | α (graus) | β (graus) | Base b | Perímetre pₙ | Aproximació πₙ | Error |",
                     "|---:|---:|---:|---:|---:|---:|---:|"]
            for n in seleccio:
                d = dades_poligon(n)
                files.append(f"| {n} | {d['alpha']:.3f} | {d['beta']:.3f} | {d['base']:.8f} | "
                             f"{d['perimetre']:.8f} | {d['pi_aprox']:.8f} | {math.pi-d['pi_aprox']:.8f} |")
            display(Markdown("\n".join(files)))
            '''),
            md(r'''
            **Llegeix l'última fila:** amb 300 costats, $\alpha=1{,}2^\circ$ i $\beta=0{,}6^\circ$.
            La base és aproximadament $0{,}02094357$ i el perímetre $6{,}28307047$.
            Així obtenim $\pi_{300}\approx3{,}141535235$, amb un error d'uns $0{,}00005742$.
            **No hem obtingut π exactament.** Arrodonint a tres decimals, tant $\pi_{300}$
            com π donen $3{,}142$; a quatre decimals encara difereixen: $3{,}1415$ i $3{,}1416$.
            '''),
            md(r'''
            ## 5. Experimenta: canvia el nombre de costats

            Mou el control de 3 a 300. El punt taronja indica al gràfic l'aproximació del
            polígon escollit. Sota el dibuix pots seguir **angle → mitja base → base → perímetre → aproximació**.
            Amb molts costats el polígon i el cercle gairebé no es distingeixen; comprova la
            diferència numèrica. Si el control no apareix, modifica `n` a la crida següent.
            '''),
            code(r'''
            def explora_aproximacio(n=12):
                d = dades_poligon(n)
                fig, (ax, bx) = plt.subplots(1, 2, figsize=(11, 4))
                dibuixa_poligon(ax, n)
                ax.set_title(f"Polígon inscrit de {n} costats")
                bx.plot(costats, aproximacions, color="#2563eb", label="Aproximacions")
                bx.axhline(math.pi, color="#b91c1c", ls="--", label="π de referència")
                bx.scatter([n], [d["pi_aprox"]], color="#ea580c", s=65, zorder=5)
                bx.set(xlim=(3, 300), xlabel="Nombre de costats n", ylabel="Aproximació de π",
                       title=f"π amb {n} costats ≈ {d['pi_aprox']:.9f}")
                bx.legend(loc="lower right")
                fig.tight_layout()
                plt.show()
                display(Markdown(
                    f"**Amb {n} costats i radi 1:**\n\n"
                    f"1. Angle superior: **360° / {n} = {d['alpha']:.6f}°**.\n"
                    f"2. Mig angle: **{d['alpha']:.6f}° / 2 = {d['beta']:.6f}°**.\n"
                    f"3. Mitja base: **sin({d['beta']:.6f}°) ≈ {d['base']/2:.9f}**.\n"
                    f"4. Base completa: **2 × {d['base']/2:.9f} ≈ {d['base']:.9f}**.\n"
                    f"5. Perímetre: **{n} × {d['base']:.9f} ≈ {d['perimetre']:.9f}**.\n"
                    f"6. Aproximació de π: **{d['perimetre']:.9f} / 2 ≈ {d['pi_aprox']:.9f}**.\n\n"
                    f"Error respecte al valor de referència: **{math.pi-d['pi_aprox']:.9f}**. "
                    "Els valors mostrats s'han arrodonit; el càlcul conserva tots els decimals."
                ))

            # Exemple visible també en lectors que no mostren controls interactius.
            explora_aproximacio(n=12)
            '''),
            code(r'''
            try:
                import ipywidgets as widgets
            except ImportError:
                print("Pots explorar altres valors executant explora_aproximacio(n=300).")
            else:
                control = widgets.IntSlider(value=12, min=3, max=300, step=1,
                                            description="Costats n:", continuous_update=False)
                panell = widgets.interactive(explora_aproximacio, n=control)
                display(panell)
            '''),
            md(r'''
            ## 6. Ampliació: aproximar per sota i per sobre

            Un polígon **circumscrit** té els costats tangents a la circumferència.
            Si el seu perímetre és $P_n$, la comparació geomètrica dona
            $p_n<2\pi<P_n$ per a radi 1. Dividint per 2:

            $$L_n=\frac{p_n}{2}<\pi<\frac{P_n}{2}=U_n.$$

            Per a l'hexàgon, $L_6=3$ i $U_6=2\sqrt3$. L'algorisme d'Arquimedes duplica
            els costats amb arrels quadrades i operacions aritmètiques. En aquest apartat
            comparem $6,12,24,\ldots,192$ costats; el gràfic anterior sí que inclou **tots**
            els enters fins a 300. Estudiarem la recurrència al quadern següent.

            Les cotes geomètriques exactes encerclen π; el programa en mostra valors arrodonits.
            '''),
            code(arquimedes),
            code(r'''
            def poligons(iteracions=2):
                n, inferior, superior = arquimedes(iteracions)[-1]
                fig, (ax, bx) = plt.subplots(1, 2, figsize=(12, 4))
                # Aquestes funcions trigonomètriques només serveixen per dibuixar.
                angles = np.linspace(0, 2*np.pi, n+1)
                t = np.linspace(0, 2*np.pi, 500)
                radi_exterior = 1 / np.cos(np.pi/n)
                ax.plot(np.cos(t), np.sin(t), color="0.4", label="Circumferència")
                ax.plot(np.cos(angles), np.sin(angles), color="#2563eb", label="Inscrit")
                ax.plot(radi_exterior*np.cos(angles+np.pi/n),
                        radi_exterior*np.sin(angles+np.pi/n), color="#d97706", label="Circumscrit")
                ax.set_aspect("equal")
                ax.set_title(f"{n} costats")
                ax.legend(fontsize=9)
                files = arquimedes(iteracions)
                for k, (_, a, b) in enumerate(files):
                    bx.plot([float(a), float(b)], [k, k], "o-", color="#7c3aed")
                bx.set_yticks(range(len(files)), [str(f[0]) for f in files])
                bx.set(xlabel="Semiperímetre", ylabel="Nombre de costats", title="Intervals cada vegada més estrets")
                fig.tight_layout()
                plt.show()
                print(f"Cota inferior ≈ {inferior:.12f}; cota superior ≈ {superior:.12f}")
                print(f"Amplada aproximada: {superior-inferior:.4E}")

            poligons(iteracions=5)
            '''),
            md(r'''
            ## 7. Què hem après? Aplica-ho

            **En cap pas finit el polígon es converteix en la circumferència.** Aproximem π
            amb polígons cada vegada més precisos. Una mostra fins a 300 costats permet observar
            la tendència, però no és una demostració d'un límit infinit.

            1. Per a $n=20$, calcula $\alpha$, $\beta$, $b$, $p_n$ i $\pi_n$, en aquest ordre.
               Dibuixa $O$, $A$, $B$ i $M$ i indica on hi ha $b/2$.
            2. Un alumne escriu $b=\sin(360^\circ/n)$ quan $r=1$. Explica **els dos errors**.
            3. Compara les files de 6, 48 i 300 costats: què passa amb la base, amb el perímetre
               i amb l'error? Per què una base més petita no implica un perímetre més petit?
            4. Amb 300 costats, hem trobat π o una aproximació? Per què necessitem l'ampliació
               del gràfic i la columna de l'error?
            5. **Ampliació:** executa `dades_poligon(20, radi=3)`. Què es multiplica per 3?
               Per què l'aproximació de π és la mateixa?
            6. **Ampliació:** si $L_n<\pi<U_n$, justifica que el punt mig $(L_n+U_n)/2$
               té un error menor que $(U_n-L_n)/2$ (amb les cotes exactes).

            <details><summary>Pistes i comprovació després d'intentar-ho</summary>

            1. $\alpha=18^\circ$, $\beta=9^\circ$, $b\approx0{,}31286893$,
               $p_{20}\approx6{,}25737860$, $\pi_{20}\approx3{,}12868930$.
            2. Cal utilitzar **mig angle**, $180^\circ/n$, i multiplicar per **2** per passar
               de mitja base a la base completa.
            3. La base disminueix, el perímetre augmenta i l'error disminueix: el nombre de
               costats també augmenta i cal considerar el producte $n b$.
            4. És una aproximació; a l'escala del dibuix dues línies poden semblar coincidents.
            5. Base i perímetre es tripliquen; en dividir per $2r=6$, la proporció es conserva.
            6. La distància del punt mig a qualsevol punt interior és menor que la meitat
               de l'amplada de l'interval.

            </details>

            **Cap al quadern següent.** Podem reduir l'amplada dels intervals tant com vulguem?
            Què garanteix que determinen un únic nombre real? Aquestes preguntes ens conduiran
            a l'algorisme d'Arquimedes i a la completesa de ℝ.
            '''),
        ], previous="Q_conjunt_dens.ipynb", following="NumeroPi.ipynb",
    )
