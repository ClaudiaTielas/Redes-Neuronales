# Redes-Neuronales

Los datos a tratar corresponden a un experimento en ratones relacionado con la predicción de 8 clases a partir de los niveles de expresión de proteínas/modificaciones de proteínas que produjeron señales detectables en la fracción nuclear de la corteza.

Cada clase se basa en el genotipo, comportamiento y tratamiento. Según el genotipo, los ratones pueden ser controles (c) o trisómicos (t). Según el comportamiento, algunos ratones han sido estimulados para aprender (context-shock(CS)) y otros no (shock-context(SC)) y con el fin de evaluar el efecto del fármaco memantina (m) en la recuperación de la capacidad de aprendizaje en algunos ratones se ha inyectado la droga y a otros se ha inyectado suero salino (s) como placebo. Las 8 clases son:

- c-CS-s: control-context-shock-salino
- c-CS-m: control-context-shock-memantina
- c-SC-s: control-shock-context-salino
- c-SC-m: control-shock-context-memantina
- t-CS-s: trisómico-context-shock-salino
- t-CS-m: trisómico-context-shock-memantina
- t-SC-s: trisómico-shock-context-salino
- t-SC-m: trisómico-shock-context-memantina

Los datos para esta actividad se encuentran en dos ficheros. El fichero data3.csv y el fichero clase3.csv. El fichero data3.csv con los niveles de proteínas, tiene 1080 filas (muestras) y 73 columnas. La primera columna es el código de la muestra y el resto de columnas son proteínas. El fichero clase3.csv con los valores de la clase de 1 a 8, tiene 1080 filas (muestras) y una columna con el valor de la clase.

El objetivo planteado es la implementación y evaluación de una red neuronal basada en capas densas (fc) para la clasificación de las 8 clases.
