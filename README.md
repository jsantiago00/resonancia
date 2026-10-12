# Resonancia

Visualizador de música que reacciona al sonido como materia real: una esfera de ferrofluido, una gota de ferrofluido sobre una placa y figuras de Chladni (arena sobre un parlante).

**Abrir la app:** https://santiagososa.com.ar/resonancia/

## Modos

- **⚫ Esfera**: ferrofluido flotando que forma picos con la música y vuelve a ser esfera en silencio.
- **💧 Gota**: ferrofluido visto desde arriba; vibra, suelta gotitas y se vuelve loco con un drop de dubstep.
- **⏹ Arena**: figuras de Chladni que cambian con el tono; en silencio la arena se dispersa.
- **⭕ Anillo**: espectro circular; curva suave en chill, gira al ritmo en bailable, tiembla en agresivo.
- **🌀 Túnel**: viaje por un túnel de luces; la velocidad sigue la energía de la música.
- **✨ Partículas**: miles de partículas con estela; seda lenta, anillo que late o explosiones según el ánimo.
- **🧑‍💻 Mini Santi**: un personajito trabajando que se estresa con el ruido (ideal con el micrófono en la tablet). Con música tranqui se pone los auriculares y mueve la cabeza. El control de sensibilidad ajusta su tolerancia. Se personaliza con el objeto `SANTI` en `index.html`.

En celular y tablet la pantalla se mantiene encendida mientras la app está andando, y se puede instalar en la pantalla de inicio ("Agregar a pantalla de inicio").

## Ánimo de la música

La app detecta si lo que suena es **🔥 agresivo**, **🌙 chill** o **💃 bailable** y cambia el movimiento y los colores:

- Un detector propio (golpes por segundo, bajo relativo y regularidad del ritmo), calibrado con `herramientas/analizar.py`.
- Opcionalmente (botón 🧠) los modelos de [Essentia](https://essentia.upf.edu/) `mood_aggressive`, `mood_relaxed` y `danceability`, que se descargan (~13 MB) la primera vez.

## Fuentes de audio

- 🔊 Audio del PC / pestaña (Chrome/Edge en computadora: al compartir, activar "Compartir audio").
- 🎤 Micrófono (también en celular y tablet).
- 🎵 Un archivo de audio.
- ✨ Demo sin audio.

## Como fondo de pantalla en Windows

Con [Lively Wallpaper](https://www.rocksdanister.com/lively/): arrastrar `index.html` (o la carpeta, que incluye `LivelyInfo.json`) a Lively.

## Atajos

`M` cambiar modo · `F` pantalla completa · `H` ocultar controles

## Licencias de terceros

- essentia.js: AGPL-3.0.
- Modelos de Essentia (Universitat Pompeu Fabra): CC BY-NC-ND 4.0, uso no comercial.
- TensorFlow.js: Apache-2.0.
