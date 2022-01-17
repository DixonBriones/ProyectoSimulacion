import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

class Estadistica:
    """
    Clase estadistica que se encarga de realizar diferentes
    calculos estadisticos sobre el proyecto de Muertes por diabetes
    """
    def __init__(self):
        self.df = pd.read_csv('informacion/muertesdiabetes.csv', sep=";")
    
    def datosExcel(self):
        """
        funcion que retorna el dataframe
        """
        return self.df

    def graficoGeneral(self):
        """
        Funcion que retorna la grafica general de las muertes por provincias
        """
        img = io.BytesIO()
    

        distritos = self.df['Provincia']
        dolares = []
        for i in distritos:
            suma = self.df.loc[self.df['Provincia'] == i, ['Total']].sum()[0]
            dolares.append(suma)

        plt.figure(figsize=(10,5))
        plt.bar(distritos, dolares, color='green')
        plt.title('Casos reportados de muertes por diabetes del 2014-2019')
        plt.xticks(rotation=80)
        plt.ylabel('Total casos')
        plt.savefig(img, format='png')
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()
        return img_url

    def graficoTop10(self):
        """
        Funcion que retorna el top 10 con las provincias que mas muertes tienen 
        """
        img = io.BytesIO()
        
        df2 = self.df.sort_values('Total',ascending=False)
        x=df2.head(10)

        plt.figure(figsize=(10,5))
        plt.bar(x['Provincia'], x['Total'], color='blue')
        plt.title('Casos reportados de muertes por diabetes del 2014-2019')
        plt.xticks(rotation=80)
        plt.ylabel('Total casos')

        plt.savefig(img, format='png')
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()
        return img_url
        
    def graficoLineas(self):
        """
        Funcion que devuelve la cantidad de contagios por años en grafico de lineas
        """
        img = io.BytesIO()

        x = self.df["Provincia"]
        t1= self.df["2014"]
        t2= self.df["2015"]
        t3= self.df["2017"]
        t4= self.df["2018"]
        t5= self.df["2019"]

        plt.figure(figsize=(10,5))
        plt.plot(x,t1,x,t2,x,t3,x,t4,x,t5,marker='o')
        plt.xlabel('Provincia')
        plt.ylabel('Cantidad de muertes')

        plt.legend(("2014","2015","2016","2017","2018","2019"), prop = {'size':10})
        
        plt.savefig(img, format='png')
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()
        return img_url

