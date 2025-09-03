class Productos:
    def __init__(self, id_producto, nombreP, precioP, stock, id_categoria, totalventas=0, totalcompras=0):
        self.id_producto = id_producto
        self.nombreP = nombreP
        self.precioP = precioP
        self.stock = stock
        self.id_categoria = id_categoria #llave
        self.totalventas = totalventas
        self.totalcompras = totalcompras
    def actualizar_stock(self, tipo, cantidad):
        if tipo == "compra":
            self.stock += cantidad
            self.totalcompras += cantidad
        elif tipo == "venta":
            if cantidad <= self.stock:
                self.stock -= cantidad
                self.totalventas += cantidad
            else:
                raise ValueError(f"No hay suficiente stock para vender {cantidad} unidades de {self.nombreP}")
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
    def __init__(self, id_venta, fecha, cliente, empleado, metodo_pago):
        self.id_venta = id_venta
        self.fecha = fecha
        self.cliente = cliente
        self.empleado = empleado
        self.metodo_pago = metodo_pago
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
        return (f"Venta No. {self.id_venta} - Fecha: {self.fecha} - Cliente: {self.cliente.nombreCl} - "
                f"Empleado: {self.empleado.nombreE} - Método de pago: {self.metodo_pago} - "
                f"Total: Q.{self.total:.2f} - Ahorro por ofertas: Q.{self.ahorro_total:.2f}")

class DetalleVentas:
    def __init__(self, id_detalle_venta, id_venta, producto, cantidad):
        self.id_detalle_venta = id_detalle_venta
        self.id_venta = id_venta
        self.id_producto = producto.id_producto
        self.cantidad = cantidad
        self.precio = producto.precioP
        self.subtotal = self.precio * self.cantidad
    def resumen(self):
        return (f"Detalle No. {self.id_detalle_venta} - Venta No. {self.id_venta} - Producto ID: {self.id_producto} -"
                f"Cantidad: {self.cantidad} - Precio: Q.{self.precio:.2f} - Subtotal: {self.subtotal:.2f}")

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
        detalleC = DetalleCompras(len(self.detalles) + 1, self, producto, cantidad, fecha_caducidad)
        self.detalles.append(detalleC)
        self.total += detalleC.subtotal  #se acumula el total
    def resumen(self):
        proveedor = proveedores.get(self.id_proveedor)
        empleado = empleados.get(self.id_empleado)
        nombre_proveedor = proveedor.nombrePro if proveedor else "Desconocido"
        nombre_empleado = empleado.nombreE if empleado else "Desconocido"
        return (f"Compra No. {self.id_compra} - Fecha: {self.fecha} - Proveedor: {nombre_proveedor} - "
                f"Empleado: {nombre_empleado} - Total: Q.{self.total:.2f}")

class DetalleCompras:
    def __init__(self, id_detalle_compra, compra, producto, cantidad, fecha_caducidad):
        self.id_detalle_compra = id_detalle_compra
        self.compra = compra
        self.producto = producto
        self.id_producto = producto.id_producto
        self.cantidad = cantidad
        self.precio_compra = producto.precioP
        self.subtotal = self.precio_compra * self.cantidad
        self.fecha_caducidad = fecha_caducidad
    def resumen(self):
        return (f" Detalle No. {self.id_detalle_compra} - Compra No. {self.compra.id_compra} - "
                f"Producto: {self.producto.nombreP} - (ID: {self.id_producto}) - "
                f"Cantidad: {self.cantidad} - Precio: Q.{self.precio_compra:.2f} - "
                f"Subtotal: Q.{self.subtotal:.2f} - Caduca: {self.fecha_caducidad}")
#guardar info
categorias = {}
productos = {}
clientes = {}
empleados = {}
proveedores = {}
ofertas = {}
ventas = []
compras = []
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
    stock = int(input("Stock inicial: "))
    print("Categorías disponibles:")
    for c in categorias.values():
        print(c.resumen())
    id_categoria = int(input("ID de la categoría: "))
    categoria = categorias.get(id_categoria)
    if not categoria:
        print("Categoría no encontrada")
        return
    productos[id_producto] = Productos(id_producto, nombreP, precioP, stock, id_categoria)
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
    fecha = input("Fecha (dd/mm/aaaa): ")
    metodo_pago = input("Método de pago (Efectivo/Tarjeta): ").strip().capitalize()
    cliente = clientes.get(nit)
    empleado = empleados.get(id_empleado)
    if not cliente or not empleado:
        print("El cliente o empleado no fue encontrado.")
        return
    venta = Ventas(len(ventas) + 1, fecha, cliente, empleado, metodo_pago)
    if input("¿Desea registrar una oferta antes de vender? [S/N]: ").lower() == "s":
        registrar_oferta()
    while True:
        id_producto = int(input("ID del producto: "))
        producto = productos.get(id_producto)
        if not producto:
            print("El producto no existe.")
            continue
        cantidad = int(input("Cantidad del producto: "))
        if producto.stock < cantidad:
            print("Stock insuficiente.")
            continue
        precio_unitario = producto.precioP
        descuento = ofertas.get(id_producto, 0)
        precio_final = precio_unitario * (1 - descuento / 100)
        print(f"Descuento aplicado: {descuento}%")
        print(f"Precio con descuento: Q{precio_final:.2f}")
        try:
            venta.agregar_detalleV(producto, cantidad, precio_final, descuento)
            print("Producto agregado con descuento.")
            producto.stock -= cantidad
            producto.totalventas += cantidad
        except ValueError as e:
            print(f"Error al agregar producto: {e}")
            opcion = input("¿Desea intentar con otro producto? [S/N]: ").lower()
            if opcion != "s":
                print("Cancelando venta. Regresando al menú...")
                return
            else:
                continue
        if input("¿Desea agregar otro producto? [S/N]: ").lower() != "s":
            break
    guardar_detalles_venta(venta)
    ventas.append(venta)
    guardar_productos()
    print(f"Venta registrada con éxito. Total: Q{venta.total:.2f}")

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
    print("\nRegistrar Compra")
    id_compra = len(compras) + 1
    fecha = input("Fecha (dd/mm/aaaa): ")
    print("Proveedores disponibles:")
    for p in proveedores.values():
        print(p.resumen())
    id_proveedor = int(input("ID del proveedor: "))
    print("Empleados disponibles:")
    for e in empleados.values():
        print(e.resumen())
    id_empleado = int(input("ID del empleado: "))
    compra = Compras(id_compra, fecha, id_proveedor, id_empleado)
    while True:
        print("\nProductos disponibles:")
        for p in productos.values():
            print(p.resumen())
        id_producto = int(input("ID del producto a comprar: "))
        producto = productos.get(id_producto)
        if not producto:
            print("Producto no encontrado.")
            continue
        cantidad = int(input("Cantidad a comprar: "))
        precio_unitario = float(input("Precio unitario de compra: Q."))
        fecha_caducidad = input("Fecha de caducidad (dd/mm/aaaa): ")
        producto.precioP = precio_unitario
        compra.agregar_detalleC(producto, cantidad, precio_unitario, fecha_caducidad)
        producto.stock += cantidad
        producto.totalcompras += cantidad
        continuar = input("¿Agregar otro producto? (s/n): ").lower()
        if continuar != "s":
            break
    compras.append(compra)
    guardar_detalles_compra(compra)
    print(f"Compra agregada con éxito. Total: Q{compra.total:.2f}")
    guardar_productos()

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
        print(f"ID Compra: {compra.id_compra}")
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
        print(f"ID Venta: {venta.id_venta}")
        print(f"Fecha: {venta.fecha}")
        print(f"Cliente: {venta.cliente.nombreCl}")
        print(f"Empleado: {venta.empleado.nombreE}")
        print(f"Total: Q{venta.total:.2f}")
        print(f"Método de pago: {venta.metodo_pago}")
        print("Detalles:")
        for detalle in venta.detalles:
            producto = detalle["producto"]
            print(f"  - Producto: {producto.nombreP}")
            print(f"    Método de pago: {venta.metodo_pago}")
            print(f"    Precio Unitario: Q{detalle['precio_unitario']:.2f}")
            print(f"    Subtotal: Q{detalle['subtotal']:.2f}")
            print(f"    Descuento aplicado: {detalle['descuento']}%")

def mostrar_empleados():
    print("\nListado de Empleados")
    if not empleados:
        print("No hay empleados registrados.")
        return
    for e in empleados.values():
        print(f"• {e.resumen()}")

def mostrar_proveedores():
    print("\nListado de Proveedores")
    if not proveedores:
        print("No hay proveedores registrados.")
        return
    for p in proveedores.values():
        print(f"• {p.resumen()}")

def mostrar_clientes():
    print("\nListado de Clientes")
    if not clientes:
        print("No hay clientes registrados.")
        return
    for c in clientes.values():
        print(f"• {c.resumen()}")

def consultar_inventario():
    print("Inventario Actual")
    print(f"Productos registrados: {len(productos)}")
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
# cargar .txt´s
def cargar_todo():
    cargar_productos()
    cargar_clientes()
    cargar_empleados()
    cargar_categorias()
    cargar_proveedores()
    cargar_ventas()
    cargar_compras()
#.txt´s
def guardar_productos():
    with open("productos.txt", "w", encoding="utf-8") as f:
        for p in productos.values():
            f.write(f"{p.id_producto}:{p.nombreP}:{p.precioP}:{p.stock}:{p.id_categoria}:{p.totalventas}:{p.totalcompras}\n")
def cargar_productos():
    try:
        with open("productos.txt", "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.split(":")
                if len(partes) == 7:
                    id_producto = int(partes[0])
                    nombreP = partes[1]
                    precioP = float(partes[2])
                    stock = int(partes[3])
                    cat = int(partes[4])
                    ventas = int(partes[5])
                    compras = int(partes[6])
                    producto = Productos(id_producto, nombreP, precioP, stock, cat, ventas, compras)
                    productos[id_producto] = producto
    except FileNotFoundError:
        pass

def guardar_categorias():
    with open("categorias.txt", "w", encoding="utf-8") as f:
        for c in categorias.values():
            f.write(f"{c.id_categoria}:{c.nombreCate}\n")
def cargar_categorias():
    try:
        with open("categorias.txt", "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.split(":")
                if len(partes) == 2:
                    id_categoria = int(partes[0])
                    nombre = partes[1]
                    categorias[id_categoria] = Categorias(id_categoria, nombre)
    except FileNotFoundError:
        pass

def guardar_clientes():
    with open("clientes.txt", "w", encoding="utf-8") as f:
        for c in clientes.values():
            f.write(f"{c.nit}:{c.nombreCl}:{c.telefono}:{c.direccion}:{c.correo}\n")
def cargar_clientes():
    try:
        with open("clientes.txt", "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.split(":")
                if len(partes) == 5:
                    nit, nombreCl, telefono, direccion, correo = partes
                    clientes[nit] = Clientes(nit, nombreCl, telefono, direccion, correo)
    except FileNotFoundError:
        pass

def guardar_empleados():
    with open("empleados.txt", "w", encoding="utf-8") as f:
        for e in empleados.values():
            f.write(f"{e.id_empleado}:{e.nombreE}:{e.telefonoE}:{e.direccionE}:{e.correoE}\n")
def cargar_empleados():
    try:
        with open("empleados.txt", "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.split(":")
                if len(partes) == 5:
                    id_empleado = int(partes[0])
                    nombreE = partes[1]
                    telefonoE = partes[2]
                    direccionE = partes[3]
                    correoE = partes[4]
                    empleados[id_empleado] = Empleados(id_empleado, nombreE, telefonoE, direccionE, correoE)
    except FileNotFoundError:
        pass

def guardar_proveedores():
    with open("proveedores.txt", "w", encoding="utf-8") as f:
        for p in proveedores.values():
            f.write(f"{p.id_proveedor}:{p.nombre_Pro}:{p.empresa}:{p.telefono_Pro}:{p.direccion_Pro}:{p.correo_Pro}:{p.id_categoria}\n")
def cargar_proveedores():
    try:
        with open("proveedores.txt", "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.split(":")
                if len(partes) == 7:
                    id_proveedor = int(partes[0])
                    nombre_Pro = partes[1]
                    empresa = partes[2]
                    telefono_Pro = partes[3]
                    direccion_Pro = partes[4]
                    correo_Pro = partes[5]
                    id_categoria = int(partes[6])
                    proveedores[id_proveedor] = Proveedores(id_proveedor, nombre_Pro, empresa, telefono_Pro, direccion_Pro, correo_Pro, id_categoria)
    except FileNotFoundError:
        pass

def guardar_ventas():
    with open("ventas.txt", "w", encoding="utf-8") as f:
        for v in ventas:
            f.write(f"{v.id_venta}:{v.fecha}:{v.cliente.nit}:{v.empleado.id_empleado}:{v.metodo_pago}:{v.total}\n")
def cargar_ventas():
    try:
        with open("ventas.txt", "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.split(":")
                if len(partes) == 6:
                    id_venta = int(partes[0])
                    fecha = partes[1]
                    nit = partes[2]
                    id_empleado = int(partes[3])
                    metodo_pago = partes[4]
                    total = float(partes[5])
                    cliente = clientes.get(nit)
                    empleado = empleados.get(id_empleado)
                    venta = Ventas(id_venta, fecha, cliente, empleado, metodo_pago)
                    venta.total = total
                    ventas.append(venta)
    except FileNotFoundError:
        pass
def guardar_detalles_venta(venta):
    with open("detalles_venta.txt", "w") as archivo:
        for detalle in venta.detalles:
            archivo.write(f"{venta.id_venta}:{detalle['producto'].id_producto}:{detalle['producto'].nombreP}:"
                          f"{detalle['cantidad']}:{detalle['precio_unitario']}:{detalle['descuento']}\n")

def guardar_compras():
    with open("compras.txt", "w", encoding="utf-8") as f:
        for c in compras:
            f.write(f"{c.id_compra}:{c.fecha}:{c.id_proveedor}:{c.id_empleado}:{c.total}\n")
def cargar_compras():
    try:
        with open("compras.txt", "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.split(":")
                if len(partes) == 5:
                    id_compra = int(partes[0])
                    fecha = partes[1]
                    id_proveedor = int(partes[2])
                    id_empleado = int(partes[3])
                    total = float(partes[4])
                    compra = Compras(id_compra, fecha, id_proveedor, id_empleado)
                    compra.total = total
                    compras.append(compra)
    except FileNotFoundError:
        pass
def guardar_detalles_compra(compra):
    with open("detalles_compra.txt", "w") as archivo:
        for detalle in compra.detalles:
            archivo.write(f"{compra.id_compra}:{detalle.producto.id_producto}:{detalle.producto.nombreP}:"
                          f"{detalle.cantidad}:{detalle.precio_compra}:{detalle.fecha_caducidad}\n")
#guardar .txt´s
def guardar_todo():
    guardar_productos()
    guardar_clientes()
    guardar_empleados()
    guardar_categorias()
    guardar_proveedores()
    guardar_ventas()
    guardar_compras()
# menú
cargar_todo()
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
                elif opcion_gerencia == "5":
                    mostrar_empleados()
                elif opcion_gerencia == "6":
                    mostrar_proveedores()
                elif opcion_gerencia == "7":
                    mostrar_clientes()
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