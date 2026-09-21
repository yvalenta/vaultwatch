---
estado: hecha
dueño: ambos
fecha: 2026-09-20
tema: veredicto sobre Jev (TypeSafe AI) y el método — el proveedor no entra; del patrón sobrevive un solo chequeo candidato, determinista
criterio_cierre: visto de Yonatan sobre el veredicto; el chequeo candidato solo entra a references/auditor-checks.md si un piloto sobre ≥3 archivos de un vault vivo encuentra afirmaciones sin ancla que importen, con su prueba negativa
---

Pregunta del 20-sep: ¿se puede aprovechar Jev —un clasificador por API que no
genera texto: `state` + preguntas tipadas (sí/no, elegir-una, nivel) →
probabilidades— para mejorar el método del vault auditado? Tres pasadas: medir
el terreno, refutar cinco propuestas, leer el código de las nueve demos más
vistas de la semana del lanzamiento. Este repo es público: acá va solo lo que
toca al método; lo interno de la casa vive en su repo.

## Veredicto

**El proveedor, no.** Cinco días de vida, acceso temprano, API cerrada sin
pesos, y una auditoría independiente (scienthoon/jev-ood-calibration) lo midió
bien calibrado en benchmarks públicos pero sobreconfiado (0,74 de probabilidad
media) cuando la respuesta depende de una política que no está en el texto —
que es justo la forma de las preguntas de un vault («¿esto sigue siendo cierto
allá afuera?»). Un modelo probabilístico dentro de un auditor contradice la
tesis: el rojo tiene que ser una medición, no una opinión con decimales.

**Del patrón, una sola cosa sobrevive — y sin modelo.** La propuesta «barrer
cada línea de `state/` con preguntas tipadas para hallar afirmaciones sin
ancla» volvió de la crítica así: el método ya probó un detector genérico de
«afirmación sin sitio», dio falsos positivos sobre texto bien escrito y se
angostó a propósito. Lo que sí vale es la versión determinista: **grep de
formas reconocibles** (direcciones, hashes, CIDs, fechas, entero+unidad) en
`state/`, cruzado contra la lista de lo que los auditores de verdad leen;
lo que tiene forma de dato y ningún lector es el candidato a fila nueva. Es
consultivo (jamás pone rojo) y se imprime con su banner de humildad.

## Lo que murió, y por qué (para no volver a proponerlo)

- **«Canario de guarda» como ley y chequeo nuevos** — la ley ya está escrita
  cinco veces en este repo («silence looks identical to green») y el chequeo
  es el #7 de auditor-checks.md (`requires_site`) más «Perimeter guards». Una
  sexta copia violaría el chequeo #8 del propio catálogo.
- **Una pieza pública montada en la ola de Jev** — el ejemplo central estaba
  mal leído (el `fail_open` de LiteLLM con Jev es de compactación, documentado,
  configurable y con rastro: benigno), el casillero está ocupado (≥22 repos de
  guardrails en cinco días) y el día 1 del adoptante sería un resultado nulo.
- **Presupuesto en bytes de las puertas del arranque en frío** — la cuenta de
  ahorro ignoraba que la re-lectura se paga como caché; medido bien, el efecto
  es de alrededor del 1 %. Y la historia del propio método documenta que leer o
  corregir parcial ya costó una ronda de mentiras.

## Lo aprendido de las nueve demos que sí es método

- **Relevancia no es reproducibilidad.** Un plugin que tira resultados de
  herramientas «irrelevantes» perdió una cifra que después no se pudo regenerar
  porque el código que la producía había cambiado. Primo de «nunca escribas lo
  que un run VA a decir»: tampoco tires lo que un run YA dijo si no podés
  volver a correrlo igual.
- **El show está en el generador de candidatas, no en el clasificador** (la
  demo de conducción, la de Doom): el estado llega masivamente pre-procesado.
- **Dos números, no uno.** El único eval de «portero barato antes de lo caro»
  que se dejó leer comparaba contra etiquetas de otro LLM, no contra la verdad.
  Un filtro se reporta con lo bueno que se comió y la basura que dejó pasar.

## Adenda (20-sep, noche): Laya, el clon local y abierto

El único disparador que quedó escrito para reabrir el tema era «un clasificador
local y abierto, para un sitio con caudal real de decisiones». Laya
(`NandhaKishorM/laya`, Apache-2.0, pesos en Hugging Face, creado el 18-sep,
5.028 estrellas en dos días) cumple la primera mitad. **El veredicto no se
mueve**, y las razones salen de su propio `BENCHMARKS.md`:

- **Sin afinar no decide.** En typed-decisions los dos checkpoints base dan
  0,361 y 0,342 según su tabla (0,362 y 0,3515 en el crudo de T4) — por debajo
  de la clase mayoritaria (0,461). El 0,766 del
  titular es del checkpoint afinado con el split de entrenamiento de ese mismo
  benchmark, y las etiquetas son de un LLM maestro (el «techo» 0,735 es su
  autoacuerdo): es acuerdo con otro modelo, no con la verdad — «dos números, no
  uno». En sus palabras: «a fast base to specialise, not a zero-shot decision
  engine». Usarlo cuesta ~30k preguntas etiquetadas y 4–5 h de 2×T4.
- **Fuera de su entrenamiento se cae.** Jailbreak 0,708–0,762, prompt-injection
  0,698 (n=116), moderación 0,530 (azar). Lo fuerte (spam y phishing, 0,99)
  estaba en la mezcla de entrenamiento.
- **Español: 0,530** en intención de 20 opciones, ECE 0,275.
- **El `state` es de ~320–768 tokens** (Jev: ~64k). No entra un archivo de
  `state/`.
- **Sale sobreconfiado** (ECE 0,466 y 0,314); el arreglo es ajustar
  temperaturas con datos propios etiquetados. El checkpoint inglés nunca baja de
  0,885 de confianza media a ningún nivel de acierto (jemer: 0,000 de acierto a
  0,952). Es la forma que descalificó a Jev para un auditor, más pronunciada.
- En CPU: 193–464 ms con el modelo residente, 7,4 s en frío.

**Lo aprovechable es el espécimen, no la dependencia.** `BENCHMARKS.md` practica
el banner de humildad mejor que nada visto esta semana: cada cifra con su
procedencia («third-party published, never measured here», «in training» /
«held out») y una sección «Limits, stated plainly». Y a la vez, con dos días de
vida, ya es un caso de los chequeos #1 y #3 (la cifra afirmada en dos sitios; el
doc contra el disco). Las filas de abajo pasaron por refutación con repro sobre
el commit `42626c3` y después las replicó la sesión contra los JSON crudos —
la primera versión de esta adenda tenía la fila 1 al revés:

1. **La fila del titular no está en los resultados commiteados.**
   `BENCHMARKS.md` L8 dice que el barrido en CPU trae typed-decisions de los
   tres checkpoints; en `cpu_51_language_sweep.json`, `part_b.by_model` tiene
   una sola llave, `english` (0,3615 — la fila `laya` de la tabla, al dígito).
   El JSON de T4 solo trae `laya` (0,362) y `laya-multilingual` (0,3515). El
   0,766, su Brier y su ECE no están en ningún archivo del repo. El script
   vuelca el JSON después de cada modelo: tiene cara de archivo parcial
   commiteado. De ahí cuelgan las divergencias: multilingüe 0,342 en las tablas
   contra 0,352 y «0,35» en la prosa (el crudo respalda a la **prosa**); 0,361
   contra 0,362 (dos corridas, sin rotular); Brier 0,061 contra 0,062.
2. **README L273** dice que toda cifra es lo que devuelve
   `Router().predict(...)`, «not a hand-picked best of three». Para la fila de
   typed-decisions no: `auto_task_detection` es `False` por defecto
   (`router.py` L151, docstring L26–28), `tests/test_router.py` L145 fija que un
   `Router()` por defecto devuelve `english` sobre esas preguntas, y el arnés
   que produjo la fila carga cada checkpoint con `laya.load()` sin construir un
   Router (`bench_local.py` L147–150, L268–271). En la misma tabla, los 32,8 ms
   son del multilingüe, y el propio README (L92) manda el inglés a `laya`, 39,5
   ms: por eso «6–7x» (L269) y «7,8×» (L284) conviven. (Leído, no corrido.)
3. **El titular empareja checkpoints distintos**: 0,766 es del afinado (ECE
   0,213); 0,081 es la media de `laya` en 49 suites tras el ajuste, y
   `calibration_repair` no cubre al afinado. El 0,246 de Jev es la suite «S5
   confidence honesty» de un tercero, tal como sale; en typed-decisions la
   propia tabla le da 0,144. README L296 los funde. El ajuste en sí es honesto
   (se ajusta con una mitad y se mide en la otra) — eso no se objeta.
4. **Punteros a archivos que no están**: `research/results/app_benchmark.json`
   (`BENCHMARKS.md` L9, toda la tabla de «Themes») no existe en el árbol, ni en
   la rama `research`, ni en el PR que creó la carpeta, y `bench_apps.py` L39
   escribiría en otra ruta; README L254 nombra `notebooks/…colab.ipynb`, enlaza
   a la raíz y el archivo vive en `research/scripts/`; los 193–464 ms y los
   7,4 s / 10,3 s en CPU no tienen archivo de resultados; de «103–332
   preguntas/s» el crudo da 55,2–535,6 y el 332 no aparece.

**La fila que cayó como hallazgo nuestro:** la contradicción del apartado de
confidence gating (README L192–206). Es real —en suites en inglés bien
ruteadas (las dos de MASSIVE) la confianza media es ≥ 0,99 con 60–78 % de
acierto—, pero el
mantenedor ya la había reconocido ese mismo día en su issue #35 («confidence
gating should not be presented as usable until temperatures are fitted»). Sin
el barrido de duplicados se la habríamos «descubierto» a quien ya la sabía.

Lo que el barrido encontró coherente también cuenta, para que la ausencia de
fila signifique algo: la tabla de latencia, 45 de 51 idiomas, las 17.416
preguntas, 0,466 → 0,081 y la tabla de orden de opciones coinciden con el JSON.

El borrador del issue upstream (filas 1–4, con un bloque de comandos que
reproduce cada una) quedó escrito y entregado a Yonatan; mandarlo es suyo.
Como canal para el método, lo esperable el día 1 es nulo.

## Piloto del chequeo candidato (21-sep) — a medio camino, cortado por la regla de 200k

Yonatan dio el visto al veredicto el 21-sep («vamos, completa lo restante»). Lo
que queda del criterio de cierre es el piloto. Se corrió sobre un vault vivo
privado (8 archivos de estado, 195 KB), siempre en una copia del árbol
commiteado (`git archive`) fuera del repo; el repo medido quedó intacto. Acá
van solo conteos: los valores son internos.

**El chequeo cambió de forma al pilotearlo.** «Grep de formas cruzado contra la
lista de lo que los auditores leen» pide una lista que nadie tiene. Lo que sí
se puede medir es la prueba negativa al por mayor: **mutar cada dato con forma
reconocible en un carácter, correr la puerta sin red, y anotar cuáles la dejan
verde.** Verde tras mutar = nadie lo lee. Es determinista, consultivo, y no
adivina lectores: los mide.

Medido:
- 548 datos con forma (fecha, entero+unidad, URL, IP:puerto, sha corto, monto,
  dirección, hash, CID). El auditor sin red, solo: **11 leídos, 537 no** (60 s,
  0,11 s por corrida). Lee los 2 CID, 3 de 5 direcciones, 5 de 156
  entero+unidad, 1 de 263 fechas; cero URL, IP, sha, monto o hash.
- Cruce con el auditor con red (cargado con los sockets prohibidos, sin
  correrlo): lee `estado/` por 9 patrones más un lector de identidad de 15
  campos. Rescata 6 datos más. Un cruce por literal contra el código del
  auditor dio 141 «lectores» falsos (fechas que aparecen en comentarios): el
  cruce estático miente, que es justo por qué la mutación es el instrumento.
- Quedan **265 datos (207 líneas) que ningún instrumento lee**, sin contar
  fechas. Prueba negativa contra la puerta COMPLETA (49 comprobaciones, 1.340
  pruebas, 11,5 s): **262 la dejan verde, 3 tienen lector en una suite** (612 s
  con 6 copias en paralelo).

**Lo que eso NO dice todavía:** que esos 262 importen. La doctrina del catálogo
es que el auditor crece por autopsia, no por ambición; historia e instantáneas
no se anclan. Falta el juicio.

**El juicio (21-sep, sesión fría).** El workflow de clasificación había
terminado a medias: tres de los cinco escépticos murieron por un tope de 300
caracteres en el schema. Se relanzaron solo esos (18 líneas). Resultado sobre
las 207 líneas: 91 historia, 69 medidas por otra vía, 14 ruido, 7
instantáneas y **26 vivas sin ancla** (el escéptico bajó 7 de 33). Al cruzar
las 26 contra la prueba negativa, una estaba entre los 3 rojos: clasificador
y escéptico, los dos con grep en mano, la dieron por «sin lector» y la
mutación ya le había hallado uno (una prueba que compara el HTML commiteado
contra el regenerado — lee la frase, no mide el hecho). Quedan **25 con su
prueba negativa**, en 6 archivos.

**¿Importan?** 13 son hechos de otro repo de la casa (direcciones locales,
cadencias, techos de memoria): fuera del alcance por diseño; lo que piden es
cita, no fila. Las otras 12 son propias y al alcance, y entre ellas hay un
precio que fijamos nosotros, el techo de gasto por defecto de un script que
paga en firme, el umbral de una alerta de presupuesto, y el ritmo del vigía
que es el único lector de otra línea del vault. Eso cumple el criterio: **el
chequeo entró a `references/auditor-checks.md` como #9**, consultivo, con sus
límites escritos (rojo tras mutar prueba que alguien lee la frase, no que
alguien mida el hecho; no ve afirmaciones sin forma; una corrida de puerta
por dato). Las líneas concretas quedaron como tarea `propuesta` en el repo
del vault medido. Scripts, clasificación y veredictos, con valores internos,
siguen fuera de este repo:
`~/.claude/projects/-Users-yonatan-Developer-audited-vault/piloto-forma-sin-lector/`.

## Bitácora
- 2026-09-21 (tarde, sesión fría): relanzados los 3 escépticos caídos (2 agentes en el modelo mediano, ~0,27 M tokens, sin schema: JSON a archivo, validado, con `razon` y `greps` no vacíos comprobados). 18 de 18 con veredicto: 13 siguen, 5 bajan a historia. El cruce de los 26 sobrevivientes contra `gate_completo.json` lo hizo la sesión y tumbó uno; el mecanismo del lector se leyó en el test. Las cifras del #9 se recontaron contra los JSON (91+69+14+7+26 = 207). La entrega (el texto del #9) NO pasó por un refutador aparte: es catálogo, no dinero ni autorización. Sin push: pide GO.
- 2026-09-21: visto de Yonatan al veredicto. Piloto del chequeo candidato corrido hasta la prueba negativa (548 datos, 11 leídos por el auditor sin red; 262 de 265 sin lector dejan verde la puerta completa). La sesión pasó los 200k de contexto (260k, 26 de 61 turnos sobre el umbral) y cierra acá por la regla de corte, con el workflow de clasificación todavía corriendo: lo que falta quedó escrito arriba.
- 2026-09-20 (noche, tras el GO): refutación de las filas antes de redactar el issue. Siete agentes de solo lectura, todos en el modelo mediano (replicar/verificar/leer), ~0,9 M tokens, 13 min. Cuatro filas sobrevivieron, una cayó por ya reconocida upstream, y la fila 1 estaba al revés en la primera adenda (el crudo respalda a la prosa, no a las tablas) — se corrigió ANTES del push. Un agente devolvió un resultado vacío con veredicto («placeholder»: se le rompió la salida estructurada); su trabajo se recuperó del transcript y la sesión lo replicó a mano contra los JSON. Todo lo que afirma esta adenda lo corrió la sesión, no solo un agente; el bloque de comandos del borrador se ejecutó tal cual y cada cita de línea se comprobó con `sed`.
- 2026-09-20 (noche): adenda de Laya. Leídos en crudo README, BENCHMARKS y `laya/router.py` del repo (sin instalar ni correr nada); metadatos por la API de GitHub; las divergencias de cifras, verificadas por grep. Sin agentes.
- 2026-09-20: tres workflows de solo lectura (19 agentes). 10 de 10 citas clave abrieron; 7 confirmadas textual, 3 con matiz (una cifra de calibración atribuida al checkpoint equivocado de un clon; un titular de US$40 M cuyo cuerpo dice US$25,9 M; «lista de espera» está en el blog, no en la portada). Un crítico afirmó «cero coincidencias» en dos greps que dieron 2 y 1: sus hallazgos del piloto quedan como punteros a verificar, no como hechos.
