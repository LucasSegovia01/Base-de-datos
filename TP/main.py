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

SQL_QUERY_DISTRIBUCION = """
SELECT
    a.nombre_comercial,
    pr.resultado,
    COUNT(pr.id_prueba) AS total_pruebas
FROM
    PruebaResistencia pr
JOIN Antibiotico a ON pr.id_antibiotico = a.id_antibiotico
GROUP BY
    a.nombre_comercial, pr.resultado
ORDER BY
    a.nombre_comercial, pr.resultado DESC;
"""

def analizar_distribucion_atb():
    conn = None
    try:
        print("Intentando conectar para el análisis de distribución por antibiótico...")
        conn = psycopg2.connect(**DB_CONFIG)
        
        df = pd.read_sql(SQL_QUERY_DISTRIBUCION, conn)
        
        if df.empty:
            print("No se encontraron datos de prueba de resistencia.")
            return

        #PROCESAMIENTO DE DATOS
        # 1Calcular el total de pruebas realizadas para CADA antibiótico
        df['total_por_atb'] = df.groupby('nombre_comercial')['total_pruebas'].transform('sum')
        
        # 2Calcular el porcentaje de cada resultado (resistente, sensible, intermedio)
        df['porcentaje'] = (df['total_pruebas'] / df['total_por_atb']) * 100
        
        # 3.tabla para el gráfico de barras apiladas
        df_pivot = df.pivot(index='nombre_comercial', columns='resultado', values='porcentaje').fillna(0)
        
        # Garantizar el orden de las columnas (sensible abajo, resistente arriba)
        orden_columnas = ['sensible', 'intermedio', 'resistente']
        df_pivot = df_pivot.reindex(columns=orden_columnas, fill_value=0)

        # VISUALIZACIÓN DE DATOS 
        
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # Crear gráfico de barras apiladas
        df_pivot.plot(kind='bar', stacked=True, ax=ax, 
                      color={'resistente': 'darkred', 'intermedio': 'orange', 'sensible': 'green'})
        
        # Etiquetas y Títulos
        ax.set_title('Distribución de Resultados de Resistencia por Antibiótico', fontsize=16)
        ax.set_ylabel('Porcentaje (%) de Pruebas', fontsize=12)
        ax.set_xlabel('Antibiótico', fontsize=12)
        ax.legend(title='Resultado', loc='upper right')
        
        plt.yticks(range(0, 101, 10))
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        plt.show()

    except psycopg2.Error as e:
        print(f"Error al conectar o ejecutar la consulta: {e}")
    finally:
        if conn:
            conn.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    analizar_distribucion_atb()