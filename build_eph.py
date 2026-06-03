import pandas as pd
from pathlib import Path

# ANO4 -> año
# TRIMESTRE -> trimestre
# AGLOMERADO A USAR: 23 = GRAN SALTA | 29 = GRAN TUCUMAN - TAFI VIEJO pag 18
# ESTADO -> Condicion de actividad = 0, 1, 2, 3, 4 pag 22
# P21 -> MONTO INGRESO 
# CH04 -> sexo pag 19
# CH06 -> edad pag 19
# NIVEL_ED - nivel educativo pag 21
# PP04A -> que tipo de trabajo es: 1 ESTATAL/2 PRIVADO/3 OTRO TIPO pag 24
# PONDERA -> ponderacion (importancia relativa)

ruta = Path("microdatos_2016_2025")

lista_trimestres_df = []
columnas_usadas = ["ANO4", "TRIMESTRE", "AGLOMERADO", "ESTADO", "P21", "CH04", "CH06", "NIVEL_ED", "PP04A", "PONDERA"] #columnas a elegir para realizar analisis

for archivo in ruta.rglob("usu_individual_*.txt"): #gracias a rglob, leo dentro de la ruta todos las carpetas y busca si coinciden con lo pasado por parametro

    print("Leyendo archivo: ", archivo);

    try: #tengo que usar try porque usu_individual_T424 tiene un error
        df = pd.read_csv(archivo, sep=";", usecols=columnas_usadas)

        lista_trimestres_df.append(df)
    except Exception as e: # problemas para cargar el 4to trimestre 2024

        print(f"Reintentando con engine='python': {archivo}")

        df = pd.read_csv(archivo, sep=";", usecols=columnas_usadas, engine="python")

        lista_trimestres_df.append(df)

eph_df = pd.concat(lista_trimestres_df, ignore_index=True) # unimos todos los df en uno solo, ignorando indices! osea generamos nuevos indices

eph_df = eph_df[eph_df["AGLOMERADO"].isin([23,29])] ### solo elegir los aglomerados 23 y 29

print(eph_df["AGLOMERADO"].value_counts())

eph_df.to_csv(
    "microdatos_2016_2025/eph_salta_tucuman_22016_42025.csv",
    index=False
)
