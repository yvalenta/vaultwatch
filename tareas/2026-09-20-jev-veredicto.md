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

## Bitácora
- 2026-09-20: tres workflows de solo lectura (19 agentes). 10 de 10 citas clave abrieron; 7 confirmadas textual, 3 con matiz (una cifra de calibración atribuida al checkpoint equivocado de un clon; un titular de US$40 M cuyo cuerpo dice US$25,9 M; «lista de espera» está en el blog, no en la portada). Un crítico afirmó «cero coincidencias» en dos greps que dieron 2 y 1: sus hallazgos del piloto quedan como punteros a verificar, no como hechos.
