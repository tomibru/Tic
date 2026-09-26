# TIC – Teoría de la Información y la Comunicación

Documentación de los ejercicios en Python organizados por guía. El `.rar` contiene dos carpetas: `Guia2` y `Guia 3`.

---

## 📁 Guia2

Ejercicios sobre fuentes de información, extensiones de alfabeto, entropía y cadenas de Markov.

### `2.py`
Extrae alfabeto y probabilidades de un mensaje, y genera un mensaje simulado nuevo con esas probabilidades.

### `3.py`
**Archivo vacío** (0 bytes).

### `10.py`
Calcula la extensión de orden `n` de una fuente (todas las combinaciones de `n` símbolos y su probabilidad).

### `14.py`
Calcula el vector estacionario de una cadena de Markov y la entropía asociada. ⚠️ El bucle acumula valores con `append` en vez de reemplazarlos, conviene revisarlo.

### `15.py`
A partir de una cadena ingresada por consola, arma la matriz de transición de Markov (inciso A) y genera una nueva cadena simulada a partir de esa matriz (inciso B).

### `cantInfo_Entropia.py`
Debería calcular cantidad de información y entropía de una fuente fija. ⚠️ Tiene un bug: trata la lista de probabilidades como si fuera un diccionario, no corre correctamente.

---

## 📁 Guia 3

Ejercicios sobre codificación de fuente: códigos no singulares, instantáneos, unívocamente decodificables (Sardinas-Patterson), inecuación de Kraft, códigos compactos y generación de mensajes aleatorios.

### `6.py`
Verifica si un código es no singular, instantáneo, y si no lo es, corre Sardinas-Patterson para ver si es unívocamente decodificable.

### `9.py`
Obtiene el alfabeto código y las longitudes de las palabras, y verifica si el código cumple la inecuación de Kraft.

### `11.py`
Define funciones de entropía y longitud media de un código, pero no las llama ni imprime resultados.

### `14.py`
Verifica si un código es unívocamente decodificable y compacto (óptimo según Shannon), y prueba varios códigos de ejemplo.

### `16.py`
Genera un mensaje aleatorio ponderado por probabilidades a partir de un alfabeto fijo.

---

## Resumen rápido

| Carpeta | Archivo | Tema principal |
|---|---|---|
| Guia2 | 2.py | Alfabeto/frecuencias + generación de mensaje simulado |
| Guia2 | 3.py | (vacío) |
| Guia2 | 10.py | Extensión de orden n de una fuente |
| Guia2 | 14.py | Vector estacionario y entropía de cadena de Markov |
| Guia2 | 15.py | Matriz de transición + simulación de cadena de Markov |
| Guia2 | cantInfo_Entropia.py | Cantidad de información y entropía (contiene un bug) |
| Guia 3 | 6.py | No singular / instantáneo / Sardinas-Patterson (UD) |
| Guia 3 | 9.py | Inecuación de Kraft |
| Guia 3 | 11.py | Entropía y longitud media (sin ejecución de ejemplo) |
| Guia 3 | 14.py | Códigos compactos (Shannon) |
| Guia 3 | 16.py | Generación de mensaje aleatorio ponderado |