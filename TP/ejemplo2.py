import psycopg2 
import pandas as pd
import matplotlib.pyplot as plt

#CONFIGURACIÓN DE CONEXIÓN
DB_CONFIG = {
    'dbname': 'TIF Prueba1',
    'user': 'postgres',
    'password': 'jaguar123',
    'host': 'localhost',
    'port': '5432'
}

# CONSULTA SQL: Total de especies distintas aisladas por CADA investigador
SQL_QUERY_DIVERSIDAD = """
SELECT
    i.nombre || ' ' || i.apellido AS investigador_completo,
    COUNT(DISTINCT c.id_microorganismo) AS total_especies_aisladas
FROM
    Investigador i
JOIN Muestra mstr ON i.dni_investigador = mstr.dni_investigador
JOIN Placa p ON mstr.id_muestra = p.id_muestra
JOIN Colonia c ON p.codigo_placa = c.codigo_placa
GROUP BY
    i.nombre, i.apellido, i.dni_investigador
ORDER BY
    total_especies_aisladas DESC;
"""

def analizar_diversidad():
    conn = None
    try:
        # CONEXIÓN Y EXTRACCIÓN DE DATOS 
        print("Intentando conectar a la base de datos...")
        
        conn = psycopg2.connect(**DB_CONFIG) 
        
        # Ejecutar la consulta y obtener el DataFrame
        df = pd.read_sql(SQL_QUERY_DIVERSIDAD, conn)
        
        if df.empty:
            print("No se encontraron datos de colonias aisladas. Verifique el poblado de las tablas Colonia y Microorganismo.")
            return
        
        print("\nDatos crudos obtenidos:")
        print(df)

        # PROCESAMIENTO Y VISUALIZACIÓN 
        
        df_final = df 
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Crear gráfico de barras para el total de especies aisladas
        ax.bar(df_final['investigador_completo'], df_final['total_especies_aisladas'], color='teal')
        
        # Etiquetas y Títulos
        ax.set_title('Contribución Total a la Diversidad Microbiana por Investigador')
        ax.set_ylabel('Número Total de Especies Distintas Aisladas')
        ax.set_xlabel('Investigador')
        
        # Rotar etiquetas X para mayor legibilidad
        plt.xticks(rotation=45, ha='right')
        
        # Añadir valor en la parte superior de cada barra
        for index, row in df_final.iterrows():
            ax.text(index, row['total_especies_aisladas'] + 0.05, str(row['total_especies_aisladas']), ha='center')

        plt.grid(axis='y', linestyle='--')
        plt.tight_layout()
        plt.show()

    except psycopg2.Error as e:
        print(f"Error al conectar o ejecutar la consulta: {e}")
    finally:
        if conn:
            conn.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    analizar_diversidad()