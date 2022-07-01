
from cProfile import label
import re
from PyQt5 import uic
from PyQt5 import QtWidgets


class Pila:
    def __init__(self):
        """ Crea una pila vacía. """
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


# <Clase :
# nombre : student
# parametro : name, age
# tipo de dato : string, int
# metodos : +getName()
# relacion : uses : teacher
# Fin>


class Analizador():
    pila = Pila()
    count = 0
    items = []
    predict_table = [
        ["", "<", "nombre", "parametro", "tipo de dato", "metodos", "relacion", "Fin", "Clase", ":",
            ">", "a-Z", ",", "string", "-", "get", "()", "int", "float", "double", "+", "set",  "$"],
        ["S", ["Inicio", "N", "P", "TD", "M", "R", "Final"], "", "", "", "",
            "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["Inicio", ["MQ", "CLASS", "PP"], "", "", "", "", "", "", "",
            "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["N", "", ["NO", "PP", "VN"], "", "", "", "", "", "", "",
            "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["P", "", "", ["PA", "PP", "VN", "RC"], "", "", "", "", "",
            "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["TD", "", "", "", ["TT", "PP", "D", "RD"], "", "", "", "",
            "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["M", "", "", "", "", ["ME", "PP", "CM", "RM"], "", "", "",
            "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["R", "", "", "", "", "", ["RE", "PP", "VN", "PP", "VN"], "",
            "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["Final", "", "", "", "", "", "", ["F", "MQA"], "", "",
            "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["MQ", "<", "", "", "", "", "", "", "", "", "", "",
            "", "", "", "", "", "", "", "", "", "", ""],
        ["CLASS", "", "", "", "", "", "", "", "Clase", "", "",
            "", "", "", "", "", "", "", "", "", "", "", ""],
        ["NO", "", "nombre", "", "", "", "", "", "", "", "",
            "", "", "", "", "", "", "", "", "", "", "", ""],
        ["PP", "", "", "", "", "", "", "", "", ":", "", "",
            "", "", "", "", "", "", "", "", "", "", ""],
        ["F", "", "", "", "", "", "", "Fin", "", "", "",
            "", "", "", "", "", "", "", "", "", "", "", ""],
        ["MAQ", "", "", "", "", "", "", "", "", "", ">",
            "", "", "", "", "", "", "", "", "", "", "", ""],
        ["VN", "", "", "", "", "", "", "", "", "", "", ["LETRAS", "RI"],
            "", "", "", "", "", "", "", "", "", "", ""],
        ["PA", "", "", "parametro", "", "", "", "", "", "", "",
            "", "", "", "", "", "", "", "", "", "", "", ""],
        ["RC", "", "", "", "$", "", "", "", "", "", "", "", [
            "C", "LETRAS", "RC"], "", "", "", "", "", "", "", "", "", "$"],
        ["TT", "", "", "", "tipo de dato", "", "", "", "", "",
            "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["D", "", "", "", "", "", "", "", "", "", "", "",
            "", "D", "", "", "", "D", "D", "D", "", "", ""],
        ["RD", "", "", "", "", "vacio", "", "", "", "", "", "", [
            "C", "D", "RD"], "", "", "", "", "", "", "", "", "", "$"],
        ["ME", "", "", "", "", "metodos", "", "", "", "", "",
            "", "", "", "", "", "", "", "", "", "", "", ""],
        ["CM", "", "", "", "", "", "", "", "", "", "", "", "", "", [
            "TM", "GS", "VN", "PR"], "", "", "", "", "", ["TM", "GS", "VN", "PR"], "", ""],
        ["RM", "", "", "", "", "", "vacio", "", "", "", "", "", ["C", "TM",
                                                            "GS", "VN", "PR", "RM"], "", "", "", "", "", "", "", "", "", "$"],
        ["RE", "", "", "", "", "", "relacion", "", "", "", "",
            "", "", "", "", "", "", "", "", "", "", "", ""],
        ["GS", "", "", "", "", "", "", "", "", "", "", "",
            "", "", "", "GS", "", "", "", "", "", "GS", ""],
        ["PR", "", "", "", "", "", "", "", "", "", "", "",
            "", "", "", "", "()", "", "", "", "", "", ""],
        ["C", "", "", "", "", "", "", "", "", "", "", "",
            ",", "", "", "", "", "", "", "", "", "", ""],
        ["LETRAS", "", "", "", "", "", "", "", "", "", "",
            "a-z|A-Z", "", "", "", "", "", "", "", "", "", "", ""],
        ["TM", "", "", "", "", "", "", "", "", "", "", "",
            "", "", "-", "", "", "", "", "", "+", "", ""],
        ["RI", "", "", "$", "$", "", "", "", "", "$", "", "a-z|A-Z",
            "", "", "", "", "$", "", "", "", "", "", "$"],
    ]

    def __init__(self):
        app = QtWidgets.QApplication([])
        self.window = uic.loadUi('Interfaz.ui')
        self.window.analizar.clicked.connect(self.entry)
        self.window.show()
        app.exec()

    def check_chain(self, chain):
        chain = chain.split("\n")
        print(chain)
        for i in chain:
            # print(i)
            aux = i.split("\t")
            if len(aux) == 1:
                self.items.append(aux[0])
            else:
                self.items.append(aux[1])
        chain = self.items.copy()
        self.items.clear()
        for i in chain:
            aux = i.split(" ")
            # print(aux)

            for y in aux:
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

        self.items.remove("de")
        self.items.remove("dato")

        chain = self.items.copy()
        self.items.clear()
        for i in chain:
            if i == "tipo":
                x = "tipo de dato"
                self.items.append(x)
            else:
                self.items.append(i)

        print(self.items)

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
        print(self.predict_table[20][5])

        while self.pila.es_vacia() == False:
            character = self.items[len(self.items)-1]
            cima = self.pila.desapilar()

            x, y = self.search(cima, character)
            print(cima, character)
            print(x, y)

            if self.predict_table[x][y] == "vacio":
                cima = self.pila.desapilar()
                print(cima, character)
                x, y = self.search(cima, character)

            if cima == "VN":
                if self.check_letras(character) == False:
                    print("ERROR: Expected a word")

            elif cima == "RC":
                if self.check_RC(character) == False:
                    print("ERROR: Expected a word")

            elif self.predict_table[x][0] == cima and self.predict_table[0][y] == character:
                print(character)
                if (type(self.predict_table[x][y])) == list:
                    aux = ((self.predict_table[x][y])[::-1])
                    for i in aux:
                        self.pila.apilar(i)

                else:
                    self.items.pop()

                self.pila.print_stack()
            else: print("ERROR")
        self.pila.print_stack()               

    def entry(self):
        chain = self.window.plainTextEdit.toPlainText()
        self.pila.print_stack()
        print('Pop')
        print('Push')
        self.check_chain(chain)
        if len(self.items) != 0:
            # se agrega la gramatica inicial S
            valor_pila = self.pila.ver()
            if valor_pila == 'S':
                self.identifier()
        else:
            print('cadena ingresada incorrecta')

    def check_letras(self, input):

        aux = ((self.predict_table[15][11])[::-1])
        for i in aux:
            self.pila.apilar(i)

        self.pila.print_stack()

        expression = re.compile(f"^([A-z][A-z | , A-z | \s]*)")
        result = re.fullmatch(expression, input)
        if result == None:
            print("Cadena incorrecta")
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

        expression = re.compile(f"^([A-z][A-z | , A-z | \s]*)")
        result = re.fullmatch(expression, input)
        if result == None:
            print("Cadena incorrecta")
        else:
            print("Cadena correcta")
            self.pila.desapilar()
            self.pila.desapilar()
            self.pila.desapilar()
            self.items.pop()
            return True


if __name__ == "__main__":
    Analizador()
