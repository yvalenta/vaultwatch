---
estado: propuesta
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
  0,361 y 0,342 — por debajo de la clase mayoritaria (0,461). El 0,766 del
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
vida, ya es un caso del chequeo #1 (la cifra afirmada en dos sitios), verificado
por grep sobre el commit del 20-sep:

- multilingüe base: 0,342 (tablas, README L308 y L323) contra 0,352 y «0,35»
  (prosa, README L360 y L393); inglés base 0,361 (BENCHMARKS L143) contra 0,362
  (README L307); Brier 0,061 contra 0,062; «6–7x faster» (README L269) contra
  «7,8× faster» (L284).
- README L273 dice que toda cifra de Laya es lo que devuelve
  `Router().predict(...)`, «not a hand-picked best of three»; `laya/router.py`
  L26–27 dice que `typed-decisions` jamás se elige solo salvo opt-in. Un
  `Router()` por defecto sobre esas preguntas devuelve el checkpoint de 0,362,
  no el de 0,766. (Leído en el código, no corrido.)
- El titular empareja el acierto de un checkpoint (0,766, el afinado, ECE 0,213)
  con la calibración de otro (0,081, el inglés base tras ajustar), y compara
  Laya ajustado contra Jev tal como sale. README L296 los funde en una frase.
- README L192–206 recomienda automatizar sin humano con confianza ≥ 0,85; L138
  del mismo archivo dice «confidence gating cannot save you».
- `BENCHMARKS.md` L9 cita `research/results/app_benchmark.json`, que no está en
  el árbol: la tabla de «Themes» entera no tiene archivo de resultados. README
  L254 manda a reproducir con `notebooks/laya_benchmark_colab.ipynb`; el archivo
  vive en `research/scripts/`.

Candidato aparcado (publicar es de Yonatan, y no pasó por refutación): un issue
upstream con esas cinco filas. Vale por sí mismo para el mantenedor; como canal
para el método, lo esperable el día 1 es nulo.

## Bitácora
- 2026-09-20 (noche): adenda de Laya. Leídos en crudo README, BENCHMARKS y `laya/router.py` del repo (sin instalar ni correr nada); metadatos por la API de GitHub; las divergencias de cifras, verificadas por grep. Sin agentes.
- 2026-09-20: tres workflows de solo lectura (19 agentes). 10 de 10 citas clave abrieron; 7 confirmadas textual, 3 con matiz (una cifra de calibración atribuida al checkpoint equivocado de un clon; un titular de US$40 M cuyo cuerpo dice US$25,9 M; «lista de espera» está en el blog, no en la portada). Un crítico afirmó «cero coincidencias» en dos greps que dieron 2 y 1: sus hallazgos del piloto quedan como punteros a verificar, no como hechos.
