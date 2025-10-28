horarios = {
    'María':  ('08', '16'),
    'Juan':   ('09', '17'),
    'Lucía':  ('07', '15'),
    'Diego':  ('10', '18'),

    'Ana':    ('08', '14'),
    'Raúl':   ('12', '20'),
}

def mostrar_registros():
    """
    Recorre el diccionario y muestra los empleados con sus horarios,
    numerados a partir de 1.
    """
    print("\n--- Lista de empleados y horarios ---")
    for i, (nombre, (entrada, salida)) in enumerate(horarios.items(), start=1):
        print(f"{i}. {nombre} -> Entrada: {entrada}h | Salida: {salida}h")
    print()

def contar_entradas():
    """
    Solicita una hora al usuario y cuenta cuántas personas
    entraron antes o a esa hora.
    """
    try:
        hora_ref = int(input("Introduce una hora de referencia (0-23): ").strip())
        if hora_ref < 0 or hora_ref > 23:
            print("La hora debe estar entre 0 y 23.\n")
            return
    except ValueError:
        print("Debes introducir un número entero válido.\n")
        return

    contador = 0
    for nombre, (entrada, _) in horarios.items():
        if int(entrada) <= hora_ref:
            contador += 1

    print(f"{contador} empleados entraron antes o a las {hora_ref}h.\n")
 
def menu():
    """
    Menú principal repetitivo (bucle while) para elegir acciones:
      1) Mostrar registros
      2) Contar entradas
      3) Salir
    """
    while True:
        print("========== MENÚ ==========")
        print("1) Mostrar registros")
        print("2) Contar entradas")
        print("3) Salir")
        opcion = input("Elige una opción (1-3): ").strip()
 
        if opcion == '1':
            mostrar_registros()
        elif opcion == '2':
            contar_entradas()
        elif opcion == '3':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.\n")

if __name__ == '__main__': 
    menu()