#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os

#Arrancamos el escenario vnx
def crear():
	print("Creamos el escenario")
	os.system("sudo vnx -f /home/upm/pfinal/pfinal.xml --create")
#Paramos el escenario vnx y borramos todas las configuraciones 
def borrar():
	print("Destruimos el escenario")
	os.system("sudo vnx -f /home/upm/pfinal/pfinal.xml --destroy")
#Paramos el escenario vnx guardando los cambios
def parar():
	print("Paramos el escenario")
	os.system("sudo vnx -f /home/upm/pfinal/pfinal.xml --shutdown")
#Rearrancamos el escenario vnx con los cambios guardados
def arrancar():
	print("Rearrancamos el escenario")
	os.system("sudo vnx -f /home/upm/pfinal/pfinal.xml --start")
# VAMOS A HACER QUE LOS COMANDOS PASEN COMO ARGUMENTO
f = sys.argv
args = len(f)

if args > 1:
	metodo = f[1]
	print("El argurmento 1 es :"+  str(metodo))
	
	if metodo == "crear":
		crear()
	elif metodo == "borrar":
		borrar()		
	elif metodo == "parar":
		parar()
	elif metodo == "arrancar":
		arrancar()
	elif metodo == "ayuda":
		print("\n\n######## AYUDA #######\n")

		print("* './Confi_inicial.py' ejecuta diferentes funciones segun la opcion que se añada detras: \n ")
		print("* './Confi_inicial.py crear' creamos el escenario vnx\n")
		print("* './Confi_inicial.py borrar' borra el escenario vnx\n ")
		print("* './Confi_inicial.py parar'  para el escenario vnx y guarda los cambios\n ")
		print("* './Confi_inicial.py arrancar'  arranca el escenario vnx con los cambios guardados\n")
		print("\n######## FIN DE LA AYUDA #######\n\n")
		
else:
	print "Las opciones son erroneas. Introduzca './Confi_Inicial.py ayuda' para mas informacion"
