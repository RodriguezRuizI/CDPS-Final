#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from subprocess import call

#CONFIGURACIONES EN LA BBDD
def bbddConf():
	print("Configuración de la base de datos")
	#INSTALAMOS MARIADB
	line="sudo lxc-attach --clear-env -n bbdd -- apt update"
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n bbdd -- apt -y install mariadb-server"
	call(line, shell=True)
	#EMPEZAMOS LAS CONFIGURACIONES
	line="sudo lxc-attach -n bbdd -- sed -i -e 's/bind-address.*/bind-address=0.0.0.0/' -e 's/utf8mb4/utf8/' /etc/mysql/mariadb.conf.d/50-server.cnf"
	call(line, shell=True)
	#REINICIAMOS LA BASE DE DATOS CON LAS CONFIGURACIONES YA FIJADAS.
	line="sudo lxc-attach --clear-env -n bbdd -- systemctl restart mysql"
	call(line, shell=True)
	#DAMOS PERMISO A MYSQLADMIN
	line="sudo lxc-attach --clear-env -n bbdd -- mysqladmin -u root password xxxx"
	call(line, shell=True)
	#CONFIGURAMOS LA BASE DE DATOS DANDOLE UN NOMBRE UN USUARIO CON TODOS SUS PRIVILEGIOS Y UNA CONTRASEÑA AL USUARIO
	line="sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"CREATE USER 'quiz' IDENTIFIED BY 'xxxx';\""
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"CREATE DATABASE quiz;\""
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"GRANT ALL PRIVILEGES ON quiz.* to 'quiz'@'localhost' IDENTIFIED by 'xxxx';\""
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"GRANT ALL PRIVILEGES ON quiz.* to 'quiz'@'%' IDENTIFIED by 'xxxx';\""
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"FLUSH PRIVILEGES;\""
	call(line, shell=True)
	#REINICIAMOS LA BASE DE DATOS CON LAS CONFIGURACIONES YA FIJADAS.
	line="sudo lxc-attach --clear-env -n bbdd -- systemctl restart mysql"
	call(line, shell=True)

#CONFIGURACIONES DE LA NAS
def NASConf():
	print("Configuracion de las NAS para poder usarlas")
	#AÑADIMOS LOS SERVIDORES GLUSTER
	line="sudo lxc-attach --clear-env -n nas1 -- gluster peer probe 20.2.4.22"
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n nas1 -- gluster peer probe 20.2.4.23"
	call(line, shell=True)
	#CREAMOS EL VOLUMEN PARA LOS TRES SERVIDORES NAS
	line="sudo lxc-attach --clear-env -n nas1 -- gluster volume create nas replica 3 transport tcp 20.2.4.21:/nas 20.2.4.22:/nas 20.2.4.23:/nas force"
	call(line, shell=True)
	#ARRANCAMOS EL VOLUMEN
	line="sudo lxc-attach --clear-env -n nas1 -- gluster volume start nas"
	call(line, shell=True)
	#POR SI TUVIESEMOS QUE RECUPERAR EL VOLUMEN ANTE POSIBLES CAIDAS DE UNO DE LOS SERVIDORES
	line="sudo lxc-attach --clear-env -n nas1 -- gluster volume set nas network.ping-timeout 5"
	call(line, shell=True)

def serversConf():
	print("Hacemos configuraciones en los servidores")
	#INSTALACION DE MARIA DB EN LOS SERVES
	line="sudo lxc-attach --clear-env -n s1 -- apt -y install mariadb-client"
	call(line, shell=True)
#	line="sudo lxc-attach --clear-env -n s1 -- mysql -h 20.2.4.31 -u quiz --password='xxxx' quiz"
#	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n s2 -- apt -y install mariadb-client"
	call(line, shell=True)
#	line="sudo lxc-attach --clear-env -n s2 -- mysql -h 20.2.4.31 -u quiz --password='xxxx' quiz"
#	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n s3 -- apt -y install mariadb-client"
	call(line, shell=True)
#	line="sudo lxc-attach --clear-env -n s3 -- mysql -h 20.2.4.31 -u quiz --password='xxxx' quiz"
#	call(line, shell=True)
	#MONTAMOS LA NAS EN LOS SERVES
	line="sudo lxc-attach --clear-env -n s1 -- mkdir /mnt/nas"
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n s1 -- mount -t glusterfs 20.2.4.21:/nas /mnt/nas"
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n s2 -- mkdir /mnt/nas"
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n s2 -- mount -t glusterfs 20.2.4.21:/nas /mnt/nas"
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n s3 -- mkdir /mnt/nas"
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n s3 -- mount -t glusterfs 20.2.4.21:/nas /mnt/nas"
	call(line, shell=True)


def lbConf():
# Configuracion del balanceador de carga
	line="sudo lxc-attach --clear-env -n lb -- apt-get update"
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n lb -- apt -y  install haproxy"
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n lb -- bash -c 'echo -e \"frontend lb \n bind *:80 \n mode http \n default_backend webservers \nbackend webservers \n mode http \n balance roundrobin \n server s1: 20.2.3.11:3000 check \n server s2: 20.2.3.12:3000 check \n server s3: 20.2.3.13:3000 check \n \" >> /etc/haproxy/haproxy.cfg'"
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n lb -- sudo service haproxy restart"
	call(line, shell=True)

def quizConf():

# Instalamos nodejs y npm en los servidores
	line="sudo lxc-attach --clear-env -n s1 -- apt update"
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n s1 -- apt -y install nodejs"
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n s1 -- apt -y install npm"
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n s2 -- apt update"
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n s2 -- apt -y install nodejs"
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n s2 -- apt -y install npm"
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n s3 -- apt update"
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n s3 -- apt -y install nodejs"
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n s3 -- apt -y install npm"
	call(line, shell=True)
	# Clonamos el repositorio
	line="sudo lxc-attach --clear-env -n s1 -- bash -c \"cd /root; git clone https://github.com/CORE-UPM/quiz_2019.git; cd /root/quiz_2019; npm install; npm install forever; npm install mysql2; export QUIZ_OPEN_REGISTER=yes; export DATABASE_URL=mysql://quiz:xxxx@20.2.4.31:3306/quiz; npm run-script migrate_cdps; npm run-script seed_cdps; ./node_modules/forever/bin/forever start ./bin/www\""
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n s2 -- bash -c \"cd /root; git clone https://github.com/CORE-UPM/quiz_2019.git; cd /root/quiz_2019; npm install; npm install forever; npm install mysql2; export QUIZ_OPEN_REGISTER=yes; export DATABASE_URL=mysql://quiz:xxxx@20.2.4.31:3306/quiz; ./node_modules/forever/bin/forever start ./bin/www\""
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n s3 -- bash -c \"cd /root; git clone https://github.com/CORE-UPM/quiz_2019.git; cd /root/quiz_2019; npm install; npm install forever; npm install mysql2; export QUIZ_OPEN_REGISTER=yes; export DATABASE_URL=mysql://quiz:xxxx@20.2.4.31:3306/quiz; ./node_modules/forever/bin/forever start ./bin/www\""
	call(line, shell=True)
	# Hacemos el enlace simbólico con el directorio asociado al cluster
	line="sudo lxc-attach --clear-env -n s1 -- bash -c \"cd /root/quiz_2019/public; ln -s /mnt/nas uploads \""
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n s2 -- bash -c \"cd /root/quiz_2019/public; ln -s /mnt/nas uploads \""
	call(line, shell=True)
	line="sudo lxc-attach --clear-env -n s3 -- bash -c \"cd /root/quiz_2019/public; ln -s /mnt/nas uploads \""
	call(line, shell=True)

def fwConf():
	#COPIA EL ARCHIVO .FW DENTRO DEL FIREWALL DEL ESCENARIO
	line="sudo cp fw.fw /var/lib/lxc/fw/rootfs/root"
	call(line, shell=True)
	#EJECUTA EL ARCHIVO .FW HACIENDO VIGENTES LAS NORMAS
	line="sudo lxc-attach --clear-env -n fw -- bash -c  /root/fw.fw"
	call(line, shell=True)

def configurarTodo():
	print("Hacemos las configuraciones de todo el sistema")
	bbddConf()
	NASConf()
	serversConf()
	lbConf()
	quizConf()
	fwConf()
# VAMOS A HACER QUE LOS COMANDOS PASEN COMO ARGUMENTO
f = sys.argv
args = len(f)

if args > 1:
	metodo = f[1]
	print("El argurmento 1 es :"+  str(metodo))
	
	if metodo == "bbddConf":
		bbddConf()
	elif metodo == "NASConf":
		NASConf()		
	elif metodo == "serversConf":
		serversConf()
	elif metodo == "lbConf":
		lbConf()
	elif metodo == "quizConf":
		quizConf()
	elif metodo == "fwConf":
		fwConf()
	elif metodo == "configurarTodo":
		configurarTodo()
	elif metodo == "ayuda":
		print("\n\n######## AYUDA #######\n")

		print("* './Configuracion.py' ejecuta diferentes funciones segun la opcion que se añada detras: \n ")
		print("* './Configuracion.py bbddConf'\n")
		print("* './Configuracion.py NASConf'\n")
		print("* './Configuracion.py' serversConf\n")
		print("* './Configuracion.py' lbConf\n")
		print("* './Configuracion.py' quizConf\n")
		print("* './Configuracion.py' fwConf\n")
		print("* './Configuracion.py' configurarTodo\n")
		print("\n######## FIN DE LA AYUDA #######\n\n")
		
else:
	print "Las opciones son erroneas. Introduzca './Configuracion.py ayuda' para mas informacion"
