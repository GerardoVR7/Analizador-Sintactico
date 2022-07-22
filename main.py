
import re
from PyQt5 import uic
from PyQt5 import QtWidgets
from diagram import Diagram

class Pila:
    def __init__(self):
        """ Crea una pila vacía. """
        self.p = ['S']

    def start(self):
        self.p = ['S']

    def apilar(self, x):
        """ Agrega el elemento x a la pila. """
        self.p.append(x)

    def desapilar(self):
        """ Devuelve el elemento tope y lo elimina de la pila.
            Si la pila está vacía levanta una excepción. """
        try:
            return self.p.pop()
        except IndexError:
            raise ValueError("La pila está vacía")

    def es_vacia(self):
        """ Devuelve True si la lista está vacía, False si no. """
        return self.p == []

    def print_stack(self):
        '''Metodo para mostrar los elementos de la pila'''
        print(self.p)

    def ver(self):
        '''Metodo para ver lo que esta en la cima de la pila'''
        if not self.es_vacia():
            return self.p[len(self.p)-1]

    def large(self):
        '''Metodo para retornar el tamano de la pila'''
        return len(self.p)

class Analizador():
    pila = Pila()
    diagram = Diagram()
    flag_relation = 0
    count = 0
    use_relation = ''
    class_to_relation = ''
    class_to_relation_2 = ''
    items = []
    ayuda = []
    ayuda2 = []
    data1 = ''
    data2 = ''
    predict_table = [
        ["", "<", "nombre", "parametro", "tipo de dato", "metodos", "relacion", "Fin", "Clase", ":", ">", "a-Z", ",", "string", "-", "get", "()", "int", "float", "double", "+", "set",  "$"],
        ["S", ["Inicio", "N", "P", "TD", "M", "R", "Final"], "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["Inicio", ["MQ", "CLASS", "PP"], "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["N", "", ["NO", "PP", "VN"], "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["P", "", "", ["PA", "PP", "VN", "RC"], "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["TD", "", "", "", ["TT", "PP", "D", "RD"], "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["M", "", "", "", "", ["ME", "PP", "CM", "RM"], "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["R", "", "", "", "", "", ["RE", "PP", "VN", "PP", "VN"], "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["Final", "", "", "", "", "", "", ["F", "MQA"], "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["MQ", "<", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["CLASS", "", "", "", "", "", "", "", "Clase", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["NO", "", "nombre", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["PP", "", "", "", "", "", "", "", "", ":", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["F", "", "", "", "", "", "", "Fin", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["MAQ", "", "", "", "", "", "", "", "", "", ">", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["VN", "", "", "", "", "", "", "", "", "", "", ["LETRAS", "RI"], "", "", "", "", "", "", "", "", "", "", ""],
        ["PA", "", "", "parametro", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["RC", "", "", "", "vacio", "", "", "", "", "", "", "", ["C", "LETRAS", "RC"], "", "", "", "", "", "", "", "", "", "$"],
        ["TT", "", "", "", "tipo de dato", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["D", "", "", "", "", "", "", "", "", "", "", "", "", "D", "", "", "", "D", "D", "D", "", "", ""],
        ["RD", "", "", "", "", "vacio", "", "", "", "", "", "", ["C", "D", "RD"], "", "", "", "", "", "", "", "", "", "$"],
        ["ME", "", "", "", "", "metodos", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["CM", "", "", "", "", "", "", "", "", "", "", "", "", "", ["TM", "GS", "VN", "PR"], "", "", "", "", "", ["TM", "GS", "VN", "PR"], "", ""],
        ["RM", "", "", "", "", "", "vacio", "", "", "", "", "", ["C", "TM", "GS", "VN", "PR", "RM"], "", "", "", "", "", "", "", "", "", "$"],
        ["RE", "", "", "", "", "", "relacion", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["GS", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "GS", "", "", "", "", "", "GS", ""],
        ["PR", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "()", "", "", "", "", "", ""],
        ["C", "", "", "", "", "", "", "", "", "", "", "", ",", "", "", "", "", "", "", "", "", "", ""],
        ["LETRAS", "", "", "", "", "", "", "", "", "", "", "a-z|A-Z", "", "", "", "", "", "", "", "", "", "", ""],
        ["TM", "", "", "", "", "", "", "", "", "", "", "", "", "", "-", "", "", "", "", "", "+", "", ""],
        ["RI", "", "", "vacio", "vacio", "", "", "", "", "$", "", "a-z|A-Z", "", "", "", "", "vacio", "", "", "", "", "", "$"],
    ]

    def __init__(self):
        app = QtWidgets.QApplication([])
        self.window = uic.loadUi('Interfaz.ui')
        self.window.analizar.clicked.connect(self.entry)
        self.window.diagramUML.clicked.connect(self.diagram.crear)
        self.window.show()
        app.exec()

    def check_chain(self, chain):
        if self.flag_relation != 1:
            self.ayuda.clear()
        else: self.ayuda2.clear()
        self.items.clear()
        chain = chain.split("\n")
        print(chain)
        print('here')
        for i in chain:
            print(i)
            aux = i.split("\t")
            if len(aux) == 1:
                self.items.append(aux[0])
            else:
                self.items.append(aux[1])
        chain = self.items.copy()
        self.items.clear()
        for i in chain:
            print(i)
            aux = i.split(" ")
            print(aux)
            for y in aux:
                if y == '':
                    print('se identifico un vacio')
                else:
                    if y[0] == "+" or y[0] == "-":
                        self.items.append(y[0])
                        self.items.append(y[1:4])
                        self.items.append(y[4:-2])
                        self.items.append(y[-2:])
                    else:
                        self.items.append(y)
        chain = self.items.copy()
        self.items.clear()
        for i in chain:
            if i == "<Clase":
                self.items.append(i[0])
                self.items.append(i[1:6])
            elif i == "Fin>":
                self.items.append(i[:-1])
                self.items.append(i[3])
            else:
                self.items.append(i)
        chain = self.items.copy()
        self.items.clear()
        aux = ""
        aux2 = ""
        for i in chain:
            if i == "tipo" or i == "de" or  i == "dato":
                if i == "dato":
                    aux = str(i)
                    aux2 = aux2 +  aux
                else:
                    aux = str(i) + " "
                    aux2 = aux2 +  aux
                if aux2 == "tipo de dato":
                    self.items.append(aux2)
            else:
                self.items.append(i)

        print(self.items)
        if self.flag_relation != 1:
            self.ayuda = self.items.copy()
        else: self.ayuda2 = self.items.copy()

    def check_structure(self):
        self.flags = 0
        for i in self.items:
            if i == "Clase" or i == "<Clase":
                self.flags += 1
            elif i == "nombre":
                self.flags += 1
            elif i == "parametro":
                self.flags += 1
            elif i == "tipo de dato":
                self.flags += 1
            elif i == "metodos":
                self.flags += 1
            elif i == "relacion":
                self.flags += 1
            elif i == "Fin" or i == "Fin>":
                self.flags += 1

        for i in range(len(self.items)-1):
            if self.items[i] == ":":
                if self.items[i+1] == "parametro":
                    self.flags +=  1
                elif self.items[i+1] == "tipo de dato":
                    self.flags +=  1
                elif self.items[i+1] == "metodos":
                    self.flags +=  1
                elif self.items[i+1] == "relacion":
                    self.flags +=  1
                elif self.items[i+1] == "Fin":
                    self.flags +=  1
                elif self.items[i+1] == ":":
                    self.flags += 1

        for i in range(len(self.items)-1):
            if self.items[i] == "relacion":
                if self.items[i+1] == ":":
                    # print('uso de la clase')
                    print(self.items[i+2])
                    self.use_relation = self.items[i+2]
                    # print('clase a apuntar')
                    print(self.items[i+4])
                    if self.flag_relation != 1:
                        self.class_to_relation = self.items[i+4]
                    else: self.class_to_relation_2 = self.items[i+4]

        if self.flag_relation == 1:
            if self.class_to_relation == self.class_to_relation_2:
                print('RELACION A LA MISMA CLASE ES INCORRECTO')
                self.flags += 1

        if self.flags == 7:
            print("Estructura correcta")
            return True
        else:
            print("Estructura incorrecta")
            return False

    def get_data(self):
        if self.flags == 7:
            self.diagram.get(self.ayuda, self.ayuda2)
            self.diagram.identifier()
            self.flag_relation = 0


    def search(self, cima, terminal):
        position1 = 0
        position2 = 0
        for i in range(30):
            if self.predict_table[i][0] == cima:
                position1 = i
        for i in range(22):
            if self.predict_table[0][i] == terminal:
                position2 = i
        return position1, position2

    def identifier(self):
        self.pila.print_stack()
        self.items.reverse()
        self.aux = False
        self.count = 0

        while self.pila.es_vacia() == False:
            character = self.items[len(self.items)-1]
            cima = self.pila.desapilar()

            x, y = self.search(cima, character)
            print(cima, character)
            # print(x, y)

            if self.predict_table[x][y] == "vacio":
                cima = self.pila.desapilar()
                print(cima, character)
                # print('entra')
                x, y = self.search(cima, character)

            if cima == "VN":
                if self.check_letras(character) == False:
                    print("ERROR: Expected a word")
                    break

            elif cima == "RC":
                if self.check_RC(character) == False:
                    print("ERROR: Expected a word")
                    break

            elif self.predict_table[x][0] == cima and self.predict_table[0][y] == character:
                if (type(self.predict_table[x][y])) == list:
                    aux = ((self.predict_table[x][y])[::-1])
                    for i in aux:
                        self.pila.apilar(i)

                else:
                    self.items.pop()

                self.pila.print_stack()
            else:break
        self.pila.print_stack()
        self.items.pop()

    def entry(self, use):
        chain = ''
        for i in range(2):
            if i ==  0:
                chain = self.window.plainTextEdit.toPlainText()
                self.data1 = chain
            elif i == 1:
                self.flag_relation = 1
                chain = self.window.plainTextEdit_2.toPlainText()
                self.data2 = chain
            self.pila.start()
            self.pila.print_stack()
            print('Pop')
            print('Push')
            self.check_chain(chain)
            if len(self.items) != 0:
                # se agrega la gramatica inicial S
                valor_pila = self.pila.ver()
                if valor_pila == 'S':
                    if self.check_structure() is True:
                        self.identifier()
                    else:
                        print("CHECAR LA ESTRUCTURA VUELVA A INTENTAR")
            else:
                print('cadena ingresada incorrecta')

        self.get_data()

    def check_letras(self, input):

        aux = ((self.predict_table[15][11])[::-1])
        for i in aux:
            self.pila.apilar(i)

        self.pila.print_stack()

        expression = re.compile(f"^([A-z][A-z | , A-z | \s]*)")
        result = re.fullmatch(expression, input)
        if result == None:
            print("Cadena incorrecta")
            return False
        else:
            print("Cadena correcta")
            self.pila.desapilar()
            self.pila.desapilar()
            self.items.pop()
            return True

    def check_RC(self, input):

        aux = ((self.predict_table[17][12])[::-1])
        for i in aux:
            self.pila.apilar(i)

        self.pila.print_stack()

        expression = re.compile(f"^([A-z][A-z|,A-z|\s]*)")
        result = re.fullmatch(expression, input)
        if result == None:
            print("Cadena incorrecta")
            return False
        else:
            print("Cadena correcta")
            self.pila.desapilar()
            self.pila.desapilar()
            self.items.pop()
            return True


if __name__ == "__main__":
    Analizador()
