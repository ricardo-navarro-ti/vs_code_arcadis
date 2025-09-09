import pandas as pd
import os

print("Iniciando proceso de anonimización...")

try:
    # Verificar si el archivo existe
    if not os.path.exists('powerbi_datos_detalle.csv'):
        print("Error: No se encuentra el archivo powerbi_datos_detalle.csv")
        exit()

    # Leer el archivo
    print("Leyendo archivo de datos...")
    df = pd.read_csv('powerbi_datos_detalle.csv')
    print(f"Archivo leído. Dimensiones: {df.shape}")

    # Verificar columnas
    print("Columnas en el archivo:", df.columns.tolist())

    # Anonimizar nombres
    if 'Nombre' in df.columns:
        print("Anonimizando nombres...")
        nombres_unicos = df['Nombre'].unique()
        mapeo_nombres = {nombre: f'Usuario {i+1}' for i, nombre in enumerate(nombres_unicos)}
        df['Nombre'] = df['Nombre'].map(mapeo_nombres)

    # Anonimizar asesores
    if 'Asesor HSW' in df.columns:
        print("Anonimizando asesores...")
        asesores_unicos = df['Asesor HSW'].unique()
        mapeo_asesores = {asesor: f'Asesor {i+1}' for i, asesor in enumerate(asesores_unicos)}
        df['Asesor HSW'] = df['Asesor HSW'].map(mapeo_asesores)

    # Guardar archivo anonimizado
    print("Guardando archivo anonimizado...")
    df.to_csv('powerbi_datos_detalle_anonimo.csv', index=False)
    print("¡Proceso completado con éxito!")

    # Verificar que el archivo se creó
    if os.path.exists('powerbi_datos_detalle_anonimo.csv'):
        print("Archivo anonimizado creado correctamente")
        print(f"Tamaño del archivo: {os.path.getsize('powerbi_datos_detalle_anonimo.csv')} bytes")
    else:
        print("Error: El archivo no se creó correctamente")

except Exception as e:
    print(f"Error durante el proceso: {str(e)}")
