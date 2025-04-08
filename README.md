# Análisis de Sentimientos en Comentarios

Este proyecto implementa un sistema de análisis de sentimientos para comentarios en español utilizando un modelo pre-entrenado de BERT.

## Características

- Análisis de sentimientos en español
- Clasificación en tres categorías: positivo, neutral y negativo
- Procesamiento de comentarios desde archivos Excel
- Exportación de resultados en formato Excel

## Requisitos

- Python 3.8 o superior
- pandas
- transformers
- torch
- openpyxl
- numpy

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/JeffReynaud/LLM.git
cd LLM
```

2. Crear y activar un entorno virtual:
```bash
python -m venv venv
.\venv\Scripts\activate  # En Windows
source venv/bin/activate  # En Linux/Mac
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Coloca tu archivo Excel con los comentarios en el directorio del proyecto
2. Asegúrate de que la columna con los comentarios se llame "Comentario"
3. Ejecuta el script:
```bash
python sentiment_analysis.py
```

4. Los resultados se guardarán en un archivo Excel con el formato: `Sentiment_Analysis_Resultados_YYYYMMDD_HHMMSS.xlsx`

## Estructura del Proyecto

- `sentiment_analysis.py`: Script principal para el análisis de sentimientos
- `requirements.txt`: Lista de dependencias del proyecto
- `.gitignore`: Archivos y directorios a ignorar en el control de versiones

## Clasificación de Sentimientos

El modelo clasifica los comentarios en tres categorías:
- Positivo: 4-5 estrellas
- Neutral: 3 estrellas
- Negativo: 1-2 estrellas

## Autor

Jefferson Reynaud 