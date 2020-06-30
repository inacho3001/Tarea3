import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import stats
from scipy.optimize import curve_fit


#Lectura de los datos para generar los modelos de las funciones de densidad marginales
data = np.genfromtxt('xy.csv',delimiter=',')
data = np.delete(data, 0, axis=0)
data = np.delete(data, 0, axis=1)

#Obtencion de los valores para cada funcion de densidad marginal con los datos suministrados
X = np.linspace(5,15,11)
Y = np.linspace(5,25,21)

fX = np.sum(data, axis=1)
fY = np.sum(data, axis=0)

#Graficacion de las funciones de densidad marginales para identificar el mejor ajuste
plt.plot(X,fX)
plt.title("Funcion de densidad marginal de X con datos")
plt.xlabel("x")
plt.ylabel("fX(x)")
plt.savefig('../Graficas/X.png')

plt.close()

plt.plot(Y,fY)
plt.title("Funcion de densidad marginal de Y con datos")
plt.xlabel("y")
plt.ylabel("fY(y)")
plt.savefig('../Graficas/Y.png')

plt.close()

#Definicion de la funcion de densidad con distribucion normal y la funcion de densidad conjunta
def normal(x, mu, sigma):
    return 1/(np.sqrt(2*np.pi*sigma**2))*np.exp(-(x-mu)**2/(2*sigma**2))

def conjunta(x, y, mu_x, mu_y, sigma_x, sigma_y):
    return 1/(2*np.pi*sigma_x*sigma_y)*np.exp(-1/2*((x-mu_x)**2/sigma_x**2+(y-mu_y)**2/sigma_y**2))

#Obtencion de parametros para las funciones de densidad marginales de X y Y
paramX,_ = curve_fit(normal, X, fX)
paramY,_ = curve_fit(normal, Y, fY)

#Obtencion de los modelos con el ajuste a distribucion normal y sus graficas
fX_ajuste = normal(X, paramX[0], paramX[1])
fY_ajuste = normal(Y, paramY[0], paramY[1])

plt.plot(X,fX_ajuste, 'green')
plt.title("Funcion de densidad marginal de X con el modelo encontrado")
plt.xlabel("x")
plt.ylabel("fX(x)")
plt.savefig('../Graficas/X_ajuste.png')

plt.close()

plt.plot(Y,fY_ajuste, 'green')
plt.title("Funcion de densidad marginal de Y con el modelo encontrado")
plt.xlabel("y")
plt.ylabel("fY(y)")
plt.savefig('../Graficas/Y_ajuste.png')

plt.close()

#Lectura de los datos para obtener los momentos de las variables aleatorias multiples
data_m = np.genfromtxt('xyp.csv',delimiter=',')
data_m = np.delete(data_m, 0, axis=0)

#Obtencion de la correlacion
correlacion = 0
for row in data_m:
    mul = row[0] * row [1] * row [2]
    correlacion += mul

#Obtencion de la covarianza
muX = paramX[0]
muY = paramY[0]

covarianza = 0
for row in data_m:
    mul = (row[0]-muX) * (row[1]-muY) * row[2]
    covarianza += mul

#Obtencion del coeficiente de correlacion
sigmaX = paramX[1]
sigmaY = paramY[1]

coef_correlacion = covarianza/(sigmaX*sigmaY)

#Obtencio de los datos para generar el grafico de la funcion de densidad conjunta en 3D y su grafica
x, y = np.meshgrid(X,Y)

z = conjunta(x, y, muX, muY, sigmaX, sigmaY)

plt.figure()
ax = plt.axes(projection='3d')

ax.plot_surface(x, y, z, cmap='plasma',edgecolor = 'none')
ax.set_title("Funcion de densidad conjunta con el modelo encontrado")
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('fX,Y(x,y)')
plt.savefig('../Graficas/conjunta.png')

plt.close()

#Impresion de resultados
print('----------------------------------------------------------------')

print("Los parametros para la funcion de densidad marginal de X son: ")
print("mu = " + str(muX))
print("sigma = " + str(sigmaX))
print("Los parametros para la funcion de densidad marginal de Y son: ")
print("mu = " + str(muY))
print("sigma = " + str(sigmaY))

print('----------------------------------------------------------------')

print("El valor para la correlacion es: " + str(correlacion))
print("El valor para la covarianza es: " + str(covarianza))
print("El valor para el coeficiente de correlacion es: " + str(coef_correlacion))

print('----------------------------------------------------------------')