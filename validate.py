#!/usr/bin/env python3
"""
validate.py — validador de fichas character-canon.

Comprueba, sin ojo humano, el checklist del Paso 5 de SKILL.md sobre una ficha
rellenada a partir de plantilla-personaje.json.

Uso:
    python3 validate.py mi-personaje.json

Salida: una línea por comprobación (PASS / WARN / FAIL) y un resumen.
Código de salida: 0 si no hay ningún FAIL; 1 si hay al menos un FAIL.

Sin dependencias externas: solo biblioteca estándar.
"""

import json
import re
import sys

# Marcadores de texto que delatan un campo SIN rellenar (heredado de la plantilla).
PLACEHOLDER_MARKERS = (
    "ARCHIVO", "descripción", "descripcion", "ej:", "ej.", "#000000",
    "ancla dura", "elemento que aparece", "estado_1", "bloque_1",
    "lo que el personaje NO es", "estereotipo a evitar", "rango de edad",
    "Nombre completo", "nombre-personaje", "La regla esencial",
    "Frase fija", "Todo lo que el personaje", "modo de fallo conocido",
)

# Anclas blandas: términos relativos que el modelo promedia.
# Se permiten SOLO si en el mismo campo hay un número, hex o proporción concreta.
SOFT_TERMS = re.compile(
    r"\b(medi[ao]s?|ligera(?:mente)?|suaves?|normal(?:es)?|mediana?s?|"
    r"poco|algo|un tanto|moderad[ao]s?)\b",
    re.IGNORECASE,
)
HAS_NUMBER = re.compile(r"(#[0-9a-fA-F]{3,6}|\d|tercio|proporci|asimetr|estrech|ancho|largo|corto)", re.IGNORECASE)

results = []  # (level, message)


def add(level, msg):
    results.append((level, msg))


def is_placeholder(value):
    if value is None:
        return True
    if isinstance(value, (int, float)):
        return value == 0
    if not isinstance(value, str):
        return False
    v = value.strip()
    if not v:
        return True
    return any(m.lower() in v.lower() for m in PLACEHOLDER_MARKERS)


def get(d, *path, default=None):
    cur = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def check(data):
    # 1 — canon congelado declarado
    canon = get(data, "meta", "canon_image")
    if is_placeholder(canon):
        add("FAIL", "meta.canon_image vacío o placeholder — no hay canon congelado.")
    else:
        add("PASS", f"Canon congelado: {canon}")

    # core_rule
    if is_placeholder(get(data, "meta", "core_rule")):
        add("WARN", "meta.core_rule sin rellenar — falta la regla del personaje en una frase.")

    # 2 — hard_anchors 4-7, todas reales
    anchors = get(data, "hard_anchors", "list", default=[])
    real = [a for a in anchors if not is_placeholder(a)]
    if not (4 <= len(real) <= 7):
        add("FAIL", f"hard_anchors.list tiene {len(real)} anclas reales; deben ser 4-7.")
    else:
        add("PASS", f"hard_anchors: {len(real)} anclas duras.")
    if len(real) < len(anchors):
        add("WARN", f"hard_anchors contiene {len(anchors) - len(real)} entradas sin rellenar.")

    # 3 — face sin adjetivos relativos sin cuantificar
    face = get(data, "identity_lock", "face", default={})
    soft_hits = []
    if isinstance(face, dict):
        for k, v in face.items():
            if isinstance(v, str) and SOFT_TERMS.search(v) and not HAS_NUMBER.search(v):
                soft_hits.append(f"face.{k}: \"{v}\"")
    if soft_hits:
        add("FAIL", "Anclas BLANDAS en face (relativo sin cuantificar): " + "; ".join(soft_hits))
    else:
        add("PASS", "face sin adjetivos relativos sin cuantificar.")

    # rasgo distintivo (crítico en caras genéricas)
    marks = get(data, "identity_lock", "face", "distinctive_marks")
    if is_placeholder(marks):
        add("WARN", "face.distinctive_marks vacío — una cara genérica deriva sin al menos un rasgo distintivo.")

    # 4 — identity_lock y states no se contradicen (heurística)
    states = get(data, "states", default={})
    FACE_WORDS = re.compile(r"\b(nariz|pómulos|pomulos|mandíbula|mandibula|rostro|cara|forma de la cara|facial features|face shape)\b", re.IGNORECASE)
    redef = []
    if isinstance(states, dict):
        for sid, st in states.items():
            if sid.startswith("_"):
                continue
            pp = st.get("positive_prompt", "") if isinstance(st, dict) else ""
            if isinstance(pp, str) and FACE_WORDS.search(pp):
                redef.append(sid)
    if redef:
        add("WARN", f"states redefinen la cara en positive_prompt ({', '.join(redef)}) — la identidad solo en identity_lock.")
    else:
        add("PASS", "Ningún state redefine la cara.")

    # 5 — camera_grammar: lente, luz, formato
    cam = get(data, "camera_grammar", default={})
    missing = [f for f in ("lens", "lighting_grammar", "framing")
               if is_placeholder(cam.get(f) if isinstance(cam, dict) else None)]
    if missing:
        add("FAIL", f"camera_grammar incompleta: falta {', '.join(missing)}.")
    else:
        add("PASS", "camera_grammar define lente, luz y formato.")

    # 6 — voice_lock bloqueado si el personaje habla
    voice = get(data, "voice_lock", default={})
    if isinstance(voice, dict) and not is_placeholder(voice.get("voice_id")):
        if voice.get("voice_id_locked") is not True:
            add("FAIL", "voice_lock tiene voice_id pero voice_id_locked no es true.")
        else:
            add("PASS", "voice_lock con Voice_ID bloqueado.")
    else:
        add("WARN", "voice_lock sin voice_id — OK si el personaje no habla.")

    # 7 — global_negative_prompt con contenido
    if is_placeholder(get(data, "global_negative_prompt")):
        add("WARN", "global_negative_prompt vacío — sin errores recurrentes del modelo recogidos.")
    else:
        add("PASS", "global_negative_prompt rellenado.")

    # continuity_lock_phrase recomienda cerrar anclando al canon
    clp = get(data, "continuity_lock_phrase", default="")
    if is_placeholder(clp):
        add("WARN", "continuity_lock_phrase vacía.")
    elif "match the canon" not in clp.lower():
        add("WARN", "continuity_lock_phrase no termina anclando al canon ('match the canon image exactly').")


def main():
    if len(sys.argv) != 2:
        print("uso: python3 validate.py <ficha.json>", file=sys.stderr)
        return 2
    try:
        with open(sys.argv[1], encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        print(f"No existe el archivo: {sys.argv[1]}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"JSON inválido: {e}", file=sys.stderr)
        return 2

    check(data)

    icon = {"PASS": "✓", "WARN": "▲", "FAIL": "✗"}
    for level, msg in results:
        print(f"  {icon[level]} [{level}] {msg}")

    fails = sum(1 for lvl, _ in results if lvl == "FAIL")
    warns = sum(1 for lvl, _ in results if lvl == "WARN")
    print(f"\n  {'—' * 40}")
    if fails:
        print(f"  FICHA NO VÁLIDA — {fails} fallo(s), {warns} aviso(s).")
        return 1
    print(f"  Ficha válida — 0 fallos, {warns} aviso(s) a revisar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
