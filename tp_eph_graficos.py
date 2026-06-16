# hacer los graficos dentro de este archivo (podes crear otros archivos asi te queda mas ordenado)

#OJO: FILTRA EL AÑO 2016 POR QUE NO TIENEN DATOS DE ESE AÑO.
#ANTES DE GRAFICAR, TENES QUE ELIMINAR EL AÑO 2016 PARA QUE NO NOS QUEDE UN HUECO.
#CUALQUIER COSA LO VEMOS TODOS JUNTOS EN UNA REUNION ANTES DE HACER LA ENTREGA
import pandas as pd

#usar estos archivo csv con los analisis univariados y multivariados.
# csvs con los respectivos analisis de los salarios segun tipo de trabajo, sexo o educacion (podes hacer los 3 o uno depende que tan extenso nos quede el informe) 
df = pd.read_csv("datos/multivariado_ingresos_tipo_trabajo.csv")
df = pd.read_csv("datos/multivariado_mercado_educacion.csv")
df = pd.read_csv("datos/multivariado_mercado_sexo.csv")


#csv con lo analisis de la: tasa de desocupación, la tasa de empleo, la tasa de actividad y los ingresos de la población
df = pd.read_csv("datos/reporte_indicadores_mercado.csv")


# csv con los analisis con las medidas de tendencias central (media - mediana), de posicion (en quartiles) y el desvio estandar
df = pd.read_csv("datos/univariado_ingresos_historico.csv")

