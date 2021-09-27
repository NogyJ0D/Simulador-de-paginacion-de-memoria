# Autor: Valentin Giarra / NogyJ0D  -  2021
# Idea tomada de: https://www.youtube.com/watch?v=9mgcXXE5y74
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PyQt5 import uic
from MainWindow import * 

Total, Ejecutando, Esperando, Terminado = [], [], [], []

class Ventana(QMainWindow):                 # Clase heredada de QMainWindow (Constructor de ventanas)
    def __init__(self):                             # Metodo constructor
        QMainWindow.__init__(self)                          # Iniciar el objeto QMainWindow
        # self.ui = uic.loadUi("Procesos.ui", self)         # Cargar la configuración del .ui en el objeto
        self.ui = Ui_MainWindow()                           # Cargar el archivo de interfaz ya convertido a .py
        self.ui.setupUi(self)                               # '                                               '

        self.ui.BtnAgrAgr.clicked.connect(self.Agregar)     # Al tocar el botón de Agregar, ir a la función Agregar()
        self.ui.BtnFinFin.clicked.connect(self.Eliminar)    # Al tocar el botón de Finalizar, ir a la función Eliminar()

    def Agregar(self):                          # AgregarProceso()
        global Total, Esperando, Terminado          # Traer variables globales
        InpN = self.ui.InpAgrNom.currentText()      # El contenido de esa caja, tomalo
        InpC = self.ui.InpAgrCan.value()            # '                              '
#
        if (len(Total) + InpC) < 21:                # Si la cantidad de elementos en Total sumada a la cantidad del proceso es menor a 21:
            for i in range(InpC):                   #   Para cada elemento del proceso ingresado, segun la cantidad elegida:
                Total.append(InpN)                  #       Agregarlos a Total
            Ejecutando.append(InpN)                 #   Agregar la letra del proceso a Ejecutando
            self.Estado()                           #   Acomodar los textos
        elif (len(Total) + InpC) >= 20:             # Si la cantidad de elementos en Total sumada a la cantidad del proceso es mayor o igual a 20:
            Esperando.append(str(f'{InpN}-{InpC}')) #   Agregá el proceso elegido y su cantidad a la zona de espera
            self.Falta(InpN)                        #   Como no puede entrar, notificar
            self.Estado()                           #   Acomodar los textos
            if InpN in Terminado:                   #   Si el proceso ingresado no puede entrar, pero ya fue finalizado anteriormente:
                Terminado.remove(InpN)              #       Sacalo de Terminado

    def Estado(self):                                   # EstadoDeLosTextos()
        global Total, Esperando, Ejecutando, Terminado      # Traer las variables globales

        self.ui.LblIni.setText('')                          # Ponelo en blanco
        for item in Ejecutando:                             # Para cada elemento de la variable:
            self.ui.LblIni.append(item)                     #   Metelo a la caja

        self.ui.LblEsp.setText('')                          # Ponelo en blanco
        for item in Esperando:                              # Para cada elemento de la variable:
            self.ui.LblEsp.append(item)                     #   Metelo a la caja

        self.ui.LblFin.setText('')                          # Ponelo en blanco
        for item in Terminado:                              # Para cada elemento de la variable:
            self.ui.LblFin.append(item)                     #   Metelo a la caja

        self.ui.LblEso.setText('')                          # Ponelo en blanco
        for item in Total:                                  # Para cada elemento de la variable:
                self.ui.LblEso.append(item)                 #   Metelo a la caja

        self.ui.LblTot.setText('Total: ' + str(len(Total))) # Acomodá la leyenda de abajo

    def Eliminar(self):                                             # EliminarProceso()
        global Total, Ejecutando, Esperando, Terminado                  # Traer las variables globales
        InpN = self.ui.InpFinNom.currentText()                          # El contenido de esa caja, tomalo

        if InpN in Ejecutando:                                          # Si el proceso elegido está siendo ejecutado:
            for i in range(len(Total)):                                 #   Revisar todos los elementos de Total:
                if InpN in Total:                                       #       Si el proceso está en Total:
                    Total.remove(InpN)                                  #           Eliminalo
            Ejecutando.remove(InpN)                                     #   Borrarlo de Ejecutando
            Terminado.append(InpN)                                      #   Y meterlo en Finalizando
        else: return 0
        if len(Total) <= 20 and len(Total) > 0 and len(Esperando) > 0:  #   Si Total tiene 20 o menos elementos, si tiene mas de 0 (no está vacío), y hay objetos en espera:
            for item2 in Esperando:                                     #       Para cada item en espera:
                item = item2.split('-')                                 #           Separar el item en 2, el nombre por un lado y su cantidad por otro
                if (int(item[1]) + len(Total)) <= 20:                   #           Si la cantidad de ese elemento sumada a la cantidad del Total es 20 o menos:
                    Esperando.remove(item2)                             #               Eliminá el proceso de Esperando
                    Ejecutando.append(str(item[0]))                     #               Metelo en Ejecutando
                    for j in range(int(item[1])):                       #               Por la cantidad elegida para el proceso en espera:
                        Total.append(item[0])                           #                   Agregar la letra al Total
        self.Estado()                                                   #   Acomodar los textos
    
    def Falta(self, InpN):                                                                                                  # FaltaEspacio()
        Faltante = QMessageBox()                                                                                                # Crear la caja de alerta
        Faltante.setIcon(QMessageBox.Warning)                                                                                   # Ponerle un ícono predeterminado
        Faltante.setText('No hay espacio suficiente (20 procesos) para correr otro proceso. ' + InpN + ' se pondrá en espera.') # Asignar su texto
        Faltante.setWindowTitle('Relajá un poco changó')                                                                        # Asignar el nombre de la ventanita
        Faltante.setStandardButtons(QMessageBox.Ok)                                                                             # Crear el botón de Ok
        Faltante.setDefaultButton(QMessageBox.Ok)                                                                               # X
        Salir = Faltante.exec()                                                                                                 # Cerrar si se toca el botón

app = QApplication(sys.argv)    # Iniciar la aplicacion
GUI = Ventana()                 # Crear un objeto de la clase
GUI.show()                      # Mostrar la ventana
app.exec_()                     # Ejecutar la aplicacion