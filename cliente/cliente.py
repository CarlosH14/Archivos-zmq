import zmq
import sys, os
import json

# python3       cliente.py      carlos      subir       DF11.rar
# sys arg           0             1           2           3

if __name__ == "__main__":

    context = zmq.Context()
    s = context.socket(zmq.REQ)
    s.connect('tcp://localhost:8001')

    fin="fin"
    fin=fin.encode('utf-8')

    nombre = sys.argv[1]
    funcion = sys.argv[2]
    aux = sys.argv[3]

    auxseek0 = 0
    auxseek10 = 1024*1024*10

    if funcion == "subir":
        file = open(aux, "rb")
        file.seek(0)
        nombre = nombre.encode('utf-8')
        funcion = funcion.encode('utf-8')
        aux = aux.encode('utf-8')
        while True:
            contenido = file.read(auxseek10)
            if not contenido:
                s.send_multipart([fin])
                break
            s.send_multipart([nombre, funcion, aux, contenido])
            m = s.recv_multipart()
            print(m[0], aux)

    if funcion == "descargar":
        nombre = nombre.encode('utf-8')
        funcion = funcion.encode('utf-8')
        aux = aux.encode('utf-8')
        while True:
            contenido = b'0'
            s.send_multipart([nombre, funcion, aux, contenido])
            m = s.recv_multipart()
            if m[0] == fin:
                break
            desc_aux= aux.decode('utf-8')
            desc_cont= m[1]
            with open(desc_aux,"wb") as file: #Abre el archivo solo para las funciones descargar y descargarenlace que retornan el nombre del archivo con su contenido
                file.seek(auxseek0)
                auxseek0 = auxseek0 + auxseek10

                file.write(desc_cont)
            m[1]=aux
            print(m)


    if funcion == "descargarenlace":
        nombre = nombre.encode('utf-8')
        funcion = funcion.encode('utf-8')
        aux = aux.encode('utf-8')
        while True:
            contenido = b'0'
            s.send_multipart([nombre, funcion, aux, contenido])
            m = s.recv_multipart()
            if m[0] == fin:
                break
            enlace = aux.decode('utf-8') #Obtiene el enlace de la tercera posicion del comando y la recibe como parametro
            ruta = enlace.split("$") #Separa en ruta el enlace antes y despues del $
            n_arch = ruta[0].split("/") #Variable que guarda la dirección del archivo
            ruta = (n_arch[2]) #Se crea la ruta a partir de los parametros anteriores
            desc_cont= m[1]
            with open(ruta,"wb") as file: #Abre el archivo solo para las funciones descargar y descargarenlace que retornan el nombre del archivo con su contenido
                file.seek(auxseek0)
                auxseek0 = auxseek0 + auxseek10

                file.write(desc_cont)
            m[1]=aux
            print(m)

    if funcion == "enlace":
        contenido = b'0'
        nombre = nombre.encode('utf-8')
        funcion = funcion.encode('utf-8')
        aux = aux.encode('utf-8')
        while True:
            s.send_multipart([nombre, funcion, aux, contenido])
            m = s.recv_multipart()
            print("Enlace: " , m[0].decode('utf-8'))
            if m[1] == fin:
                s.send_multipart([fin])
                break
