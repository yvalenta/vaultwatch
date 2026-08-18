# audited-vault en la constelación

Declaración de este repo para el grafo de proyectos de la casa (lo lee
el observatorio interno de la casa, que documenta el formato). Repo público:
solo superficies públicas.

| campo | valor |
|---|---|
| id | audited-vault |
| clase | conocimiento |
| qué | vaultwatch: el método del vault auditado empaquetado para afuera — el artículo y la skill instalable `skills/vaultwatch` (CC BY 4.0) |
| dónde | GitHub; la skill se copia a `~/.claude/skills/` de quien la instala |
| servicio | `—` |
| atiende | sesiones de Claude a demanda |
| contexto | `README.md` |
| visibilidad | público: `github:yvalenta/vaultwatch` (la carpeta local sigue siendo `audited-vault`; el nombre viejo redirige) |

## Aristas

| a | b | tipo | por | medición |
|---|---|---|---|---|
| audited-vault | github | publica | el repo público es la superficie (CC BY 4.0) | `remoto origin` |
| audited-vault | nomicheck | mira | el método nació operando ese producto; las demás aristas las declaran los repos que lo usan | `—` |
