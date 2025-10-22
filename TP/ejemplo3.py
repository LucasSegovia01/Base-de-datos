import psycopg2 
import pandas as pd
import matplotlib.pyplot as plt

# CONFIGURACIÓN DE CONEXIÓN 
DB_CONFIG = {
    'dbname': 'TIF Prueba1',
    'user': 'postgres',
    'password': 'jaguar123',
    'host': 'localhost',
    'port': '5432'
}

# CONSULTA SQL: Microorganismos Multirresistentes
SQL_QUERY_MULTIRRESISTENCIA = """
SELECT
    m.genero || ' ' || m.especie AS especie_completa,
    COUNT(pr.id_antibiotico) AS total_antibioticos_resistentes
FROM
    PruebaResistencia pr
JOIN CultivoSuspendido cs ON pr.id_cultivo_suspendido = cs.id_CultivoSuspendido
JOIN Repique r ON cs.id_repique = r.id_repique
JOIN Colonia c ON r.id_colonia = c.id_colonia AND r.codigo_placa = c.codigo_placa
JOIN Microorganismo m ON c.id_microorganismo = m.id_microorganismo
WHERE
    pr.resultado = 'resistente'
GROUP BY
    m.genero, m.especie
HAVING
    COUNT(pr.id_antibiotico) > 1
ORDER BY
    total_antibioticos_resistentes DESC;
"""

def analizar_multirresistencia():
    conn = None
    try:
        # CONEXIÓN Y EXTRACCIÓN DE DATOS
        print("Intentando conectar a la base de datos...")
        conn = psycopg2.connect(**DB_CONFIG) 
        
        # Ejecutar la consulta. 
        df = pd.read_sql(SQL_QUERY_MULTIRRESISTENCIA, conn)
        
        if df.empty:
            print("No se encontraron microorganismos multirresistentes. Ajuste el poblado de datos (debe haber al menos una colonia resistente a dos antibióticos).")
            return
        
        print("\nDatos crudos obtenidos:")
        print(df)

        #VISUALIZACIÓN DE DATOS
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Crea gráfico de barras: Especie vs. Nivel de Resistencia
        ax.bar(df['especie_completa'], df['total_antibioticos_resistentes'], color='darkorange')
        
        # Etiquetas y Títulos
        ax.set_title('Nivel de Multirresistencia por Especie (> 1 Antibiótico)', fontsize=14)
        ax.set_ylabel('N° de Antibióticos a los que es Resistente', fontsize=12)
        ax.set_xlabel('Especie Microbiana', fontsize=12)
        
        plt.xticks(rotation=45, ha='right')
        
        # Añadir valores en la parte superior de cada barra
        for index, row in df.iterrows():
            ax.text(index, row['total_antibioticos_resistentes'], str(row['total_antibioticos_resistentes']), ha='center', va='bottom', fontsize=12)

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
    analizar_multirresistencia()