import pandas as pd

# dedicado al formateo y obtencion de valores de IPC

archivo = "microdatos_2016_2025/IPC_trimestre_2017_2025/sh_ipc_05_26.xls"

excel = pd.ExcelFile(archivo)

print(excel.sheet_names)

df = pd.read_excel(archivo, sheet_name="Variación mensual IPC Nacional", header=None)

meses = df.iloc[5, 1:] #index location! fila 6 en excel, indice 5 porque pandas empieza en 0, lo mismo en la columna 1 = columna B de excel

variaciones = df.iloc[9, 1:]

ipc = pd.DataFrame({
    "periodo": meses.values,
    "variacion": variaciones.values
})

ipc = ipc.dropna()

ipc = ipc[ipc["periodo"] <= "2025-12-31"]

ipc["variacion"] = pd.to_numeric(ipc["variacion"])

ipc["indice"] = (100 * (1 + ipc["variacion"] / 100).cumprod())

ipc["ANO4"] = ipc["periodo"].dt.year
ipc["TRIMESTRE"] = ipc["periodo"].dt.quarter

ipc_trimestral = (ipc.groupby(
    ["ANO4", "TRIMESTRE"]
    ) ["indice"].mean().reset_index()
)

print(ipc_trimestral)

ipc_trimestral.to_csv(
    "microdatos_2016_2025/IPC_trimestre_2017_2025/ipc_trimestral_12017_42025.csv",
    index=False
)