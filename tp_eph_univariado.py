import pandas as pd
import numpy as np

# 1. Cargar el dataset limpio generado por el Integrante 1
df = pd.read_csv("eph_limpio_con_ipc.csv")

# Mapear los códigos de aglomerados para que sean legibles
aglomerados_map = {23: "Gran Salta", 29: "Gran Tucumán - Tafí Viejo"}
df["nom_aglomerado"] = df["AGLOMERADO"].map(aglomerados_map)

# FILTRO UNIVARIADO: Para analizar ingresos reales, seleccionamos solo a la 
# población ocupada (ESTADO == 1) que declaró ingresos positivos (> 0).
df_ingresos = df[(df["ESTADO"] == 1) & (df["P21_real"] > 0)].copy()

# =========================================================================
# FUNCIONES AUXILIARES PARA ESTADÍSTICA PONDERADA (Metodología Oficial)
# =========================================================================

def media_ponderada(valores, pesos):
    """Calcula la media aritmética considerando los ponderadores."""
    return np.average(valores, weights=pesos)

def desvio_ponderado(valores, pesos):
    """Calcula el desvío estándar considerando los ponderadores."""
    media = media_ponderada(valores, pesos)
    varianza = np.average((valores - media)**2, weights=pesos)
    return np.sqrt(varianza)

def percentil_ponderado(valores, pesos, percentil):
    """
    Calcula medidas de posición (Cuartiles/Mediana) ponderadas.
    percentil debe ser un valor entre 0 y 1 (ej: 0.25 para Q1, 0.50 para Mediana)
    """
    valores = np.array(valores)
    pesos = np.array(pesos)
    
    # Ordenar los valores y sus respectivos pesos
    indices_ordenados = np.argsort(valores)
    valores_ordenados = valores[indices_ordenados]
    pesos_ordenados = pesos[indices_ordenados]
    
    # Calcular la distribución acumulada de los pesos
    pesos_acumulados = np.cumsum(pesos_ordenados) - 0.5 * pesos_ordenados
    pesos_acumulados /= np.sum(pesos_ordenados)
    
    # Interpolar para encontrar el valor exacto del percentil
    return np.interp(percentil, pesos_acumulados, valores_ordenados)


# =========================================================================
# PROCESAMIENTO AGRUPADO POR PERÍODO HISTÓRICO
# =========================================================================

def calcular_metricas_univariadas(group):
    ingresos = group["P21_real"]
    pesos = group["PONDERA"]
    
    if len(ingresos) == 0:
        return pd.Series({"Media": 0, "Q1_25": 0, "Mediana": 0, "Q3_75": 0, "Desvio_Std": 0})
    
    # Cálculo de cada medida solicitada
    media_val = media_ponderada(ingresos, pesos)
    q1_val = percentil_ponderado(ingresos, pesos, 0.25)
    mediana_val = percentil_ponderado(ingresos, pesos, 0.50)
    q3_val = percentil_ponderado(ingresos, pesos, 0.75)
    std_val = desvio_ponderado(ingresos, pesos)
    
    return pd.Series({
        "Media": round(media_val, 2),
        "Q1_25": round(q1_val, 2),
        "Mediana": round(mediana_val, 2),
        "Q3_75": round(q3_val, 2),
        "Desvio_Std": round(std_val, 2)
    })

# Agrupar históricamente por Año, Trimestre y Región
evolucion_univariada = (
    df_ingresos.groupby(["ANO4", "TRIMESTRE", "nom_aglomerado"])
    .apply(calcular_metricas_univariadas, include_groups=False)
    .reset_index()
)

# Crear etiqueta temporal para el eje X ("2017-T1") y ordenar cronológicamente
evolucion_univariada["Periodo"] = evolucion_univariada["ANO4"].astype(str) + "-T" + evolucion_univariada["TRIMESTRE"].astype(str)
evolucion_univariada = evolucion_univariada.sort_values(by=["ANO4", "TRIMESTRE"])

# Guardar matriz de datos univariados para el Integrante 3 (Gráficos de caja/líneas históricos)
evolucion_univariada.to_csv("datos/univariado_ingresos_historico.csv", index=False)

# =========================================================================
# VISTA DE LA TABLA FINAL
# =========================================================================
columnas_reporte = [
    "Periodo", 
    "nom_aglomerado", 
    "Media", 
    "Q1_25", 
    "Mediana", 
    "Q3_75", 
    "Desvio_Std"
]

print("\n" + "="*110)
print(" EVOLUCIÓN HISTÓRICA DEL INGRESO REAL: TENDENCIA CENTRAL Y POSICIÓN (PONDERADO)")
print("="*110)
print(evolucion_univariada[columnas_reporte].to_string(index=False))
print("="*110)