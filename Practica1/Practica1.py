#Ennunciado 1:
num_trabajadores = int(input("Cuántos empleados vas a introducir?\n"))
hora_referencia = int(input("Hora de referencia (0-23):"))

contar_tiempo = 0;
empleado_salida_temprana = "";
salida_temprana = 24;

#Enunciado 2:
for i in range(num_trabajadores):
    print("\nEmpleado", i + 1);
    nombre = input("Nombre: ")
    hora_entrada = int(input("Hora de entrada (0-23): "))
    hora_salida = int(input("Hora de salida (0-23): "))

#Enunciado 3:
    if hora_salida > hora_entrada:
        print("Horario correcto")
    else:
        print("Horario incorrecto")
        continue

#Enunciado 4:
    if hora_entrada <= hora_referencia:
        contar_tiempo += 1

#Enunciado 5:
    if hora_entrada > empleado_salida_temprana:
        salida_temprana = hora_salida
        empleado_salida_temprana = nombre

print("\n=========RESULTADO=========")
print("Empleado que entraron antes o la hora de referencia: " , contar_tiempo)
print("Empleado que salio mas temprano: " , salida_temprana)




