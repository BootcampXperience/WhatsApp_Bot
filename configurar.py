from time import sleep
import os,cv2
from PIL import Image, ImageGrab
import pyperclip
import pyautogui as pt
import pyscreenshot
import pytesseract
import openai
import configparser

#Tesseract para Windows: 
	#1. Instalar OCR: https://github.com/UB-Mannheim/tesseract/wiki
	#2. Bajar todos los .traineddata de https://github.com/tesseract-ocr/tessdata/ 
	#	y guardarlos en C:\\Program Files\\Tesseract-OCR\\tessdata\\
	#3. pip install pytesseract
#Tesseract para MacOs:
	#1. Instalar Homebrew: https://brew.sh/
	#2. brew install tesseract-lang

#pip install opencv-python
#pip install Pillow
#pip install pyperclip
#pip install PyAutoGUI
#pip install pyscreenshot
#pip install openai
#pip install configparser


'''
#1. Crear las imagenes:
#Abrir WhatsApp
os.system("open /Applications/WhatsApp.app") 	#Para MacOS
#os.system("start WhatsApp:") 					#Para Windows10+
sleep(1)
pt.screenshot('imagenes/screen.png')
'''

'''
#2. Configurar posición de inicio del mensaje
#Abrir WhatsApp
os.system("open /Applications/WhatsApp.app") 	#Para MacOS
#os.system("start WhatsApp:") 					#Para Windows10+
sleep(1)
pct_x = pt.size()[0]/ImageGrab.grab().size[0]
pct_y = pt.size()[1]/ImageGrab.grab().size[1]
posicion = pt.locateCenterOnScreen('imagenes/clip.png', grayscale=False, confidence=.9)
if posicion is not None:
	x = int(posicion[0])*pct_x
	y = int(posicion[1])*pct_y
	pt.moveTo(x,y, duration=.05)
	pt.moveTo(x*0.98, y*0.935, duration = .5)				#Ajustar aqui valores de x,y
	pt.click()
	coor_x_ini,coor_y_ini = int(x*0.98),int(y*0.935)		#Ajustar aqui valores de x,y
	sleep(1)
'''