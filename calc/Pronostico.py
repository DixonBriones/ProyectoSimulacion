import matplotlib
matplotlib.use('Agg')
import io
import base64
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Pronostico:

    def promedioMovil(self, x:str, y:str, xlbl:str, ylbl:str):
        # Convertir en lista los datos separandolos con una ,
        datosX = []
        datosY = []
        for i in x.split(','):
            datosX.append(float(i))
        for i in y.split(','):
            datosY.append(float(i))

        data = {xlbl: datosX, ylbl: datosY}

        movil = pd.DataFrame(data)
        # calculamos para la primera media móvil MMO_3
        for i in range(0,movil.shape[0]-2):
            movil.loc[movil.index[i+2],'MMO_3'] = np.round(((movil.iloc[i,1]+movil.iloc[i+1,1]+movil.iloc[i+2,1])/3),1)
        #  calculamos para la segunda media móvil MMO_4 
        for i in range(0,movil.shape[0]-3):
            movil.loc[movil.index[i+3],'MMO_4'] = np.round(((movil.iloc[i,1]+movil.iloc[i+1,1]+movil.iloc[i+2,1]+movil.iloc[i+3,1])/4),1)
        
        proyeccion = movil.iloc[movil.shape[0]-3:,[1,2,3]]
        p1,p2,p3 =proyeccion.mean()
        # incorporamos al DataFrame
        intervalo = datosX[1]-datosX[0]
        a = movil.append({xlbl:datosX[-1]+intervalo,ylbl:p1, 'MMO_3':p2, 'MMO_4':p3},ignore_index=True)
        # mostramos los resultados
        a['e_MM3'] = a[ylbl]-a['MMO_3']
        a['e_MM4'] = a[ylbl]-a['MMO_4']
         # calculamos el promedio de los cada una de las columnas de df
        m1,m2,m3,m4,m5,m6 =a.mean()
        mm3=a['MMO_3'].values[5]
        mm4=a['MMO_4'].values[5]
        # Grafica
        img = io.BytesIO()
        plt.figure(figsize=(10,5))
        plt.grid()
        plt.plot(a[ylbl],label=ylbl,marker='o', color='blue')
        plt.plot(a['MMO_3'],label='Media Móvil 3 años', marker='*', color='cyan')
        plt.plot(a['MMO_4'],label='Media Móvil 4 años', marker='+', color='red')
        plt.legend(loc=2)
        plt.savefig(img, format='png')
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()

        return(a,img_url, round(m5), round(m6), round(m4), round(m3), round(m2), round(m1),mm3,mm4)
    
    def suavizacionExponencial(self, x:str, y:str, xlbl:str, ylbl:str):
        # Convertir en lista los datos separandolos con una ,
        datosX = []
        datosY = []
        for i in x.split(','):
            datosX.append(float(i))
        for i in y.split(','):
            datosY.append(float(i))

        data = {xlbl: datosX, ylbl: datosY}

        movil = pd.DataFrame(data)
        alfa = 0.1
        unoalfa = 1. - alfa
        for i in range(0,movil.shape[0]-1):
            movil.loc[movil.index[i+1],'SN'] = np.round(movil.iloc[i,1],1)
        for i in range(2,movil.shape[0]):
            movil.loc[movil.index[i],'SN'] = np.round(movil.iloc[i-1,1],1)*alfa + np.round(movil.iloc[i-1,2],1)*unoalfa
        i=i+1
        intervalo = datosX[1]-datosX[0]
        p1=0
        p2=np.round(movil.iloc[i-1,1],1)*alfa + np.round(movil.iloc[i-1,2],1)*unoalfa
        a = movil.append({xlbl:datosX[-1]+intervalo,ylbl:p1, 'SN':p2},ignore_index=True)
        
        return a

    def regresionLineal(self, x:str, y:str, xlbl:str, ylbl:str):
        # Convertir en lista los datos separandolos con una ,
        datosX = []
        datosY = []
        for i in x.split(','):
            datosX.append(float(i))
        for i in y.split(','):
            datosY.append(float(i))

        data = {xlbl: datosX, ylbl: datosY}
        a = pd.DataFrame(data)
        x = a.index.values
        y = a[ylbl]
        # ajuste de la recta (polinomio de grado 1 f(x) = ax + b)
        p = np.polyfit(x,y,1) # 1 para lineal, 2 para polinomio ...
        yAjuste = p[0]*x + p[1]
        plt.plot(x,y,'b.')
        # Dibujamos la recta de ajuste
        plt.plot(x,yAjuste, 'g-')
        img = io.BytesIO()
        plt.title('Ajuste lineal por mínimos cuadrados')
        plt.xlabel('Eje x')
        plt.ylabel('Eje y')
        plt.legend(('Datos experimentales','Ajuste lineal',), loc="upper left")
        plt.savefig(img, format='png')
        plt.clf()
        img.seek(0)

        img_url2 = base64.b64encode(img.getvalue()).decode()
        
        return img_url2

    def regresionLinealCuadratica(self, x:str, y:str, xlbl:str, ylbl:str):
        # Convertir en lista los datos separandolos con una ,
        datosX = []
        datosY = []
        for i in x.split(','):
            datosX.append(float(i))
        for i in y.split(','):
            datosY.append(float(i))

        data = {xlbl: datosX, ylbl: datosY}
        a = pd.DataFrame(data)
        x = a.index.values
        y = a[ylbl]

        p = np.polyfit(x,y,2)

        y_ajuste = p[0]*x*x + p[1]*x + p[2]
        # dibujamos los datos experimentales de la recta 
        img = io.BytesIO()
        plt.plot(x,y,'b.')
        # Dibujamos la curva de ajuste
        plt.plot(x,y_ajuste, 'g-')
        plt.title('Ajuste Polinomial por mínimos cuadrados')
        plt.xlabel('Eje x')
        plt.ylabel('Eje y')
        plt.legend(['Datos experimentales','Ajuste Polinomial'], loc="upper left")
        plt.savefig(img, format='png')
        plt.clf()
        img.seek(0)
        img_url3 = base64.b64encode(img.getvalue()).decode()
        return img_url3
                

# pro = Pronostico()
# pro.regresionLinealCuadratica(
#     '2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017',
#     '5501.0, 6232.7, 8118.3, 10137.00, 10449.50, 12794.60, 9939.10,13193.00, 16036.2, 18496.90, 18709.30, 19363.50, 16521.50, 15175.40,16927.00',
#     'Año','Exportaciones')
# # print(a)