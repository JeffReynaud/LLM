import pandas as pd
from transformers import pipeline
import numpy as np
import os
from datetime import datetime

def listar_archivos_excel():
    """
    Lista todos los archivos Excel en el directorio actual
    """
    archivos_excel = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.xls'))]
    return archivos_excel

def cargar_comentarios_analisis(nombre_archivo):
    """
    Carga los comentarios del archivo Excel especificado
    """
    try:
        print(f"\nCargando archivo: {nombre_archivo}")
        df = pd.read_excel(nombre_archivo)
        
        # Verificar si existe la columna 'Comentario'
        if 'Comentario' not in df.columns:
            print("\nColumnas disponibles en el archivo:")
            print(df.columns.tolist())
            columna = input("\nIngrese el nombre exacto de la columna que contiene los comentarios: ")
            if columna not in df.columns:
                raise ValueError(f"La columna '{columna}' no existe en el archivo")
            return df[columna].tolist()
        
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
    print("\nInicializando el modelo de análisis de sentimientos...")
    sentiment_analyzer = pipeline(
        "sentiment-analysis",
        model="nlptown/bert-base-multilingual-uncased-sentiment",
        device=-1  # Usar CPU
    )
    
    resultados = []
    total = len(comentarios)
    
    print(f"\nProcesando {total} comentarios...")
    for i, comentario in enumerate(comentarios, 1):
        try:
            print(f"Procesando comentario {i}/{total}", end='\r')
            resultado = sentiment_analyzer(comentario)[0]
            estrellas = int(resultado['label'].split()[0])
            clasificacion = mapear_sentimiento(estrellas)
            
            resultados.append({
                'comentario': comentario,
                'sentimiento_modelo': resultado['label'],
                'clasificacion': clasificacion,
                'score': resultado['score']
            })
        except Exception as e:
            print(f"\nError al analizar el comentario {i}: {str(e)}")
            resultados.append({
                'comentario': comentario,
                'sentimiento_modelo': 'ERROR',
                'clasificacion': 'ERROR',
                'score': 0.0
            })
    
    print("\nAnálisis completado!")
    return pd.DataFrame(resultados)

def guardar_resultados(df_resultados, nombre_archivo_original):
    """
    Guarda los resultados en un archivo Excel
    """
    # Crear nombre del archivo de salida
    nombre_base = os.path.splitext(nombre_archivo_original)[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f'{nombre_base}_Analizado_{timestamp}.xlsx'
    
    # Guardar resultados
    df_resultados.to_excel(nombre_archivo, index=False)
    print(f"\nResultados guardados en: {nombre_archivo}")
    return nombre_archivo

def mostrar_resumen(resultados):
    """
    Muestra un resumen de los resultados del análisis
    """
    print("\nResumen de clasificaciones:")
    print("-" * 30)
    resumen = resultados['clasificacion'].value_counts()
    for categoria, cantidad in resumen.items():
        porcentaje = (cantidad / len(resultados)) * 100
        print(f"{categoria}: {cantidad} comentarios ({porcentaje:.1f}%)")
    
    print("\nMuestra de resultados:")
    print("-" * 30)
    print(resultados[['comentario', 'sentimiento_modelo', 'clasificacion']].head().to_string())

def main():
    print("=" * 50)
    print("Análisis de Sentimientos en Comentarios")
    print("=" * 50)
    
    # Listar archivos Excel disponibles
    archivos_excel = listar_archivos_excel()
    
    if not archivos_excel:
        print("\nNo se encontraron archivos Excel en el directorio actual.")
        return
    
    print("\nArchivos Excel disponibles:")
    for i, archivo in enumerate(archivos_excel, 1):
        print(f"{i}. {archivo}")
    
    # Seleccionar archivo
    while True:
        try:
            seleccion = int(input("\nSeleccione el número del archivo a analizar: "))
            if 1 <= seleccion <= len(archivos_excel):
                nombre_archivo = archivos_excel[seleccion - 1]
                break
            else:
                print("Por favor, seleccione un número válido.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
    
    # Cargar y analizar comentarios
    comentarios = cargar_comentarios_analisis(nombre_archivo)
    
    if not comentarios:
        print("No se pudieron cargar los comentarios. Verifique el archivo.")
        return
    
    print(f"\nSe cargaron {len(comentarios)} comentarios para análisis")
    
    # Analizar los comentarios
    resultados = analizar_sentimientos(comentarios)
    
    # Guardar y mostrar resultados
    archivo_resultados = guardar_resultados(resultados, nombre_archivo)
    mostrar_resumen(resultados)
    
    print("\n" + "=" * 50)
    print(f"Proceso completado. Resultados guardados en: {archivo_resultados}")
    print("=" * 50)

if __name__ == "__main__":
    main() 