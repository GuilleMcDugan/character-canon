# Caso de estudio — diagnóstico de una deriva de identidad

Documento de la skill `character-canon`.
Caso real: producción de un cortometraje de ficción.

---

## El síntoma

En el tráiler hay varios personajes recurrentes. Casi todos se replicaron plano
a plano con consistencia. Uno, Daniel, no.

La descripción exacta del fallo, en palabras del director: *"Era Daniel en todos
los planos — reconocible, a veces más expresivo que nunca — pero nunca el mismo
Daniel. Algo cambiaba ligeramente cada vez."*

No era un fallo de calidad. Cada plano de Daniel era bueno. Era un fallo de
**consistencia de identidad**: el rostro pasaba el listón de "esto es Daniel"
pero no el de "esto es exactamente el mismo Daniel que el plano anterior".

Iterar los planos no lo resolvía. El proceso se hacía lento y la deriva
persistía.

---

## El diagnóstico

Al revisar todo el material del personaje —no solo los planos del tráiler, sino
el historial completo de generaciones— el origen quedó claro. No estaba en el
tráiler. Estaba antes.

### Causa raíz: un linaje de canones, no un canon

Daniel no tenía UNA imagen base. Tenía una cadena de ellas:

1. **v0 / v4** — primeras generaciones. Cara más ancha, redonda, juvenil.
2. **v5** — usada como base durante meses. Más enjuta, ojos más juntos. "Para
   mí era Daniel", pero se veía claramente IA, no foto.
3. **Canon Humano** — para el tráiler se reescribió el JSON y se pasó a un modelo
   de imagen el JSON nuevo + la imagen v5, pidiendo un Daniel "hiperrealista
   humano". Salió otra cara: emparentada, pero distinta.
4. **La ficha visual** se intentó tres veces porque "se salía del tiesto".
5. **Los planos del tráiler** acabaron de definir otra variante más.

Puestas en fila, las imágenes "canon" de Daniel (v0, v4, v5, Canon Humano) **no
son la misma persona**. Son cuatro hombres parecidos. Un árbol de primos.

Cuando se produjeron los planos del tráiler, el modelo se apoyaba en esa
herencia inestable. El resultado: cada plano se anclaba en un punto distinto
del linaje. "Daniel nunca era el mismo" — literalmente, porque nunca hubo *un*
Daniel que replicar.

### Causa agravante: un rostro estadísticamente genérico

Comparado con la protagonista femenina —pelirroja, pecas densas, ojos verde-ámbar: tres rasgos
infrecuentes— Daniel es un hombre joven mediterráneo, pelo oscuro ondulado, ojos
marrones, barba corta. Cada rasgo lo comparten millones de caras del
entrenamiento del modelo. Sin anclas duras, una cara así "deriva hacia la
media" en cada generación.

La ficha original de Daniel, además, describía el rostro con anclas blandas:
"nariz de longitud media", "pómulos suaves medio-bajos", "mandíbula de
definición media". Todo relativo. Nada que el modelo no pudiera promediar.
la protagonista femenina tenía el mismo tipo de descripción facial — pero sus rasgos infrecuentes
compensaban. Daniel no tenía nada que compensara.

### Lo que NO era el problema

Se sospechó del implante neural en la oreja como foco de inestabilidad. El
director confirmó que el implante salió siempre igual y nunca dio problema.
**Lección de método: no asumir la causa, verificarla con quien produjo los
planos.**

---

## El matiz importante: ¿de quién es el problema?

Hay dos niveles de consistencia (ver SKILL.md, paso 0.1). El tráiler de Daniel
falla en *identidad* pero NO en *reconocimiento*: el espectador medio, viendo
el tráiler una vez con música, no detecta nada raro.

¿Quién detecta la deriva? El director. Porque tiene la cara de Daniel memorizada
con una precisión que el público no tiene. Y porque —sin darse cuenta— compara
cada plano del tráiler con los OTROS Daniels del linaje que también tiene en la
cabeza.

Conclusión doble:

- **El tráiler está bien.** La inconsistencia es real pero invisible al público.
  No se publicó nada defectuoso.
- **Para el futuro sí hay que arreglarlo.** No para el espectador — para el
  director. Un director que pelea con la cara de su personaje en cada plano
  trabaja peor y más lento.

---

## La solución

No hay que rehacer el tráiler. Hay que hacer una sola cosa: **cerrar el canon.**

1. **Canon congelado.** De todo el material, el fotograma P25B (Daniel en la
   cabaña, plano del tráiler) se elige como canon oficial. Razones: es el más
   reciente y resuelto, tiene varios "hermanos" coherentes entre los planos del
   tráiler, es el que el público ya ha visto, y es el que el director identificó
   en presente — "este sí es Daniel". Las versiones anteriores (v0, v4, v5, Canon
   Humano) quedan jubiladas.
2. **El canon no se regenera nunca más.** Decisión cerrada.
3. **Anclas endurecidas.** La ficha v0.2 reescribe el bloque `face` con
   proporciones absolutas y añade `hard_anchors`: una lista corta de rasgos no
   negociables, incluido al menos un rasgo distintivo, para compensar lo
   genérico de la cara.
4. **Retrato canon de trabajo** (opcional): extraer de P25B una versión frontal,
   luz neutra, para inyectar como referencia. Con image-to-image desde P25B,
   nunca con prompt nuevo.

La ficha resultante se construyó con esta skill — la prueba de que el
método nace de un problema real y de su solución.

---

## Las lecciones, destiladas

1. El enemigo de la consistencia no es el prompt. Es regenerar el canon.
2. Cada "mejora" del canon crea una persona nueva.
3. Una cara genérica necesita más anclas duras que una cara con rasgos raros.
4. "Medio", "ligeramente", "suave" no son anclas. Son permiso para derivar.
5. La identidad se define UNA vez y se hereda. No se reescribe en cada estado.
6. Distingue reconocimiento de identidad antes de perseguir la perfección.
7. No asumas la causa de un fallo: verifícala con quien hizo el trabajo.
