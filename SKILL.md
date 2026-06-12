---
name: character-canon
description: Construye y mantiene el canon visual y sonoro de un personaje generado con IA —rostro, cuerpo, piel, voz, gramática de cámara y fotorrealismo— para que siga siendo exactamente el mismo y siga pareciendo una persona real a lo largo de decenas de planos. Universal: vale para cine IA, podcast/avatar, UGC o cualquier producción de varios planos. Úsala cuando el usuario diga "crea la ficha de canon de [personaje]", "ficha JSON del personaje", "diseña un personaje consistente", "este personaje cambia de cara entre planos", "se me deriva la cara", "blinda la consistencia de [personaje]", "por qué no es el mismo en cada plano", "mi personaje parece CGI / de plástico / generado por IA", "hazlo fotorrealista", "anclas de realismo", "perfil de cámara del personaje", o pegue material de un personaje y pida congelar, diseñar o diagnosticar su identidad. También en inglés: "build a character canon", "design a consistent character", "my character's face keeps changing", "make it photoreal", "lock character identity across shots", "consistent actor/avatar". NO la uses para diseñar la psicología o el arco dramático de un personaje desde cero (eso es character-builder), ni para fijar el estilo visual global del proyecto (eso es cine-dna): character-canon congela y endurece la identidad VISUAL y SONORA de UN personaje. Es tool-agnóstica (cualquier modelo de imagen/voz) y NO cubre el pipeline de animación posterior (motion, lipsync, montaje).
---

# character-canon

Sistema para construir y mantener el **canon** de un personaje generado con IA:
el conjunto de rasgos —rostro, cuerpo, piel, voz, gramática de cámara— que lo
hacen el mismo personaje, y una persona creíble, en todos los planos de una
producción.

No es una skill para "generar un personaje". Generar uno es fácil. Esta skill
trata dos problemas difíciles a la vez:

1. Que el personaje siga siendo **exactamente el mismo** a lo largo de treinta,
   cincuenta o cien planos (consistencia de identidad).
2. Que **parezca una persona real** y no un render (fotorrealismo).

Es **universal**: el mismo método sirve para un protagonista de cine, un host de
podcast/avatar o un creador UGC. Y es **tool-agnóstica**: describe el método, no
una herramienta. Donde diga "tu modelo de imagen" o "tu TTS", usa el que tengas.

Nace de un caso real: la producción de un cortometraje de ficción, donde cuatro
personajes se replicaron con consistencia y uno de ellos derivaba en cada plano.
El diagnóstico de ese fallo es el origen del método y está en `caso-deriva-identidad.md`.

El objetivo de la ficha no es ser bonita. Es que **un modelo generativo la
obedezca sin margen de interpretación**.

> **Fuera de alcance.** Esta skill diseña y congela un personaje *estático* y
> sus imágenes base. NO cubre el pipeline de animación posterior —fuerza de
> movimiento, lipsync, generación de vídeo, montaje—: eso vive en el pipeline de
> producción de tu proyecto, no aquí.

---

## PASO 0 — Principios. Leer antes de tocar el JSON.

### 0.1 — Los dos niveles de consistencia

No son lo mismo, y confundirlos hace perder horas:

- **Consistencia de reconocimiento.** ¿El espectador identifica que es el mismo
  personaje? Basta con poco: pelo, silueta, edad, vestuario. Quien ve la pieza
  una vez, a ritmo normal, con música, no detecta micro-fallos.
- **Consistencia de identidad.** ¿Es *exactamente* la misma cara, al milímetro,
  plano a plano? Esto es lo difícil. Y es lo que el director nota —porque tiene
  la cara memorizada— aunque el público no.

**Decide qué nivel necesitas antes de iterar.** Un figurante necesita
reconocimiento. Un protagonista que sale en cincuenta planos necesita identidad.
Perseguir la identidad absoluta donde basta el reconocimiento es quemar tiempo.

### 0.2 — La regla de oro: el canon se congela

El mayor enemigo de la consistencia **no es un mal prompt. Es regenerar el canon.**

Cada vez que se "mejora" la imagen base de un personaje generándola de nuevo, no
sale una versión mejor del mismo personaje: sale una persona nueva, emparentada
pero distinta. Diez regeneraciones son diez primos. Al producir los planos, el
modelo navega entre todos esos primos y el personaje "nunca es el mismo".

**Se elige UN fotograma como canon y NO SE REGENERA NUNCA MÁS.** Por mejorable
que parezca un día. El canon es una decisión cerrada. Mejorar el canon es
romper la consistencia.

Esto vale para el rostro y vale para la voz (ver capa de voz, paso 2.6).

### 0.3 — Anclas duras vs. anclas blandas

Un **ancla blanda** es un rasgo relativo que el modelo interpreta distinto cada
vez: "nariz mediana", "pómulos suaves", "mandíbula normal". Cada generación
elige un punto del rango. La cara deriva. Las anclas blandas son, literalmente,
permiso para derivar.

Un **ancla dura** es un rasgo que el modelo no puede promediar:
- Algo infrecuente y concreto: un lunar en posición exacta, una cicatriz, pecas.
- Una proporción absoluta: "tercio inferior del rostro más corto que el medio".
- Una asimetría: "ceja izquierda ligeramente más alta".
- Una referencia visual fija: la imagen canon, inyectada como referencia.

**Cuanto más genérica es la cara, más anclas duras necesita.** Una cara con
rasgos infrecuentes se ancla casi sola. Una cara común hay que clavarla.

### 0.4 — La semilla NO es un ancla

Un mito extendido: fijar la semilla (`seed`) mantiene la cara. Falso. La semilla
fija el punto de partida del ruido, pero en cuanto cambia el prompt —y cambia en
cada plano, porque cambia la acción— la cara se mueve igual. La semilla ayuda
marginalmente; no ancla. El ancla real es la imagen canon más las anclas duras.
No confíes la identidad de tu personaje a un número.

### 0.5 — Identidad y realismo son dos ejes distintos

Un personaje puede ser **consistente** (siempre la misma cara) y aun así parecer
**falso** (piel de plástico, luz perfecta, CGI). Y al revés. Son dos problemas:

- **Identidad** la dan las anclas duras + la imagen canon (Pasos 1–3).
- **Realismo** lo da el Motor de Realismo (Paso 5): las micro-imperfecciones que
  separan una fotografía de un render.

Ancla las dos. Una cara consistente pero de plástico sigue delatando la IA.

---

## PASO 1 — Fijar el canon visual

1. **Reúne todo el material existente del personaje.** Generaciones, pruebas,
   fotogramas. En fila.
2. **Detecta el linaje.** Es muy probable que las "versiones" del personaje sean
   personas distintas emparentadas. Identifícalas. Solo una será el canon.
3. **Elige UN fotograma canon.** Criterios, en orden:
   - El que mejor captura quién es el personaje (lo decide el director).
   - El más reciente y resuelto técnicamente.
   - Preferible: uno con "hermanos" coherentes (varios planos donde esa cara ya
     funcione) — eso es un set de identidad medio hecho.
4. **Congélalo.** A partir de aquí es intocable.
5. **Extrae un retrato canon de trabajo** (recomendado): el fotograma canon
   suele ser un plano de escena (3/4, luz dura). Para usarlo como referencia
   conviene una versión neutra —misma cara exacta, de frente, luz pareja, fondo
   plano— hecha con image-to-image DESDE el canon, nunca con un prompt nuevo.
   Vara de medir: "¿es el mismo?", nunca "¿me gusta más?".

> Si el personaje aún NO existe (lo estás diseñando desde cero), genera primero
> un set de candidatos, elige uno, y a partir de ahí trátalo como canon: congela
> y no regeneres. El método es el mismo desde el momento en que hay un fotograma.

---

## PASO 2 — Construir la ficha por capas

Usa `plantilla-personaje.json`. Claves en inglés (los modelos responden mejor);
valores descriptivos en el idioma de trabajo.

### 2.1 — `meta`
Identificación. Incluye los dos campos críticos: `canon_image` (el fotograma
congelado del Paso 1) y `core_rule` (la regla del personaje en una frase).
Incluye `context_profile`: `cinema` | `podcast` | `ugc` (ver Paso 6).

### 2.2 — `dramatic_function`
Qué papel cumple el personaje, su eje emocional, y `do_not_frame_as`: lo que el
personaje NO es (estereotipos a evitar).

### 2.3 — `identity_lock` — LO QUE NUNCA CAMBIA
El corazón. `face`, `eyes`, `skin`, `hair`, `facial_hair`, `body`, `hands`.
Cada subcampo, un ancla dura siempre que se pueda (ver Paso 3). Incluye
`constant_items`: lo que aparece siempre (un anillo, una cicatriz, un objeto).

### 2.4 — `hard_anchors` — las 4-7 anclas no negociables
La lista corta que se repite en CADA prompt. En caras genéricas, el salvavidas.
Incluye al menos un rasgo distintivo concreto. Nómbralas SIEMPRE en el mismo
orden entre planos (de más rara a menos), y con descriptores anatómicos, no
estéticos ("lunar sobre la ceja izquierda", no "guapa").

### 2.5 — `camera_grammar` — la capa de cámara (central, esto es cine)
No es decoración: la cámara es parte de la identidad del personaje.
- `lens`: focal y diafragma fijos del personaje (ej. 85mm f/1.8).
- `film_profile`: respuesta de película / sensor, grano, grado de color.
- `lighting_grammar`: esquema de luz comprometido — de dónde viene la luz clave.
- `eyeline`: hacia dónde mira en plano/contraplano.
- `framing`: formato (ej. 9:16, 2.39:1).
Hereda el estilo de la biblia visual del proyecto si existe, y se ajusta al
`context_profile` (Paso 6).

### 2.6 — `voice_lock` — la voz también es canon
La voz deriva como la cara. Se bloquea igual.
- `platform` y `voice_id`.
- `voice_id_locked: true` — y nota: no se cambia sin autorización explícita.
- Parámetros (stability, similarity, style).
- Convención de nombrado de archivos de audio.
Capa contenida: cuatro campos. La voz es parte del canon, no un tratado.

### 2.7 — `states` — LO QUE VARÍA POR ESCENA
Cada estado es el personaje en un momento (cansado, herido). Lleva
`physical_markers`, `emotional_markers`, `wardrobe`, `positive_prompt`. La
identidad NO se redefine aquí: se hereda de `identity_lock`.

### 2.8 — `wardrobe`
Vestuario por bloque. Separado de la identidad: la ropa cambia, la cara no.

### 2.9 — `realism_anchors`, `continuity_lock_phrase` y `global_negative_prompt`
La selección de anclas del Motor de Realismo para este personaje (Paso 5); una
frase fija que abre todos los prompts resumiendo la identidad; y la lista de lo
que el personaje NUNCA debe ser (errores recurrentes del modelo).

### 2.10 — `plane_state_map` y `prompt_usage_notes`
Qué estado usa cada plano; cómo se montan los prompts; modos de fallo conocidos.

---

## PASO 3 — Endurecer las anclas (el paso que casi todos saltan)

Revisa cada rasgo de `identity_lock`. Pregunta: **"¿el modelo puede interpretar
esto de varias maneras?"** Si sí, es blanda. Endurécela.

| Ancla blanda (mal) | Ancla dura (bien) |
|---|---|
| nariz de longitud media | puente recto, tercio nasal más corto que el frontal, base estrecha |
| pómulos suaves | pómulos medios, poca proyección, transición plana a la mejilla |
| ojos oscuros | marrón muy oscuro #3A2418, almendrados, separación interocular ancha |
| pelo rizado | rizo cerrado 3A-3B, nacimiento bajo, raya indefinida, volumen alto |
| complexión normal | complexión delgada, hombros estrechos, cuello largo |

La diferencia: el ancla dura nombra **proporciones, posiciones y valores
absolutos**. El modelo no tiene margen para promediar.

**Expresión:** lo mismo aplica a la emoción. No uses emociones genéricas
("feliz", "triste"). Usa micro-expresiones concretas: "media sonrisa contenida",
"una ceja ligeramente alzada", "mirada que se va hacia dentro". El director
piensa en gestos, no en adjetivos.

**Caras genéricas:** nombra al menos UN rasgo distintivo —asimetría, lunar,
forma de ceja—. Si no lo tiene, considera añadirlo al canon con coherencia
narrativa. Un rasgo infrecuente ancla más que veinte adjetivos.

---

## PASO 4 — Preparar la ficha para el pipeline

La imagen base no se genera solo para ser imagen: se genera para lo que viene
después (vídeo, lipsync). Tener en cuenta:

- **Boca cerrada en las imágenes base.** Si el personaje va a tener lipsync, las
  imágenes base se generan con la boca cerrada ("labios juntos, boca cerrada").
  Una boca abierta en la base genera artefactos al sincronizar audio después.
- **Manos lejos de la cara.** Las manos sobre el rostro son punto de fallo del
  modelo y rompen el lipsync. Mantenlas fuera del óvalo facial en las bases.
- **Expresión neutra-base disponible.** Conviene tener el canon también en
  expresión neutra, no solo en una emoción concreta — es el punto de partida
  más versátil para derivar estados.
- **Coherencia de luz entre planos contiguos.** Si dos planos van seguidos en el
  montaje, la dirección de la luz clave se mantiene salvo corte explícito.

---

## PASO 5 — Motor de Realismo: las 10 anclas de fotorrealismo

La consistencia hace que sea el mismo. El realismo hace que sea *alguien*. Sin
estas anclas, una cara consistente sigue pareciendo un render: piel de porcelana,
luz perfecta, cero ruido = CGI inmediato. Cada ancla nombra una micro-imperfección
que el ojo lee como "fotografía real".

**Regla:** cada prompt de imagen incluye **mínimo 6** anclas. En registro
hiperrealista de primer plano (UGC, selfie), las **10**. Guarda la selección
elegida en `realism_anchors` y repítela entre planos.

| # | Ancla | Fragmento de prompt (ejemplo, EN) | Anti-patrón a evitar |
|---|---|---|---|
| 01 | **skin_pores** | visible skin pores on nose and cheeks, open pores near T-zone, natural skin texture with microscopic irregularities | smooth porcelain skin, airbrushed complexion |
| 02 | **stray_hairs** | two or three stray baby hairs near temples, flyaway strands catching light, slightly imperfect hairline | perfect hair, every strand in place, salon-ready |
| 03 | **under_eye_texture** | subtle under-eye texture, faint blue-purple undertones, light tear-trough shadow, natural orbital fat visibility | no under-eye circles, concealed perfectly |
| 04 | **uneven_skin_tone** | slightly uneven skin tone, subtle redness around nostrils, faint hyperpigmentation, natural color variation | perfectly even skin tone, one uniform color |
| 05 | **fabric_texture** | fabric weave visible, slight wrinkles at elbows and collar, natural drape with micro-wrinkles, thread count visible | perfectly smooth, plastic-looking fabric |
| 06 | **environmental_noise** | natural depth-of-field fall-off, environmental imperfections (slight dust motes, soft bokeh variation) | perfectly clean background, studio void |
| 07 | **lighting_imperfection** | natural light wrap, slight hot spot on forehead, soft fall-off on one side, non-uniform illumination | perfectly even lighting, studio-perfect |
| 08 | **camera_artifacts** | subtle lens distortion at frame edges, faint chromatic aberration on high-contrast edges, natural sensor noise | perfect lens, clinical sharpness, no noise |
| 09 | **nail_detail** | natural nail beds, subtle cuticle detail, slight nail ridging, real color variation (not perfect manicure) | flawless manicure, plastic-looking nails |
| 10 | **jewelry_physics** | jewelry obeys gravity (necklace drape, earring hang), slight tarnish/wear, realistic chain-link shadows | perfectly polished, floating, rigid metal |

**Prioridad de selección por contexto** (cuando uses solo 6):
- **Cinema:** uneven_skin_tone, lighting_imperfection, camera_artifacts, fabric_texture, environmental_noise, stray_hairs.
- **Podcast/avatar:** skin_pores, under_eye_texture, uneven_skin_tone, fabric_texture, lighting_imperfection, camera_artifacts.
- **UGC:** las 10 (registro de máxima cercanía y máxima exigencia de realismo).

Las manos (`nail_detail`) y la joyería (`jewelry_physics`) son los puntos de
fallo más comunes del modelo: priorízalas en cualquier plano donde aparezcan.

---

## PASO 6 — Perfiles de contexto (cine / podcast / UGC)

Un personaje no cambia de cara entre contextos, pero **sí cambia de cámara, luz
y entorno**. El `context_profile` ajusta `camera_grammar` sin tocar la identidad.

- **`cinema`** — óptica de cine (anamórfico, 85mm f/1.8, ARRI/Sony cine), luz
  comprometida y direccional, entorno de set, encuadre 2.39:1 o 9:16 cinematográfico.
- **`podcast`** — mirrorless o cámara fija (Sony A7IV 85mm f/1.8 típico), luz de
  set controlada pero natural, entorno de estudio/sala, mirada a cámara o a
  interlocutor, encuadre busto.
- **`ugc`** — cámara de teléfono, óptica con ligera distorsión de barril,
  encuadre selfie vertical, luz natural de ventana, entorno doméstico real. La
  "imperfección" es parte del lenguaje: el realismo aquí se exige al máximo.

Perfiles de cámara de teléfono útiles para `ugc` (ejemplos, model-agnósticos):
- **Selfie frontal** — front cam, ~23mm equiv. f/1.9, ligera distorsión de barril,
  brazo parcialmente visible, cara ~65% del alto, luz de ventana, bokeh suave de borde.
- **Cámara trasera** — ~24mm f/1.78, detalle nítido, perspectiva natural, ligero
  viñeteo, sujeto a distancia de brazo. Producto / tercera persona.
- **Espejo** — teléfono visible en el reflejo, espejo de baño/dormitorio con leve
  smudge y hotspot, cuerpo de cabeza a medio muslo. Outfit / GRWM.

> El estilo visual GLOBAL del proyecto (paleta, grano, look de toda la pieza)
> NO se define aquí: eso es `cine-dna`. Aquí solo entra la gramática de cámara
> que pertenece a ESTE personaje en ESTE contexto.

---

## PASO 7 — Sistema de 6 capas para el prompt de imagen

Estructura modular para construir prompts consistentes a lo largo de múltiples
planos con **cualquier** modelo de imagen. Cada capa suma información sin
contradicción. El orden importa. Nunca omitas las capas 1 y 6.

**Capa 1 — Persona (identity_lock).** La base inmóvil, siempre primero.
`continuity_lock_phrase` + `hard_anchors` en su orden fijo.
> `Xavier, 34, [etnia/origen], lunar sobre ceja izquierda, tres lunares lado izq. cuello, pecas en puente nasal`

**Capa 2 — Emoción/Estado (micro-expresión).** Gestos concretos, no adjetivos.
Subvocales ("dándose cuenta", "confesando"), no "sonriendo/feliz". Eyeline si hay diálogo.
> `media sonrisa contenida, mirada que no alcanza los ojos, mano derecha gesticulando fuera del óvalo facial`

**Capa 3 — Acción/Entorno.** Qué hace, dónde, con qué luz ambiente.
> `sentado en escritorio, salón al fondo desenfocado, luz dorada de tarde desde ventana cámara-izquierda`

**Capa 4 — Cámara (camera_grammar + context_profile).** Dispositivo, óptica, encuadre.
Repetir idéntica en planos del mismo bloque.
> `Sony A7IV 85mm f/1.8, key suave cámara-izquierda, Rec.709` · o · `selfie front cam ~23mm f/1.9, distorsión de barril`

**Capa 5 — Inyección de realismo (Motor de Realismo, Paso 5).** Mínimo 6 anclas,
10 en UGC. La misma selección entre planos.

**Capa 6 — Negativo.** `global_negative_prompt` + negativo del estado. Universales:
`CGI, 3D render, illustration, airbrushed skin, plastic skin, perfect symmetry,
studio backdrop, ring-light halo in eyes, HDR overprocessing, watermark`.
Si hay lipsync, negativos de boca: `open mouth, speaking, hand near mouth/chin`.

> **Capa 6 ≠ estilo de proyecto.** El look global (paleta, grano de toda la pieza)
> es `cine-dna`, no esta capa.

**Flujo:** Capa 1 + 2 + 3 + 4 + 5 + 6. Y, si el modelo lo permite, **inyectar la
imagen canon como referencia visual**: el texto ancla, la imagen ancla más.

---

## PASO 8 — Protocolo multi-imagen consistente

Cómo mantener consistencia al producir varias imágenes del mismo personaje en la
misma sesión. (La animación posterior —vídeo, lipsync— queda fuera de esta skill.)

**1. Pre-producción**
- [ ] Ficha JSON lista: `identity_lock`, `hard_anchors`, `camera_grammar`, `realism_anchors`.
- [ ] Canon visual congelado (no regenerar).
- [ ] `voice_id` bloqueado si el personaje habla.
- [ ] Tabla de planos: qué estado y qué acción usa cada uno.

**2. Retrato canon de trabajo (UNA vez)**
- Genera el retrato canon en expresión neutra, frente, luz pareja.
- Guárdalo. No lo regeneres aunque parezca mejorable.
- Úsalo como referencia visual en CADA prompt de imagen.

**3. Por cada plano**
- Construye el prompt con las 6 capas (Paso 7); luz IDÉNTICA dentro del mismo bloque.
- Inyecta la imagen canon como referencia.
- **Validación rápida** antes de pasar al siguiente:
  - ¿Es el mismo personaje? (sí/no)
  - ¿Luz coherente con el plano anterior del bloque? (sí/no)
  - ¿Realismo presente (piel, luz, ruido) o parece render? (sí/no)
  - ¿Expresión marcada pero coherente? (sí/no)

**4. Si un plano deriva**
- Localiza el plano problemático. NO regeneres el canon.
- Refuerza la(s) ancla(s) que falló: descriptor más específico en Capa 1, y
  repítela también en Capa 5 como refuerzo.
- Vuelve a inyectar la imagen canon como referencia.

**5. Documentación**
- Guarda la tabla de planos con la selección de anclas y los ajustes usados.
- Notas: "Plano 7 necesitó ancla extra: [detalle]". Útil si extiendes la producción.

---

## PASO 9 — Validar antes de producir

- [ ] Hay un canon congelado y no se va a regenerar.
- [ ] `hard_anchors` tiene 4-7 entradas, todas duras, en orden fijo.
- [ ] `face` no contiene adjetivos relativos sin cuantificar.
- [ ] `identity_lock` y `states` no se contradicen.
- [ ] `camera_grammar` define lente, luz y formato, acorde al `context_profile`.
- [ ] `realism_anchors` tiene ≥6 anclas seleccionadas (10 si es UGC).
- [ ] `voice_lock` tiene el Voice_ID bloqueado, si el personaje habla.
- [ ] `global_negative_prompt` recoge los errores típicos del personaje + anti-CGI.
- [ ] Si la cara es genérica, hay al menos un rasgo distintivo nombrado.
- [ ] Las imágenes base previstas tienen la boca cerrada y manos fuera de la cara (si habrá lipsync).

`python3 validate.py mi-personaje.json` comprueba buena parte de esto sin ojo humano.

---

## PASO 10 — Flujo de prompt recomendado (resumen)

Para cada plano, en orden:

1. `continuity_lock_phrase` — abre anclando identidad.
2. `hard_anchors` — las 4-7, siempre, en el mismo orden.
3. `positive_prompt` del estado (según `plane_state_map`) — micro-expresión concreta.
4. Acción y entorno del plano.
5. `camera_grammar` — lente, luz, formato (según `context_profile`).
6. Inyección de realismo — las anclas de `realism_anchors` (≥6 / 10 en UGC).
7. `global_negative_prompt` + negativo del estado (+ negativos de boca si lipsync).
8. Si el modelo lo permite: **inyectar la imagen canon como referencia.**

---

## Archivos de la skill

- `SKILL.md` — este documento.
- `plantilla-personaje.json` — plantilla en blanco.
- `caso-deriva-identidad.md` — el caso real de diagnóstico que originó el método.
- `validate.py` — validador de fichas (comprueba el checklist del Paso 9).
- `evals/` — casos de prueba del comportamiento de la skill.

## Modos de fallo conocidos

- **El linaje de canones.** Regenerar "para mejorar" crea personas nuevas.
  → Congelar un canon, no regenerar.
- **El rostro genérico.** Una cara común deriva hacia la media del modelo.
  → Más anclas duras, al menos un rasgo distintivo.
- **Anclas relativas.** "Medio", "ligeramente", "suave" sin cuantificar.
  → Proporciones y valores absolutos.
- **Identidad redefinida en cada estado.** Repetir la descripción facial con
  otras palabras en cada `state` introduce deriva. → La identidad solo en
  `identity_lock`; los estados solo añaden lo que cambia.
- **Confiar en la semilla.** La semilla no ancla la cara. → Canon + anclas duras.
- **Emociones genéricas.** "Feliz", "triste" se interpretan de mil formas.
  → Micro-expresiones concretas.
- **Cara consistente pero de plástico.** Identidad clavada, pero parece CGI.
  → Motor de Realismo: mínimo 6 anclas, 10 en primer plano.
- **Piel de porcelana / luz perfecta.** El sello del render. → skin_pores,
  uneven_skin_tone, lighting_imperfection, camera_artifacts.
- **Manos y joyería.** El punto de fallo más visible del modelo. → nail_detail,
  jewelry_physics, manos fuera del óvalo facial.
- **Olvidar el pipeline.** Imágenes base con boca abierta rompen el lipsync.
  → Boca cerrada en las bases.
- **Multi-shot sin referencia visual.** Generar cada plano solo con prompt permite deriva.
  → Inyectar imagen canon como referencia en CADA prompt.
