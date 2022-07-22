from os import system

class Diagram():

    def __init__(self) -> None:
        
        self.items = []
        self.auxlist = []

    def get(self, data1, data2):
        self.data1 = data1
        self.data2 = data2
        print(self.data1)
        print(self.data2)

        self.new_list_1 = [ x for x in self.data1 
        if x != ':' and x != ',' and x != '<' and x != 'Clase'and x != 'nombre' and x != 'parametro' 
        and x != 'tipo de dato' and x != 'metodos' and x != 'relacion' and x != 'Fin' and x != '>']        
        print("List1 ",self.new_list_1)

        self.new_list_2 = [ x for x in self.data2 
        if x != ':' and x != ',' and x != '<' and x != 'Clase'and x != 'nombre' and x != 'parametro' 
        and x != 'tipo de dato' and x != 'metodos' and x != 'relacion' and x != 'Fin' and x != '>']
        print("List2 ",self.new_list_2)
    
    def identifier(self):
        self.class_1 = ''
        self.class_2 = ''
        self.pa1 = ''
        self.pa2 = ''
        self.me1 = ''
        self.me2 = ''
        self.td1 = []
        self.td2 = []
        self.type_re1 = ''
        self.type_re2 = ''
        self.class_1 = self.new_list_1[0]
        self.class_2 = self.new_list_2[0]

        validation = 2
        validation2 = 2
        for i in range(len(self.new_list_1)-1):
            if self.new_list_1[i] == "string" or self.new_list_1[i] == "int" or self.new_list_1[i] == "float" or self.new_list_1[i] == "double":
                range_p = i
                validation += 1
                break
        for i in range(len(self.new_list_2)-1):
            if self.new_list_1[i] == "string" or self.new_list_1[i] == "int" or self.new_list_1[i] == "float" or self.new_list_1[i] == "double":
                range_p2 = i
                validation2 += 1
                break

        for i in range(len(self.new_list_1)-1):
            if self.new_list_1[i] == "-" or self.new_list_1[i] == "+":
                range_td = i
                break

        for i in range(len(self.new_list_2)-1):
            if self.new_list_2[i] == "-" or self.new_list_2[i] == "+":
                range_td2 = i
                break

        for i in range(range_p,range_td):
            self.td1.append(self.new_list_1[i])

        for i in range(range_p2,range_td2):
            self.td2.append(self.new_list_2[i])

        print(len(self.td1))
        print(len(self.td2))
        print(range_p)
        print(range_p2)

        if len(self.td1) == (range_p)-1 and len(self.td2) == (range_p2)-1:



            for i in range(len(self.new_list_1)-1):
                if self.new_list_1[i] == "-" or self.new_list_1[i] == "+":
                    aux = self.new_list_1[i] + self.new_list_1[i+1] + self.new_list_1[i+2] + self.new_list_1[i+3]
                    self.me1 = self.me1 + self.class_1 + " : " + aux + "\n"

            for i in range(len(self.new_list_2)-1):
                if self.new_list_2[i] == "-" or self.new_list_2[i] == "+":
                    aux = self.new_list_2[i] + self.new_list_2[i+1] + self.new_list_2[i+2] + self.new_list_2[i+3]
                    self.me2 =  self.me2 + self.class_2 + " : " + aux + "\n"
            


            count = 0
            for i in range(1,range_p):
                aux = self.class_1 + " : " + self.new_list_1[i] + ":" + self.td1[count] + "\n"
                self.pa1 = self.pa1 + aux
                count += 1 
            count2 = 0
            for i in range(1,range_p2):
                aux2 = self.class_2 + " : " + self.new_list_2[i] + ":" + self.td2[count2] + "\n"
                self.pa2 = self.pa2 + aux2
                count2 += 1 



            print(self.class_1)
            print(self.class_2)
            print(self.pa1)
            print(self.pa2)
            print(self.me1)
            print(self.me2)
        

        else: print('ES NECESARIO LA MISMA CANTIDAD DE PARAMETROS Y TIPOS DE CADA UNO DE ELLOS')


    def crear(self):
        f= open("G:/Mi unidad/Universidad/CompiladoreS-C2/Analizador-Sintactico/diagrama.txt","w+")
        f.write(f"""
        skinparam classAttributeIconSize 0

        {self.class_1} ---- {self.class_2}

        {self.pa1}
        {self.me1}

        {self.pa2}
        {self.me2}
        """)

        f.close()
        system("python -m plantuml diagrama.txt")

