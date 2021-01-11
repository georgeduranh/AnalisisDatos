library(robustbase)
library(MASS)


print(getwd())
## Cambiar ruta
setwd("D:\\1- Master - BigData\\Asignaturas\\4. Analisis e interpretación de datos\\Actividades\\Actividad 1") 
print(getwd())
Prueba <- read.csv(file = 'Pruebas_positivos_excel.csv', sep = ";")
head(Prueba)


y=Prueba["Casos.positivos"]
x=Prueba["Pruebas.diarias"]

plot(Prueba)

resultado = ltsReg(x,y)
print(resultado)

cor(x,y)

yestimada = 0.2404*x-88.2145

x2 <- data.frame(x, yestimada)

par(new=TRUE)
plot(x2, type="l",  xaxt='n',  yaxt='n', ann=FALSE)


res = residuals(resultado)
x3 <- data.frame(x, res)
plot(x3)




