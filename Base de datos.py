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
        return f"{self.id_producto} - {self.nombreP} - Q.{self.precio} - {self.stock}"

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
        producto.actualizar_stock(cantidad, "Venta")
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
        return (f"Venta No. {self.id_venta} | Fecha: {self.fecha} | Cliente: {self.cliente.nombre} | "
            f"Empleado: {self.empleado.nombre} | Total: Q.{self.total:.2f} | "
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
        self.proveedor = id_proveedor #llave
        self.empleado = id_empleado #llave
        self.detalles = []
        self.total = 0.0
    def agregar_detalleC(self, producto, cantidad, precio_uni, fecha_caducidad):
        producto.actualizar_stock(cantidad, "Compra")
        detalleC = DetalleCompras(len(self.detalles) + 1, self.id_compra, producto, cantidad, precio_uni, fecha_caducidad)
        self.detalles.append(detalleC)
        self.total += detalleC.subtotal  #se acumula el total
    def resumen(self):
        return (f"Compra No. {self.id_compra} | Fecha: {self.fecha} | Proveedor: {self.proveedor} | "
               f"Empleado: {self.empleado} | Total: Q.{self.total:.2f}")

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
    precioP = int(input("Precio: "))
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
    proveedores[id_proveedor] = Proveedores(
        id_proveedor, nombrePro, empresa, telefonoPro, direccionPro, correoPro, id_categoria
    )
    print("Proveedor agregado con éxito.")

def registrar_venta():
    print("\nInformación de la Venta")
    nit = int(input("NIT: "))
    id_empleado = int(input("ID del empleado: "))
    fecha = input("Fecha (YYYY-MM-DD): ")
    cliente = clientes.get(nit)
    empleado = empleados.get(id_empleado)
    if not cliente or not empleado:
        print("El cliente o empleado no fue encontrado.")
        return
    venta = Ventas(len(ventas) + 1, cliente, empleado, fecha)
    while True:
        id_producto = int(input("ID del producto: "))
        producto = productos.get(id_producto)
        if not producto:
            print("El producto no existe.")
            continue
        cantidad = int(input("Cantidad del producto: "))
        precio_unitario = producto.precio
        # Verifico si hay oferta
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

def registrar_compra():
    print("\n Informacion de la Compra")
    id_proveedor = int(input("ID proveedor: "))
    id_empleado = int(input("ID empleado: "))
    Fecha = input("Fecha (YYYY-MM-DD): ")
    proveedor = proveedores.get(id_proveedor)
    empleado = empleados.get(id_empleado)
    if not proveedor or not empleado:
        print("Proveedor o empleado no encontrado.")
        return
    compra = Compras(len(compras) + 1, proveedor, empleado, Fecha)
    while True:
        id_producto = int(input("ID producto: "))
        producto = productos.get(id_producto)
        if not producto:
            print("Producto no existe.")
            continue
        cantidad = int(input("Cantidad: "))
        precio_unitario = int(input("Precio unitario: Q."))
        fecha_caducidad = input("Fecha de caducidad del producto (YYYY-MM-DD): ")
        compra.agregar_detalleC(producto, cantidad, precio_unitario, fecha_caducidad)
        print("Producto agregado.")
        if input("¿Agregar otro producto? [S/N]: ").lower() != "s":
            break
        compras.append(compra)
        print(f"Compra agregada con exito. Total: Q{compra.total:.2f}")

def mostrar_compras():
    print("Listado de Compras")
    if not compras:
        print("No hay compras registradas.")
        return
    for compra in compras:
        print(f"\nID Compra: {compra.id}")
        print(f"Fecha: {compra.fecha}")
        print(f"Proveedor: {compra.proveedor.nombre}")
        print(f"Empleado: {compra.empleado.nombre}")
        print(f"Total: Q{compra.total:.2f}")
        print("Detalles:")
        for detalle in compra.detalles:
            print(f"  - Producto: {detalle['producto'].nombre}")
            print(f"    Cantidad: {detalle['cantidad']}")
            print(f"    Precio Unitario: Q{detalle['precio_unitario']}")
            print(f"    Subtotal: Q{detalle['subtotal']:.2f}")

def mostrar_ventas():
    print("Listado de Ventas")
    if not ventas:
        print("No hay ventas registradas.")
        return
    for venta in ventas:
        print(f"ID Venta: {venta.id}")
        print(f"Fecha: {venta.fecha}")
        print(f"Cliente: {venta.cliente.nombre}")
        print(f"Empleado: {venta.empleado.nombre}")
        print(f"Total: Q{venta.total:.2f}")
        print("Detalles:")
        for detalle in venta.detalles:
            print(f"  - Producto: {detalle['producto'].nombre}")
            print(f"    Cantidad: {detalle['cantidad']}")
            print(f"    Precio Unitario: Q{detalle['precio_unitario']}")
            print(f"    Subtotal: Q{detalle['subtotal']:.2f}")

def consultar_inventario():
    print("\nInventario actual.")
    for p in productos.values():
        print(p.resumen())

while True:
    print("•••••••Menú Principal•••••••")
    print("1. Área de Bodega.")
    print("2. Área de Cajas.")
    print("3. Gerencia.")
    print("4. Salir")
    opcion = input("Selecciona una opción: ").strip()
    match (opcion):
        case "1":
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
        case "2":
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
        case "3":
            while True:
                print("Bienvenido a Gerencia.")
                print("1. Agregar empleado.")
                print("2. Consultar inventario.")
                print("3. Mostrar ventas.")
                print("4. Mostrar compras.")
                print("5. Regresar al menú principal.")
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
                    break
                else:
                    print("Opción inválida, intente de nuevo.")
        case "4":
            print("Cerrando el sistema. ¡Hasta pronto!")
            exit()
        case _:
            print("Opción inválida, intente de nuevo.")