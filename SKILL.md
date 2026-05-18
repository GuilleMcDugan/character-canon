---
name: character-canon
description: Construye y mantiene el canon visual y sonoro de un personaje de cine generado con IA. Úsala para crear la ficha JSON de un personaje protagónico o recurrente, para diagnosticar por qué un personaje "cambia de cara" entre planos, o para blindar la consistencia de identidad de cara a una producción de varios planos o escenas. Pensada para cine generativo: imagen, vídeo y voz.
---

# character-canon

Sistema para construir y mantener el **canon** de un personaje de cine generado
con IA: el conjunto de rasgos —rostro, cuerpo, voz, gramática de cámara— que lo
hacen el mismo personaje en todos los planos de una producción.

No es una skill para "generar un personaje". Generar uno es fácil. Esta skill
trata el problema difícil: que ese personaje siga siendo **exactamente el mismo**
a lo largo de treinta, cincuenta o cien planos.

Nace de un caso real: la producción de un cortometraje de ficción, donde cuatro
personajes se replicaron con consistencia y uno de ellos derivaba en cada plano.
El diagnóstico de ese fallo es el origen del método y está en `caso-deriva-identidad.md`.

El objetivo de la ficha no es ser bonita. Es que **un modelo generativo la
obedezca sin margen de interpretación**.

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

---

## PASO 2 — Construir la ficha por capas

Usa `plantilla-personaje.json`. Claves en inglés (los modelos responden mejor);
valores descriptivos en el idioma de trabajo.

### 2.1 — `meta`
Identificación. Incluye los dos campos críticos: `canon_image` (el fotograma
congelado del Paso 1) y `core_rule` (la regla del personaje en una frase).

### 2.2 — `dramatic_function`
Qué papel cumple el personaje, su eje emocional, y `do_not_frame_as`: lo que el
personaje NO es (estereotipos a evitar).

### 2.3 — `identity_lock` — LO QUE NUNCA CAMBIA
El corazón. `face`, `eyes`, `skin`, `hair`, `facial_hair`, `body`, `hands`.
Cada subcampo, un ancla dura siempre que se pueda (ver Paso 3). Incluye
`constant_items`: lo que aparece siempre (un anillo, una cicatriz, un objeto).

### 2.4 — `hard_anchors` — las 4-7 anclas no negociables
La lista corta que se repite en CADA prompt. En caras genéricas, el salvavidas.
Incluye al menos un rasgo distintivo concreto.

### 2.5 — `camera_grammar` — la capa de cámara (central, esto es cine)
No es decoración: en cine la cámara es parte de la identidad del personaje.
- `lens`: focal y diafragma fijos del personaje (ej. 85mm f/1.8).
- `film_profile`: respuesta de película / sensor, grano, grado de color.
- `lighting_grammar`: esquema de luz comprometido — de dónde viene la luz clave.
- `eyeline`: hacia dónde mira en plano/contraplano.
- `framing`: formato (ej. 9:16, 2.39:1).
Hereda el estilo de la biblia visual del proyecto si existe.

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

### 2.9 — `continuity_lock_phrase` y `global_negative_prompt`
Una frase fija que abre todos los prompts resumiendo la identidad; y la lista
de lo que el personaje NUNCA debe ser (errores recurrentes del modelo).

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
- **Expresión neutra-base disponible.** Conviene tener el canon también en
  expresión neutra, no solo en una emoción concreta — es el punto de partida
  más versátil para derivar estados.
- **Coherencia de luz entre planos contiguos.** Si dos planos van seguidos en el
  montaje, la dirección de la luz clave se mantiene salvo corte explícito.

---

## PASO 5 — Validar antes de producir

- [ ] Hay un canon congelado y no se va a regenerar.
- [ ] `hard_anchors` tiene 4-7 entradas, todas duras.
- [ ] `face` no contiene adjetivos relativos sin cuantificar.
- [ ] `identity_lock` y `states` no se contradicen.
- [ ] `camera_grammar` define lente, luz y formato.
- [ ] `voice_lock` tiene el Voice_ID bloqueado, si el personaje habla.
- [ ] `global_negative_prompt` recoge los errores típicos del personaje.
- [ ] Si la cara es genérica, hay al menos un rasgo distintivo nombrado.
- [ ] Las imágenes base previstas tienen la boca cerrada (si habrá lipsync).

---

## PASO 6 — Flujo de prompt recomendado

Para cada plano:

1. `continuity_lock_phrase` — abre anclando identidad.
2. `hard_anchors` — las 4-7, siempre.
3. `positive_prompt` del estado (según `plane_state_map`).
4. Acción y entorno del plano. Micro-expresión concreta, no emoción genérica.
5. `camera_grammar` — lente, luz, formato.
6. `global_negative_prompt` + negativo del estado.
7. Estilo visual de la biblia del proyecto.
8. Si el modelo lo permite: **inyectar la imagen canon como referencia.** El
   texto ancla; la imagen ancla más.

---

## Archivos de la skill

- `SKILL.md` — este documento.
- `plantilla-personaje.json` — plantilla en blanco.
- `caso-deriva-identidad.md` — el caso real de diagnóstico que originó el método.

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
- **Olvidar el pipeline.** Imágenes base con boca abierta rompen el lipsync.
  → Boca cerrada en las bases.
