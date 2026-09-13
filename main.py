# ============================================
# main.py
# API de Ventas - Endpoints (Parte A + Parte B)
# ============================================

from fastapi import FastAPI, HTTPException
from typing import List

from database import Producto, Venta, db_session
from schema import ProductoCreate, ProductoResponse, VentaCreate, VentaResponse

app = FastAPI(title="API de Ventas", version="1.0.0")

# ============================================
# ENDPOINTS DE PRODUCTOS (PARTE A)
# ============================================

@app.post("/productos", response_model=ProductoResponse)
def crear_producto(producto: ProductoCreate):
    db_producto = Producto(nombre=producto.nombre, precio=producto.precio)
    db_session.add(db_producto)
    db_session.commit()
    db_session.refresh(db_producto)
    return db_producto

@app.get("/productos", response_model=List[ProductoResponse])
def listar_productos():
    return Producto.query.all()

@app.get("/productos/{id}", response_model=ProductoResponse)
def obtener_producto(id: int):
    producto = Producto.query.get(id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.put("/productos/{id}", response_model=ProductoResponse)
def actualizar_producto(id: int, producto: ProductoCreate):
    db_producto = Producto.query.get(id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db_producto.nombre = producto.nombre
    db_producto.precio = producto.precio
    db_session.commit()
    db_session.refresh(db_producto)
    return db_producto

@app.delete("/productos/{id}")
def eliminar_producto(id: int):
    db_producto = Producto.query.get(id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db_session.delete(db_producto)
    db_session.commit()
    return {"mensaje": "Producto eliminado"}

# ============================================
# ENDPOINTS DE VENTAS (PARTE B)
# ============================================

@app.post("/ventas", response_model=VentaResponse)
def crear_venta(venta: VentaCreate):
    # Verificar que el producto existe
    producto = Producto.query.get(venta.id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Calcular precio_total automáticamente
    precio_total = producto.precio * venta.cantidad
    
    # Crear la venta
    db_venta = Venta(
        fecha=venta.fecha,
        hora=venta.hora,
        id_producto=venta.id_producto,
        cantidad=venta.cantidad,
        precio_total=precio_total
    )
    db_session.add(db_venta)
    db_session.commit()
    db_session.refresh(db_venta)
    return db_venta

@app.get("/ventas", response_model=List[VentaResponse])
def listar_ventas():
    return Venta.query.all()

@app.get("/ventas/{id}", response_model=VentaResponse)
def obtener_venta(id: int):
    venta = Venta.query.get(id)
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta

@app.put("/ventas/{id}", response_model=VentaResponse)
def actualizar_venta(id: int, venta: VentaCreate):
    db_venta = Venta.query.get(id)
    if not db_venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    
    # Verificar producto
    producto = Producto.query.get(venta.id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Actualizar campos
    db_venta.fecha = venta.fecha
    db_venta.hora = venta.hora
    db_venta.id_producto = venta.id_producto
    db_venta.cantidad = venta.cantidad
    db_venta.precio_total = producto.precio * venta.cantidad
    
    db_session.commit()
    db_session.refresh(db_venta)
    return db_venta

@app.delete("/ventas/{id}")
def eliminar_venta(id: int):
    db_venta = Venta.query.get(id)
    if not db_venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    db_session.delete(db_venta)
    db_session.commit()
    return {"mensaje": "Venta eliminada"}

# ============================================
# BIENVENIDA
# ============================================
@app.get("/")
def root():
    return {"mensaje": "API de Ventas funcionando", "docs": "/docs"}