#!/usr/bin/env python3
try:
    # Intentamos importar alguno de los modulos necesarios
    import time 
    import sys
    from pwn import *
    import signal
    from termcolor import colored
except ImportError:
    print("Modulos no encontrados.")
    print("[+] Puedes descargar cada modulo con python3 -m venv .venv")
    print("[+] source .venv/bin/activate")
    print("[+] pip3 install <modulos_faltantes>")
    # Si sale mal, daremos instrucciones para poder tener los modulos necesarios y salimos con un codigo de estado exitoso xd
    sys.exit(0)



def handler(sig, frame):
    print(colored("\n\n[!] Saliendo...\n",'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, handler)
# Funcion de ctrl_c para la salida forzada

data = {
        "Usuario" : "Contraseña"
        }
# data se refiere a los usuarios en la base de datos
admins = {
        "admin" : "123"
        }
# administrador, aunque le puedes agregar mas admins jeje
usuarios_eliminados = []
salida = lambda: log.failure("Saliendo...")
#tiempo = time.strftime('%H:%M:%S') -- No sale xD
#print(f'\rHora: {tiempo}', end='')


def iniciar_sesion():
    # Funcion para iniciar sesion
    usuario = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")
    if usuario in data and contraseña in data[f'{usuario}']:
        log.success("Inicio de sesión exitoso!!")
    else:
        log.failure("Nombre de usuario o contraseñas incorrecto")

def registrarse():
    new_user = input("Nombre de usuario: ")
    if new_user in data:
        log.failure("El nombre de usuario ya esta en uso, considera usar otro...")
        registrarse()
    passwd_for_user = input("Contraseña: ") 
    repeat_passwd = input("Repite la contraseña: ")
    if passwd_for_user != repeat_passwd:
        log.failure("Las contraseñas no pueden ser distintas")
        registrarse()
    else:
        data[f'{new_user}'] = f'{passwd_for_user}'
        log.success(f"Usuario {new_user} creado con exito :)")
        Inicio()

def AdminPanel():
    while True:
        #log.info(f'{tiempo}')
        log.info("Panel de administrador, opciones disponibles: ")
        print(f"\t1) Conocer usuario en la base de datos ")
        print(f"\t2) Extraer número de usuarios ")
        print(f"\t3) Cambiar contraseña o usuario de algún individuo ")
        print(f"\t4) Eliminar usuarios")
        print(f"\t5) Salir")
        try:
            value = int(input("Elige alguna de las opciones: "))
            if value == 1:
                know_user = input("¿Qué usuario deseas averiguar? ")
                if know_user in data:
                    log.success("El usuario indicado esta en la base de datos")
                else:
                    log.failure("El usuario indicado no esta en la base de datos")
            elif value == 2:
                conteo = len(data)
                if conteo == 1:
                    log.info("Hay un usuario en la base de datos")
                elif conteo == 0:
                    log.info("No hay usuarios en la base de datos...")
                else:
                    print(f"Hay {conteo} usuarios en la base de datos")
                    pregunta = input("¿Deseas listar los usuarios? ").lower().strip()
                    if pregunta == "si" or pregunta == "s":
                        print("   ▼                     ▼")
                        for key, value in data.items():
                            print(f"{key}     -     {value}" )

                        input("Presiona cualquier tecla para regresar: ")
            elif value == 3:
                try:
                    passwd_or_user = int(input("¿Sobre que deseas hacer un cambio, usuario o contraseña?(1/2) "))
                    if passwd_or_user == 1:
                        usuario = input("Nombre de usuario: ")
                        if usuario in data:
                            nuevo_usuario = input("Nuevo nombre de usuario: ")
                            contraseña = input("Contraseña: ")
                            if contraseña in data[f'{usuario}']:
                                data[f'{nuevo_usuario}'] = data.pop(f'{usuario}')
                                log.success("Nombre de usuario cambiado")
                    elif passwd_or_user == 2:
                        validador_user = input("Nombre del usuario: ")
                        if validador_user in data:
                            act_passwd = input("Contraseña actual: ")
                            if act_passwd in data[f'{validador_user}']:
                                new_passwd = input("Nueva contraseña: ")
                                data[f'{validador_user}'] = f'{new_passwd}'
                                log.success("Contraseña cambiada con exito")
                            else:
                                log.failure("Error al introducir datos del usuario")
                    else:
                        log.failure("ERROR")
                except ValueError:
                    log.failure("ERROR")
            elif value == 5:
                salida()
                Inicio()
            elif value == 4:
                some = int(input("¿Deseas eliminar un usuario, o limpiar la base de datos?(1/2) "))
                if some == 1:
                    user = input("Especifica el usuario a eliminar: ")
                    if user in data:
                        data.pop(user)
                        usuarios_eliminados.append(user)
                        #log.info(f"El usuario eliminado a sido {user}")
                        listado = str(input("Deseas listar los usuarios eliminados?(s/n) ")).strip().lower()
                        if listado == "s" or listado == "si":
                            comprobador = int((len(usuarios_eliminados)))
                            if comprobador == 1:
                                log.info(f"El usuario eliminado es {' '.join(usuarios_eliminados)}")
                            else:
                                log.info(f"Los usuarios eliminados son {', '.join(usuarios_eliminados)}")
                        elif listado == "n" or listado == "no":
                            None
                    else:
                        log.failure("El usuario indicado no esta dentro de la base datos")
                elif some == 2:
                    longitud = len(data)
                    if longitud == 0:
                        log.failure("¿Como vas a intentar borrar una base de datos vacia?")
                    else:
                        data.clear()
                        log.info("Base de datos vaciada, suerte intentando iniciar sesion")
            else:
                log.failure("Opcion desconocida...")
        except ValueError:
            log.failure("ERROR")

def Inicio():
    while True:
        log.info("Bienvenido a la base de datos, por favor elige alguna de las opciones")
        print("\t1) Iniciar sesión" )
        print("\t2) Registrarse ")
        print("\t3) Iniciar como administrador ")
        print("\t4) Salir ")
        try:
            value = int(input("Tu opción va por aqui: "))
            if value == 1:
                iniciar_sesion()
            elif value == 2:
                registrarse()
            elif value == 3:
                usuario = input("Nombre de usuario: ")
                contraseña = input("Contraseña: ")
                if usuario in admins and contraseña in admins[f'{usuario}']:
                    AdminPanel()
                else:
                    log.failure("¿Quien rayos eres?, largo de aquí!!")
            elif value == 4:
                salida()
                sys.exit(1)
            else:
                log.failure("Opción no valida.")
        except (ValueError, TypeError):
            log.failure("ERROR")

Inicio()

