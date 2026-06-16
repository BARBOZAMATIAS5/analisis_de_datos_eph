import pandas as pd

df = pd.read_csv("eph_limpio_con_ipc.csv")

# Mapear los códigos de aglomerados para que sean legibles
aglomerados_map = {23: "Gran Salta", 29: "Gran Tucumán - Tafí Viejo"}
df["nom_aglomerado"] = df["AGLOMERADO"].map(aglomerados_map)

# 2. Función que calcula las tasas y el ingreso promedio (usando PONDERA)
def calcular_indicadores_completo(group):
    ocupados = group[group["ESTADO"] == 1]
    desocupados = group[group["ESTADO"] == 2]
    
    # Sumas ponderadas básicas
    ocupados_ponderados = ocupados["PONDERA"].sum()
    desocupados_ponderados = desocupados["PONDERA"].sum()
    pea_ponderada = ocupados_ponderados + desocupados_ponderados
    poblacion_total_ponderada = group["PONDERA"].sum()
    
    # Cálculo de Tasas Oficiales INDEC
    tasa_desocupacion = (desocupados_ponderados / pea_ponderada * 100) if pea_ponderada > 0 else 0
    tasa_actividad = (pea_ponderada / poblacion_total_ponderada * 100) if poblacion_total_ponderada > 0 else 0
    tasa_empleo = (ocupados_ponderados / poblacion_total_ponderada * 100) if poblacion_total_ponderada > 0 else 0
    
    # Cálculo del Ingreso Principal Real Promedio Ponderado
    # Solo tomamos ocupados con ingresos mayores a cero
    ocupados_con_ingreso = ocupados[ocupados["P21_real"] > 0]
    if not ocupados_con_ingreso.empty:
        ingreso_medio_real = (ocupados_con_ingreso["P21_real"] * ocupados_con_ingreso["PONDERA"]).sum() / ocupados_con_ingreso["PONDERA"].sum()
    else:
        ingreso_medio_real = 0
    
    return pd.Series({
        "Tasa_Actividad": round(tasa_actividad, 2),
        "Tasa_Empleo": round(tasa_empleo, 2),
        "Tasa_Desocupacion": round(tasa_desocupacion, 2),
        "Ingreso_Medio_Real": round(ingreso_medio_real, 2)
    })

# 3. Agrupar por Año, Trimestre y Aglomerado
evolucion_completa = (
    df.groupby(["ANO4", "TRIMESTRE", "nom_aglomerado"])
    .apply(calcular_indicadores_completo, include_groups=False)
    .reset_index()
)

# Crear la columna combinada de Período (ej: "2017-T1")
evolucion_completa["Periodo"] = evolucion_completa["ANO4"].astype(str) + "-T" + evolucion_completa["TRIMESTRE"].astype(str)

# Ordenar cronológicamente
evolucion_completa = evolucion_completa.sort_values(by=["ANO4", "TRIMESTRE"])

# Guardar la matriz completa en un CSV (este es el entregable para el Integrante 3)
evolucion_completa.to_csv("datos/reporte_indicadores_mercado.csv", index=False)

# 4. SELECCIÓN Y MUESTRA DE LA TABLA SOLICITADA
columnas_visibles = [
    "Periodo", 
    "nom_aglomerado", 
    "Tasa_Actividad", 
    "Tasa_Empleo", 
    "Tasa_Desocupacion", 
    "Ingreso_Medio_Real"
]

print("\n" + "="*90)
print(" TABLA COMPARATIVA DE EVOLUCIÓN LABORAL E INGRESOS REALES (Gran Salta vs. Gran Tucumán)")
print("="*90)
# to_string(index=False) hace que se vea limpio como una tabla real en la consola
print(evolucion_completa[columnas_visibles].to_string(index=False))
print("="*90)






