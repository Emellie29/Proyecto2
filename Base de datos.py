class Productos:
    def __init__(self, id_producto, nombreP, precioP, id_categoria, totalventas=0, totalcompras=0):
        self.id_producto = id_producto
        self.nombreP = nombreP
        self.precioP = precioP
        self.stock = 0
        self.id_categoria = id_categoria #llave
        self.totalventas = totalventas
        self.totalcompras = totalcompras
    def actualizar_stock(self, cantidad, tipo):
        if tipo == "compra":
            self.stock += cantidad
        elif tipo == "venta":
            if cantidad > self.stock:
                raise ValueError("Producto insuficiente")
            self.stock -= cantidad
            self.totalventas += cantidad
    def resumen(self):
        return f"{self.id_producto} - {self.nombreP} - Q.{self.precioP:.2f} - Stock: {self.stock}"

class Categorias:
    def __init__(self, id_categoria, nombreCate):
        self.id_categoria = id_categoria
        self.nombreCate = nombreCate
    def resumen(self):
        return f"{self.id_categoria} - {self.nombreCate}"

class Clientes:
    def __init__(self, nit, nombreCl, telefono, direccion, correo):
        self.nit = nit
        self.nombreCl = nombreCl
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo
    def resumen(self):
        return (f"NIT: {self.nit} - {self.nombreCl} - Tel: {self.telefono} - Dirección: {self.direccion}"
               f" - Correo: {self.correo}")

class Empleados:
    def __init__(self, id_empleado, nombreE, telefonoE, direccionE, correoE):
        self.id_empleado = id_empleado
        self.nombreE = nombreE
        self.telefonoE = telefonoE
        self.direccionE = direccionE
        self.correoE = correoE
    def resumen(self):
        return (f"{self.id_empleado} - {self.nombreE} - Tel: {self.telefonoE} - Dirección: {self.direccionE}"
               f" - Correo: {self.correoE}")

class Proveedores:
    def __init__(self, id_proveedor, nombre_Pro, empresa, telefono_Pro, direccion_Pro, correo_Pro, id_categoria):
        self.id_proveedor = id_proveedor
        self.nombre_Pro = nombre_Pro
        self.empresa = empresa
        self.telefono_Pro = telefono_Pro
        self.direccion_Pro = direccion_Pro
        self.correo_Pro = correo_Pro
        self.id_categoria = id_categoria
    def resumen(self):
        return (f"{self.id_proveedor} - {self.nombre_Pro} - Empresa: {self.empresa} - Tel: {self.telefono_Pro} - "
                f"Direccion: {self.direccion_Pro} - Correo: {self.correo_Pro} - Producto: {self.id_categoria}")

class Ventas:
    def __init__(self, id_venta, fecha, cliente, empleado):
        self.id_venta = id_venta
        self.fecha = fecha
        self.cliente = cliente
        self.empleado = empleado #llave
        self.detalles = []
        self.total = 0.0
    def agregar_detalleV(self, producto, cantidad, precio_unitario, descuento=0):
        producto.actualizar_stock(cantidad, "venta")
        subtotal = cantidad * precio_unitario
        precio_original = precio_unitario / (1 - descuento / 100) if descuento > 0 else precio_unitario
        ahorro = cantidad * (precio_original - precio_unitario)
        detalle = {
            "producto": producto,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "subtotal": subtotal,
            "descuento": descuento,
            "ahorro": ahorro
        }
        self.detalles.append(detalle)
        self.total += subtotal
        if not hasattr(self, "ahorro_total"):
            self.ahorro_total = 0.0
        self.ahorro_total += ahorro
    def resumen(self):
        return (f"Venta No. {self.id_venta} | Fecha: {self.fecha} | Cliente: {self.cliente.nombreCl} | "
            f"Empleado: {self.empleado.nombreE} | Total: Q.{self.total:.2f} | "
            f"Ahorro por ofertas: Q.{self.ahorro_total:.2f}")

class DetalleVentas:
    def __init__(self, id_detalle_venta, id_venta, producto, cantidad):
        self.id_detalle_venta = id_detalle_venta
        self.id_venta = id_venta
        self.id_producto = producto.id_producto
        self.cantidad = cantidad
        self.precio = producto.precio
        self.subtotal = self.precio * self.cantidad
    def resumen(self):
        return (f"Detalle No. {self.id_detalle_venta} | Venta No. {self.id_venta} | Producto ID: {self.id_producto} |"
                f"Cantidad: {self.cantidad} | Precio: Q.{self.precio:.2f} | Subtotal: {self.subtotal:.2f}")

class Compras:
    def __init__(self, id_compra, fecha, id_proveedor, id_empleado):
        self.id_compra = id_compra
        self.fecha = fecha
        self.id_proveedor = id_proveedor #llave
        self.id_empleado = id_empleado #llave
        self.detalles = []
        self.total = 0.0
    def agregar_detalleC(self, producto, cantidad, precio_uni, fecha_caducidad):
        producto.actualizar_stock(cantidad, "compra")
        detalleC = DetalleCompras(len(self.detalles) + 1, self.id_compra, producto, cantidad, precio_uni, fecha_caducidad)
        self.detalles.append(detalleC)
        self.total += detalleC.subtotal  #se acumula el total
    def resumen(self):
        proveedor = proveedores.get(self.id_proveedor)
        empleado = empleados.get(self.id_empleado)
        nombre_proveedor = proveedor.nombrePro if proveedor else "Desconocido"
        nombre_empleado = empleado.nombreE if empleado else "Desconocido"
        return (f"Compra No. {self.id_compra} | Fecha: {self.fecha} | "
                f"Proveedor: {nombre_proveedor} | Empleado: {nombre_empleado} | Total: Q.{self.total:.2f}")

class DetalleCompras:
    def __init__(self, id_detalle_compra,id_compra, id_producto, cantidad, precio_compra, fecha_caducidad):
        self.id_detalle_compra = id_detalle_compra
        self.id_compra = id_compra
        self.producto = id_producto
        self.cantidad = cantidad
        self.precio_compra = precio_compra
        self.subtotal = self.precio_compra * self.cantidad
        self.fecha_caducidad = fecha_caducidad
    def resumen(self):
        return (f" Detalla No. {self.id_detalle_compra} | Compra No. {self.id_compra} | Producto ID: {self.id_producto}"
                f" | Cantidad: {self.cantidad} | Precio: Q.{self.precio_compra:.2f} | Subtotal: Q.{self.subtotal:.2f}"
                f"  | Caduca: {self.fecha_caducidad}")
#guardar info
categorias = {}
productos = {}
clientes = {}
empleados = {}
proveedores = {}
ofertas = {}
ventas = []
compras = []
#cargar .txt´s
def cargar_todo():
    cargar_productos()
    cargar_clientes()
    cargar_empleados()
    cargar_categorias()
    cargar_proveedores()
    cargar_ventas()
    cargar_compras()
#agregar info
def agregar_categoria():
    print("\nAgregar Categoría")
    id_categoria = len(categorias) + 1
    nombreCate = input("Nombre de la categoría: ")
    categorias[id_categoria] = Categorias(id_categoria, nombreCate)
    print("Categoría agregada con éxito.")

def agregar_producto():
    print("\nAgregar Producto")
    id_producto = len(productos) + 1
    nombreP = input("Nombre del producto: ")
    precioP = float(input("Precio: Q."))
    print("Categorías disponibles:")
    for c in categorias.values():
        print(c.resumen())
    id_categoria = int(input("ID de la categoría: "))
    categoria = categorias.get(id_categoria)
    if not categoria:
        print("Categoría no encontrada")
        return
    productos[id_producto] = Productos(id_producto, nombreP, precioP, id_categoria)
    print("Producto agregado con éxito.")

def informacion_cliente():
    print("\n Informacion de Cliente")
    nit = input("NIT: ")
    if nit in clientes:
        print("El NIT ya existe")
        return
    nombreCL = input("Nombre: ")
    telefono = input("Teléfono: ")
    direccion = input("Dirección: ")
    correo = input("Correo: ")
    clientes[nit] = Clientes(nit, nombreCL, telefono, direccion, correo)
    print("Cliente agregado.")

def informacion_empleado():
    print("\n Informacion del Empleado")
    id_empleado = len(empleados)+1
    nombreE = input("Nombre: ")
    telefonoE = input("Teléfono: ")
    direccionE = input("Dirección: ")
    correoE = input("Correo: ")
    empleados[id_empleado] = Empleados(id_empleado, nombreE, telefonoE, direccionE, correoE)
    print("Empleado agregado.")

def informacion_proveedor():
    print("\nInformación del Proveedor")
    id_proveedor = len(proveedores) + 1
    nombrePro = input("Nombre: ")
    empresa = input("Empresa: ")
    telefonoPro = input("Teléfono: ")
    direccionPro = input("Dirección: ")
    correoPro = input("Correo: ")
    print("Categorías disponibles:")
    for c in categorias.values():
        print(f"ID: {c.id_categoria} - Nombre: {c.nombreCate}")
    id_categoria = int(input("ID de la categoría que provee: "))
    if id_categoria not in categorias:
        print("Categoría no encontrada.")
        return
    proveedores[id_proveedor] = Proveedores(id_proveedor, nombrePro, empresa, telefonoPro, direccionPro, correoPro, id_categoria)
    print("Proveedor agregado con éxito.")

def registrar_venta():
    print("\nInformación de la Venta")
    nit = input("NIT: ").strip()
    print("Empleados disponibles:")
    for e in empleados.values():
        print(f"ID: {e.id_empleado} - Nombre: {e.nombreE}")
    id_empleado = int(input("ID del empleado: "))
    fecha = input("Fecha (YYYY-MM-DD): ")
    cliente = clientes.get(nit)
    empleado = empleados.get(id_empleado)
    if not cliente or not empleado:
        print("El cliente o empleado no fue encontrado.")
        return
    venta = Ventas(len(ventas) + 1, fecha, cliente, empleado)
    if input("¿Desea registrar una oferta antes de vender? [S/N]: ").lower() == "s":
        registrar_oferta()
    while True:
        id_producto = int(input("ID del producto: "))
        producto = productos.get(id_producto)
        if not producto:
            print("El producto no existe.")
            continue
        cantidad = int(input("Cantidad del producto: "))
        precio_unitario = producto.precioP
        descuento = ofertas.get(id_producto, 0)
        precio_final = precio_unitario * (1 - descuento / 100)
        print(f"Descuento aplicado: {descuento}%")
        print(f"Precio con descuento: Q{precio_final:.2f}")
        try:
            venta.agregar_detalleV(producto, cantidad, precio_final, descuento)
            print("Producto agregado con descuento.")
        except ValueError as e:
            print(f"Error al agregar producto: {e}")
        if input("¿Desea agregar otro producto? [S/N]: ").lower() != "s":
            break
    ventas.append(venta)
    print(f"Venta agregada con éxito. Total: Q{venta.total:.2f}")
    print(f"Ahorro total por ofertas: Q{venta.ahorro_total:.2f}")

def registrar_oferta():
    print("Registrar Oferta")
    id_producto = int(input("ID del producto: "))
    producto = productos.get(id_producto)
    if not producto:
        print("El producto no existe.")
        return
    print(f"Producto seleccionado: {producto.nombreP}")
    descuento = float(input("Porcentaje de descuento (%): "))
    if descuento < 0 or descuento > 100:
        print("El descuento debe estar entre 0 y 100.")
        return
    ofertas[id_producto] = descuento
    print(f"Oferta registrada: {descuento}% para el producto '{producto.nombreP}' (ID: {id_producto})")

def registrar_compra():
    print("\n Informacion de la Compra")
    id_proveedor = int(input("ID proveedor: "))
    id_empleado = int(input("ID empleado: "))
    fecha = input("Fecha (YYYY-MM-DD): ").strip()
    proveedor = proveedores.get(id_proveedor)
    empleado = empleados.get(id_empleado)
    if not proveedor or not empleado:
        print("Proveedor o empleado no encontrado.")
        return
    compra = Compras(len(compras) + 1, fecha, id_proveedor, id_empleado)
    while True:
        id_producto = int(input("ID producto: "))
        producto = productos.get(id_producto)
        if not producto:
            print("Producto no existe.")
            continue
        cantidad = int(input("Cantidad: "))
        precio_unitario = float(input("Precio unitario: Q."))
        fecha_caducidad = input("Fecha de caducidad del producto (YYYY-MM-DD): ")
        compra.agregar_detalleC(producto, cantidad, precio_unitario, fecha_caducidad)
        print("Producto agregado.")
        if input("¿Desea agregar otro producto? [S/N]: ").lower() != "s":
            break
    compras.append(compra)
    print(f"Compra agregada con exito. Total: Q{compra.total:.2f}")

def mostrar_compras():
    print("Listado de Compras")
    if not compras:
        print("No hay compras registradas.")
        return
    for compra in compras:
        proveedor = proveedores.get(compra.id_proveedor)
        empleado = empleados.get(compra.id_empleado)
        nombre_proveedor = proveedor.nombre_Pro if proveedor else "Desconocido"
        nombre_empleado = empleado.nombreE if empleado else "Desconocido"
        print(f"\nID Compra: {compra.id_compra}")
        print(f"Fecha: {compra.fecha}")
        print(f"Proveedor: {nombre_proveedor}")
        print(f"Empleado: {nombre_empleado}")
        print(f"Total: Q{compra.total:.2f}")
        print("Detalles:")
        for detalle in compra.detalles:
            producto = detalle.producto
            nombre_producto = producto.nombreP if producto else "Producto desconocido"
            print(f"  • Producto: {nombre_producto}")
            print(f"    Cantidad: {detalle.cantidad}")
            print(f"    Precio Unitario: Q{detalle.precio_compra}")
            print(f"    Subtotal: Q{detalle.subtotal:.2f}")
            print(f"    Caducidad: {detalle.fecha_caducidad}")

def mostrar_ventas():
    print("Listado de Ventas")
    if not ventas:
        print("No hay ventas registradas.")
        return
    for venta in ventas:
        print(f"\nID Venta: {venta.id_venta}")
        print(f"Fecha: {venta.fecha}")
        print(f"Cliente: {venta.cliente.nombreCl}")
        print(f"Empleado: {venta.empleado.nombreE}")
        print(f"Total: Q{venta.total:.2f}")
        print("Detalles:")
        for detalle in venta.detalles:
            producto = detalle["producto"]
            print(f"  - Producto: {producto.nombreP}")
            print(f"    Precio Unitario: Q{detalle['precio_unitario']:.2f}")
            print(f"    Subtotal: Q{detalle['subtotal']:.2f}")
            print(f"    Descuento aplicado: {detalle['descuento']}%")
def consultar_inventario():
    print("Inventario Actual")
    print(f"Productos registrados: {len(productos)}\n")
    if not productos:
        print("No hay productos registrados.")
        return
    for producto in productos.values():
        nombre_cate = categorias[producto.id_categoria].nombreCate if producto.id_categoria in categorias else "Sin categoría"
        print(f"•Producto ID: {producto.id_producto}")
        print(f"    Nombre: {producto.nombreP}")
        print(f"    Precio Unitario: Q{producto.precioP:.2f}")
        print(f"    Stock Disponible: {producto.stock}")
        print(f"    Categoría: {nombre_cate}")
        print(f"    Total Compras: {producto.totalcompras}")
        print(f"    Total Ventas: {producto.totalventas}")
#.txt´s
def guardar_productos():
    with open("productos.txt", "w", encoding="utf-8") as f:
        for p in productos.values():
            f.write(f"{p.id_producto}|{p.nombreP}|{p.precioP}|{p.stock}|{p.id_categoria}|{p.totalventas}|{p.totalcompras}")
def cargar_productos():
    try:
        with open("productos.txt", "a", encoding="utf-8") as f:
            f.append("nueva linea de texto")
            for linea in f:
                id_producto, nombre, precio, stock, cat, ventas, compras = linea.split(":")
                producto = Productos(int(id_producto), nombre, float(precio), int(cat), int(ventas), int(compras))
                producto.stock = int(stock)
                productos[int(id_producto)] = producto
    except FileNotFoundError:
        print("productos.txt no encontrado.")

def guardar_categorias():
    with open("categorias.txt", "w", encoding="utf-8") as f:
        for c in categorias.values():
            f.write(f"{c.id_categoria}|{c.nombreCate}")

def cargar_categorias():
    try:
        with open("categorias.txt", "a", encoding="utf-8") as f:
            f.append("nueva linea de texto")
            for linea in f:
                id_categoria, nombre = linea.split(":")
                categorias[int(id_categoria)] = Categorias(int(id_categoria), nombre)
    except FileNotFoundError:
        print("categorias.txt no encontrado.")

def guardar_clientes():
    with open("clientes.txt", "w", encoding="utf-8") as f:
        for c in clientes.values():
            f.write(f"{c.nit}|{c.nombreCl}|{c.telefono}|{c.direccion}|{c.correo}")

def cargar_clientes():
    try:
        with open("clientes.txt", "a", encoding="utf-8") as f:
            f.append("nueva linea de texto")
            for linea in f:
                nit, nombre, telefono, direccion, correo = linea.split(":")
                clientes[nit] = Clientes(nit, nombre, telefono, direccion, correo)
    except FileNotFoundError:
        print("clientes.txt no encontrado.")

def guardar_empleados():
    with open("empleados.txt", "w", encoding="utf-8") as f:
        for e in empleados.values():
            f.write(f"{e.id_empleado}|{e.nombreE}|{e.telefonoE}|{e.direccionE}|{e.correoE}")

def cargar_empleados():
    try:
        with open("empleados.txt", "a", encoding="utf-8") as f:
            f.append("nueva linea de texto")
            for linea in f:
                id_empleado, nombreE, telefonoE, direccionE, correoE = linea.split(":")
                empleados[int(id_empleado)] = Empleados(int(id_empleado), nombreE, telefonoE, direccionE, correoE)
    except FileNotFoundError:
        print("empleados.txt no encontrado.")

def guardar_proveedores():
    with open("proveedores.txt", "w", encoding="utf-8") as f:
        for p in proveedores.values():
            f.write(f"{p.id_proveedor}|{p.nombre_Pro}|{p.empresa}|{p.telefono_Pro}|{p.direccion_Pro}|{p.correo_Pro}")

def cargar_proveedores():
    try:
        with open("proveedores.txt", "a", encoding="utf-8") as f:
            f.append("nueva linea de texto")
            for linea in f:
                id_proveedor, nombre_Pro, empresa, telefono_Pro, direccion_Pro, correo_Pro, id_categoria = linea.split(":")
                proveedores[int(id_proveedor)] = Proveedores(int(id_proveedor), nombre_Pro, empresa, telefono_Pro, direccion_Pro, correo_Pro, id_categoria, dir)
    except FileNotFoundError:
        print("proveedores.txt no encontrado.")

def guardar_ventas():
    with open("ventas.txt", "w", encoding="utf-8") as f:
        for v in ventas:
            f.write(f"{v.id_venta}|{v.fecha}|{v.cliente.nit}|{v.empleado.id_empleado}|{v.total}\n")

def cargar_ventas():
    try:
        with open("ventas.txt", "a", encoding="utf-8") as f:
            f.append("nueva linea de texto")
            for linea in f:
                id_detalle_venta, fecha, nit, id_empleado, total = linea.split(":")
                cliente = clientes.get(nit)
                empleado = empleados.get(int(id_empleado))
                venta = Ventas(int(id_detalle_venta), fecha, cliente, empleado)
                venta.total = float(total)
                ventas.append(venta)
    except FileNotFoundError:
        print("ventas.txt no encontrado.")

def guardar_detalles_venta():
    with open("detalles_venta.txt", "w", encoding="utf-8") as f:
        for v in ventas:
            for d in v.detalles:
                f.write(f"{v.id_venta}|{d['producto'].id_producto}|{d['cantidad']}|{d['precio_unitario']}|{d['subtotal']}|{d['descuento']}\n")

def guardar_compras():
    with open("compras.txt", "w", encoding="utf-8") as f:
        for c in compras:
            f.write(f"{c.id_compra}|{c.fecha}|{c.proveedor.id_proveedor}|{c.total}\n")

def cargar_compras():
    try:
        with open("compras.txt", "a", encoding="utf-8") as f:
            f.append("nueva linea de texto")
            for linea in f:
                id_detalle_compra, fecha, id_proveedor, total = linea.split(":")
                proveedor = proveedores.get(int(id_proveedor))
                compra = Compras(int(id_detalle_compra), fecha, proveedor)
                compra.total = float(total)
                compras.append(compra)
    except FileNotFoundError:
        print("compras.txt no encontrado.")

def guardar_detalles_compra():
    with open("detalles_compra.txt", "w", encoding="utf-8") as f:
        for c in compras:
            for d in c.detalles:
                f.write(f"{c.id_compra}|{d['producto'].id_producto}|{d['cantidad']}|{d['precio_unitario']}|{d['subtotal']}|{d['fecha_caducidad']}\n")
#guardar .txt´s
def guardar_todo():
    guardar_productos()
    guardar_clientes()
    guardar_empleados()
    guardar_categorias()
    guardar_proveedores()
    guardar_ventas()
    guardar_compras()
#menú
while True:
    print("•••••••Menú Principal•••••••")
    print("1. Gerencia.")
    print("2. Área de Bodega.")
    print("3. Área de Cajas.")
    print("4. Salir")
    opcion = input("Selecciona una opción: ").strip()
    match (opcion):
        case "1":
            while True:
                print("Bienvenido a Gerencia.")
                print("1. Agregar empleado.")
                print("2. Consultar inventario.")
                print("3. Mostrar ventas.")
                print("4. Mostrar compras.")
                print("5. Mostrar empleados.")
                print("6. Mostrar proveedores.")
                print("7. Mostrar clientes.")
                print("8. Regresar al menú principal.")
                opcion_gerencia = input("Seleccione una opción: ").strip()
                if opcion_gerencia == "1":
                    informacion_empleado()
                elif opcion_gerencia == "2":
                    consultar_inventario()
                elif opcion_gerencia == "3":
                    mostrar_ventas()
                elif opcion_gerencia == "4":
                    mostrar_compras()
                elif opcion_gerencia == "8":
                    break
                else:
                    print("Opción inválida, intente de nuevo.")
        case "2":
            while True:
                print("Bienvenido al área de bodega")
                print("1. Agregar categoría.")
                print("2. Agregar producto.")
                print("3. Agregar proveedor.")
                print("4. Registrar compra.")
                print("5. Mostrar compras.")
                print("6. Regresar al menú principal.")
                opcion_bodega = input("Seleccione una opción: ").strip()
                if opcion_bodega == "1":
                    agregar_categoria()
                elif opcion_bodega == "2":
                    agregar_producto()
                elif opcion_bodega == "3":
                    informacion_proveedor()
                elif opcion_bodega == "4":
                    registrar_compra()
                elif opcion_bodega == "5":
                    mostrar_compras()
                elif opcion_bodega == "6":
                    break
                else:
                    print("Opción inválida, intente de nuevo.")
        case "3":
            while True:
                print("Bienvenido al área de cajas.")
                print("1. Agregar cliente.")
                print("2. Registrar venta.")
                print("3. Consultar inventario.")
                print("4. Mostrar ventas.")
                print("5. Regresar al menú principal.")
                opcion_cajas = input("Seleccione una opción: ").strip()
                if opcion_cajas == "1":
                    informacion_cliente()
                elif opcion_cajas == "2":
                    registrar_venta()
                elif opcion_cajas == "3":
                    consultar_inventario()
                elif opcion_cajas == "4":
                    mostrar_ventas()
                elif opcion_cajas == "5":
                    break
                else:
                    print("Opción inválida, intente de nuevo.")
        case "4":
            print("Guardando información...")
            guardar_todo()
            print("Cerrando el sistema. ¡Hasta pronto!")
            exit()
        case _:
            print("Opción inválida, intente de nuevo.")