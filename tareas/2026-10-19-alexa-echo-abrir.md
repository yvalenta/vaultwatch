---
estado: en-curso
dueño: ambos
fecha: 2026-10-19
tema: los Echo de la casa — medir su telemetría sin tocarlos, decir con fuentes qué se puede abrir por generación (REA/AVS), y proponer un cerebro de voz local en el homelab que controle la casa sin nube
criterio_cierre: documento de factibilidad con fuentes verificadas (qué se puede y qué no, por generación), medición de telemetría de los Echo reales (dominios, frecuencia, reposo) y propuesta concreta del cerebro de voz local con GO/no-GO de Yonatan; nada levantado ni cambiado en la red sin su GO explícito
---

Nace de la sesión del TV Samsung (18/19-oct): Yonatan siente los Echo «muy
limitados» y quiere entenderlos, medir su privacidad y abrirlos vía control
local. Es su hardware y su red. Patrón heredado del TV: medir leyendo el
caché del router sin recursión y el dnsmasq temporal del homelab; investigar
con workflow (lectores sonnet + verificador adversarial) separando lo
documentado de lo rumoreado; ser honesto con lo que NO tiene camino público.
Nada de exploits ni instrucciones para saltar protecciones: de una fuente así
se cita alcance y resultado, no el cómo.

Tres frentes, de más seguro a más ambicioso:
1. **Descubrir y medir**: ubicar los Echo en la LAN, modelo/generación por lo
   que se lea sin tocarlos; dominios de Amazon a los que hablan, frecuencia,
   tráfico en reposo.
2. **Entender con REA**: app Alexa (APK) y protocolo AVS; qué es
   direccionable localmente, qué exige nube, qué autenticación; estado real
   de root/firmware abierto por generación, con evidencia.
3. **Abrir vía control local**: cerebro de voz local en el homelab (HA
   Assist vs Rhasspy vs Willow) para luces, el TV ya abierto, Jellyfin y la
   flota/Oráculo por voz; más una skill privada de Alexa por la API oficial
   como puente al homelab (funciona hoy sin tocar el Echo).

**Dónde vive el detalle.** Este repo es público (`yvalenta/vaultwatch`), así
que acá no van direcciones, MACs, seriales ni hostnames de la casa: el
documento de factibilidad con las mediciones vive fuera del repo, en la
carpeta de notas compartidas de la sesión madre
(`~/Library/Application Support/Claude/side-session-notes/<sesión madre>/`),
hasta que Yonatan nombre el nodo privado de los aparatos de la casa (cámara,
TV, Echo), que la constelación no tiene.

## Bitácora
- 2026-10-19: declarada desde la sesión del TV. `/casa`: tabla MUDA (13 d sin
  regenerar, la copia del homelab es la misma) y sin nodo que cubra los
  aparatos de la casa. El dnsmasq temporal del homelab está arriba pero nadie
  apunta ahí todavía (solo pruebas).
- 2026-10-19: **frente 1 medido, sin tocar ningún aparato.** Dos Echo
  ubicados en la Wi-Fi de la casa por OUI de Amazon + mDNS: los dos anuncian
  `_matter._tcp` y `_meshcop._udp` (border routers Thread de la misma red
  Thread de Amazon, `vn=amazon mn=echo`, versiones Thread 1.3.0 y 1.1.1) y
  Spotify Connect; uno se presenta como `Android.local`, el otro como
  `linux.local`. Ninguno responde SSDP. Puertos TCP: 55442 (HTTP, 404 a
  todo) y 55443 (TLS 1.2 con certificado autofirmado `O=WHALEXA`, exige
  certificado de cliente) en ambos; el «linux» suma 1080 (SOCKS5 que acepta
  el saludo sin auth pero NO relaya a destinos de la LAN: dos pruebas, time
  out) y 8888 (abre, no contesta HTTP). El router Wi-Fi respeta RD=0 (nombre
  nunca resuelto → solo NS de `com.` en caché): es instrumento válido. En 6
  rondas de 45 s su caché tenía siempre los dominios del Echo: avs/bob-
  dispatch/alexa gateway (voz), device-metrics-us y -us-2 (métricas), unagi,
  arcus, dcape, msh, det-ta-g7g, device-messaging, dp-gw, dp-discovery, api,
  pitangui, softwareupdates, ntp-g7g, cognito, cloudfront. El router de cable
  tiene los mismos más `kindle-time` y `fireoscaptiveportal`: o hay un
  aparato Fire OS en esa red que no responde ping, o reenvía al otro —
  pruebas contradictorias, queda abierto. Captura pasiva de 150 s de lo que
  los Echo gritan en broadcast/multicast: en la nota de relevo. Lo medido
  (JSON de barridos, mDNS, snoop, captura) y los scripts quedaron en la
  carpeta de notas compartidas, `alexa-echo/`.
- 2026-10-19: **frente 2 lanzado**: workflow `alexa-echo-factibilidad`
  (6 lectores sonnet + 6 verificadores adversariales sonnet + crítico), run
  `wf_aeeaf549-128`, corriendo al cierre; su journal queda en
  `~/.claude/projects/-Users-yonatan-Developer-audited-vault/bc7304ec-6f98-437e-ac8a-92de59bcb49a/subagents/workflows/wf_aeeaf549-128/journal.jsonl`.
  REA clonado solo para leer sus docs; el APK de la app Alexa no se bajó de
  ningún mirror: sale del teléfono de Yonatan por `adb pull` o no sale.
  **Terminó a las 19:40**: 13/13 agentes, 0 errores, 2,37 M tokens, 30 min;
  resultado y journal copiados a la carpeta de notas (`alexa-echo/out/`).
  Sin leer a fondo todavía (corte): la sesión fresca lo cruza con lo medido.
- 2026-10-19: **corte a 200k** (hook: contexto=202k, umbral 200k). La
  sesión cierra acá por la regla de `/casa`. Falta, para la sesión fresca:
  (a) leer el journal del workflow y escribir el documento de factibilidad
  (en la carpeta de notas, no en este repo público); (b) resumir el snoop de
  40 rondas (`~/alexa-snoop.log` en el homelab, unit `alexa-snoop-1019`,
  script `snoop-resumen.py`); (c) que Yonatan confirme modelo/generación de
  los dos Echo desde la app (Dispositivos → Echo → Acerca de) y si hay un
  Fire TV u otro Echo en la red de cable; (d) la propuesta del cerebro de
  voz local con GO/no-GO; (e) retirar el snoop y, cuando se retire `tv-dns`,
  avisar a la sesión de Jellyfin para tachar su fila en AUTONOMIA.
- 2026-10-19/20 (sesión fresca, desde el relevo): **informe escrito y
  snoop retirado.** `FACTIBILIDAD.md` quedó en la carpeta de notas
  compartidas (`alexa-echo/`, fuera de este repo), con el borrador de la
  ronda 1 y los dos journals en `out/`. Ronda 1 leída entera (84 hallazgos
  con veredicto); ronda 2 lanzada y cerrada (`wf_1b1d8947-b3a`: 4 frentes
  —identificar modelos por huellas, cifras de la skill, control local sin
  nube, satélite y CPU—, 56 hallazgos, 50 confirmados, 9 agentes sonnet,
  1,58 M tokens, 31 min); el crítico dejó lo que sigue sin respaldo y no
  habrá ronda 3. Snoop de 40 rondas resumido: ~13 dominios de Amazon con
  TTL 60 s se re-resuelven más o menos cada minuto entre los dos Echo, la
  ruta de voz siempre en caché, OTA y hora cada ~5 min; bytes/día sin
  dato. Corrección: el barrido SSDP del segundo Echo no es «cada 3 s»
  continuo sino ráfagas de descubrimiento (SSDP `ssdp:all` +
  `upnp:rootdevice` por tamaño, más inventario mDNS). Los cachés de los dos
  routers son independientes (probado en los dos sentidos): en la red de
  cable hay un aparato Alexa/Fire OS que no responde ping, sin identificar.
  Yonatan (19:50, vía la sesión madre): «hay un echo studio y un echo»; con
  la lista de border routers Thread de Amazon (1.1 = solo Echo 4ª gen; 1.3
  incluye «Echo Studio (1st Gen and newer, 2025 release)») el mapeo más
  consistente es Echo 4ª gen + Echo Studio 1ª gen (Fire OS); lo cierra la
  versión de software en la app. **Conclusión: para los dos no hay camino
  público de apertura** (bootloader bloqueado, exploit de la familia
  «parcheado hacia 2022» según su autor; ausencia de evidencia, no prueba),
  como con el Samsung. Lo local hoy: Matter/Thread (el Echo es controlador)
  y un puente Matter desde Home Assistant (fork vivo); `emulated_hue` queda
  disputado. Propuesta para GO/no-GO: HA Container + Wyoming (whisper
  base-int8, piper es_MX, openWakeWord, Speech-to-Phrase) en el homelab
  (medido: 4 hilos sin GPU, ≈4,4 GB disponibles, puertos 80/8123 libres,
  sin Bluetooth) con satélite propio (USD 29,90–69, envío a Colombia sin
  dato) y dos experimentos de 10 min (bridge Hue emulado; puente Matter);
  skill privada en development (120 KB, ≈8 s, cuenta gratis, 443 + CA
  pública). Retirados del homelab los scripts y el log del snoop; `tv-dns`
  sigue arriba (sin GO). Preguntas abiertas y la de GO: §8 del informe.
  Nota de método: la sesión pasó el umbral de 200k (398k al cierre) por
  esperar y leer los dos workflows; el detalle largo quedó en la carpeta de
  notas y no acá. Falta: la decisión de Yonatan.
- 2026-10-20 (sesión hija, con el GO de arrancar la tarjeta): **stack de
  voz local arriba en el homelab y experimento A listo, esperando a
  Yonatan.** Cuatro contenedores con techo de RAM y datos en una carpeta
  propia fuera de producción: Home Assistant Container (red de host, 8123
  solo en las dos LAN), whisper `base-int8` (4 hilos, beam 1), piper
  `es_MX-ald-medium`, openWakeWord; Speech-to-Phrase declarado pero no
  levantado (necesita un token de HA que solo existe tras el asistente
  inicial). Medido con el stack en reposo: HA 315 MiB, whisper 718 MiB
  (la guía decía ~400), piper 187 MiB, openWakeWord 20 MiB de RAM real
  (anon del cgroup); la caja pasó de 4,36 a 3,30 GB disponibles. Latencia
  STT en esta CPU (3 clips en español de 1,8–3,5 s sintetizados con piper,
  3 rondas): **base-int8 2,2–2,9 s** por comando tras calentar (3,7 s en
  frío); **small-int8 4,5–6,3 s** en un contenedor temporal ya retirado;
  la exactitud sobre audio sintético fue pobre en los dos (aciertan una de
  tres), así que para órdenes queda Speech-to-Phrase como decía el informe
  y falta repetir con micrófono real. Piper: 0,4–0,5 s por frase tras la
  primera (9,8 s, carga la voz). Experimento A: `emulated_hue` en el
  puerto 80 de la Wi-Fi con una sola entidad expuesta («luz de prueba»);
  autoprueba desde el homelab OK (descripción del bridge, usuario, lista,
  y el PUT llegó al `input_boolean` en 11 ms, registrado por una
  automatización en el log); HA ya responde M-SEARCH de otros aparatos de
  la casa; ningún paquete de los Echo todavía. Captura pasiva corriendo en
  la Wi-Fi (SSDP + HTTP de los dos Echo, se apaga sola a las 8 h).
  **Falta de Yonatan**: descubrir el bridge desde la app Alexa (Philips
  Hue V1 round; si no sale, reiniciar el Studio y apagar el otro Echo
  durante el descubrimiento), decir «Alexa, enciende la luz de prueba», y
  hacer el asistente inicial de HA (su usuario) para seguir con
  Speech-to-Phrase, el TV y Jellyfin. Experimento B no arrancado: pide
  IPv6 en Docker (reinicia el daemon y con él todos los contenedores) y
  solo va con GO explícito. Nada tocó los Echo ni el router. Detalle con
  identificadores, compose, configuración, cliente Wyoming y cintas crudas
  en la carpeta de notas compartidas de la sesión hija (`voz-local/`).
  Push aparcado.
- 2026-10-20 (corrección, misma sesión): HA reinició solo su proceso a los
  5 min de arrancar: la versión actual migra el bloque `http:` del YAML a
  su almacén una sola vez y lo trata como config «pendiente»; si nadie la
  promueve desde la interfaz (usuario autenticado) en 5 minutos, vuelve a
  la estable y reinicia. Resultado: **el 8123 quedó en todas las
  interfaces, tailscale incluido**, no «solo en las dos LAN» como dice la
  entrada anterior; el 80 del bridge sigue solo en la Wi-Fi. Sin OOM ni
  más reinicios; el bridge y la entidad de prueba sobrevivieron. Intenté
  dejar el YAML comentado con la explicación y el clasificador de la sesión
  lo negó (abre HA hacia afuera): queda como decisión de Yonatan, dejarlo
  así (HA tiene su autenticación) o restringirlo desde la UI una vez
  dentro, promoviéndolo en la ventana de 5 min. Conviene hacer el
  asistente inicial pronto: hasta entonces la página de alta es alcanzable
  desde cualquier aparato de su tailnet.
