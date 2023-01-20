from time import sleep
import os,cv2
from PIL import Image, ImageGrab
import pyperclip
import pyautogui as pt
import pyscreenshot
import pytesseract
import openai
import configparser

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract' 					#Para MacOS
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract' 	#Para Windows

#Leer API Key ChatGPT
config = configparser.ConfigParser()
config.read('login.ini')
api_key = config.get('login', 'api_key')
openai.api_key = api_key

#Ajuste del Pixel
pct_x = pt.size()[0]/ImageGrab.grab().size[0]
pct_y = pt.size()[1]/ImageGrab.grab().size[1]
inverso = int(ImageGrab.grab().size[0]/pt.size()[0])

#Abrir WhatsApp
sleep(3)
os.system("open /Applications/WhatsApp.app") 	#Para MacOS
#os.system("start WhatsApp:") 					#Para Windows10+

#Enviar Respuesta
def enviar_respuesta():
	posicion = pt.locateCenterOnScreen('imagenes/clip.png', grayscale=False, confidence=.9)
	if posicion is not None:
		x = int(posicion[0])*pct_x
		y = int(posicion[1])*pct_y
		pt.moveTo(x + 50, y, duration=.5)
		pt.click()
		pt.hotkey("command", "v")				#Para MacOS
		#pt.hotkey("ctrl", "v")					#Para Windows
		pt.typewrite("\n", interval=.01)
		sleep(1)
		pt.typewrite("\n", interval=.01)
		sleep(1)

#Decidir que responder
def buscar_respuesta(comentario):
	comentario+= '. Responda en pocas palabras y en un único parrágrafo.'
	try:
		completions = openai.Completion.create(
			engine="text-davinci-003",
			prompt=comentario,
			max_tokens=1024,
			temperature=0.9,
			n=1,
			stop=None,
		)
		message = completions.choices[0].text
	except openai.error.ServiceUnavailableError as e:
		message = 'ElProfeAlejo está ocupado, intenta de nuevo más tarde'
	except:
		message = 'ElProfeAlejo está ocupado, intenta de nuevo más tarde'
	return message.strip()

#Leer Mensaje
def leer_mensaje():
	img = cv2.imread('imagenes/texto.png')
	img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
	img = cv2.medianBlur(img,1)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)[1]
	rect_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
	dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
	contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	mensaje = ''

	for cnt in contours[::-1]:
		x, y, w, h = cv2.boundingRect(cnt)
		cropped = thresh1[y:y + h, x:x + w]
		config = ('--oem 1 --psm 6')				#Activar para cualquier idioma
		#config = ('-l spa --oem 1 --psm 6')		#Activar sólo para español
		text = pytesseract.image_to_string(cropped, config=config)
		text = text.replace('\n',' ')
		mensaje += text

	if mensaje != '':
		respuesta = buscar_respuesta(mensaje)
		pyperclip.copy(respuesta)
		sleep(1)
		enviar_respuesta()

#Capturar una foto del mensaje
def extraer_mensaje():
	coor_x_ini,coor_y_ini,coor_x_fin,coor_y_fin = 0,0,0,0

	posicion = pt.locateCenterOnScreen('imagenes/nuevo.png', grayscale=False, confidence=.9)
	if posicion is not None:
		x = int(posicion[0])*pct_x
		y = int(posicion[1])*pct_y
		pt.moveTo(x,y, duration=.05)
		pt.click()
		sleep(1)

	posicion = pt.locateCenterOnScreen('imagenes/clip.png', grayscale=False, confidence=.9)
	if posicion is not None:
		x = int(posicion[0])*pct_x
		y = int(posicion[1])*pct_y
		pt.moveTo(x,y, duration=.05)
		pt.moveTo(x*0.98, y*0.935, duration = .5)				#Ajustar aqui valores de x,y
		pt.click()
		coor_x_ini,coor_y_ini = int(x*0.98),int(y*0.935)		#Ajustar aqui valores de x,y
		sleep(1)

	posicion = pt.locateCenterOnScreen('imagenes/happy.png', grayscale=False, confidence=.9)
	if posicion is not None:
		x = int(posicion[0])*pct_x
		y = int(posicion[1])*pct_y
		pt.moveTo(x,y, duration=.05)
		coor_x_fin,coor_y_fin = int(x),int(y)

	if coor_x_ini !=0 and coor_y_ini !=0 and coor_x_fin!=0 and coor_y_fin!=0:
		pic = pyscreenshot.grab(bbox=(coor_x_ini*inverso, (coor_y_fin - (coor_y_ini-coor_y_fin))*inverso, coor_x_fin*inverso, coor_y_ini*inverso))
		img2 = Image.open('imagenes/black.png')
		pic.paste(img2, ((pic.size[0] - img2.size[0]),0), mask = img2)
		pic.save('imagenes/texto.png')
		sleep(1)
		leer_mensaje()
	else:
		print('Oh Oh tenemos algún problema')

#Buscar nuevos mensajes
def buscar_nuevo_mensaje():
	posicion = pt.locateCenterOnScreen('imagenes/circulo.png', grayscale=False, confidence=.9)
	if posicion is not None:
		x = int(posicion[0])*pct_x
		y = int(posicion[1])*pct_y
		pt.moveTo(x,y, duration=.05)
		sleep(1)
		pt.moveTo(x-22,y, duration=.05)
		pt.click()
		sleep(1)
		extraer_mensaje()
	else:
		sleep(1)
		posicion = pt.locateCenterOnScreen('imagenes/inicio.png', grayscale=False, confidence=.9)
		if posicion is not None:
			x = int(posicion[0])*pct_x
			y = int(posicion[1])*pct_y
			pt.moveTo(x-50,y, duration=.05)
			pt.click()
		print('No hay nuevos mensajes')

while True:
	sleep(3)
	buscar_nuevo_mensaje()

