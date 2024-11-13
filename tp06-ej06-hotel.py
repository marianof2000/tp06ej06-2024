"""
Un hotel necesita un programa para gestionar la operación de sus habitaciones. 
El hotel cuenta con 10 pisos y 6 habitaciones por piso. 
Por cada huésped o grupo familiar que se aloja en el mismo se registra la siguiente información:
    DNI del cliente (número entero)
    Apellido y Nombre
    Fecha de ingreso (DDMMAAAA)
    Fecha de egreso (DDMMAAAA)
    Cantidad de ocupantes

Se solicita desarrollar un programa para realizar las siguientes tareas:
·Registrar el ingreso de huéspedes al hotel, hasta que se ingrese un número de DNI -1.
Esta información deberá grabarse en un archivo CSV donde cada registro incluirá todos
los campos indicados más arriba. Tener en cuenta que los números de DNI no pueden
repetirse y que la fecha de salida debe ser mayor a la de entrada.
·Finalizado el ingreso de huéspedes se solicita:
    a.Leer el archivo de huéspedes y asignar la habitaciones a cada uno. 
    El piso y habitación son asignados arbitrariamente, y no puede asignarse una habitación ya otorgada.
    b.Mostrar el piso con mayor cantidad de habitaciones ocupadas.
    c.Mostrar cuántas habitaciones vacías hay en todo el hotel.
    d.Mostrar el piso con mayor cantidad de personas.
    e.Mostrar cuál será la próxima habitación en desocuparse. La fecha actual se ingresa por teclado. 
    Mostrar todas las que correspondan.
    f.Mostrar un listado de todos los huéspedes registrados en el hotel, ordenado por cantidad de días de alojamiento.
"""

# Ej: 06

import os
import random as rn
from datetime import datetime
from tabulate import tabulate


def limpiar_consola():
    """
    Limpia la consola de comandos.
    Esta función ejecuta un comando del sistema operativo para limpiar la consola,
    tanto en sistemas Windows como en MacOS y Linux.
    """
    os.system("cls" if os.name == "nt" else "clear")


def graba_huespedes(dict_huespedes):
    """
    Graba en un archivo CSV el diccionario de huéspedes, con sus respectivos datos.
    El archivo se llama "huespedes.csv" y se crea en la carpeta actual.
    """
    encabezado = ["DNI", "ApeNom", "F_Ingreso", "F_Egreso", "Ocupantes"]
    try:
        with open("huespedes.csv", "wt", encoding="utf-8") as f:
            f.write(",".join(encabezado) + "\n")
            for dni, datos in dict_huespedes.items():
                linea = []
                linea.append(dni)
                for dato in datos.values():
                    linea.append(dato)
                linea_str = f'{",".join(linea)}\n'
                f.write(linea_str)
    except Exception as e:
        print(f"Error: {e}")
    else:
        print("Se guardó el archivo de huéspedes")


def verifica_dni(dni, huespedes):
    """
    Verifica si un DNI ya se encuentra en el diccionario de huéspedes.
    Parameters:
    dni (int): DNI a verificar
    huespedes (dict): Diccionario de huéspedes con sus respectivos datos
    Returns:
    bool: True si el DNI se encuentra en el diccionario, False en caso de no encontrarse
    """
    return dni in huespedes.keys()


def valida_fecha(f_ing, f_egr):
    """
    Valida que la fecha de ingreso sea menor a la fecha de egreso
    Parameters:
    f_ing (str): Fecha de ingreso en formato "%d%m%Y"
    f_egr (str): Fecha de egreso en formato "%d%m%Y"
    Returns:
    bool: True si la fecha de ingreso es menor, False en caso de error
    """
    if len(f_ing) == 8 and len(f_egr) == 8:
        try:
            f_ing = datetime.strptime(f_ing, "%d%m%Y")
            f_egr = datetime.strptime(f_egr, "%d%m%Y")
        except:
            return False
        else:
            return f_ing < f_egr
    return False


def registrar_ingresos():
    """
    Registra los ingresos de huéspedes.
    Pide al usuario que ingrese los datos de cada huésped y los guarda en un diccionario.
    Verifica que el DNI no se encuentre en el diccionario y que las fechas sean correctas.
    Si el usuario ingresa -1, se guardan los datos en un archivo y se cierra el programa.
    """
    huespedes = {}
    while True:
        datos = {}
        dni = input("Ingrese el DNI: ")
        if dni == "-1":
            if len(huespedes):
                print(huespedes)
                graba_huespedes(huespedes)
            else:
                print("No se registraron huespedes")
            return
        elif len(dni) != 8 and not dni.isdigit():
            print("El DNI debe tener 8 dígitos")
        elif not verifica_dni(dni, huespedes):
            while True:
                ape_nom = input("Ingrese el apellido y nombre: ").capitalize()
                if ape_nom:
                    break
                else:
                    print("El apellido y nombre deben contener solo letras")
            while True:
                f_ing = input("Ingrese la fecha de ingreso (DDMMAAAA): ")
                f_egr = input("Ingrese la fecha de egreso (DDMMAAAA): ")
                if (
                    f_ing != f_egr
                    and f_ing.isnumeric()
                    and f_egr.isnumeric()
                    and valida_fecha(f_ing, f_egr)
                ):
                    break
                else:
                    print("Las fechas son incorrectas")
            while True:
                try:
                    cant_ocupantes = int(input("Ingrese la cantidad de ocupantes: "))
                except:
                    print("La cantidad de ocupantes debe ser un número entero")
                else:
                    if cant_ocupantes > 0:
                        break
                    else:
                        print("Ingrese un número de ocupantes")
            datos["ape_nom"] = ape_nom
            datos["f_ingreso"] = f_ing
            datos["f_egreso"] = f_egr
            datos["ocupantes"] = str(cant_ocupantes)
            huespedes[dni] = datos
        else:
            print("El DNI ya se encuentra registrado")


def opcion_a(pisos, habitaciones):
    """
    Asigna aleatoriamente habitaciones a los pasajeros en un hotel.
    Intenta abrir el archivo 'huespedes.csv' para leer la información de los pasajeros.
    Para cada pasajero, asigna aleatoriamente un piso y una habitación que no estén
    ocupados. Almacena la información de la habitación y el pasajero en una lista.
    Parameters
    ----------
    pisos : int
        Número total de pisos en el hotel.
    habitaciones : int
        Número total de habitaciones por piso en el hotel.
    Returns
    -------
    list
        Una lista de tuplas, donde cada tupla contiene:
        - Una tupla (piso, habitacion) que representa la ubicación de la habitación.
        - Una tupla (dni, ape_nom, f_ingreso, f_egreso, cant_ocupantes) con los datos
          del pasajero.
    """
    ocupadas = []
    piso_hab = []
    try:
        with open("huespedes2.csv", "rt", encoding="utf-8") as f:
            pasajeros = [linea.strip().split(",") for linea in f.readlines()[1:]]
    except Exception as e:
        print(f"Error: {e}")
    else:
        if len(pasajeros) > pisos * habitaciones:
            print("No hay suficientes habitaciones para todos los pasajeros")
        for p in pasajeros[: pisos * habitaciones]:
            while True:
                piso = rn.randint(1, pisos)
                habitacion = rn.randint(1, habitaciones)
                if (piso, habitacion) not in piso_hab:
                    piso_hab.append((piso, habitacion))
                    break
            ocupadas.append(((piso, habitacion), tuple(p)))
    # Genera esta estructura
    # [((piso, habitacion), (dni, ape_nom, f_ingreso, f_egreso, cant_ocupantes)), ...]
    return ocupadas


def opcion_b(hotel, pisos):
    """
    Muestra el piso con más habitaciones ocupadas
    Recibe una lista de tuplas (habitación, pasajero) y el total de pisos en el hotel.
    Calcula la cantidad de habitaciones ocupadas por piso y muestra el piso con más habitaciones ocupadas.
    Parameters
    ----------
    hotel : list
        lista de tuplas (habitación, pasajero)
    pisos : int
        total de pisos en el hotel
    Returns
    -------
    None
    """
    total = [
        sum([1 for hab, pasajero in hotel if hab[0] == p]) for p in range(1, pisos + 1)
    ]
    maximo = max(total)
    ocupadas = total.index(maximo) + 1
    print(
        f"El piso con mayor cantidad de habitaciones ocupadas es el {ocupadas} con {maximo} habitaciones"
    )


def opcion_c(hotel, total):
    """
    Muestra la cantidad de habitaciones vacías en el hotel
    Recibe una lista de tuplas (habitación, pasajero) y el total de habitaciones
    en el hotel. Calcula la cantidad de habitaciones ocupadas y muestra la
    cantidad de habitaciones vacías.
    Parameters
    ----------
    hotel : list
        lista de tuplas (habitación, pasajero)
    total : int
        total de habitaciones en el hotel
    Returns
    -------
    None
    """
    ocupadas = len(hotel)
    print(f"Hay {total - ocupadas} habitaciones vacias")


def opcion_d(hotel, pisos):
    """
    Muestra el piso con mayor cantidad de personas
    Recibe una lista de tuplas (habitación, pasajero) y el total de pisos en el hotel.
    Calcula la cantidad de personas por piso y muestra el piso con mayor cantidad de personas.
    Parameters
    ----------
    hotel : list
        lista de tuplas (habitación, pasajero)
    pisos : int
        total de pisos en el hotel
    Returns
    -------
    None
    """
    mayor_cantidad = [
        sum([int(pasajero[4]) for hab, pasajero in hotel if hab[0] == p])
        for p in range(1, pisos + 1)
    ]
    maximo = max(mayor_cantidad)
    piso = mayor_cantidad.index(maximo) + 1
    print(
        f"El piso con mayor cantidad de personas es el {piso} con {maximo} personas"
    )


def invertir_fecha(fecha):
    """
    Invierte el formato de una fecha de 'DDMMAAAA' a 'AAAAMMDD'.
    Parameters
    ----------
    fecha : str
        Fecha en formato 'DDMMAAAA'.
    Returns
    -------
    str
        Fecha en formato 'AAAAMMDD'.
    """
    return fecha[6:] + fecha[3:5] + fecha[:2]


def opcion_e(hotel, fecha):
    """
    Encuentra la habitación cuyo pasajero tiene la fecha de egreso más cercana a la fecha dada.
    Recibe una lista de tuplas (habitación, pasajero) y una fecha.
    Filtra las habitaciones cuyos pasajeros tienen una fecha de egreso mayor o igual a la fecha dada,
    y retorna la habitación con la fecha de egreso más cercana a la fecha proporcionada.
    Parameters
    ----------
    hotel : list
        Lista de tuplas (habitación, pasajero).
    fecha : str
        Fecha en formato 'DDMMAAAA'.
    Returns
    -------
    list
        Una lista con una tupla que contiene la habitación y el pasajero cuyo egreso es más cercano a la fecha dada.
    """
    filtrado = [
        (hab, pasajero)
        for hab, pasajero in hotel
        if int(invertir_fecha(pasajero[3])) >= int(invertir_fecha(fecha))
    ]
    ordenado = sorted(
        filtrado,
        key=lambda x: (int(invertir_fecha(x[1][3])) - int(invertir_fecha(fecha))),
    )
    return [ordenado[0]]


def opcion_f(hotel):
    """
    Ordena el listado de habitaciones por la duración de la estadía.
    Parameters
    ----------
    hotel : list
        lista de tuplas (habitación, pasajero)
    Returns
    -------
    list
        lista de tuplas (habitación, pasajero) ordenada por la duración de la estadía
    """
    ordenado = sorted(
        hotel,
        key=lambda x: (int(invertir_fecha(x[1][3])) - int(invertir_fecha(x[1][2]))),
    )
    return ordenado


def mostrar_listado(hotel):
    """
    Muestra el listado de habitaciones ocupadas
    Recibe una lista de tuplas (habitación, pasajero) y la imprime en formato de tabla.
    Parameters
    ----------
    hotel : list
        lista de tuplas (habitación, pasajero)
    Returns
    -------
    None
    """
    encabezado = ["Piso/Hab", ("DNI", "Pasajero", "Ingreso", "Egreso", "Ocupantes")]
    print(
        tabulate(
            sorted(hotel, key=lambda x: x[0][0]), headers=encabezado, tablefmt="grid"
        )
    )


def main():
    """
    Programa principal que muestra el menú de opciones del hotel y permite
    seleccionar una opción para realizar una acción.
    """
    pisos = 10
    habitaciones = 6
    limpiar_consola()
    registrar_ingresos()
    pausa = input("\nPresione Enter para continuar...")
    # Nota: se debería usar un dict de funciones (tema de otra materia)
    hotel = opcion_a(pisos, habitaciones)
    if hotel:
        mostrar_listado(hotel)
        pausa = input("\nPresione Enter para continuar...")
        limpiar_consola()
        # opcion b
        mostrar_listado(hotel)
        opcion_b(hotel, pisos)
        pausa = input("\nPresione Enter para continuar...")
        limpiar_consola()
        # opcion c
        mostrar_listado(hotel)
        opcion_c(hotel, pisos * habitaciones)
        pausa = input("\nPresione Enter para continuar...")
        limpiar_consola()
        # opcion d
        mostrar_listado(hotel)
        opcion_d(hotel, pisos)
        pausa = input("\nPresione Enter para continuar...")
        limpiar_consola()
        # opcion e
        while True:
            fecha = input("Ingrese la fecha de ingreso (DDMMAAAA): ")
            if len(fecha) == 8 and fecha.isnumeric():
                try:
                    fecha2 = datetime.strptime(fecha, "%d%m%Y")
                except:
                    pass
                else:
                    print("Próxima habitación a desocuparse")
                    encabezado = [
                        "Piso/Hab",
                        ("DNI", "Pasajero", "Ingreso", "Egreso", "Ocupantes"),
                    ]
                    print(
                        tabulate(
                            opcion_e(hotel, fecha), headers=encabezado, tablefmt="grid"
                        )
                    )
                    break
            print("La fecha ingresada es incorrecta\n")
        pausa = input("\nPresione Enter para continuar...")
        limpiar_consola()
        # opcion f
        print("Listado ordenado por cantidad de días de alojamiento")
        print(tabulate(opcion_f(hotel), tablefmt="grid"))
        pausa = input("\nPresione Enter para continuar...")
    else:
        print("\nNo hay pasajeros registrados")


if __name__ == "__main__":
    # No se usan clases ni dataclass
    main()
