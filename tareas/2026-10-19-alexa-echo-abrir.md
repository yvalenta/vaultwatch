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
