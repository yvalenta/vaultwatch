---
estado: abierta
dueño: ambos
fecha: 2026-10-14
tema: sello de auditoría — que un vault verde deje una marca verificable de qué árbol midió y cuándo, para que cualquier capa de lectura (un RAG, un índice) pueda citar de dónde viene cada fragmento y negarse a servir lo no auditado
criterio_cierre: veredicto escrito sobre dónde vive el sello y cómo se invalida; si procede, entra a references/auditor-checks.md solo con un piloto en un vault vivo y su prueba negativa (tocar un archivo después del sello lo invalida; un auditor en rojo no emite sello)
---

Viene de la conversación del 14-oct sobre «vault rags». La conclusión fue que
un RAG tiene sentido como capa de lectura **sobre vaults ya auditados**, no
como sustituto de la auditoría. Eso exige algo que hoy no existe: una forma
de saber, desde fuera del vault, que lo que se está leyendo pasó verde y
**con qué contenido exacto**. Hoy el verde es un exit 0 efímero: se imprime,
se lee y se pierde. Un lector que llega después no puede distinguir un árbol
medido de uno editado a mano la hora siguiente.

## Qué tiene que cumplir un sello

- **Lo emite el auditor, nunca una mano.** Es salida de una corrida, no un
  texto escrito: es la ley «nunca escribas lo que un comando IMPRIMIRÁ,
  escribe lo que imprimió» aplicada a la marca misma.
- **Solo verde lo emite.** Un rojo no deja sello; un sello viejo no sobrevive
  a un rojo posterior.
- **Se invalida solo.** Ata el sello al contenido auditado (hash del árbol, no
  una fecha). Tocar un archivo después hace que el sello deje de coincidir.
  Si se invalidara por una decisión de alguien, sería una opinión.
- **Dice qué midió y qué no.** Los dos auditores (coherencia y mundo) son
  instrumentos distintos: el sello nombra cuál corrió. Un sello de solo
  coherencia no puede leerse como «el mundo coincide». Banner de humildad:
  verde significa que lo que los scripts vigilan sigue en su sitio, y nada
  más.
- **Los snapshots no caducan el sello.** Las filas SNAPSHOT se reportan pero
  nunca ponen rojo (ya es regla); el sello no puede depender de ellas.

## Preguntas abiertas (decidir antes de redactar nada)

1. **¿Dónde vive?** Candidatos: (a) una ref o tag de git sobre el commit
   auditado; (b) un archivo gitignored en el árbol; (c) solo la salida del
   auditor, que un lector reconstruye volviendo a correrlo. Ojo con (b) si se
   comitea: un archivo dentro del árbol cambia el hash del árbol que dice
   sellar. Hay que elegir sin crear esa circularidad.
2. **¿Qué se ata?** El hash del árbol completo o solo el de `state/` + `laws/`.
   Lo segundo evita invalidar el sello por tocar `history/`, pero abre la
   pregunta de si un cambio en `history/` puede volver falso algo en `state/`.
3. **¿Cuánto vale la fecha?** Una afirmación de `state/` medida contra el
   mundo caduca por el mundo, no por el árbol. Un sello con el mismo hash pero
   de hace tres semanas dice algo distinto de uno de hoy. Decidir si el sello
   lleva fecha, si el lector la muestra y si hay un umbral.
4. **¿Hace falta?** Si el único consumidor sería un RAG que todavía no existe
   (ver la tarea hermana), el sello puede esperar. El sello solo se justifica
   si algo más lo lee: la guarda de publicación, `/contexto` en una
   sesión fría, o el índice compartido entre proyectos.

## Lo que no entra

- Un sello firmado criptográficamente o publicado en cadena. Es otra
  superficie con sus propias identidades; el problema es de contenido, no de
  autoría.
- Un «nivel de confianza» numérico. El método rechaza opiniones con decimales
  en el lugar de una medición (ver 2026-09-20-jev-veredicto.md).

## Cómo se prueba

Prueba negativa en un vault vivo, sobre copia (`git archive`), no sobre el
repo: (1) base verde → sello emitido; (2) tocar un archivo de `state/` →
sello inválido sin volver a correr nada; (3) plantar un rojo → no hay sello
nuevo y el anterior queda invalidado; (4) tocar solo `history/` → comportamiento
conforme a lo decidido en la pregunta 2, escrito de antemano.

## Bitácora
- 2026-10-14: declarada. Nada tocado en la skill. Este repo es público: acá
  va solo lo que toca al método; lo interno de la casa vive en su repo.
