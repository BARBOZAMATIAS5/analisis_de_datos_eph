import pandas as pd


# lectura de csv (dataframes)
df_eph = pd.read_csv("microdatos_2016_2025/eph_salta_tucuman_22016_42025.csv")
df_ipc_trimestral = pd.read_csv("microdatos_2016_2025/IPC_trimestre_2017_2025/ipc_trimestral_12017_42025.csv")

# limpiamos
df_eph = df_eph[df_eph["P21"] != -9] # elimina no corresponde
df_eph = df_eph.dropna(subset=["P21", "ESTADO", "CH04", "CH06", "NIVEL_ED"]) # elimina valores nan en las columnas escritas

# tenemos de referencia el ultimo cuatrimestre de 2025, indice base
indice_base = df_ipc_trimestral[
    (df_ipc_trimestral["ANO4"] == 2025) & (df_ipc_trimestral["TRIMESTRE"] == 4)
]["indice"].values[0]

# normalizamos el indice
df_ipc_trimestral["indice_normalizado"] = df_ipc_trimestral["indice"] / indice_base * 100

# nuevo dataframe con estos datos
df_merge = df_eph.merge(df_ipc_trimestral[["ANO4", "TRIMESTRE", "indice_normalizado"]], on=["ANO4", "TRIMESTRE"], how="left")

df_merge["P21_real"] = df_merge["P21"] / df_merge["indice_normalizado"] * 100

print(df_merge.shape)

print(df_merge.dtypes)
# PROBLEMA! NO EXISTE IPC DE 2016 :( veremos despues
print(df_merge[df_merge["ANO4"] >= 2017].head())

df_merge.to_csv("eph_limpio_con_ipc.csv", index=False)