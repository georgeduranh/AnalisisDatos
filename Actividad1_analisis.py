
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
from scipy.stats.mstats import winsorize

from sklearn import preprocessing

df = pd.read_csv('Casos_positivos_de_COVID-19_en_Colombia.csv')


print("***Análisis preliminar del dataset***")
#print(df.describe())

#Atributos de entrada
print("\n ***Atributos de entrada***")
atributos = df.columns.tolist()
print(atributos)

#Valores atributos 
#print("\n ***Valores atributos***")
#print(df.groupby("Nombre departamento").size())

df["Tipo de contagio"].replace(('En Estudio'),('En estudio'),inplace=True)
df["Tipo de contagio"].replace(('EN ESTUDIO'),('En estudio'),inplace=True)

df["Tipo de contagio"].replace(('RELACIONADO'),('Relacionados'),inplace=True)

df["Estado"].replace(('moderado'),('Moderado'),inplace=True)
df["Estado"].replace(('LEVE'),('Leve'),inplace=True)

#Bogota
bog = df["Nombre departamento"] == "BOGOTA"  
df = df[bog]


positivos_dia = df.groupby("Fecha de diagnóstico").size()
positivos_dia.reset_index().to_csv('pruebas.csv')

print(positivos_dia)
#year = df["fecha reporte web"]<"1/1/2021 0:00:00"
#df= df[year] 


print("***Contagiados***")
print(df['Edad'].describe())

rec = 0.05

media = df["Edad"].mean()
mediana = df["Edad"].median()
moda = df["Edad"].mode()
media_recortada = stats.trim_mean(df["Edad"], rec)
var = df["Edad"].var(ddof=0)
iqr = df["Edad"].quantile(0.75) - df["Edad"].quantile(rec)
mediaWin = winsorize(df["Edad"], limits=[rec, rec])


print("""
    Media: %d
    Mediana: %d
    Moda: %d
    Media_recortada: %d
    Varianza: %d
    IQR: %d
    Media Win: %d
    Std win: %d
    Var win: %d
""" % (media,mediana,moda,media_recortada, var,iqr, mediaWin.mean(), mediaWin.std(ddof=0), mediaWin.var(ddof=0)))


x = df["Estado"] == "Fallecido"  
fallecidos = df[x]


print("\n***Fallecidos***")
print(fallecidos['Edad'].describe())

media = fallecidos["Edad"].mean()
mediana = fallecidos["Edad"].median()
moda = fallecidos["Edad"].mode()
media_recortada = stats.trim_mean(fallecidos["Edad"], rec)
mediaWin = winsorize(fallecidos["Edad"], limits=[rec, rec])

var = fallecidos["Edad"].var(ddof=0)
iqr = fallecidos["Edad"].quantile(0.75) - fallecidos["Edad"].quantile(0.25)

print("""
    Media: %d
    Mediana: %d
    Moda: %d
    Media_recortada: %d
    Varianza: %d
    IQR: %d
    Media Win: %d
    Std win: %d
    Var win: %d
""" % (media,mediana,moda,media_recortada, var,iqr, mediaWin.mean(), mediaWin.std(ddof=0), mediaWin.var(ddof=0)))

## Grafica dsitribución por edades 

fig, axs = plt.subplots(nrows=2)
fig.suptitle('Cantidad Fallecidos vs Cantidad contagiados')
ax1 = sns.countplot(ax=axs[0], x="Edad", data=fallecidos, color="r")
ax2 = sns.countplot(ax=axs[1], x="Edad", data=df, color="b")
axs[0].set_title("Fallecidos", horizontalalignment="left")
axs[1].set_title("Contagiados", horizontalalignment="left")
axs[0].set_xticklabels(axs[0].get_xticklabels(),rotation=35, fontsize=8)
axs[1].set_xticklabels(axs[1].get_xticklabels(),rotation=35, fontsize=8)
plt.show()


winf= winsorize(fallecidos["Edad"], limits=[rec, rec])
wina= winsorize(df["Edad"], limits=[rec, rec])

#print(winf)

# ## Grafica dsitribución por winsorizadas 
# fig, axs = plt.subplots(nrows=2)
# fig.suptitle('Fallecidos vs contagiados')
# ax1 = sns.scatterplot(ax=axs[0], data=winf)
# ax2 = sns.scatterplot(ax=axs[1], data=wina)
# axs[0].set_title("Fallecidos")
# axs[1].set_title("Contagiados")
# axs[0].set_xticklabels(axs[0].get_xticklabels(),rotation=35)
# axs[1].set_xticklabels(axs[1].get_xticklabels(),rotation=35)
# plt.show()


fig, axs = plt.subplots(ncols=2)
fig.suptitle('Contagiados  vs Fallecidos')
ax1 = sns.boxplot(ax=axs[0], y='Edad', data=df, color="b")
ax2 = sns.boxplot(ax=axs[1], y='Edad', data=fallecidos, color="r")
plt.show()


# bins = [0, 4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 115]
# names = ["0-4", "5-9", "10-14", "15-19", " 20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80 y más"]



# corr = df.loc[:, ['Edad', 'Estado']]

# corr.Estado.replace(('Leve'),('1'),inplace=True)
# corr.Estado.replace(('Moderado'),('2'),inplace=True)
# corr.Estado.replace(('Grave'),('3'),inplace=True)
# corr.Estado.replace(('Fallecido'),('4'),inplace=True)
# #print(corr.head())
# ## Fallecidos 
# corr["Edad"] = pd.cut(corr["Edad"], bins, labels = names)

# estado = pd.get_dummies(corr, columns = ["Estado"], drop_first = False)
# print(estado.head())

# print(estado.corr())


# edades = estado.groupby("Edad").size()
# print(edades)
# sns.set_theme(style="darkgrid")
# ax = sns.scatterplot(x="Edad", y="Estado", data=estado)
# plt.title('Cantidad de fallecidos por rangos de edad  por cada 100mil habitantes')
# plt.show()   ######### No olvidar quitar comentario


# ##RAngos
#poblacion = pd.read_csv('osb_piramide_poblacional_2020.csv')

bins = [0, 4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 115]
names = ["0-4", "5-9", "10-14", "15-19", " 20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80 y más"]
poblacion = [493287,482823,490700,550879, 711590, 749246,673163,613704,539925,477123,468097,435209,352709,260464,183141,119787,142108]



## Fallecidos 
fallecidos["Edad"] = pd.cut(fallecidos["Edad"], bins, labels = names)
rango_edades = fallecidos.groupby("Edad").size()
rango_edades = rango_edades.tolist()

c = np.divide(rango_edades, poblacion)*100000
c = c.tolist()

data = [names, c]
numpy_array = np. array(data)
transpose = numpy_array.T
data= pd.DataFrame(transpose, columns=["RangosEdad", "conteo"])
data["conteo"] = data["conteo"].astype(float)





## contagiados 
df["Edad"] = pd.cut(df["Edad"], bins, labels = names)
rango_edades_df = df.groupby("Edad").size()
rango_edades_df = rango_edades_df.tolist()

c_df = np.divide(rango_edades_df, poblacion)*100000
c_df = c_df.tolist()

data_df = [names, c_df]
numpy_array_df = np. array(data_df)
transpose_df = numpy_array_df.T
data_df= pd.DataFrame(transpose_df, columns=["RangosEdad", "conteo"])
data_df["conteo"] = data_df["conteo"].astype(float)


# # sns.set_theme(style="darkgrid")
# # ax = sns.barplot(x="RangosEdad", y="conteo", data=data)
# # plt.title('Cantidad de fallecidos por rangos de edad  por cada 100mil habitantes')
# # plt.show()   ######### No olvidar quitar comentario


# ## Grafica dsitribución por 100mil habitantes rangos de edads

fig, axs = plt.subplots(nrows=2)
fig.suptitle('Cantidad de fallecidos por rangos de edad  por cada 100 mil habitantes')
ax1 = sns.barplot(ax=axs[0], x="RangosEdad", y="conteo", data=data, color="r")
ax2 = sns.barplot(ax=axs[1], x="RangosEdad", y="conteo", data=data_df, color="b")
axs[0].set_title("Fallecidos", horizontalalignment="left")
axs[1].set_title("Contagiados", horizontalalignment="left")
axs[0].set_xticklabels(axs[0].get_xticklabels(),rotation=0, fontsize=8)
axs[1].set_xticklabels(axs[1].get_xticklabels(),rotation=0, fontsize=8)
plt.show()



