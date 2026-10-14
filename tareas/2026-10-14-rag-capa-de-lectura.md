---
estado: abierta
dueño: ambos
fecha: 2026-10-14
tema: capa de lectura (RAG) sobre vaults ya auditados — solo lee, nunca decide; primero medir si el cold-start por puertas deja de alcanzar, y solo entonces construir
criterio_cierre: veredicto escrito, con cifras de un piloto, de si la capa de lectura gana a leer HANDOFF + state/ en orden; si gana, spec de un prototipo de solo lectura sobre state/ y laws/ con su prueba negativa; si no, se descarta con ese motivo
---

Viene de la conversación del 14-oct. La respuesta a «¿qué cambia con vault
rags?» fue: el RAG resuelve **encontrar**, el método resuelve que lo
encontrado **siga siendo cierto**. Un RAG sobre notas sin auditar las vuelve
más accesibles y más creíbles, que es el peor trato. Sobre un vault auditado
puede tener sentido, con una condición: que el RAG solo lea. Los auditores
siguen siendo los únicos que ponen rojo.

Depende de `2026-10-14-sello-de-auditoria.md`. Sin sello no hay forma de
saber qué se indexó ni si sigue vigente; construir esto antes es reintroducir
el problema que el método quita.

## La pregunta que va primero

El cold-start actual ya funciona sin RAG: la sesión lee las puertas en orden
(`HANDOFF.md` con la tabla de dirección, `state/`, `laws/`, la autopsia de las
mentiras), mide, corrige, prueba y commitea. **¿Cuándo deja eso de alcanzar?**
Hipótesis a medir, no a asumir:

- **Un vault grande**: `state/` + `laws/` no caben cómodos en el turno 1. Medir
  el tamaño real de los vaults vivos y la parte del piso de contexto que ya se
  lleva, no estimarlo.
- **Preguntas entre proyectos** («¿dónde hablamos de X?») que el índice fino
  de una línea por proyecto no contesta.
- **Preguntas abiertas** que no caen en una puerta conocida.

Si ninguna duele hoy, esta tarea se cierra con ese veredicto y se reabre el
día que alguna duela. Tampoco cuenta como razón «sería lindo».

## Reglas que la capa tendría que cumplir (si se construye)

1. **Solo indexa lo sellado.** Reconstruye desde un commit con sello válido.
   Un vault en rojo no se indexa, o sale marcado «no confiable».
2. **Cada fragmento viaja con su sello**: proyecto, sha, qué auditor corrió,
   cuándo, y de qué archivo viene. La respuesta cita el sello y, si es viejo,
   lo dice antes que el contenido.
3. **Punteros, no copias.** Devuelve fragmento + ruta; el agente abre el
   original. La copia indexada es para encontrar, no para citar (es la regla
   del índice compartido).
4. **`state/` y `laws/` pesan más que `history/`.** `history/` solo sale ante una
   pregunta histórica, para que una nota vieja no gane por parecerse mucho a la
   consulta.
5. **Nunca produce un rojo ni lo tapa.** No hay «puntaje de verdad». Si un
   fragmento contradice al mundo, lo dice el auditor, no el recuperador.
6. **Si el índice y el árbol discrepan, gana el árbol.** El índice es una caché
   y se tira sin pena.

## Cómo se mide el piloto

Sobre un vault vivo, con preguntas de respuesta conocida (escritas antes de
mirar los resultados): (a) ¿acierta la ruta correcta?; (b) ¿cita sello cada
vez?; (c) **negativa**: con un rojo plantado en una copia, ¿se niega a indexar
o lo marca?; (d) **negativa**: con una nota vieja en `history/` que contradice
a `state/`, ¿gana `state/`?; (e) contra la línea base, leer las puertas en
orden: ¿cuántos tokens y cuántos aciertos cada uno? Esa última comparación es
la que decide.

## Lo que no entra

- Un RAG que reescriba o «arregle» notas. Si hay que corregir algo, la
  corrección va al sitio de aserción, con el ritual.
- Embeddings como juez de contradicción entre notas. El método ya separó quién
  puede resolver cada contradicción: nota contra nota se señala; nota contra
  mundo lo decide el mundo.

## Bitácora
- 2026-10-14: declarada. Bloqueada por la tarea del sello. Nada medido ni
  construido todavía.
