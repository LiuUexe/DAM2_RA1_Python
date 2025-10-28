Mini-CRM de Eventos

Aplicación de consola en Python que gestiona clientes, eventos y ventas mediante ficheros CSV.
Incluye un menú interactivo, programación orientada a objetos y manejo de fechas con datetime.

Mini-CRM de Eventos

Aplicación de consola en Python que gestiona clientes, eventos y ventas mediante ficheros CSV.
Incluye un menú interactivo, programación orientada a objetos y manejo de fechas con datetime.


Tecnologías y conceptos

Python estándar (csv, datetime, statistics, os, re).

POO: clases Cliente, Evento, Venta.

Colecciones: listas, diccionarios, conjuntos y tuplas.

Validaciones: email, fechas y errores de archivo.

PracticaFinal/
├─ Final.py                 # Código principal con el menú y la lógica del Mini-CRM
└─ data/                    # Carpeta que contiene los ficheros de datos
   ├─ clientes.csv          # Lista de clientes (id, nombre, email, fecha_alta, activo)
   ├─ eventos.csv           # Lista de eventos (id, nombre, categoría, fecha, precio)
   └─ ventas.csv            # Lista de ventas (id, cliente_id, evento_id, fecha, unidades, precio_unitario)

   El programa lee los tres CSV desde la carpeta data/.

Los archivos de salida (informe_resumen.csv o nuevos clientes) también se guardan ahí.

El nombre Final.py es correcto; solo asegúrate de actualizar las rutas en el código si cambias de carpeta.
