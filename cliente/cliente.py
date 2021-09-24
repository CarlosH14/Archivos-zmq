import zmq
import sys, os
import json

# python3       cliente.py      carlos      subir       DF11.rar
# sys arg           0             1           2           3

if __name__ == "__main__":

    context = zmq.Context()
    s = context.socket(zmq.REQ)
    s.connect('tcp://localhost:8001')

    fin="fin" # Acuse de finalización para cliente
    fin=fin.encode('utf-8') # Acuse codificado

    nombre = sys.argv[1] # Parametro del nombre de usuario
    funcion = sys.argv[2] # Parametro de la función
    aux = sys.argv[3] # Parametro de nombre de archivo o enlace

    auxseek0 = 0 # Seek inicial de archivo
    auxseek10 = 1024*1024*10 # Seek de 10 MB para segmentación

    if funcion == "subir": # Función de subir
        file = open(aux, "rb") # Abre el archivo del cliente
        file.seek(auxseek0) # Se ubica al inicio del archivo
        nombre = nombre.encode('utf-8') # Codifica el nombre
        funcion = funcion.encode('utf-8') # Codifica la función
        aux = aux.encode('utf-8') # Codifica el nombre del archivo
        while True: # Envío segmentado
            contenido = file.read(auxseek10) # Lee 10 MB del archivo y se desplaza hasta alli
            if not contenido: # Si no hay mas contenido para leer
                s.send_multipart([fin]) # Envia el acuse de finalización
                break # Termina la operación
            s.send_multipart([nombre, funcion, aux, contenido]) # Envia los parametros y los 10 MB del contenido del archivo
            m = s.recv_multipart() # Recibe resupuesta del servidor
            print(m[0], aux) # Imprime la respuesta y el nombre del archivo

    if funcion == "descargar": # Función de descargar
        nombre = nombre.encode('utf-8') # Codifica el nombre
        funcion = funcion.encode('utf-8') # Codifica la función
        aux = aux.encode('utf-8') # Codifica el nombre del archivo
        while True: # Recibo segmentado
            contenido = b'0' #Establece el contenido como vacío
            s.send_multipart([nombre, funcion, aux, contenido]) # Envia los parametros y el contenido vacío
            m = s.recv_multipart()  # Recibe resupuesta del servidor
            if m[0] == fin: # Si recibe el acuse de finalización
                break # Termina la operación
            desc_aux= aux.decode('utf-8') # Decodifica el nombre del archivo
            desc_cont= m[1] # Asigna el contenido del archivo recibido a desc_cont
            if auxseek0 == 0:
                with open(desc_aux,"wb") as file: # Crea el archivo o lo abre para sobreescribirlo
                    file.seek(auxseek0) # Se ubica dentro del archivo
                    auxseek0 = auxseek0 + auxseek10 # Aumenta el seek para la ubicación
                    file.write(desc_cont) # Escribe el contenido en el archivo
            else:
                with open(desc_aux,"ab") as file: # Crea el archivo o lo abre para sobreescribirlo
                    file.write(desc_cont) # Escribe el contenido en el archivo
            m[1]=aux # Cambia el contenido del archivo por el nombre del archivo para imprimirlo en pantalla
            print(m) # Imprime en pantalla la respuesta del servidor

    if funcion == "descargarenlace": # Función de descargar por enlace
        nombre = nombre.encode('utf-8') # Codifica el nombre
        funcion = funcion.encode('utf-8') # Codifica la función
        aux = aux.encode('utf-8') # Codifica el nombre del archivo
        while True: # Recibo segmentado
            contenido = b'0' # Establece el contenido como vacío
            s.send_multipart([nombre, funcion, aux, contenido]) # Envia los parametros y el contenido vacío
            m = s.recv_multipart() # Recibe resupuesta del servidor
            if m[0] == fin: # Si recibe el acuse de finalización
                break # Termina la operación
            enlace = aux.decode('utf-8') # Decodifica el enlace como el auxiliar del comando
            ruta = enlace.split("$") # Separa en ruta el enlace antes y despues del $
            n_arch = ruta[0].split("/") # Variable que guarda la dirección del archivo
            ruta = (n_arch[2]) # Se crea la ruta a partir de los parametros anteriores
            desc_cont= m[1]  # Asigna el contenido del archivo recibido a desc_cont
            if auxseek0 == 0:
                with open(ruta,"wb") as file: # Crea el archivo o lo abre para sobreescribirlo
                    file.seek(auxseek0) # Se ubica dentro del archivo
                    auxseek0 = auxseek0 + auxseek10 # Aumenta el seek para la ubicación
                    file.write(desc_cont) # Escribe el contenido en el archivo
            else:
                with open(ruta,"ab") as file: # Crea el archivo o lo abre para sobreescribirlo
                    file.write(desc_cont) # Escribe el contenido en el archivo
            m[1]=aux # Cambia el contenido del archivo por el nombre del archivo para imprimirlo en pantalla
            print(m) # Imprime en pantalla la respuesta del servidor

    if funcion == "enlace": # Función de obtener enlace
        contenido = b'0' # Establece el contenido como vacío
        nombre = nombre.encode('utf-8') # Codifica el nombre
        funcion = funcion.encode('utf-8') # Codifica la función
        aux = aux.encode('utf-8') # Codifica el nombre del archivo
        while True: #Envio de parametros
            s.send_multipart([nombre, funcion, aux, contenido]) # Envia los parametros y el contenido vacío
            m = s.recv_multipart() # Recibe resupuesta del servidor
            print("Enlace: " , m[0].decode('utf-8')) # Imprime la respuesta del servidor
            if m[1] == fin: # Si recibe el acuse de finalización
                s.send_multipart([fin]) # Envia el acuse de finalización
                break # Termina la operación
