import pandas as pd
import numpy as np

# 1. Cargar el dataset limpio generado por el Integrante 1
df = pd.read_csv("eph_limpio_con_ipc.csv")

# =========================================================================
# MAPEOS Y PREPARACIÓN DE LAS 3 VARIABLES
# =========================================================================
aglomerados_map = {23: "Gran Salta", 29: "Gran Tucumán - Tafí Viejo"}
df["nom_aglomerado"] = df["AGLOMERADO"].map(aglomerados_map)

# Variable 1: Sexo (CH04)
df["Sexo"] = df["CH04"].map({1: "Varón", 2: "Mujer"})

# Variable 2: Nivel Educativo (NIVEL_ED)
nivel_ed_map = {
    1: "Primaria Incompleta", 2: "Primaria Completa",
    3: "Secundaria Incompleta", 4: "Secundaria Completa",
    5: "Superior Incompleta", 6: "Superior Completa",
    7: "Sin Instrucción"
}
df["Nivel_Educativo"] = df["NIVEL_ED"].map(nivel_ed_map)

# Variable 3: Tipo de Trabajo / Sector (PP04A)
df["Tipo_Trabajo"] = df["PP04A"].map({1: "Estatal/Público", 2: "Privado", 3: "Otro"})


# =========================================================================
# FUNCIÓN DE CÁLCULO PONDERADO 
# =========================================================================
def calcular_metricas_multivariado(group):
    ocupados = group[group["ESTADO"] == 1]
    desocupados = group[group["ESTADO"] == 2]
    
    # Sumas ponderadas (población real estimada)
    ocupados_pond = ocupados["PONDERA"].sum()
    desocupados_pond = desocupados["PONDERA"].sum()
    pea_pond = ocupados_pond + desocupados_pond
    poblacion_total_pond = group["PONDERA"].sum()
    
    # Cálculo de Tasas
    tasa_desocupacion = (desocupados_pond / pea_pond * 100) if pea_pond > 0 else 0
    tasa_actividad = (pea_pond / poblacion_total_pond * 100) if poblacion_total_pond > 0 else 0
    tasa_empleo = (ocupados_pond / poblacion_total_pond * 100) if poblacion_total_pond > 0 else 0
    
    # Ingreso Medio Real (solo ocupados con ingresos positivos)
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

# Crear la etiqueta temporal para ordenar cronológicamente
df["Periodo"] = df["ANO4"].astype(str) + "-T" + df["TRIMESTRE"].astype(str)


# =========================================================================
# PROCESAMIENTO Y EXPORTACIÓN DE LAS TABLAS MULTIVARIADAS
# =========================================================================

# 1. Tabla Multivariada por SEXO
multivariado_sexo = df.groupby(["Periodo", "nom_aglomerado", "Sexo"]).apply(calcular_metricas_multivariado, include_groups=False).reset_index()
multivariado_sexo.to_csv("datos/multivariado_mercado_sexo.csv", index=False)

# 2. Tabla Multivariada por NIVEL EDUCATIVO
multivariado_educacion = df.groupby(["Periodo", "nom_aglomerado", "Nivel_Educativo"]).apply(calcular_metricas_multivariado, include_groups=False).reset_index()
multivariado_educacion.to_csv("datos/multivariado_mercado_educacion.csv", index=False)

# 3. Tabla Multivariada por TIPO DE TRABAJO (Filtramos solo ocupados con registro de sector)
df_ocupados = df[(df["ESTADO"] == 1) & (df["Tipo_Trabajo"].notna())]
multivariado_trabajo = df_ocupados.groupby(["Periodo", "nom_aglomerado", "Tipo_Trabajo"]).apply(calcular_metricas_multivariado, include_groups=False).reset_index()
# De esta tabla nos quedamos solo con los ingresos medios reales por sector
multivariado_trabajo = multivariado_trabajo[["Periodo", "nom_aglomerado", "Tipo_Trabajo", "Ingreso_Medio_Real"]]
multivariado_trabajo.to_csv("datos/multivariado_ingresos_tipo_trabajo.csv", index=False)


# =========================================================================
# VISTA DE LAS TABLAS EN CONSOLA (Muestras de la estructura)
# =========================================================================

print("\n" + "="*100)
print(" 1. TABLA MULTIVARIADA: INDICADORES LABORALES E INGRESOS POR SEXO")
print("="*100)
print(multivariado_sexo.tail(6).to_string(index=False))

print("\n" + "="*100)
print(" 2. TABLA MULTIVARIADA: INDICADORES POR NIVEL EDUCATIVO (Muestra de Secundario/Superior)")
print("="*100)
filtro_ed = multivariado_educacion["Nivel_Educativo"].isin(["Secundaria Completa", "Superior Completa"])
print(multivariado_educacion[filtro_ed].tail(6).to_string(index=False))

print("\n" + "="*100)
print(" 3. TABLA MULTIVARIADA: INGRESO MEDIO REAL POR TIPO DE TRABAJO (SECTOR)")
print("="*100)
print(multivariado_trabajo.tail(6).to_string(index=False))
print("="*100)