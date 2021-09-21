# Archivos-zmq

Proyecto de Arquitectura Cliente / Servidor - UTP

Para usarlo:

Correr el servidor:   
En terminal -> python3 servidor.py

Correr el cliente:  
En terminal -> python3 cliente.py nombreUsuario nombreFuncion auxiliar

# Lista de funciones:

subir -> sube un archivo de la carpeta cliente a la carpeta del usuario del servidor

ejemplo:  
python3 cliente.py carlos subir prueba.txt

----------------------------------------------------------------------------------------------------------------------------------------------------------------
descargar -> descarga un archivo de la carpeta del usuario del servidor a la carpeta del cliente

ejemplo:  
python3 cliente.py carlos descargar anuncio.jpeg

----------------------------------------------------------------------------------------------------------------------------------------------------------------
enlace -> obtiene un enlace de un archivo de la carpeta del usuario

ejemplo:  
python3 cliente.py carlos enlace convocatoria.pdf

----------------------------------------------------------------------------------------------------------------------------------------------------------------
descargarenlace -> descarga un archivo de la carpeta del usuario del servidor a la carpeta del cliente por medio de un enlace

ejemplo:  
python3 cliente.py diego descargarenlace enlace$archivos/carlos/convocatoria.pdf

----------------------------------------------------------------------------------------------------------------------------------------------------------------
