# Laboratorio 1 Machine learning

Asignatura: Machine Learning
Institución: Universidad Católica del Norte
Carrera: Ingeniería Civil en Computación e Informática

Integrantes
* Mauricio Díaz (mauricio.diaz@alumnos.ucn.cl)
* Martina García (martina.garcia@alumnos.ucn.cl)
* Felipe Blanco (felipe.blanco@alumnos.ucn.cl)

Descripción del Proyecto
Este proyecto consiste en un sistema de procesamiento de lenguaje natural (NLP) diseñado para la extracción y análisis de datos desde X (Twitter) y Radio Cooperativa. El sistema automatiza la limpieza de textos y aplica modelos de aprendizaje no supervisado (K-Means y PCA) para descubrir patrones de discurso y temáticas ocultas en el corpus recolectado.



Instrucciones de Ejecución

1. Instalar  librerías necesarias:
* pip install pandas requests feedparser pymongo pyarrow nltk scikit-learn seaborn

+ Mediante Conda:
* conda env create -f environment.yml
* conda activate lab-1-m-l

2. Ejecutar el programa principal:
* python main.py

3. Primer paso en consola cuando se despliegue la línea: "Ingresa tu Bearer Token de X (o presiona Enter para usar respaldo local):"
* Simplemente presionar la tecla ENTER.

4. Segundo paso en consola cuando se despliegue la línea: "Ingresa tu URI de MongoDB (o presiona Enter para omitir):"
* Simplemente presionar la tecla ENTER nuevamente.

5. Revisión de resultados:
* Dirigirse a la carpeta "images" dentro del proyecto; allí se encontraran los gráficos generados (pca_clusters.png y grafico_frecuencias.png).

* Consola: Al finalizar, la terminal mostrará un resumen de los datos.