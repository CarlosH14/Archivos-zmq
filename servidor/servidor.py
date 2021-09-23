import zmq
import json
import os.path as path
import os

ROUTE = "tcp://*:8001"

def carpeta_usuario(name:str) -> bool: #Funcion para determinar si una carpeta existe
    return path.isdir("archivos/{}".format(name)) #Se usa para crear un nuevo usuario si no existe

#Funciones para los archivos que reciebn un numero de arguemntos con un nombre fijo



def descargar(nombre, funcion, aux): #Descargar archivos
    ruta = "archivos/{}/{}".format(nombre,aux) #Elabora la ruta del archivo a partir del usuario y del nombre del archivo
    if not path.isfile(ruta): #Si no encuentra el archivo retorna un error
        respuesta = "archivo no encontrado"
        respuesta.encode('utf-8')
        return respuesta
    with open(ruta,"rb") as file: #Si encuentra el archivo lee su contenido
        contenido = file.read()
    return contenido



def descargarenlace(nombre, funcion, aux): #Función para descargar un archivo a partir de un enlace
    enlace = aux #Obtiene el enlace de la tercera posicion del comando y la recibe como parametro
    print(enlace)
    ruta = enlace.split("$") #Separa en ruta el enlace antes y despues del $
    print(ruta)
    n_arch = ruta[0].split("/") #Variable que guarda la dirección del archivo
    print(n_arch)
    ruta = "archivos/{}/{}".format(n_arch[1],n_arch[2]) #Se crea la ruta a partir de los parametros anteriores
    n_archivo = n_arch[2] #El nombre del archivo se encuentra en la tercera posicion, se guarda para enviarlo en el retorno
    if not path.isfile(ruta):#Si no encuentra el archivo con respecto al enlace retorna un error
        respuesta = "archivo no encontrado"
        respuesta.encode('utf-8')
        return respuesta
    with open(ruta,"rb") as file: #Si encuentra el archivo lee su contenido
        contenido = file.read()
    return contenido

def listar(**kwargs): #Función para listar los archivos de un usuario
    pass

if __name__ == "__main__":


    context = zmq.Context()
    s = context.socket(zmq.REP)
    s.bind(ROUTE)

    fin="fin"
    fin=fin.encode('utf-8')

    while True:
        print('--- ESPERANDO SOLICITUD ---')
        auxseek0 = 0
        auxseek10 = 1024*1024*10
        while True:
            m = s.recv_multipart()
            if m[0] == fin:
                s.send_multipart([fin])
                break
            nombre=m[0]
            nombre=nombre.decode('utf-8')
            funcion=m[1]
            funcion=funcion.decode('utf-8')
            aux=m[2]
            aux=aux.decode('utf-8')
            #Imprime en pantalla el nombre del usuario
            print("Usuario: {}".format(nombre)) #Imprime en pantalla el nombre del usuario
            print("Petición: {}".format(funcion)) #Imprime en pantalla la función ingresada
            print("Auxiliar: {}".format(aux)) #Imprime en pantalla el nombre del usuario

            if funcion == "subir":
                contenido=m[3]
                if not path.isdir("archivos/{}".format(nombre)):
                    os.makedirs("archivos/{}".format(nombre)) #Crea una carpeta para el usuario si no la tiene
                with open("archivos/{}/{}".format(nombre,aux),"wb") as file:
                    file.seek(auxseek0)
                    auxseek0 = auxseek0 + auxseek10
                    file.write(contenido) #Escribe en su contenido el contenido del argumento
                respuesta = "subido"
                respuesta.encode('utf-8')

            elif funcion == "enlace":
                contenido=m[3]
                ruta = "archivos/{}/{}".format(nombre,aux) #Elabora una ruta del archivo a partir del usuario y del nombre del archivo
                if not path.isfile(ruta): #Si no encuentra el archivo retorna un error
                    respuesta = "archivo no encontrado"
                    respuesta.encode('utf-8')
                enlace = "enlace${}".format(ruta) #Crea un enlace para el archivo iniciando por "enlace$" y continuado por la ruta del archivo
                print(enlace)
                enlace.encode('utf-8')
                respuesta=enlace
                desc_cont=fin


            elif funcion == "descargar":
                ruta = "archivos/{}/{}".format(nombre,aux) #Elabora la ruta del archivo a partir del usuario y del nombre del archivo
                if not path.isfile(ruta): #Si no encuentra el archivo retorna un error
                    respuesta = "archivo no encontrado"
                    respuesta.encode('utf-8')
                with open(ruta,"rb") as file: #Si encuentra el archivo lee su contenido
                    file.seek(auxseek0)
                    auxseek0 = auxseek0 + auxseek10
                    contenido = file.read(auxseek0)
                    if not contenido:
                        s.send_multipart([fin])
                        break
                    desc_cont = contenido
                    respuesta="descargado por cliente"
            elif funcion == "descargarenlace":
                enlace = aux #Obtiene el enlace de la tercera posicion del comando y la recibe como parametro
                print(enlace)
                ruta = enlace.split("$") #Separa en ruta el enlace antes y despues del $
                print(ruta)
                n_arch = ruta[0].split("/") #Variable que guarda la dirección del archivo
                print(n_arch)
                ruta = "archivos/{}/{}".format(n_arch[1],n_arch[2]) #Se crea la ruta a partir de los parametros anteriores
                n_archivo = n_arch[2] #El nombre del archivo se encuentra en la tercera posicion, se guarda para enviarlo en el retorno
                if not path.isfile(ruta):#Si no encuentra el archivo con respecto al enlace retorna un error
                    respuesta = "archivo no encontrado"
                    respuesta.encode('utf-8')
                with open(ruta,"rb") as file: #Si encuentra el archivo lee su contenido
                    file.seek(auxseek0)
                    auxseek0 = auxseek0 + auxseek10
                    contenido = file.read(auxseek0)
                    if not contenido:
                        s.send_multipart([fin])
                        break
                    desc_cont = contenido
                    respuesta="descargado por enlace"
            else : #Condición para función incorrecta
                respuesta = "error"

            s.send_multipart([respuesta.encode('utf-8'), desc_cont]) #Envia la respuesta (retorno de la función correspondiente) en un json al cliente
