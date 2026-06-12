# character-canon

**v1.2**

Sistema para construir y mantener el **canon** de un personaje generado con IA —
el conjunto de rasgos (rostro, cuerpo, piel, voz, gramática de cámara) que lo
hacen el mismo personaje, y una persona creíble, en todos los planos de una
producción.

Resuelve dos problemas difíciles a la vez: que el personaje siga siendo
**exactamente el mismo** plano tras plano (identidad), y que **parezca real** y
no un render (fotorrealismo, vía el Motor de Realismo).

Es **universal** (cine IA, podcast/avatar, UGC) y **tool-agnóstica** (cualquier
modelo de imagen o de voz). NO cubre el pipeline de animación posterior
(fuerza de movimiento, lipsync, generación de vídeo, montaje).

## Contenido

- `SKILL.md` — el método completo, en 10 pasos (incluye Motor de Realismo y perfiles de contexto).
- `plantilla-personaje.json` — plantilla en blanco para un personaje nuevo.
- `caso-deriva-identidad.md` — el caso real de diagnóstico que originó el método.
- `validate.py` — validador de fichas: comprueba el checklist del Paso 9 sin ojo humano.
- `evals/` — casos de prueba del comportamiento de la skill.

## Instalación en Claude Code

Copia la carpeta a tu directorio de skills:

```
~/.claude/skills/character-canon/
```

Claude Code la detecta por el frontmatter de `SKILL.md` y la activa cuando
pidas crear, revisar o reparar la ficha de un personaje de cine. Frases que la
disparan:

- «crea la ficha de canon de [personaje]» / «build a character canon»
- «este personaje cambia de cara entre planos» / «my character's face keeps changing»
- «blinda la consistencia de [personaje]» / «lock character identity across shots»

## Cuándo NO usarla

- **Diseñar la psicología o el arco de un personaje desde cero** → es otra tarea
  (en nuestro estudio, la skill `character-builder`). character-canon parte de un
  personaje que YA existe visualmente y congela su identidad.
- **Fijar el estilo visual global del proyecto** (look, grano, paleta de toda la
  pieza) → eso es la biblia visual / `cine-dna`. Aquí solo entra la gramática de
  cámara que pertenece a ESE personaje (su lente, su luz).
- **Animar el personaje** (fuerza de movimiento, lipsync, generación de vídeo,
  montaje) → eso es el pipeline de producción de tu proyecto. character-canon
  prepara y congela el personaje estático; no lo mueve.

## Uso rápido

1. Lee `SKILL.md` una vez entero — sobre todo el Paso 0 (los principios).
2. Personaje nuevo: copia `plantilla-personaje.json` y síguela paso a paso.
3. Personaje que "cambia de cara": lee `caso-deriva-identidad.md` — probablemente es tu
   mismo problema.
4. Antes de producir, valida la ficha:

   ```
   python3 validate.py mi-personaje.json
   ```

## La idea en una frase

El enemigo de la consistencia no es un mal prompt: es regenerar el canon.
Congela un fotograma, endurece las anclas, no lo toques más.

---

Construida a partir de una producción real de cine con IA.

**Lemö Labs** — Laboratorio de anomalías creativas · lemolabs.studio
