import csv
import os
import re
from datetime import datetime, date
from statistics import mean
from typing import List, Dict, Tuple, Set

# ------------------------------
# Rutas de archivos CSV
# ------------------------------
DATA_DIR = "data"
CLIENTES_CSV = os.path.join(DATA_DIR, "clientes.csv")
EVENTOS_CSV = os.path.join(DATA_DIR, "eventos.csv")
VENTAS_CSV = os.path.join(DATA_DIR, "ventas.csv")
INFORME_CSV = os.path.join(DATA_DIR, "informe_resumen.csv")

DATE_FMT = "%Y-%m-%d"  # Formato de fecha estándar

# ============================================================
# 1. Clases principales (POO)
# ============================================================

class Cliente:
    """Representa un cliente del CRM."""
    def __init__(self, id_: int, nombre: str, email: str, fecha_alta: date, activo: bool):
        self.id = id_
        self.nombre = nombre
        self.email = email
        self.fecha_alta = fecha_alta
        self.activo = activo

    def antiguedad_dias(self) -> int:
        """Devuelve los días que el cliente lleva dado de alta."""
        return (date.today() - self.fecha_alta).days

    def __str__(self):
        estado = "Activo" if self.activo else "Inactivo"
        return f"[{self.id}] {self.nombre} <{self.email}> | Alta: {self.fecha_alta} | {estado}"


class Evento:
    """Representa un evento (con fecha y categoría)."""
    def __init__(self, id_: int, nombre: str, categoria: str, fecha_evento: date, precio: float):
        self.id = id_
        self.nombre = nombre
        self.categoria = categoria
        self.fecha_evento = fecha_evento
        self.precio = precio

    def dias_hasta_evento(self) -> int:
        """Devuelve cuántos días faltan hasta el evento."""
        return (self.fecha_evento - date.today()).days

    def __str__(self):
        return f"[{self.id}] {self.nombre} ({self.categoria}) | {self.fecha_evento} | {self.precio:.2f}€"


class Venta:
    """Representa una venta (un cliente compra entradas de un evento)."""
    def __init__(self, id_: int, cliente_id: int, evento_id: int, fecha_venta: date, unidades: int, precio_unitario: float):
        self.id = id_
        self.cliente_id = cliente_id
        self.evento_id = evento_id
        self.fecha_venta = fecha_venta
        self.unidades = unidades
        self.precio_unitario = precio_unitario

    @property
    def total(self) -> float:
        """Importe total de la venta."""
        return self.unidades * self.precio_unitario

    def __str__(self):
        return f"[{self.id}] C{self.cliente_id} -> E{self.evento_id} | {self.fecha_venta} | uds={self.unidades} | {self.precio_unitario:.2f}€ (total {self.total:.2f}€)"


# ============================================================
# 2. Funciones de utilidades (CSV y validaciones)
# ============================================================

def ensure_data_dir():
    """Crea la carpeta data/ si no existe."""
    os.makedirs(DATA_DIR, exist_ok=True)

def parse_bool(s: str) -> bool:
    """Convierte texto en booleano (true/false)."""
    return s.strip().lower() in {"1", "true", "t", "yes", "y", "si", "sí"}

def email_valido(email: str) -> bool:
    """Valida formato básico de email."""
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email) is not None

def parse_date(s: str) -> date:
    """Convierte texto (YYYY-MM-DD) a objeto date."""
    return datetime.strptime(s.strip(), DATE_FMT).date()

def safe_read_csv(path: str) -> List[List[str]]:
    """Lee un CSV y devuelve una lista de filas (omite cabecera si hay)."""
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";", quotechar='"')
            rows = list(reader)
        # Si hay encabezado, lo salta
        if rows and any("id" in h.lower() or "nombre" in h.lower() for h in rows[0]):
            return rows[1:]
        return rows
    except FileNotFoundError:
        print(f"No se encontró {path}.")
        return []

def append_row_csv(path: str, header: List[str], row: List):
    """Añade una fila al CSV, creando el archivo si no existe."""
    file_exists = os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(row)


# ============================================================
# 3. Carga de datos desde CSV
# ============================================================

def cargar_datos():
    """Carga clientes, eventos y ventas desde los CSV."""
    ensure_data_dir()

    # --- CLIENTES ---
    clientes = []
    cli_index = {}
    for r in safe_read_csv(CLIENTES_CSV):
        try:
            c = Cliente(int(r[0]), r[1], r[2], parse_date(r[3]), parse_bool(r[4]))
            clientes.append(c)
            cli_index[c.id] = c
        except Exception as e:
            print(f"Error en cliente {r}: {e}")

    # --- EVENTOS ---
    eventos = []
    evt_index = {}
    for r in safe_read_csv(EVENTOS_CSV):
        try:
            e = Evento(int(r[0]), r[1], r[2], parse_date(r[3]), float(r[4]))
            eventos.append(e)
            evt_index[e.id] = e
        except Exception as e:
            print(f"Error en evento {r}: {e}")

    # --- VENTAS ---
    ventas = []
    for r in safe_read_csv(VENTAS_CSV):
        try:
            v = Venta(int(r[0]), int(r[1]), int(r[2]), parse_date(r[3]), int(r[4]), float(r[5]))
            ventas.append(v)
        except Exception as e:
            print(f"Error en venta {r}: {e}")

    print(f"Cargados {len(clientes)} clientes, {len(eventos)} eventos, {len(ventas)} ventas.\n")
    return clientes, eventos, ventas, cli_index, evt_index


# ============================================================
# 4. Funciones auxiliares
# ============================================================

def listar(tabla, clientes, eventos, ventas):
    """Muestra una tabla formateada según el tipo indicado."""
    print("=" * 60)
    if tabla == "clientes":
        print("CLIENTES")
        for c in clientes: print(c)
    elif tabla == "eventos":
        print("EVENTOS")
        for e in eventos: print(e)
    elif tabla == "ventas":
        print("VENTAS")
        for v in ventas: print(v)
    print("=" * 60 + "\n")

def next_id(items, attr="id"):
    """Devuelve el siguiente ID libre basado en la lista existente."""
    return max((getattr(x, attr) for x in items), default=0) + 1


# ============================================================
# 5. Altas y filtros
# ============================================================

def alta_cliente(clientes):
    """Crea un nuevo cliente pidiendo datos por consola."""
    print("=== Alta de cliente ===")
    nombre = input("Nombre: ").strip()
    email = input("Email: ").strip()
    if not email_valido(email):
        print("Email no válido.\n")
        return

    try:
        f_alta = parse_date(input("Fecha alta (YYYY-MM-DD): "))
    except:
        print("Fecha inválida.\n")
        return

    activo = input("¿Activo? (s/n): ").lower() in {"s", "si", "1", "true"}
    cid = next_id(clientes)
    nuevo = Cliente(cid, nombre, email, f_alta, activo)
    clientes.append(nuevo)

    # Guardar incrementalmente en CSV
    append_row_csv(
        CLIENTES_CSV,
        ["id", "nombre", "email", "fecha_alta", "activo"],
        [cid, nombre, email, f_alta.strftime(DATE_FMT), int(activo)]
    )
    print(f"Cliente creado: {nuevo}\n")


def filtrar_ventas_por_rango(ventas, cli_index, evt_index):
    """Filtra las ventas entre dos fechas dadas."""
    print("=== Filtro de ventas por rango ===")
    try:
        f_ini = parse_date(input("Fecha inicio (YYYY-MM-DD): "))
        f_fin = parse_date(input("Fecha fin (YYYY-MM-DD): "))
        if f_fin < f_ini:
            raise ValueError
    except:
        print("Fechas inválidas.\n")
        return

    filtradas = [v for v in ventas if f_ini <= v.fecha_venta <= f_fin]
    print(f"\nResultados ({len(filtradas)} ventas):")
    for v in filtradas:
        cli = cli_index.get(v.cliente_id)
        evt = evt_index.get(v.evento_id)
        print(f"- {v.fecha_venta} | {cli.nombre if cli else '?'} -> {evt.nombre if evt else '?'} | {v.total:.2f}€")
    print()


# ============================================================
# 6. Estadísticas y métricas
# ============================================================

def estadisticas(eventos, ventas):
    """Calcula estadísticas globales y devuelve un resumen."""
    ingresos_totales = sum(v.total for v in ventas)

    # Totales por evento
    ingresos_por_evento = {}
    for v in ventas:
        ingresos_por_evento[v.evento_id] = ingresos_por_evento.get(v.evento_id, 0) + v.total

    # Set de categorías únicas
    categorias = {e.categoria for e in eventos}

    # Evento más próximo
    proximos = [e.dias_hasta_evento() for e in eventos if e.dias_hasta_evento() >= 0]
    dias_hasta_proximo = min(proximos) if proximos else -1

    # Precios (min, max, media)
    precios = [e.precio for e in eventos] or [0]
    resumen_precios = (min(precios), max(precios), mean(precios))

    return ingresos_totales, ingresos_por_evento, categorias, dias_hasta_proximo, resumen_precios


def mostrar_estadisticas(eventos, ventas, evt_index):
    """Muestra por pantalla las estadísticas calculadas."""
    itot, por_evt, cats, dias, tpl = estadisticas(eventos, ventas)
    print("=== Estadísticas ===")
    print(f"Ingresos totales: {itot:.2f}€")
    for eid, total in por_evt.items():
        print(f"  - {evt_index[eid].nombre}: {total:.2f}€")
    print(f"Categorías: {', '.join(sorted(cats))}")
    print(f"Días hasta evento más próximo: {dias if dias >= 0 else 'N/A'}")
    print(f"Precios (min, max, media): {tpl}\n")


# ============================================================
# 7. Exportar informe CSV
# ============================================================

def exportar_informe(eventos, ventas):
    """Genera informe_resumen.csv con ingresos totales por evento."""
    totales = {}
    for v in ventas:
        totales[v.evento_id] = totales.get(v.evento_id, 0) + v.total

    with open(INFORME_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(["evento_id", "nombre_evento", "ingresos_totales"])
        for eid, total in totales.items():
            nombre = next((e.nombre for e in eventos if e.id == eid), f"Evento {eid}")
            w.writerow([eid, nombre, f"{total:.2f}"])
    print(f"Informe exportado: {INFORME_CSV}\n")


# ============================================================
# 8. Menú interactivo
# ============================================================

def menu():
    """Menú principal en bucle con todas las opciones."""
    clientes, eventos, ventas, cli_index, evt_index = [], [], [], {}, {}

    while True:
        print("="*60)
        print(" MINI-CRM de eventos ")
        print("="*60)
        print("1) Cargar CSV")
        print("2) Listar clientes")
        print("3) Listar eventos")
        print("4) Listar ventas")
        print("5) Alta de cliente")
        print("6) Filtrar ventas por rango")
        print("7) Ver estadísticas")
        print("8) Exportar informe")
        print("0) Salir")

        op = input("Opción: ").strip()

        if op == "1":
            clientes, eventos, ventas, cli_index, evt_index = cargar_datos()
        elif op == "2" and clientes:
            listar("clientes", clientes, eventos, ventas)
        elif op == "3" and eventos:
            listar("eventos", clientes, eventos, ventas)
        elif op == "4" and ventas:
            listar("ventas", clientes, eventos, ventas)
        elif op == "5":
            alta_cliente(clientes)
        elif op == "6" and ventas:
            filtrar_ventas_por_rango(ventas, cli_index, evt_index)
        elif op == "7" and eventos:
            mostrar_estadisticas(eventos, ventas, evt_index)
        elif op == "8" and ventas:
            exportar_informe(eventos, ventas)
        elif op == "0":
            print("Hasta luego!")
            break
        else:
            print("Opción no válida o datos no cargados.\n")


# ============================================================
# 9. Punto de entrada
# ============================================================
if __name__ == "__main__":
    menu()
