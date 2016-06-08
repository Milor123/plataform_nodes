import cPickle as pickle
from newlistas import LinkedList, Node

class Estudiante(object):
    identificacion = 0
    nombres = ""
    apellidos = ""
    edad = ""


    def __init__(self, nombres, apellidos, identificacion, edad):
        self.nombres= nombres
        self.apellidos = apellidos
        self.identificacion = identificacion
        self.edad = edad
        Registrar(self)


class Registrar:

    lista_estudiantes = LinkedList()
    lista_privado = LinkedList()
    lista_usuariofinal = LinkedList()
    flag_validar = True

    def __init__(self, Estudiante_datos):
        self.flag_validar = True
        self.E = Estudiante_datos
        self.archivo()
        self.verificar()
        if self.flag_validar: # Verificar si la identifican no ha sido repetida
            self.generar_codigo()
            self.generar_usuario()
            self.generar_password()
            self.generar_dic()
            self.crear_listas()
            self.crear_usuariofinal()
        else:
            pickle.dump(self.lista_estudiantes, self.myfile,-1)
            pickle.dump(self.lista_privado, self.myfile,-1)
            pickle.dump(self.lista_usuariofinal, self.myfile,-1)
            self.myfile.close()
    def archivo(self):
        import os.path
        if os.path.isfile('database'):
            self.myfile = open('database','r+')
            self.lista_estudiantes = pickle.load(self.myfile)
            self.lista_privado = pickle.load(self.myfile)
            self.lista_usuariofinal = pickle.load(self.myfile)
            self.myfile.close()
            self.myfile = open('database','w')

        else:
            self.myfile = open('database','wb')

    def verificar(self):
        identificacion = self.E.identificacion
        for x in self.lista_estudiantes[:]:
            if identificacion in x.values():
                print ("El usuario ya esta repetido")
                self.flag_validar = False

    def generar_codigo(self):
        codigo = "{0}{1}{2}".format(self.E.nombres[:2],
                                  self.E.apellidos[:2],
                                  self.E.identificacion[:3])
        self.codigo = codigo

    def generar_usuario(self):
        usuario = "{0}{1}{2}".format(self.E.nombres[0],
                               self.E.apellidos[:3],
                               self.E.edad)
        self.usuario = usuario

    def generar_password(self):
        password = "{0}_{1}".format(self.E.identificacion,
                                    self.E.edad)
        self.password = password

    def generar_dic(self):
        # Diccionario de estudiantes
        dic_estudiantes = {'nombres':self.E.nombres,
                          'apellidos':self.E.apellidos,
                          'identificacion':self.E.identificacion,
                          'edad':self.E.edad}
        self.dic_estudiantes = dic_estudiantes

        # Diccionario de password
        dic_privado = {'password':self.password,
                        'codigo' :self.codigo,
                       'usuario':self.usuario}
        self.dic_privado = dic_privado

    def crear_listas(self):
        self.lista_estudiantes.append(self.dic_estudiantes)
        self.lista_privado.append(self.dic_privado)
        pickle.dump(self.lista_estudiantes, self.myfile,-1)
        pickle.dump(self.lista_privado, self.myfile,-1)

    def crear_usuariofinal(self):
        from datetime import date
        ultimo_dic_estudiantes = self.lista_estudiantes[-1][0]
        ultimo_dic_privado = self.lista_privado[-1][0]
        ultimo_dic_estudiantes.update(ultimo_dic_privado)

        fecha = date.today()
        fecha = "{0}/{1}/{2}".format(fecha.year,
                                     fecha.month,
                                     fecha.day)
        dic_fecha = {"fecha":fecha}
        ultimo_dic_estudiantes.update(dic_fecha) # agregar fecha el diccionario
        self.lista_usuariofinal.append(ultimo_dic_estudiantes)
        #import ipdb; ipdb.set_trace() # BREAKPOINT
        #self.lista_usuariofinal.insert(1,ultimo_dic_estudiantes)
        #TODO change insert
        pickle.dump(self.lista_usuariofinal, self.myfile,-1)
        self.myfile.close()

class Consultar:
    def __init__(self):
        self.myfile = open('database','r')
        self.lista_estudiantes = pickle.load(self.myfile)
        self.lista_privado = pickle.load(self.myfile)
        self.lista_usuariofinal = pickle.load(self.myfile)
        self.myfile.close()
    def obtener_estudiantes(self):
        return self.lista_estudiantes[:]

    def obtener_privado(self):
        return self.lista_privado[:]

    def obtener_usuarios(self):
        return self.lista_usuariofinal[:]

class Modificar:
    def __init__(self):
        pass

    def abrir(self):
        self.myfile = open('database','r')
        self.lista_estudiantes = pickle.load(self.myfile)
        self.lista_privado = pickle.load(self.myfile)
        self.lista_usuariofinal = pickle.load(self.myfile)
        self.myfile.close()
        self.myfile = open('database','w')

    def cerrar(self):
        pickle.dump(self.lista_estudiantes, self.myfile, -1)
        pickle.dump(self.lista_privado, self.myfile, -1)
        pickle.dump(self.lista_usuariofinal, self.myfile, -1)
        self.myfile.close()

    def modificar_estudiantes(self, dic, newdic):
        self.abrir()
        self.lista_estudiantes.modify(dic,newdic)
        self.cerrar()

    def modificar_privado(self, dic, newdic):
        self.abrir()
        self.lista_privado.modify(dic,newdic)
        self.cerrar()
    def modificar_usuarios(self, dic, newdic):
        self.abrir()
        self.lista_usuariofinal.modify(dic,newdic)
        self.cerrar()

    def buscar(self,parametro): # 'key:value'
        self.abrir()
        parametro = parametro.split(':')
        for number,x in enumerate(self.lista_usuariofinal[:]):
            for key,value in x.iteritems():
                if parametro[0] in key:
                    if parametro[1] in value:
                        self.cerrar()
                        self.posicion = number
                        self.valor_dictmp = x
                        print 'paso por aqui'
                        return x
        self.posicion = None
        print 'No se encontro el usuario'
        self.cerrar()

    def buscar_modificar(self,parametro, datonuevo): # 'key:value'
        nuevoparametro = parametro.split(':')
        from copy import deepcopy
        self.buscar(parametro) # esto es para sacar el self.valor_dictmp
        dic = deepcopy(self.valor_dictmp)
        dic[nuevoparametro[0]]= datonuevo
        self.abrir()
        self.lista_usuariofinal.modify(self.valor_dictmp, dic)
        self.cerrar()

    def eliminar_por_parametro(self,parametro):
        self.buscar(parametro) # esto es para sacar el self.posicion
        if self.posicion is not None:
            self.abrir()
            self.lista_estudiantes.remove(self.posicion)
            self.lista_privado.remove(self.posicion)
            self.lista_usuariofinal.remove(self.posicion)
            self.cerrar()
        else:
            print 'Lo que usted quiere eliminar no existe'





Estudiante('Juma','Gapacho','888654','15451')
Estudiante('Juma','Gapacho','777888654','15451')
import ipdb; ipdb.set_trace() # BREAKPOINT
#Estudiante('iiiiiiiiiJuma','aaaaaaGapacho','44232777888654','15451')
