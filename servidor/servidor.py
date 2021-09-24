import zmq
import json
import os.path as path
import os

ROUTE = "tcp://*:8001"

if __name__ == "__main__":

    context = zmq.Context()
    s = context.socket(zmq.REP)
    s.bind(ROUTE)

    fin="fin" # Acuse de finalización para el servidor
    fin=fin.encode('utf-8') # Acuse codificado

    while True: # Espera solicitud
        print('--- ESPERANDO SOLICITUD ---')
        auxseek0 = 0 # Seek inicial de archivo
        auxseek10 = 1024*1024*10 # Seek de 10 MB para segmentación
        while True: # Recibo de segmentación
            m = s.recv_multipart() # Recibe los parametros
            if m[0] == fin: # Si recibe acuse de finalización
                s.send_multipart([fin]) # Envia acuse de finalización
                break # Termina la operación
            nombre=m[0] # Recibe el nombre de usuario en la primera posición
            nombre=nombre.decode('utf-8') # Decodifica el nombre
            funcion=m[1]  # Recibe la función en la segunda posición
            funcion=funcion.decode('utf-8') # Decodifica la función
            aux=m[2] # Recibe el nombre del archivo o el enlace segun corresponda en la tercera posición
            aux=aux.decode('utf-8') # Decodifica el auxiliar
            #Imprime en pantalla los datos del comando
            print("Usuario: {}".format(nombre)) #Imprime en pantalla el nombre del usuario
            print("Petición: {}".format(funcion)) #Imprime en pantalla la función ingresada
            print("Auxiliar: {}".format(aux)) #Imprime en pantalla el nombre del archivo o el enlace segun corresponda

            if funcion == "subir": # Función de subir
                contenido=m[3] # Recibe el contenido en la cuarta posición
                if not path.isdir("archivos/{}".format(nombre)): # Si no existe una carpeta con el nombre del usario
                    os.makedirs("archivos/{}".format(nombre)) #Crea una carpeta para el usuario
                with open("archivos/{}/{}".format(nombre,aux),"wb") as file: # Abre el archivo en la ubicación
                    file.seek(auxseek0) # Se ubica en la posición
                    auxseek0 = auxseek0 + auxseek10 # Aumenta el seek para la ubicación
                    file.write(contenido) #Escribe el contenido en el archivo
                respuesta = "subido" # Establece la respuesta para enviar
                respuesta.encode('utf-8') # Codifica la respuesta
                desc_cont = b'0'

            elif funcion == "enlace": # Función de obtener enlace
                contenido=m[3] # Recibe el contenido en la cuarta posición
                ruta = "archivos/{}/{}".format(nombre,aux) #Elabora una ruta del archivo a partir del usuario y del nombre del archivo
                if not path.isfile(ruta): #Si no encuentra el archivo retorna un error
                    respuesta = "archivo no encontrado" # Respuesta para enviar
                    respuesta.encode('utf-8') # Respuesta codificada
                enlace = "enlace${}".format(ruta) #Crea un enlace para el archivo iniciando por "enlace$" y continuado por la ruta del archivo
                print(enlace) # Imprime el enlace
                enlace.encode('utf-8') # Codifica el enlace
                respuesta=enlace # Asigna el enlace a la respuesta
                desc_cont=fin # Envia el acuse de finalización


            elif funcion == "descargar": # Función de descargar
                ruta = "archivos/{}/{}".format(nombre,aux) #Elabora la ruta del archivo a partir del usuario y del nombre del archivo
                if not path.isfile(ruta): #Si no encuentra el archivo retorna un error
                    respuesta = "archivo no encontrado" # Respuesta para enviar
                    respuesta.encode('utf-8') # Respuesta codificada
                with open(ruta,"rb") as file: #Si encuentra el archivo lee su contenido
                    file.seek(auxseek0) # Se ubica dentro del archivo
                    auxseek0 = auxseek0 + auxseek10 # Aumenta el seek para la ubicación
                    contenido = file.read(auxseek0) # Lee 10 MB del archivo y se desplaza hasta alli
                    if not contenido: # Si no hay mas contenido para leer
                        s.send_multipart([fin]) # Envia el acuse de finalización
                        break # Termina la operación
                    desc_cont = contenido # Envia el contenido leído
                    respuesta="descargado por cliente" # Envia una respuesta

            elif funcion == "descargarenlace": # Función descargar por enlace
                enlace = aux #Obtiene el enlace de la tercera posicion del comando
                print(enlace)
                ruta = enlace.split("$") #Separa en ruta el enlace antes y despues del $
                n_arch = ruta[0].split("/") #Variable que guarda la dirección del archivo
                ruta = "archivos/{}/{}".format(n_arch[1],n_arch[2]) #Se crea la ruta a partir de los parametros anteriores
                n_archivo = n_arch[2] #El nombre del archivo se encuentra en la tercera posicion, se guarda para enviarlo en el retorno
                if not path.isfile(ruta):#Si no encuentra el archivo con respecto al enlace retorna un error
                    respuesta = "archivo no encontrado" # Respuesta de error
                    respuesta.encode('utf-8') # Respuesta codificada
                with open(ruta,"rb") as file: # Si encuentra el archivo lee su contenido
                    file.seek(auxseek0) # Se ubica dentro del archivo
                    auxseek0 = auxseek0 + auxseek10 # Aumenta el seek para la ubicación
                    contenido = file.read(auxseek0) # Lee 10 MB del archivo y se desplaza hasta alli
                    if not contenido: # Si no hay mas contenido para leer
                        s.send_multipart([fin]) # Envia el acuse de finalización
                        break # Termina la operación
                    desc_cont = contenido # Envia el contenido leído
                    respuesta="descargado por enlace" # Envia una respuesta
            else : #Condición para función incorrecta
                respuesta = "error"

            s.send_multipart([respuesta.encode('utf-8'), desc_cont]) #Envia la respuesta y el contenido si corresponde
