---
estado: propuesta
dueño: sesión
fecha: 2026-09-28
tema: chequeo candidato de ausencia — lo retirado a propósito (credencial rotada, endpoint o archivo dado de baja) queda registrado y la auditoría del mundo afirma que ya no se sirve
criterio_cierre: veredicto escrito sobre si el catálogo ya lo cubre; si no, el chequeo entra a references/auditor-checks.md solo con un piloto en un vault vivo que registre ≥3 retirados reales y su prueba negativa (volver a servir uno pone rojo)
---

Viene de la lectura de ECC (affaan-m/ecc, 28-sep). El paquete no entra; de su
skill `living-docs-governance` sale una idea: una «delete-zone», una lista de
lo que se quitó a propósito para que no vuelva a aparecer. Allá es texto que
el agente lee. Acá solo vale si es una medición: **una lista de retirados con
su forma, y un auditor que afirma que el mundo ya no los sirve.** Es el
incidente del README visto desde el otro lado: la billetera rotada que un
archivo olvidado seguía sirviendo.

## Lo que el catálogo ya tiene (medido en este repo, 28-sep)

- `references/auditor-checks.md` §4: la auditoría de coherencia barre el árbol
  entero, worktrees y gitignored incluidos, buscando literales con forma de
  constante de identidad fuera de su sitio de aserción. Eso atrapa la copia
  **local** del valor viejo.
- La tabla «Deriving measurements» admite la forma «endpoint devuelve 404». Un
  retirado puntual se puede afirmar a mano como una fila más de `state/`.

## Lo que falta comprobar antes de proponer nada

1. ¿La auditoría del mundo busca los valores retirados en los **bytes
   servidos**? Si solo compara lo servido contra la fuente de verdad actual,
   una página que sirve el valor viejo en una ruta no listada sigue verde.
2. ¿Un retirado tiene sitio propio (una lista en `state/` o en las leyes), o
   se pierde cuando se borra la fila que lo describía?
3. Si (1) y (2) ya están cubiertos, esta tarea se descarta con ese motivo.
   No duplicar la ley «silence looks identical to green» ni el chequeo #7
   (`requires_site`); ver lo que murió en 2026-09-20-jev-veredicto.md.

## Bitácora
- 2026-09-28: declarada tras leer ECC (skills `living-docs-governance`,
  `knowledge-ops`, `verification-loop`); solo la delete-zone sobrevivió como
  idea. Nada tocado en la skill todavía.
- 2026-09-28: **veredicto: el catálogo público no lo cubre, la práctica viva
  sí.** No es un chequeo nuevo, es brecha de publicación. Lo que tiene el
  vault vivo privado y `auditor-checks.md` no:
  1. un **registro declarado de retirados** (valor → motivo) en el propio
     auditor sin red, y los valores anteriores con etiqueta propia en el
     sitio de aserción de identidad (3: wallet, hash, CID);
  2. barrido del árbol entero que exige que cada mención de un retirado
     **se marque como pasado** (ventana de 3 líneas, para no castigar prosa
     envuelta), con los logs de corridas exentos porque afirman en pasado;
  3. **tolerancia cero en lo servible**: en cualquier ruta con un segmento
     `site/` o `.well-known/`, un retirado es rojo aunque esté marcado — un
     tercero lee el JSON, no el comentario;
  4. la **guarda de publicación** rechaza desplegar un artefacto que traiga
     un valor retirado.
  El §4 público solo barre literales por forma fuera del sitio de aserción:
  atrapa la copia vieja, pero no distingue retirado de desconocido ni exige
  nada de lo servido. Del lado del mundo no falta nada nuevo: la comparación
  byte a byte de lo servido contra el valor vivo ya pone rojo si una URL
  conocida sirve el viejo, y una URL que nadie lista no la cubre ningún
  registro. Las URLs retiradas (la delete-zone literal de ECC) no tienen
  autopsia; no entran.
  **Prueba negativa** sobre una copia `git archive` del vault vivo (no el
  repo): base verde, exit 0; retirado en presente en una nota y en un
  `site/` → rojo, 2 menciones, exit 1; ambos marcados «anterior» → rojo, 1
  mención (el servido), exit 1; sin el servido → verde, exit 0.
  Falta: redactar la extensión del §4 en `auditor-checks.md`. Commitear es
  local; el push a este repo público aparca para Yonatan.
