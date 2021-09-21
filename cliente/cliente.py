import zmq
import sys, os
import json

# python3       cliente.py      carlos      subir       DF11.rar
# sys arg           0             1           2           3

if __name__ == "__main__":

    context = zmq.Context()
    s = context.socket(zmq.REQ)
    s.connect('tcp://localhost:8001')

    nombre = sys.argv[1]
    funcion = sys.argv[2]
    aux = sys.argv[3]
    if funcion == "subir":
        with open(aux, "rb") as file:
            contenido = file.read()
    if funcion == "descargar":
        with open("vacio", "rb") as file:
            contenido = file.read()
    if funcion == "descargarenlace":
        with open("vacio", "rb") as file:
            contenido = file.read()
    if funcion == "enlace":
        with open(aux, "rb") as file:
            contenido = file.read()
    nombre = nombre.encode('utf-8')
    funcion = funcion.encode('utf-8')
    aux = aux.encode('utf-8')


    s.send_multipart([nombre, funcion, aux, contenido]) #Envia información en json

    m = s.recv_multipart() #Recibe información en json

    funcion=funcion.decode('utf-8')
    if funcion == "descargar":
        desc_aux= aux.decode('utf-8')
        desc_cont= m[1]
        with open(desc_aux,"wb") as file: #Abre el archivo solo para las funciones descargar y descargarenlace que retornan el nombre del archivo con su contenido
            file.write(desc_cont)
        m[1]=aux
    if funcion == "descargarenlace":
        enlace = aux.decode('utf-8') #Obtiene el enlace de la tercera posicion del comando y la recibe como parametro
        ruta = enlace.split("$") #Separa en ruta el enlace antes y despues del $
        n_arch = ruta[0].split("/") #Variable que guarda la dirección del archivo
        ruta = (n_arch[2]) #Se crea la ruta a partir de los parametros anteriores
        desc_cont= m[1]
        with open(ruta,"wb") as file: #Abre el archivo solo para las funciones descargar y descargarenlace que retornan el nombre del archivo con su contenido
            file.write(desc_cont)
        m[1]=aux
    print(m)
