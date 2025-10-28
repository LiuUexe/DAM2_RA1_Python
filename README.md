# Mini-CRM de Eventos

Proyecto final de Python: una aplicación de consola que gestiona **clientes, eventos y ventas** usando ficheros **CSV**.  
Permite leer datos, dar de alta clientes, filtrar ventas por fechas, calcular estadísticas y exportar informes.  

---

## Funcionalidades
- Carga y lectura de CSV (`clientes`, `eventos`, `ventas`)
- Alta de clientes con validación de email
- Filtro de ventas por rango de fechas
- Estadísticas: ingresos, categorías, precios y eventos próximos
- Exportación de informe `informe_resumen.csv`
- Menú interactivo en consola

---

## Estructura del proyecto
```plaintext
PracticaFinal/
├─ Final.py                 # Código principal del Mini-CRM
└─ data/                    # Carpeta con los archivos CSV
   ├─ clientes.csv
   ├─ eventos.csv
   └─ ventas.csv

