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
