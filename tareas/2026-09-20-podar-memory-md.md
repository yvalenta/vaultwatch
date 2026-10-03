---
estado: hecha
dueño: ambos
fecha: 2026-09-20
tema: MEMORY.md de este repo pesa 13,4 KB (líneas de hasta 597 caracteres) y entra entero al turno 1 de cada sesión; el de nomicheck-ops pesa 1,3 KB
criterio_cierre: MEMORY.md con una línea corta por entrada (gancho, no contenido), sin perder ningún gancho, y el turno 1 de la fila vigente de `timon/bin/contexto-vivo --piso 7` baja en lo que pesaba el recorte (~2,5k tokens)
---

Viene de `timon/tareas/2026-09-20-corte-dinamico-y-piso-de-contexto.md`,
palanca D. Es una sesión propia de este repo porque la memoria es de acá y
hay que comprobar, entrada por entrada, que el detalle de cada gancho vive en
el cuerpo de su archivo de memoria ANTES de recortar la línea del índice.
La «dieta de memoria» ya cayó una vez (1-sep) por no pagar renta: la cifra
es chica (~1k tokens del piso, ~1 turno por sesión). Hacerla solo si se
hace de paso, con la skill consolidate-memory si sigue existiendo.

## Bitácora
- 2026-09-20: declarada desde timon (sesión 7843b314). Nada tocado acá.
- 2026-09-24: **índice podado.** MEMORY.md de 14.842 a 6.700 bytes, 48 de 48
  memorias indexadas, una línea corta por entrada (la más larga era de 873
  caracteres). Antes de recortar se comprobó, entrada por entrada, que cada
  fecha, cifra y ruta del gancho viejo vive en el cuerpo de su archivo (script
  de tokens con dígito; los 9 marcados eran fechas escritas de otra forma o
  detalles ya presentes con otra redacción). Copia del índice viejo en el
  scratchpad de la sesión 854110f8. **Falta la mitad medible del cierre:** el
  turno 1 de `timon/bin/contexto-vivo --piso 7` en la próxima sesión fría de
  este repo — esta sesión cargó el índice viejo y no puede medirse a sí misma.
- 2026-10-03: medida la mitad que faltaba, en sesión fría de este repo (5cc8dce2, claude-desktop 2.1.286). `timon/bin/contexto-vivo --piso 7` desglosa el turno 1 de esta sesión y la fila de instrucciones dice `memory/MEMORY.md 7k` caracteres (7.292 bytes por `wc -c`), contra 14.842 antes del recorte: −7,5k car ≈ −1,9k tokens, en el orden de los ~2,5k prometidos. El turno 1 total (70k) NO sirve para comparar: entre el 20-sep y hoy cambió el arnés (2.1.281 → 2.1.286, esquemas de herramientas 170k car, `Artifact` sola 54k) y ese ruido tapa el recorte; la fila `memory/MEMORY.md` es la medición limpia. 48/48 ganchos siguen (bitácora anterior). Criterio cumplido en su parte medible → hecha.
