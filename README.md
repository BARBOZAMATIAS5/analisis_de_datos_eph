# Contenido del repositorio

## Archivos Python

### `build_eph.py`

Se encarga de construir el DataFrame utilizado para el análisis del proyecto a partir de los datos de la Encuesta Permanente de Hogares (EPH) del INDEC, desde el 2.º trimestre de 2016 hasta el 4.º trimestre de 2025.

**Columnas utilizadas:**

- ANO4 -> año
- TRIMESTRE -> trimestre
- AGLOMERADO -> muestra - PAG. 18
- ESTADO -> actividad - PAG. 22
- P21 -> ingreso principal
- CH04 -> sexo - PAG. 19
- CH06 -> edad - PAG. 19
- NIVEL_ED -> nivel educativo - PAG. 21
- PP04A -> tipo de trabajo (1. ESTATAL/2. PRIVADO/3. OTRO TIPO) - PAG. 24
- PONDERA -> ponderacion (importancia relativa, asignacion de "peso")

**Aglomerados analizados:**

- 23 → Gran Salta
- 29 → Gran Tucumán - Tafí Viejo

**Salida:**  
`microdatos_2016_2025/*.csv`

> **Importante:** Usar el archivo `EPH_registro_3T2024.pdf` para comprender los datos.
---

### `format_inflation.py`

Obtiene los índices mensuales del IPC y los transforma a índices trimestrales para el período comprendido entre el 1.º trimestre de 2017 y el 4.º trimestre de 2025.

**Salida:**  
`microdatos_2016_2025/IPC_trimestre_2017_2025/*.csv`

---

> **Importante:** Cree una carpeta donde van guardados los archivos csv que cree, no movi el eph_limpio_con_ipc.csv

### `analize_eph.py`

Realiza el preprocesamiento de los datos:

- Eliminación de registros no válidos.
- Tratamiento de valores faltantes.
- Definición del trimestre base (4T 2025).
- Normalización de índices.
- Combinación de los DataFrames generados previamente.
- Creación de las columnas:
  - `indice_normalizado`
  - `P21_real`

**Salida:**  
Archivo CSV en la carpeta principal del proyecto.

> **Importante:** No se dispone de índices de IPC para 2016, por lo que los valores correspondientes a ese año veremos despues de encontrarlos.

---

### `tp_eph.py`

Archivo principal del proyecto enfocado en la construcción de las tasas macroeconómicas agregadas. 

Calcula la evolución temporal de los indicadores del mercado laboral aplicando de forma estricta los factores de expansión (`PONDERA`) para reflejar los valores poblacionales reales del NOA.

- **Indicadores calculados:** Tasa de Actividad, Tasa de Empleo, Tasa de Desocupación e Ingreso Medio Real de la ocupación principal.
- **Salida:** `datos/reporte_indicadores_mercado.csv`

---

### `tp_eph_univariado.py`

Módulo dedicado al análisis univariado descriptivo de la distribución del ingreso de la ocupación principal (`P21_real`). 

Dado que las funciones tradicionales no consideran la representatividad muestral, implementa algoritmos de cálculo ponderado para analizar la estructura interna de los ingresos de la población ocupada con rendimientos positivos.

- **Métricas calculadas:** Media ponderada, Mediana ponderada (Percentil 50), Cuartiles de posición (Q1 - Percentil 25 y Q3 - Percentil 75) y Desvío Estándar ponderado.
- **Salida:** `datos/univariado_ingresos_historico.csv`

---

### `tp_eph_multivariado.py`

Se encarga del análisis multivariado mediante el cruce simultáneo de tres o más variables físicas y socio-demográficas, permitiendo evaluar la interacción y disparidad de los indicadores en subgrupos específicos de la población.

**Dimensiones analizadas:**
1. **Sexo (`CH04`):** Evolución de todas las tasas oficiales e ingresos segmentados por Varón y Mujer.
2. **Nivel Educativo (`NIVEL_ED`):** Comportamiento del mercado laboral y retornos salariales según el máximo nivel de instrucción alcanzado.
3. **Tipo de Trabajo / Sector (`PP04A`):** Evaluación del ingreso medio real comparando el desempeño del sector Estatal/Público frente al sector Privado.

**Salidas:** - `datos/multivariado_mercado_sexo.csv`
- `datos/multivariado_mercado_educacion.csv`
- `datos/multivariado_ingresos_tipo_trabajo.csv`

> **Nota metodológica para visualización:** Los archivos de salida están optimizados como matrices limpias para la posterior fase de generación de gráficos temporales, diagramas de caja y estructuras comparativas.

---

### `tp_eph_graficos.py`

Archivo para realizar el desarrollo de los graficos que vamos a utilizar en el informe.

