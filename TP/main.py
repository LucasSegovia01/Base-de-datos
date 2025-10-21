import psycopg2 # Usar 'mysql.connector' si usan MySQL
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. CONFIGURACIÓN DE CONEXIÓN ---
# Deben reemplazar estos datos con la configuración real de su base de datos
DB_CONFIG = {
    'dbname': 'TIF Prueba1',
    'user': 'postgres',
    'password': 'jaguar123',
    'host': 'localhost', # o la IP del servidor
    'port': '5432' # 5432 para PostgreSQL, 3306 para MySQL
}

SQL_QUERY = """
SELECT
    pm.tipo_zona,
    pr.resultado,
    COUNT(pr.id_prueba) AS total_pruebas
FROM
    PruebaResistencia pr
JOIN CultivoSuspendido cs ON pr.id_cultivo_suspendido = cs.id_CultivoSuspendido
JOIN Repique r ON cs.id_repique = r.id_repique
JOIN Colonia c ON r.id_colonia = c.id_colonia AND r.codigo_placa = c.codigo_placa
JOIN Microorganismo m ON c.id_microorganismo = m.id_microorganismo
JOIN Placa p ON c.codigo_placa = p.codigo_placa
JOIN Muestra mstr ON p.id_muestra = mstr.id_muestra
JOIN PuntosDeMuestreo pm ON mstr.id_PuntoMuestreo = pm.id_PuntoMuestreo
JOIN Antibiotico a ON pr.id_antibiotico = a.id_antibiotico
WHERE
    m.genero = 'Escherichia' AND m.especie = 'coli'
    AND a.nombre_comercial = 'Penicilina'
GROUP BY
    pm.tipo_zona, pr.resultado;
"""

def analizar_resistencia():
    conn = None
    try:
        # --- 2. CONEXIÓN Y EXTRACCIÓN DE DATOS ---
        print("Intentando conectar a la base de datos...")
        conn = psycopg2.connect(**DB_CONFIG)
        
        # Usamos pandas para ejecutar la consulta y obtener los resultados directamente en un DataFrame
        df = pd.read_sql(SQL_QUERY, conn)
        
        if df.empty:
            print("No se encontraron resultados para E. coli y Penicilina. Asegúrese de que los datos de prueba existan.")
            return
        
        print("\nDatos crudos obtenidos:")
        print(df)

        # --- 3. PROCESAMIENTO DE DATOS (Cálculo de Porcentajes) ---
        
        # Calcular el total de pruebas por cada tipo de zona (control vs. impacto)
        df['total_por_zona'] = df.groupby('tipo_zona')['total_pruebas'].transform('sum')
        
        # Calcular el porcentaje de cada resultado (resistente, sensible, etc.)
        df['porcentaje'] = (df['total_pruebas'] / df['total_por_zona']) * 100
        
        # Pivotear la tabla para tener las zonas como columnas (útil para graficar)
        df_pivot = df.pivot(index='resultado', columns='tipo_zona', values='porcentaje').fillna(0)

        # --- 4. VISUALIZACIÓN DE DATOS ---
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Crear gráfico de barras agrupadas
        df_pivot.plot(kind='bar', ax=ax, width=0.8)
        
        # Etiquetas y Títulos
        ax.set_title('Porcentaje de Resistencia de E. coli a Penicilina por Zona')
        ax.set_ylabel('Porcentaje (%)')
        ax.set_xlabel('Resultado de la Prueba')
        ax.legend(title='Tipo de Zona', labels=['Control', 'Impacto'])
        
        # Mejorar el formato del eje Y
        plt.yticks(range(0, 101, 10))
        plt.grid(axis='y', linestyle='--')
        plt.xticks(rotation=0) # Rotar etiquetas X si fuera necesario
        
        plt.tight_layout()
        plt.show() # Mostrar el gráfico

    except psycopg2.Error as e:
        print(f"Error al conectar o ejecutar la consulta: {e}")
    finally:
        if conn:
            conn.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    analizar_resistencia()