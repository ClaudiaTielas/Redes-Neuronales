# -*- coding: utf-8 -*-
"""RedesNeuronales.ipynb

# IMPLEMENTACIÓN Y EVALUACIÓN DE REDES NEURONALES

## Descripción

Los datos a tratar corresponden a un experimento en ratones relacionado con la predicción de 8 clases a partir de los niveles de expresión de proteínas/modificaciones de proteínas que produjeron señales detectables en la fracción nuclear de la corteza.

Cada clase se basa en el genotipo, comportamiento y tratamiento. Según el genotipo, los ratones pueden ser controles (c) o trisómicos (t). Según el comportamiento, algunos ratones han sido estimulados para aprender (context-shock(CS)) y otros no (shock-context(SC)) y con el fin de evaluar el efecto del fármaco memantina (m) en la recuperación de la capacidad de aprendizaje en algunos ratones se ha inyectado la droga y a otros se ha inyectado suero salino (s) como placebo.
Las 8 clases son:

1.   c-CS-s: control-context-shock-salino
2.   c-CS-m: control-context-shock-memantina
3.   c-SC-s: control-shock-context-salino
4.   c-SC-m: control-shock-context-memantina
5.   t-CS-s: trisómico-context-shock-salino
6.   t-CS-m: trisómico-context-shock-memantina
7.   t-SC-s: trisómico-shock-context-salino
8.   t-SC-m: trisómico-shock-context-memantina

Los datos para esta actividad se encuentran en dos ficheros. El fichero data3.csv y el fichero clase3.csv.
El fichero data3.csv con los niveles de proteínas, tiene 1080 filas (muestras) y 73 columnas. La primera columna es el código de la muestra y el resto de columnas son proteínas. El fichero clase3.csv con los valores de la clase de 1 a 8, tiene 1080 filas (muestras) y una columna con el valor de la clase.

El objetivo planteado es la implementación y evaluación de una red neuronal basada en capas densas (fc) para la clasificación de las 8 clases.

## Enunciado

##### 1. Cargar los datos (data3.csv y clase3.csv).
"""

# Comenzamos importando los paquetes necesarios
from sklearn import datasets
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

# Cargamos los datos desde los archivos CSV
data = pd.read_csv('data3.csv')
clase = pd.read_csv('class3.csv')

# Primeras filas de los datos
print("Datos:")
print(data.head())

print("\nClases:")
print(clase.head())

"""Procederemos a preprocesar los datos y a unir las tablas:"""

# Agregamos la columna 'Clase' al dataframe 'data'
data['Clase'] = clase['x']

# Visualizamos las primeras filas del dataframe combinado
print("Datos combinados:")
print(data.head())

# Obtenemos la matriz de características (X) y el vector de etiquetas (y)
X = data.drop(['MouseID', 'Clase'], axis=1)  # Eliminamos 'MouseID' y 'Clase'
y = data['Clase']  # La columna 'Clase' es nuestra etiqueta

# Dimensiones de X e y
print("\nDimensiones de X:", X.shape)
print("Dimensiones de y:", y.shape)

"""##### 2. Realizar un estudio exploratorio de los datos con gráficos y tablas."""

# Frecuencia de cada una de las 8 clases
plt.figure(figsize=(8, 6))
sns.countplot(x='Clase', data=data)
plt.title('Distribución de Clases')
plt.show()

# Estadísticas descriptivas de los niveles de expresión
descripcion = X.describe()

# Visualizamos las estadísticas descriptivas
print("Estadísticas Descriptivas de los Niveles de Expresión:")
print(descripcion)

# Calculamos la matriz de correlación
correlacion = X.corr()

# Mostramos la matriz de correlación
plt.figure(figsize=(12, 10))
sns.heatmap(correlacion, annot=False, cmap='coolwarm', cbar_kws={'label': 'Correlación'})
plt.title('Matriz de Correlación entre los Niveles de Expresión')
plt.show()

# Boxplots
features_subset = X.iloc[:, :5]  # Primeras 5 expresiones
plt.figure(figsize=(12, 6))
sns.boxplot(data=features_subset, orient='h')
plt.title('Primeras Expresiones de Proteínas')
plt.show()

"""Dado que disponemos de 72 características (columnas con expresiones de proteínas), es difícil visualizar todas ellas en un solo gráfico bidimensional. Sin embargo, utilizaremos una técnica de reducción de dimensionalidad, PCA (Análisis de Componentes Principales), para proyectar los datos en un espacio de menor dimensión y visualizar la diferencia entre las clases en 3D."""

np.random.seed(42)

# Normalizamos los datos antes de aplicar PCA
scaler = StandardScaler()
X_normalized = scaler.fit_transform(X)

# PCA para reducir a 3 dimensiones
pca = PCA(n_components=3)
X_pca = pca.fit_transform(X_normalized)

# Mostrar en 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], X_pca[:, 2], c=y - 1, cmap='viridis', s=20)

# Leyenda con etiquetas de clase
original_labels = [f'Clase {i}' for i in range(1, 9)]
ax.legend(handles=scatter.legend_elements()[0], labels=original_labels)

ax.set_xlabel('Principal Component 1')
ax.set_ylabel('Principal Component 2')
ax.set_zlabel('Principal Component 3')
ax.set_title('8-Class classification (PCA in 3D) with Original Labels in Legend')
plt.show()

"""Gracias a esta representación podemos ver como las distintas clases forman agrupaciones, algunas más dispersas que otras. Las áreas donde más se superponen las clases pueden presentar "zonas" de ambigëdad para el modelo.

##### 3. Normalizar las expresiones con la transformación minmax.

La normalización es un paso crítico cuando trabajamos con redes neuronales, ya que ayuda a estabilizar el entrenamiento y garantiza, en nuestro caso, que todas las expresiones tengan un impacto similar en el modelo.
"""

# Creamos una instancia del MinMaxScaler
scaler = MinMaxScaler()

# Aplicamos la transformación Min-Max a las expresiones (X)
X_normalized = scaler.fit_transform(X)

# Creamos un nuevo dataframe con las expresiones normalizadas
X_normalized_df = pd.DataFrame(X_normalized, columns=X.columns)

# Primeras filas del dataframe normalizado
print("Datos Normalizados:")
print(X_normalized_df.head())

"""Hemos ajustado y transformado las expresiones (columnas), escalándolas al rango [0, 1]. El resultado es un nuevo dataframe X_normalized_df que contiene las expresiones normalizadas.

##### 4. Separar los datos en train (2/3) y test (1/3).
"""

# Ajustamos la codificación de las clases restando 1 a cada elemento en y
y = y - 1

# Comprobamos que las clases estén en el nuevo rango [0, 7]
print("Clases únicas en y:", np.unique(y))

# Proporción de división: 2/3 para entrenamiento y 1/3 para prueba
test_size = 1/3

# Dividimos los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_normalized_df, y, test_size=test_size, random_state=42)

# Dimensiones de los conjuntos de entrenamiento y prueba
print("Dimensiones de X_train:", X_train.shape)
print("Dimensiones de X_test:", X_test.shape)
print("Dimensiones de y_train:", y_train.shape)
print("Dimensiones de y_test:", y_test.shape)

"""##### 5. Definir el modelo 1, que consiste en una red neuronal con una capa oculta densa de 35 nodos, con activación relu. Añadir un 20% de dropout. Proporcionar el summary del modelo y justificar el total de parámetros de cada capa."""

# Definimos el objeto Sequential(), que albergará el modelo y nos permitirá
# agregar capas de manera secuencial.
modelo1 = Sequential()

# Capa oculta densa con 35 nodos (neuronas) y activación ReLU. La capa tiene una
# entrada (input_dim) que coincide con el número de proteínas en nuestros datos)
modelo1.add(Dense(35, input_dim=X_train.shape[1], activation='relu'))

# Añadir Dropout del 20% para reducir el sobreajuste. Este apaga aleatoriamente
# un porcentaje de las neuronas durante el entrenamiento.
modelo1.add(Dropout(0.2))

# Capa de salida con activación softmax, función que se utiliza en problemas de
# clasificación multiclase, ya que produce una distribución de probabilidad
# sobre las clases.
modelo1.add(Dense(8, activation='softmax'))

# Resumen del modelo con la arquitectura de la red, el número de parámetros en
# cada capa y el total de parámetros entrenables
modelo1.summary()

"""1. **Capa Oculta Densa con 35 nodos:**
   - Número de parámetros de pesos: \(35 x Número de características de entrada\)
   - Número de parámetros de sesgo: \(35\)
   - Total de parámetros = \(35 x Número de características de entrada + 35\) = 2555

2. **Dropout (20%):**
   - Dropout no tiene parámetros entrenables. Solo "apaga" el 20% de los nodos durante el entrenamiento.

3. **Capa de Salida con 8 nodos (clasificación de 8 clases):**
   - Número de parámetros de pesos: \(35 x 8\)
   - Número de parámetros de sesgo: \(8\)
   - Total de parámetros = \(35 x 8 + 8\) = 288

**Total de parámetros entrenables:**
2555 + 0 + 288 = 2843

 Los parámetros entrenables son aquellos que se ajustarán durante el proceso de entrenamiento para optimizar el rendimiento del modelo.

##### 6. Ajustar el modelo 1 con un 20% de validación, mostrando la curva de aprendizaje de entrenamiento y validación con 50 épocas.

La elección de optimizador y el uso de técnicas como Early Stopping son estrategias comunes en el entrenamiento de modelos de aprendizaje profundo.

**Adam (Adaptive Moment Estimation)** es un algoritmo de optimización que combina las ideas de los algoritmos de momentum y RMSprop. Algunas de sus características clave son:

- **Adaptabilidad:** Ajusta automáticamente las tasas de aprendizaje de cada parámetro en función de sus gradientes pasados, lo que puede llevar a convergencia más rápida y eficiente.

- **Momentum:** Ayuda a acelerar el entrenamiento, especialmente en presencia de gradientes pequeños o ruidosos.

- **RMSprop:** Adapta las tasas de aprendizaje individualmente para cada parámetro según la magnitud de sus gradientes recientes.

**Early Stopping** es una técnica utilizada para evitar el sobreajuste del modelo. Consiste en detener el entrenamiento del modelo una vez que ciertos criterios no mejoran durante un número específico de épocas consecutivas en el conjunto de validación. Las razones por las que emplear Early Stopping son:

- **Prevención del sobreajuste:** Detiene el entrenamiento cuando el modelo comienza a ajustarse demasiado a los datos de entrenamiento y no generaliza bien a nuevos datos.

- **Ahorro de tiempo y recursos:** Evita el entrenamiento innecesario si no se observa mejora en el rendimiento en el conjunto de validación.

Implementaremos el optimizador Adam y la técnica Early Stopping para mejorar la eficiencia y el rendimiento del entrenamiento en el modelo:
"""

# Definimos el optimizador Adam y la función de pérdida
opt = Adam(learning_rate=0.001)
modelo1.compile(optimizer=opt, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Configuramos Early Stopping para detener el entrenamiento si la precisión en validación no mejora en 5 épocas
early_stopping = EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True)

# Ajustamos el modelo con un 20% de validación y mostramos la curva de aprendizaje
historia = modelo1.fit(X_train, y_train, epochs=50, validation_split=0.2, batch_size=32, callbacks=[early_stopping])

"""**monitor='val_accuracy'** indica que Early Stopping debe seguir la precisión en el conjunto de validación. El entrenamiento se detendrá si la precisión en validación no mejora en 5 épocas (**patience=5**). Además, **restore_best_weights=True** restaurará los pesos del modelo a la mejor época si se detiene prematuramente."""

# Visualizar la curva de aprendizaje
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(historia.history['accuracy'], label='Entrenamiento')
plt.plot(historia.history['val_accuracy'], label='Validación')
plt.title('Curva de Aprendizaje - Precisión')
plt.xlabel('Épocas')
plt.ylabel('Precisión')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(historia.history['loss'], label='Entrenamiento')
plt.plot(historia.history['val_loss'], label='Validación')
plt.title('Curva de Aprendizaje - Pérdida')
plt.xlabel('Épocas')
plt.ylabel('Pérdida')
plt.legend()

plt.tight_layout()
plt.show()

"""La curva de **Aprendizaje - Precisión** proporciona información valiosa sobre el rendimiento del modelo, ya que muestra su capacidad para clasificar correctamente los ejemplos de entrenamiento y validación a lo largo del tiempo. La curva de precisión aumenta, indicando que el modelo está convergiendo correctamente durante el entrenamiento.

Del gráfico **Aprendizaje - Pérdida** podemos destacar que la curva de pérdida disminuye, lo que indica que el modelo está convergiendo correctamente durante el entrenamiento. En otras palabras, el modelo está aprendiendo de manera efectiva los patrones en los datos de entrenamiento.

##### 8. Definir el modelo 2, que consiste en una red neuronal con dos capas ocultas densas de 35 nodos y 15 nodos, con activación relu. Añadir un 20% de dropout en ambas capas. Proporcionar el summary del modelo y justificar el total de parámetros de cada capa.
"""

# Definimos el modelo 2
modelo2 = Sequential()

# Primera capa oculta con 35 nodos y activación relu, con dropout del 20%
modelo2.add(Dense(35, input_dim=X_train.shape[1], activation='relu'))
modelo2.add(Dropout(0.2))

# Segunda capa oculta con 15 nodos y activación relu, con dropout del 20%
modelo2.add(Dense(15, activation='relu'))
modelo2.add(Dropout(0.2))

# Capa de salida con 8 nodos (número de clases) y activación softmax
modelo2.add(Dense(8, activation='softmax'))

# Resumen del modelo
modelo2.summary()

"""Esta estructura permite que el modelo aprenda representaciones no lineales más complejas a medida que pasa por las capas ocultas, y el dropout ayuda a prevenir el sobreajuste al apagar aleatoriamente algunas neuronas durante el entrenamiento.

1. **Primera capa oculta (Dense_2):**
   - Salida: None, 35 indica que hay 35 nodos en esta capa.
   - Parámetros: \(73 x 35 + 35 = 2555\), como se esperaba.

2. **Dropout después de la primera capa (Dropout_1):**
   - El dropout no tiene parámetros entrenables, por lo que su salida es igual a su entrada.

3. **Segunda capa oculta (Dense_3):**
   - Salida: None, 15 indica que hay 15 nodos en esta capa.
   - Parámetros: \(35 x 15 + 15 = 540\), como se esperaba.

4. **Dropout después de la segunda capa (Dropout_2):**
   - Al igual que antes, el dropout no tiene parámetros entrenables.

5. **Capa de salida (Dense_4):**
   - Salida: None, 8 indica que hay 8 nodos en esta capa (el número de clases).
   - Parámetros: (15 x 8 + 8 = 128\), como se esperaba.

En total, el modelo tiene \(3223\) parámetros, de los cuales todos son entrenables.

##### 9. Ajustar el modelo 2 con un 20% de validación, mostrando la curva de aprendizaje de entrenamiento y validación con 50 épocas.
"""

# Compilar el modelo
modelo2.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Configuramos Early Stopping para detener el entrenamiento si la precisión en validación no mejora en 5 épocas
early_stopping = EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True)

# Ajustar el modelo con un 20% de validación y mostrar la curva de aprendizaje
historia2 = modelo2.fit(X_train, y_train, epochs=50, validation_split=0.2, batch_size=32, callbacks=[early_stopping])

# Curva de aprendizaje
plt.plot(historia2.history['accuracy'], label='Training Accuracy')
plt.plot(historia2.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Épocas')
plt.ylabel('Precisión')
plt.legend()
plt.show()

"""10. Comparar en test, mediante las métricas de evaluación, los dos modelos."""

# Predicción de las probabilidades en el conjunto de prueba para ambos modelos
probas_modelo1 = modelo1.predict(X_test)
probas_modelo2 = modelo2.predict(X_test)

# Obtenemos las clases predichas para ambos modelos
y_pred_modelo1 = probas_modelo1.argmax(axis=-1)
y_pred_modelo2 = probas_modelo2.argmax(axis=-1)

# Métricas para el modelo 1
confusion_mat_modelo1 = confusion_matrix(y_test, y_pred_modelo1)
classification_rep_modelo1 = classification_report(y_test, y_pred_modelo1)
accuracy_modelo1 = accuracy_score(y_test, y_pred_modelo1)

# Métricas para el modelo 2
confusion_mat_modelo2 = confusion_matrix(y_test, y_pred_modelo2)
classification_rep_modelo2 = classification_report(y_test, y_pred_modelo2)
accuracy_modelo2 = accuracy_score(y_test, y_pred_modelo2)

# Mostramos las métricas de modelos
print("Métricas del Modelo 1:")
print("Matriz de Confusión:")
print(confusion_mat_modelo1)
print("\nReporte de Clasificación:")
print(classification_rep_modelo1)
print("\nPrecisión:", accuracy_modelo1)
print("\n----------------------------------------------\n")

print("Métricas del Modelo 2:")
print("Matriz de Confusión:")
print(confusion_mat_modelo2)
print("\nReporte de Clasificación:")
print(classification_rep_modelo2)
print("\nPrecisión:", accuracy_modelo2)

"""
**Métricas del Modelo 1:**
- **Matriz de Confusión:**
  - Se observa cierta confusión en varias clases, por ejemplo, la clase 0 y la clase 1, donde hay 22 falsos positivos y 8 falsos negativos.

- **Reporte de Clasificación:**
  - Las precisiones y recalls varían entre las clases. La clase 7 tiene baja precisión (0.51), lo que indica que muchos de los ejemplos clasificados como clase 7 son falsos positivos.
  - La clase 3 tiene una tasa de recall del 100%, lo que significa que el modelo identifica correctamente todas las instancias de esta clase.
  - El modelo tiene un accuracy general del 0.75.

**Métricas del Modelo 2:**
- **Matriz de Confusión:**
  - Al igual que en el Modelo 1, hay confusión en varias clases. Por ejemplo, la clase 0 y la clase 1 tienen 25 falsos positivos y 10 falsos negativos.

- **Reporte de Clasificación:**
  - Las precisiones y recalls también varían entre las clases. La clase 7 tiene baja precisión (0.16), lo que indica muchos falsos positivos.
  - La clase 3 tiene un recall del 100%, lo que indica una identificación perfecta de esta clase.
  - El modelo tiene un accuracy general del 0.68.

**Comparación:**
- El Modelo 1 tiene un accuracy ligeramente mayor que el Modelo 2 (0.75 frente a 0.68).
- Ambos modelos muestran dificultades en la identificación de ciertas clases, con precisiones y recalls variables.

En resumen, aunque el Modelo 1 tiene un rendimiento ligeramente superior en términos de accuracy, ambos modelos podrían beneficiarse de ajustes adicionales para mejorar la clasificación en clases específicas.
Basándonos en las métricas de evaluación de ambos modelos en el conjunto de prueba, podemos observar que ambos modelos tienen áreas donde se desempeñan bien y áreas donde pueden mejorar. Ambos modelos comparten la estrategia de dropout para mitigar el sobreajuste. La principal diferencia está en la complejidad de la arquitectura, ya que el Modelo 2 tiene dos capas ocultas en lugar de una. Esto podría permitirle capturar patrones más complejos y abstracciones en los datos. Sin embargo, también podría estar más expuesto al sobreajuste, especialmente en casos en los que no hay suficientes datos para respaldar la complejidad adicional."""
