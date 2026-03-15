# Dashboard BI Ecobici – Pronóstico y Rebalanceo de Bicicletas

## Descripción del Proyecto

Este proyecto presenta un **dashboard interactivo de Business Intelligence** para analizar y pronosticar la disponibilidad de bicicletas en el sistema de bicicletas compartidas Ecobici.

La aplicación permite explorar datos históricos de estaciones, generar pronósticos de disponibilidad de bicicletas y obtener sugerencias de redistribución de bicicletas entre estaciones para mantener un equilibrio operativo.

El dashboard fue desarrollado utilizando **Streamlit**, lo que permite crear aplicaciones interactivas de análisis de datos directamente en Python.

El objetivo principal del proyecto es demostrar cómo el análisis de datos y los modelos de pronóstico pueden apoyar la **toma de decisiones operativas en sistemas de movilidad urbana**.

---

# Funcionalidades Principales

## 1. Exploración de Datos de Estaciones

Los usuarios pueden visualizar datos históricos de cada estación, incluyendo el número de bicicletas disponibles a lo largo del tiempo.

Esto permite identificar patrones de uso, horarios pico y tendencias en la disponibilidad de bicicletas.

---

## 2. Pronóstico de Series de Tiempo

La aplicación utiliza un modelo **ARIMA (Autoregressive Integrated Moving Average)** para estimar la disponibilidad futura de bicicletas en una estación específica.

El módulo de pronóstico permite:

- Seleccionar una estación específica
- Elegir la frecuencia temporal de los datos (por ejemplo, cada 30 minutos o cada hora)
- Definir el horizonte de pronóstico
- Ajustar los parámetros del modelo ARIMA

El sistema genera una visualización que incluye:

- Datos históricos
- Predicción futura
- Intervalos de confianza del pronóstico

Esto permite anticipar posibles **escaseces o excedentes de bicicletas** en determinadas estaciones.

---

## 3. Sugerencias de Rebalanceo de Bicicletas

El sistema también incluye un algoritmo de rebalanceo que analiza el estado actual de las estaciones.

El algoritmo identifica:

- Estaciones con **exceso de bicicletas**
- Estaciones con **déficit de bicicletas**

Con base en la capacidad de cada estación y un ratio objetivo de ocupación, el sistema genera sugerencias de movimientos de bicicletas entre estaciones.

El resultado se muestra en una tabla con instrucciones como:

Mover 5 bicicletas de estación 32 a estación 15.

Este módulo demuestra cómo el análisis de datos puede apoyar la **gestión logística de sistemas de bicicletas compartidas**.

---

# Tecnologías Utilizadas

El proyecto fue desarrollado utilizando las siguientes herramientas:

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Statsmodels
- GitHub

---

# Estructura del Proyecto

El proyecto sigue una estructura modular utilizando múltiples páginas de Streamlit:

project/
│
├── app.py
├── pages/
│ ├── 01_Data_Exploration.py
│ ├── 02_Visualization.py
│ ├── 03_Map_Analysis.py
│ ├── 04_Station_Insights.py
│ └── 05_Pronostico_ARIMA.py
│
├── data/
│ └── station_data.csv
│
├── requirements.txt
└── README.md


Cada archivo dentro de la carpeta `pages` corresponde a un módulo específico del dashboard.

---

# Despliegue de la Aplicación

La aplicación fue desplegada utilizando **Streamlit Cloud** a partir de un repositorio en **GitHub**.

## Proceso de despliegue

### 1. Creación del repositorio en GitHub

El código completo del proyecto se subió a un repositorio que incluye:

- Archivos de la aplicación en Python
- Archivos de datos
- Archivo `requirements.txt`
- Archivo `README.md`

---

### 2. Definición de dependencias

El archivo `requirements.txt` contiene las librerías necesarias para ejecutar la aplicación.


Cuando la aplicación se despliega, Streamlit Cloud instala automáticamente estas dependencias.

---

### 3. Conexión con Streamlit Cloud

El despliegue se realizó siguiendo estos pasos:

1. Iniciar sesión en Streamlit Cloud
2. Seleccionar **“New App”**
3. Conectar el repositorio de GitHub
4. Seleccionar el archivo principal de la aplicación (`app.py`)
5. Lanzar la aplicación

Streamlit Cloud se encarga automáticamente de construir y ejecutar la aplicación.
