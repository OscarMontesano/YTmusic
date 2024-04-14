import tkinter as tk
from PIL import Image, ImageTk

from moviepy.editor import VideoFileClip,ImageClip
from pytube import YouTube
import eyed3
import os, sys

from threading import Thread



#Fecha 02/01/2024
#OBJ: interfaz gráfica para mi función que descarga videos de YouTube con miniatura
descargando=False

maestra=tk.Tk()
maestra.title("Descargador de Óscar")
maestra.geometry("500x500")
maestra.minsize(500, 500)
maestra.maxsize(500, 500)

miniatura=tk.Label(maestra)
miniatura.place(relx=.5, rely=.72, anchor= 'center')

urlvar=tk.StringVar()

def descargar():
    global descargando
    descargando= True
    #Funcion original, Fecha: 03/04/2023
    #OBJ: Dado un link, descarga el video y lo convierte a mp3 añadiendo miniatura (el segundo 10 de dicho video). Se descarga en el directorio en el que se ejecute.
    #PRE: Link a YouTube válido, conexión a internet, las librerías instaladas

    #Limpiamos algunas etiquetas
    miniatura.config(image="")
    etiquetaTitulo.config(text="")
    etiquetaError.config(text="")
    url=urlvar.get() 

    #Descargar video
    link = url
    try:
        youtubeObject = YouTube(link)
        etiqueta.config(text="Descargando...",fg='black')
        youtubeObject = youtubeObject.streams.get_highest_resolution()

        youtubeObject.download()
        ruta = youtubeObject.default_filename
        rutaTitulo=ruta[:len(ruta)-4]#ruta sin extensión .mp4
        print(rutaTitulo) #ruta sin extensión .mp4
        print("Descarga del vídeo completada")
        etiquetaTitulo.config(text=rutaTitulo)

        try:

            #Convertir a mp3 

            #Para ejecutable sin consola, stackoverflow, doc de sys: Note Under some conditions stdin, stdout and stderr as well as the original values __stdin__, __stdout__ and __stderr__ can be None.  It is usually the case for Windows GUI apps that aren’t connected to a console and Python apps started with pythonw.
            if sys.stderr is None:
                sys.stderr = open(os.devnull, "w")
            if sys.stdout is None:
                sys.stdout = open(os.devnull, "w")

            ruta_absoluta = os.path.abspath(ruta)
            video = VideoFileClip(ruta_absoluta)
            rutamp3=ruta[:len(ruta)-4]+ ".mp3"
            video.audio.write_audiofile(rutamp3,ffmpeg_params=["-id3v2_version", "3"]) #ffmpeg_params=["-id3v2_version", "3"] sirve para que la versión de la etiqueta sea id3v2.3 y que el explorador de windows muestre las miniaturas
            
            # Obtener el fotograma en el segundo 5
            frame = video.get_frame(10)

            # Guardar el fotograma como archivo de imagen
            frame_path = "fotograma.jpg"
            ImageClip(frame).save_frame(frame_path)
            
            image2=Image.open(r"fotograma.jpg")
            img2=image2.resize((175, 175))
            my_img2=ImageTk.PhotoImage(img2)
            miniatura.config(image=my_img2)
            miniatura.image=my_img2
            # Cerrar el archivo de video
            video.close()

            # ruta del archivo MP3 a modificar
            mp3_file = rutamp3

            # cargar el archivo MP3 como objeto AudioFile
            audiofile = eyed3.load(mp3_file)
            # agregar la miniatura al objeto AudioFile
            with open("fotograma.jpg", "rb") as thumbnail_file:
                thumbnail_data = thumbnail_file.read()
            audiofile.tag.images.set(3, thumbnail_data, "image/jpeg")
            # guardar los cambios en el archivo MP3
            audiofile.tag.save()
            #Eliminar video
            if os.path.exists(ruta):
                os.remove(ruta)


            etiqueta.config(text="¡Descargado correctamente!",fg='green')
        except Exception as e:
            print("Error conviertiendo a mp3 o añadiendo la miniatura")
            etiqueta.config(text="Error linea109: " +str(e),fg='red')

    except:
        etiquetaError.config(text="URL incorrecta")
        etiqueta.config(text=" ",fg='red')
        print("Ha ocurrido un error, contace con su ingeniero informático de confianza (le encanta python)")
        print("(Probablemtente el link no sea válido, revíselo)")

    descargando=False

cont=0
def llamarDescarga():
    global cont
    cont+=1
    global descargando
    if descargando:
        0
        if cont>10: etiquetaPesao.config(text="deja de darle ya\n hombre pesao")
    else:
        hilo = Thread(target=descargar)
        hilo.start()
        cont=0
        etiquetaPesao.config(text="")


entrada=tk.Entry(maestra,textvariable = urlvar, bd=3,  width=50)
entrada.place(relx=.5, rely=.3,anchor= 'center')
#entrada.grid(row=0, column=1)

etiqueta= tk.Label(maestra,text="",fg='green')
etiqueta.place(relx=.5, rely=.50,anchor= 'center')

etiquetaError = tk.Label(maestra,text="", fg="red", font= ('Helvetica 10 bold'))
etiquetaError.place(relx=.5, rely=.18,anchor= 'center')

etiquetaPesao = tk.Label(maestra,text="", fg="orange", font= ('Helvetica 8'))
etiquetaPesao.place(relx=.1, rely=.4)

etiquetaTitulo= tk.Label(maestra,text="",fg='black',font= ('Helvetica 10 bold'))
etiquetaTitulo.place(relx=.5, rely=.95,anchor= 'center')

titulo =tk.Label(maestra,text="Youtube a mp3", font= ('Helvetica 25 bold'))
titulo.place(relx=.5, rely=.05,anchor= 'center')

uerele =tk.Label(maestra,text="URL:", font= ('Helvetica 12'))
uerele.place(relx=.5, rely=.25,anchor= 'center')

image=Image.open(r"boton.png")
img=image.resize((25, 25))
my_img=ImageTk.PhotoImage(img)
boton=tk.Button(maestra,text='  Descargar', font= ('Helvetica 10 bold'),command=llamarDescarga, image=my_img, compound = 'left', height= 30, width=120)
boton.place(relx=.5, rely=.4,anchor= 'center')

#icono de la ventana
maestra.wm_iconphoto(False, my_img)






maestra.mainloop()


if os.path.exists("fotograma.jpg"):
    os.remove("fotograma.jpg")
    print("Borrando jpeg de la miniatura")
print("Terminado.")