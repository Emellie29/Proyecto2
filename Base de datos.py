class Productos:
    def __init__(self, id_producto, nombreP, precio, id_categoria, totalventas=0, totalcompras=0):
        self.id_producto = id_producto
        self.nombreP = nombreP
        self.precio = precio
        self.stock=0
        self.id_categoria=id_categoria #llave
        self.totalventas=totalventas
        self.totalcompras=totalcompras
    def actualizar_stock(self, cantidad, tipo):
        if tipo == "compra":
            self.stock += cantidad
        elif tipo == "venta":
            if cantidad > self.stock:
                raise ValueError("Producto insuficiente")
            self.stock -= cantidad
    def resumen(self):
        return f"{self.id_producto} - {self.nombre} - Q.{self.precio} - {self.stock}"
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
        return f"NIT: {self.nit} - {self.nombreCl} - Tel: {self.telefono} - Dirección: {self.direccion} - Correo: {self.correo}"
class Empleados:
    def __init__(self, id_empleado, nombreE, telefonoE, direccionE, correoE):
        self.id_empleado = id_empleado
        self.nombreE = nombreE
        self.telefonoE = telefonoE
        self.direccionE = direccionE
        self.correoE = correoE
    def resumen(self):
        return f"{self.id_empleado} - {self.nombreE} - Tel: {self.telefonoE} - Dirección: {self.direccionE} - Correo: {self.correoE}"
class Proveedores:
    def __int__(self, id_proveedor, nombrePr, empresa, telefonoPr, direccionPr, correoPr, id_categoria):
        self.id_proveedor = id_proveedor
        self.nombrePr = nombrePr
        self.empresa = empresa
        self.telefonoPr = telefonoPr
        self.direccionPr = direccionPr
        self.correoPr = correoPr
        self.id_categoria = id_categoria
    def resumen(self):
        return f"{self.id_proveedor} - {self.nombrePr} - Empresa: {self.empresa} - Tel: {self.telefonoPr} - Direccion: {self.direccionPr} - Correo: {self.correoPr} - Producto: {self.id_categoria}"
class Ventas:
    def __init__(self, id_venta, fecha, nit, id_empleado, categoria):
        self.id_venta = id_venta
        self.fecha = fecha
        self.nit = nit #llave
        self.id_empleado = id_empleado #llave
        self.categoria = categoria #llave
        self.detalles = []
        self.total = 0.0
    def agregar_detalleV(self, producto, cantidad):
        producto.actualizar_stock(cantidad, "Venta")
        detalle = DetalleVentas(producto, cantidad)
        self.detalles.append(detalle)
        self.total += detalle.subtotal #total acumulado
    def resumen(self):
        return f"Venta No. {self.id_venta} | Fecha: {self.fecha} | NIT: {self.nit} | Empleado: {self.id_empleado} | Total: Q.{self.total:.2f}"
class DetalleVentas:
    def __init__(self, id_detalle_venta, id_venta, id_producto, cantidad):
        self.id_detalle_venta = id_detalle_venta
        self.id_venta = id_venta
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio = id_producto.precio
        self.subtotal = self.precio * self.cantidad
    def resumen(self):
        return (f"Detalle No. {self.id_detalle_venta} | Venta No. {self.id_venta} | Producto ID: {self.id_producto} | Cantidad: {self.cantidad} |"
                f"Precio: Q.{self.precio:.2f} | Subtotal: {self.subtotal:.2f}")
class Compras:
    def __init__(self, id_compra, fecha, id_proveedor, id_empleado):
        self.id_compra = id_compra
        self.fecha = fecha
        self.proveedor = id_proveedor #llave
        self.empleado = id_empleado #llave
        self.detalles = []
        self.total = 0.0
    def agregar_detalleC(self, producto, cantidad, precio_uni):
        producto.actualizar_stock(cantidad, "Compra")
        detalleC = DetalleCompras(producto, cantidad, precio_uni)
        self.detalles.append(detalleC)
        self.total += detalleC.subtotal  #se acumula el total
    def resumen(self):
        return f"Compra No. {self.id_compra} | Fecha: {self.fecha} | Proveedor: {self.proveedor} | Empleado: {self.empleado} | Total: Q.{self.total:.2f}"
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
        return (f" Detalla No. {self.id_detalle_compra} | Compra No. {self.id_compra} | Producto ID: {self.id_producto} | Cantidad: {self.cantidad} |"
                f"Precio: Q.{self.precio_compra:.2f} | Subtotal: Q.{self.subtotal:.2f} | Caduca: {self.fecha_caducidad}")
#diccionarios
categorias = {}
productos = {}
clientes = {}
empleados = {}
proveedors = {}
ventas = []
compras = []
def agregar_catecoria():
    print("\n Agregar Categoria")
    id_categoria = len(categorias)+1
    nombre_categoria = input("Nombre de la categoria: ")
    categorias[id_categoria] = categorias(id_categoria, nombre_categoria)
    print("Categoria agregada con exito.")
def agregar_producto():
    print("\n Agregar Producto")
    id_producto = len(productos)+1
    nombre_producto = input("Nombre del producto: ")
    precio_producto = input("Precio del producto: ")
    print("Categorias disponibles: ")
    for c in Categorias.values():
        print(c.resumen())
    id_categoria = int(input("ID de la categoria: "))
    categorias=Categorias.get(id_categoria)
    if not categorias:
        print("Categoria no existe")
        return
    productos[id_producto] = Productos(id_producto, nombre_producto, precio_producto, categorias)
    print("Producto agregado")
def informacion_cliente():
    print("\n Informacion de Cliente")
    nit = input("NIT: ")
    if nit in clientes:
        print("El cliente ya existe")
        return
    nombreCL = input("Nombre del cliente: ")
    telefono = input("Telefono del cliente: ")
    direccion = input("Direccion del cliente: ")
    correo = input("Correo del cliente: ")
    clientes[nit] = Clientes(nit, nombreCL, telefono, direccion, correo)
    print("Cliente agregado.")
def informacion_empleado():
    print("\n Informacion del Empleado")
    id_empleado = len(empleados)+1
    nombreE = input("Nombre del Empleado: ")
    telefonoE = input("Telefono del Empleado: ")
    direccionE = input("Direccion del Empleado: ")
    correoE = input("Correo del Empleado: ")
    empleados[id_empleado] = Empleados(id_empleado, nombreE, telefonoE, direccionE, correoE)
    print("Empleado agregado.")
def informacion_proveedor():
    print("\n Informacion del Proveedor")