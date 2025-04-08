import pandas as pd
from transformers import pipeline
import numpy as np

def cargar_comentarios_analisis():
    """
    Carga los comentarios del archivo Sentiment_Analysis_1.xlsx
    """
    try:
        df = pd.read_excel('Sentiment_Analysis_1.xlsx')
        return df['Comentario'].tolist()
    except Exception as e:
        print(f"Error al cargar el archivo: {str(e)}")
        return []

def mapear_sentimiento(estrellas):
    """
    Mapea las estrellas (1-5) a las categorías de sentimiento
    """
    if estrellas <= 2:
        return "negativo"
    elif estrellas == 3:
        return "neutral"
    else:
        return "positivo"

def analizar_sentimientos(comentarios):
    """
    Analiza los sentimientos de una lista de comentarios usando el modelo de Hugging Face
    """
    # Inicializar el pipeline de análisis de sentimientos
    sentiment_analyzer = pipeline(
        "sentiment-analysis",
        model="nlptown/bert-base-multilingual-uncased-sentiment",
        device=-1  # Usar CPU
    )
    
    resultados = []
    total = len(comentarios)
    
    for i, comentario in enumerate(comentarios, 1):
        try:
            print(f"Procesando comentario {i}/{total}")
            # Obtener el análisis de sentimiento
            resultado = sentiment_analyzer(comentario)[0]
            # Extraer el número de estrellas del label (ejemplo: "4 stars" -> 4)
            estrellas = int(resultado['label'].split()[0])
            # Mapear a la categoría correspondiente
            clasificacion = mapear_sentimiento(estrellas)
            
            resultados.append({
                'comentario': comentario,
                'sentimiento_modelo': resultado['label'],
                'clasificacion': clasificacion,
                'score': resultado['score']
            })
        except Exception as e:
            print(f"Error al analizar el comentario {i}: {str(e)}")
            resultados.append({
                'comentario': comentario,
                'sentimiento_modelo': 'ERROR',
                'clasificacion': 'ERROR',
                'score': 0.0
            })
    
    return pd.DataFrame(resultados)

def guardar_resultados(df_resultados):
    """
    Guarda los resultados en un archivo Excel
    """
    nombre_archivo = f'Sentiment_Analysis_Resultados_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    df_resultados.to_excel(nombre_archivo, index=False)
    print(f"\nResultados guardados en: {nombre_archivo}")

def main():
    # Cargar comentarios para análisis
    print("Cargando comentarios del archivo Sentiment_Analysis_1.xlsx...")
    comentarios = cargar_comentarios_analisis()
    
    if not comentarios:
        print("No se pudieron cargar los comentarios. Verifique el archivo.")
        return
    
    print(f"Se cargaron {len(comentarios)} comentarios para análisis")
    
    # Analizar los comentarios
    print("\nIniciando análisis de sentimientos...")
    resultados = analizar_sentimientos(comentarios)
    
    # Mostrar resumen de resultados
    print("\nResumen de clasificaciones:")
    print(resultados['clasificacion'].value_counts())
    
    # Guardar resultados
    guardar_resultados(resultados)
    
    # Mostrar algunos ejemplos
    print("\nMuestra de resultados:")
    print(resultados[['comentario', 'sentimiento_modelo', 'clasificacion']].head().to_string())

if __name__ == "__main__":
    main() 