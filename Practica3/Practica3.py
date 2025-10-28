import csv

# ============================================================
# 1. Clase RegistroHorario
# ============================================================
class RegistroHorario:
    def __init__(self, empleado: str, dia: str, entrada: int, salida: int):
        self.empleado = empleado
        self.dia = dia
        self.entrada = entrada
        self.salida = salida

    def duracion(self) -> int:
        """Devuelve la cantidad de horas trabajadas en este registro"""
        return self.salida - self.entrada


# ============================================================
# 2. Funciones principales
# ============================================================

def leer_csv(nombre_archivo='horarios.csv'):
    """Lee el archivo CSV y crea una lista de objetos RegistroHorario"""
    registros = []
    try:
        with open(nombre_archivo, newline='', encoding='utf-8') as f:
            lector = csv.reader(f, delimiter=';', quotechar='"')
            next(lector, None)  # Saltar cabecera si existe
            for fila in lector:
                nombre, dia, h_entrada, h_salida = fila
                entrada = int(h_entrada)
                salida = int(h_salida)
                registros.append(RegistroHorario(nombre, dia, entrada, salida))
        print(f"Se han leído {len(registros)} registros correctamente.\n")
    except FileNotFoundError:
        print("❌ No se encontró el archivo horarios.csv.\n")
    return registros


def mostrar_empleados_por_dia(registros):
    """Muestra los empleados que trabajaron cada día"""
    empleados_por_dia = {}
    for registro in registros:
        empleados_por_dia.setdefault(registro.dia, set()).add(registro.empleado)

    print("Empleados por día:")
    for dia, empleados in empleados_por_dia.items():
        print(f"{dia}: {empleados}")
    print()
    return empleados_por_dia


def generar_resumen_horarios(registros):
    """Genera el archivo resumen_horarios.csv"""
    horas_totales = {}
    for registro in registros:
        horas_totales.setdefault(registro.empleado, 0)
        horas_totales[registro.empleado] += registro.duracion()

    with open('resumen_horarios.csv', 'w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        escritor.writerow(['Empleado', 'Horas totales'])
        for empleado, total in horas_totales.items():
            escritor.writerow([empleado, total])
    print("Archivo 'resumen_horarios.csv' generado correctamente.\n")


def empleados_madrugadores(registros, hora_referencia=8):
    """Crea un archivo con empleados que comienzan antes de cierta hora"""
    madrugadores = {r.empleado for r in registros if r.entrada < hora_referencia}
    with open('madrugadores.csv', 'w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f, delimiter=';')
        escritor.writerow(['Empleado', 'Hora entrada'])
        for r in registros:
            if r.empleado in madrugadores and r.entrada < hora_referencia:
                escritor.writerow([r.empleado, r.entrada])
    print("Archivo 'madrugadores.csv' creado.\n")


def empleados_en_dos_dias(empleados_por_dia):
    """Genera el archivo con empleados que trabajaron lunes y viernes"""
    if 'Lunes' in empleados_por_dia and 'Viernes' in empleados_por_dia:
        en_dos_dias = empleados_por_dia['Lunes'] & empleados_por_dia['Viernes']
        with open('en_dos_dias.csv', 'w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f, delimiter=';')
            escritor.writerow(['Empleado'])
            for empleado in en_dos_dias:
                escritor.writerow([empleado])
        print("Archivo 'en_dos_dias.csv' creado.\n")
    else:
        print("No hay datos de Lunes o Viernes.\n")


def resumen_semanal(registros):
    """Genera el archivo resumen_semanal.csv con días y horas totales"""
    resumen = {}
    for r in registros:
        if r.empleado not in resumen:
            resumen[r.empleado] = {'dias': set(), 'horas': 0}
        resumen[r.empleado]['dias'].add(r.dia)
        resumen[r.empleado]['horas'] += r.duracion()

    with open('resumen_semanal.csv', 'w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f, delimiter=';')
        escritor.writerow(['Empleado', 'Dias trabajados', 'Horas totales'])
        for empleado, datos in resumen.items():
            escritor.writerow([empleado, len(datos['dias']), datos['horas']])
    print("Archivo 'resumen_semanal.csv' creado.\n")


# ============================================================
# 3. Menú interactivo
# ============================================================

def menu():
    registros = []
    empleados_por_dia = {}

    while True:
        print("========== MENÚ PRINCIPAL ==========")
        print("1. Leer archivo horarios.csv")
        print("2. Mostrar empleados por día")
        print("3. Generar resumen_horarios.csv")
        print("4. Crear madrugadores.csv")
        print("5. Crear en_dos_dias.csv")
        print("6. Crear resumen_semanal.csv")
        print("0. Salir")
        print("====================================")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registros = leer_csv()

        elif opcion == "2":
            if registros:
                empleados_por_dia = mostrar_empleados_por_dia(registros)
            else:
                print("Primero debe leer el archivo CSV (opción 1).\n")

        elif opcion == "3":
            if registros:
                generar_resumen_horarios(registros)
            else:
                print("Primero debe leer el archivo CSV.\n")

        elif opcion == "4":
            if registros:
                empleados_madrugadores(registros)
            else:
                print("Primero debe leer el archivo CSV.\n")

        elif opcion == "5":
            if empleados_por_dia:
                empleados_en_dos_dias(empleados_por_dia)
            else:
                print("Primero debe generar los conjuntos por día (opción 2).\n")

        elif opcion == "6":
            if registros:
                resumen_semanal(registros)
            else:
                print("Primero debe leer el archivo CSV.\n")

        elif opcion == "0":
            print("Programa finalizado.")
            break

        else:
            print("Opción no válida. Inténtelo de nuevo.\n")


# ============================================================
# 4. Programa principal
# ============================================================
if __name__ == "__main__":
    menu()
