---
estado: hecha
dueño: ambos
fecha: 2026-10-15
tema: caso reproducible — un vault de ejemplo ejecutable, con sus dos auditores y mutaciones sobre copia, para ver fallar el método en vivo antes de confiar en él
criterio_cierre: visto de Yonatan sobre el ejemplo (`examples/demo-vault/`) y decisión sobre si el README del artículo lo enlaza; el ejemplo no entra al catálogo ni a la skill, solo vive como demostración
---

Viene de la conversación del 14-oct (idea 5 de la lista de mejoras: «un caso
de uso real y reproducible en el README»). El artículo cuenta 37 mentiras que
no se pueden ejecutar. Esto es lo contrario: un vault de juguete donde el rojo
se ve en un minuto, sin red, sin instalar nada.

## Qué se construyó

`examples/demo-vault/`: un mini-vault (`HANDOFF.md`, `state/`, `laws/`,
`history/`), un «mundo» (`world/server.py`, un endpoint HTTP de juguete que
lee `world/served.json` en cada petición) y dos auditores
(`audit/coherence.py` sin red, `audit/world.py` con llamadas HTTP reales a
localhost). `demo.sh` los corre y rompe cosas **sobre una copia**, nunca sobre
el vault: `--drift` (el mundo se mueve y los docs no), `--contradict` (una
cifra copiada a mano), `--orphan` (una nota sin enlazar) y `--proof`, que
corre todo y comprueba los códigos de salida.

El caso que importa es `--drift`: ningún documento cambió, las notas siguen de
acuerdo entre sí, la auditoría de coherencia sigue verde, y solo la del mundo
lo ve. Es el incidente de la billetera en miniatura.

## Lo que se dejó fuera a propósito

Tres chequeos de coherencia y una aserción, no el catálogo entero. Sin
constantes de identidad en código, sin higiene de tablas, sin el registro de
retirados, sin el barrido por mutación. El objetivo es que el mecanismo quepa
en una pantalla; para el resto está la skill. Sin red ni dependencias: solo
la biblioteca estándar de Python 3 y bash.

## Preguntas abiertas

1. ~~**¿El README del artículo lo enlaza?** No lo toqué: es el texto público del
   método y enlazar un ejemplo cambia cómo se lee. Si sí, una línea junto a
   «Install It As A Claude Code Skill».~~ Resuelta el 15-oct: Yonatan pidió
   enlazarlo; ver la bitácora.
2. **¿Vive en este repo o aparte?** Hoy cuelga de `examples/`. Si crece, o si
   la skill debe poder copiarlo, habría que decidir si va dentro de
   `skills/vaultwatch/`.
3. **¿Se prueba en CI?** `./demo.sh --proof` sale 0 solo si cada rojo saltó
   donde debía y el vault quedó intacto, así que sirve de prueba. No hay CI en
   este repo; añadirlo es otra decisión.

## Bitácora
- 2026-10-15: construido y medido en este contenedor (Python 3.13.16, bash
  5.2). `./demo.sh` da coherencia=0 y mundo=0. `./demo.sh --proof` da
  `base 0/0 · drift 0/1 · contradict 1/0 · orphan 1/0`, los cuatro como se
  esperaba, y la huella del vault es idéntica antes y después (`802ab3f64d7e`).
  **Prueba de la prueba**, sobre copias: (1) con el patrón de cifras de
  `coherence.py` anulado, `--proof` sale 1 y marca `contradict` como WRONG;
  (2) con la comparación de `world.py` anulada, `--proof` sale 1 y marca
  `drift` como WRONG. Un tropiezo propio, escrito para que no se pierda: mi
  primera mutación usó un patrón que aparecía en la propia línea del auditor
  y, como el auditor barre todo el árbol incluido su código, se detectó a sí
  mismo y dio un rojo que no era el que buscaba; hubo que repetirla con un
  patrón que no puede coincidir. Es el «el auditor vive en el mismo árbol que
  juzga» del catálogo, visto en pequeño. Falta el visto de Yonatan.
- 2026-10-15: **enlazado en el README del artículo**, a pedido de Yonatan. Un
  párrafo al final de «Install It As A Claude Code Skill», con el enlace a
  `examples/demo-vault/` y el caso `--drift`; el resto del artículo no se
  tocó. Medido: `./demo.sh --drift` tarda 0,5 s y `--proof` 1,0 s en este
  contenedor, así que «en un minuto» es holgado. Quedan abiertas las
  preguntas 2 (dónde vive) y 3 (CI), y el visto sobre el ejemplo.
- 2026-10-15: **hecha**, por instrucción de Yonatan. El criterio de cierre pedía
  su visto sobre el ejemplo y la decisión sobre el README; el enlace ya está
  puesto y el visto llegó con esta orden. Las preguntas 2 (si el ejemplo vive
  en `examples/` o dentro de `skills/vaultwatch/`) y 3 (si se prueba en CI) no
  se resolvieron: se cierra la tarea con ellas abiertas, y quien las retome
  abre una nueva. Hoy el ejemplo queda en `examples/demo-vault/` y se prueba a
  mano con `./demo.sh --proof`.
