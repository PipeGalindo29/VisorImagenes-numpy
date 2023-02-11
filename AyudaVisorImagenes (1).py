from ctypes import alignment
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from PIL import ImageTk,Image  
import numpy as np
import matplotlib.pyplot as plt
import math

# Crear ventana Tk

Imagen = None
MiVentana = Tk()
MiVentana.geometry('1024x720')
MiVentana.resizable(False, False)
MiVentana.title("Visor de imagenes")

# Variables de Control

Seleccion = IntVar(value=1) 

# Función para explorar sistema de ficheros
# Retorna: ruta del fichero seleccionado

def OpenFile():
    file = filedialog.askopenfilename(filetypes=[
        ('Image Files JPG/JPEG', '*jpg'),
        ('Image Files JPG/JPEG', '*jpeg'),
        ('Image Files PNG', '*png'),
        ('Image Files GIF', '*gif')]
    )
    if (file != None and file != ""):
        txtImage.delete(0, END)
        txtImage.insert(0, file)
        CargarImagen()   
    return file
    
# Procedimiento para cargar imágen en la ventana Tk -------------------------------------------------------------

def CargarImagen():
    if (txtImage.get() == ""):
        path = OpenFile()
    else:
        path = txtImage.get()

    Imagen = Image.open(path)

    change_image = False

    if op1.get()==1:
        NewImagen = ImagenCapaRoja(np.asarray(Imagen))
        change_image = True
    if op2.get()==1:
        NewImagen = ImagenCapaVerde(np.asarray(Imagen))
        change_image = True
    if op3.get()==1:
        NewImagen = ImagenCapaAzul(np.asarray(Imagen))
        change_image = True
    if op4.get()==1:
        NewImagen = ImagenCapaCian(np.asarray(Imagen))
        change_image = True
    if op5.get()==1:
        NewImagen = ImagenCapaMagenta(np.asarray(Imagen))
        change_image = True
    if op6.get()==1:
        NewImagen = ImagenCapaAmarillo(np.asarray(Imagen))
        change_image = True

    if CbOperacion.get()=='Rotar Imagen':
        NewImagen = Rotar(np.asarray(Imagen), 30)
        change_image = True

    if CbOperacion.get()=='Zoom Imagen':
        NewImagen = Zoom(np.asarray(Imagen), 80)
        change_image = True

    if SpinOpcion2.get()=='2':
        Temp2 = SpinOpcion2.get()
        NewImagen = ContrasteImagen(Imagen, Temp2)
        change_image = True

    '''if((op1.get()==1)or(op2.get()==1)or(op3.get()==1)or(op4.get()==1)or(op5.get()==1)or(op6.get()==1)and(SpinOpcion.get())):
        Temp = SpinOpcion.get()
        NewImagen = BrilloImagenCapa(Imagen, Temp)
        change_image = True
    else:'''
    if SpinOpcion.get():
        Temp = SpinOpcion.get()
        NewImagen = BrilloImagen(Imagen, Temp)
        change_image = True

    if change_image:
        Imagen = Image.fromarray(NewImagen)

    Imagen = Imagen.resize((700, 500), Image.ADAPTIVE)
    Imagen = ImageTk.PhotoImage(Imagen)
    LbImage.configure(image=Imagen)
    MiVentana.mainloop()

# Capa de colores ---------------------------------------------------------------------------------------------

def ImagenCapaRoja(MyImagen):
    ImagenCapaRoja = np.copy(MyImagen)
    ImagenCapaRoja[:, :, 1] = 0  # Capa Verde
    ImagenCapaRoja[:, :, 2] = 0  # Capa Azul
    return ImagenCapaRoja

def ImagenCapaVerde(MyImagen):
    ImagenCapaVerde = np.copy(MyImagen)
    ImagenCapaVerde[:, :, 0] = 0  # Capa Roja
    ImagenCapaVerde[:, :, 2] = 0  # Capa Azul
    return ImagenCapaVerde

def ImagenCapaAzul(MyImagen):
    ImagenCapaAzul = np.copy(MyImagen)
    ImagenCapaAzul[:, :, 0] = 0  # Capa Roja
    ImagenCapaAzul[:, :, 1] = 0  # Capa Verde
    return ImagenCapaAzul

def ImagenCapaCian(MyImagen):
    ImagenCapaCian = np.copy(MyImagen)
    ImagenCapaCian[:, :, 0] = 0  # Capa Magenta
    ImagenCapaCian[:, :, 0] = 0  # Capa Amarilla
    return ImagenCapaCian

def ImagenCapaMagenta(MyImagen):
    ImagenCapaMagenta = np.copy(MyImagen)
    ImagenCapaMagenta[:, :, 1] = 0  # Capa Cian
    ImagenCapaMagenta[:, :, 1] = 0  # Capa Amarilla
    return ImagenCapaMagenta

def ImagenCapaAmarillo(MyImagen):
    ImagenCapaAmarillo = np.copy(MyImagen)
    ImagenCapaAmarillo[:, :, 2] = 0  # Capa Magenta
    ImagenCapaAmarillo[:, :, 2] = 0  # Capa Cian
    return ImagenCapaAmarillo

# Rotar imagen -------------------------------------------------------------------------------------------------

def Rotar(MyImagen,AngDado):
    Ang = AngDado* math.pi/100
    h,w,c = np.shape(MyImagen)
    mat_inv = np.linalg.inv(np.array([[math.cos(Ang),math.sin(Ang),0],[-math.sin(Ang),math.cos(Ang),0],[0,0,1]]))
    Img_New = np.zeros_like(MyImagen)
    for ind_c in range(c):
        for ind_y in range(h):
            for ind_x in range(w):
                v = np.matmul(np.array([ind_y,ind_x,1]),mat_inv)
                y_idx = v[0]
                x_idx = v[1]
                Img_New[ind_y,ind_x,ind_c] = MyImagen[int(y_idx)%h,int(x_idx)%w,ind_c]
    return Img_New

# Zoom Imagen ---------------------------------------------------------------------------------------------------

def Zoom(MyImagen,Porc):
    filas = MyImagen.shape[0]
    columnas = MyImagen.shape[1]
    imgz = np.copy(MyImagen)
    Porc = Porc/180
    Porcy = Porc
    for i in range(filas):
        for j in range(columnas):
            imgz[i,j] = MyImagen[round(Porc*i),round(Porcy*j)]
    return imgz

# Brillo Imagen -------------------------------------------------------------------------------------------------

def BrilloImagen(MyImagen,FactBrillo):
    BrilloImagen=MatrizPorEscalar(MyImagen,FactBrillo)
    return BrilloImagen

def MatrizPorEscalar(NewMatriz,Escalar):
        Tam=np.shape(NewMatriz)
        Fila = Tam[0]
        Columna = Tam[1]
        for i in range(Fila): 
            for x in range(Columna):
                NewMatriz[i,x] = NewMatriz[i,x]*Escalar
        return NewMatriz

# Brillo Imagen Capa --------------------------------------------------------------------------------------------

def BrilloImagenCapa(MyImagen,FactorBrillo):    
    BrilloCapaImagen=MatrizPorEscalar(MyImagen,FactorBrillo)
    return BrilloCapaImagen

# Contraste Imagen ----------------------------------------------------------------------------------------------

def ContrasteImagen(MyImagen,FactContraste):
    ImgContraste = FactContraste*np.log10(1+MyImagen[:,:,:])
    #ImgContraste = FactContraste*np.log(1+np.double(MyImagen[:,:,:]))
    return ImgContraste
     
# Boton para explorar ficheros --------------------------------------------------------------------------------

btnExplorarArchivos = Button(MiVentana, text="Cargar Imagen", width=20, command=lambda:OpenFile())
btnExplorarArchivos.grid(row=2, column=0, sticky=E)

# Spinbox -----------------------------------------------------------------------------------------------------

LbinOpcion = Label(MiVentana, text="Brillo:", font=("Arial Bold",10))
LbinOpcion.place(x=760, y=100, width=80, height=20)
SpinOpcion = Spinbox(MiVentana,from_=1, to=30, state="readonly", command=CargarImagen)
SpinOpcion.place(x=840, y=100, width=80, height=20)

LbinOpcion2 = Label(MiVentana, text="Contraste:", font=("Arial Bold",10))
LbinOpcion2.place(x=760, y=120, width=80, height=20)
SpinOpcion2 = Spinbox(MiVentana,from_=1, to=30, state="readonly", command=CargarImagen)
SpinOpcion2.place(x=840, y=120, width=80, height=20)

# Scale -------------------------------------------------------------------------------------------------------
v1 = DoubleVar()
v2 = DoubleVar()
ScaleOpcion = Scale(MiVentana,variable = v1, from_ = 1, to = 100, orient = HORIZONTAL)
ScaleOpcion.place(x=920, y=100, width=80, height=20)
ScaleOpcion1 = Scale(MiVentana,variable = v2, from_ = 1, to = 100, orient = HORIZONTAL)
ScaleOpcion1.place(x=920, y=120, width=80, height=20)

# Barra -------------------------------------------------------------------------------------------------------

Seleccion= IntVar()
LbOperacion = Label(MiVentana,text="Tipo: ", font=("Arial Bold",10))
LbOperacion.place(x=760, y=140, width=80, height=20)
CbOperacion = Combobox(MiVentana, values=('Original','Rotar Imagen','Zoom Imagen'))
CbOperacion.place(x=840, y=140, width=150, height=20)
CbOperacion.current(0)

#Opciones------------------------------------------------------------------------------------------------------

op1 = IntVar()
op2 = IntVar()
op3 = IntVar()
op4 = IntVar()
op5 = IntVar()
op6 = IntVar()

ChkOpcion = Label(MiVentana,text="CanalesRGB: ", font=("Arial Bold",10))
ChkOpcion.place(x=760, y=180, width=80, height=20)
ChkOpcion = Label(MiVentana,text="CanalesCNY: ", font=("Arial Bold",10))
ChkOpcion.place(x=760, y=240, width=80, height=20)

ChkOpcion1 = Checkbutton(MiVentana, text="Red", variable=op1, width=10)
ChkOpcion1.place(x=840, y=160, width=80, height=20) 
ChkOpcion2 = Checkbutton(MiVentana, text="Green", variable=op2, width=10)
ChkOpcion2.place(x=840, y=180, width=80, height=20) 
ChkOpcion3 = Checkbutton(MiVentana, text="Blue", variable=op3, width=10)
ChkOpcion3.place(x=840, y=200, width=80, height=20) 
ChkOpcion4 = Checkbutton(MiVentana, text="Cyan", variable=op4, width=10)
ChkOpcion4.place(x=840, y=220, width=80, height=20) 
ChkOpcion5 = Checkbutton(MiVentana, text="Magenta", variable=op5, width=10)
ChkOpcion5.place(x=840, y=240, width=80, height=20) 
ChkOpcion6 = Checkbutton(MiVentana, text="Yellow", variable=op6, width=10)
ChkOpcion6.place(x=840, y=260, width=80, height=20) 

# Boton Resultado ---------------------------------------------------------------------------------------------

BtEvaluar = Button(MiVentana, text="Evaluar",command=CargarImagen)
BtEvaluar.place(x=760, y=300, width=80, height=20)

# Caja para ruta del Archivo-----------------------------------------------------------------------------------

txtImage = Entry(MiVentana, width=90)
txtImage.grid(row=2, column=1, columnspan = 3, sticky=W)

# Label para mostrar Imagen-------------------------------------------------------------------------------------

LbImage = Label(image="", text="<< Imagen >>", foreground="white", anchor=CENTER, justify=CENTER,
                 font=("Arial black", 50),pad=0 )
LbImage.grid(row=5, column=0, columnspan = 3, sticky=W)

MiVentana.mainloop()
