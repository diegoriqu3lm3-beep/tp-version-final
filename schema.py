# ============================================
# schema.py
# Validación de datos (Pydantic)
# ============================================

from pydantic import BaseModel
from datetime import date, time

# ============================================
# SCHEMAS DE PRODUCTO
# ============================================
class ProductoCreate(BaseModel):
    nombre: str
    precio: float

class ProductoResponse(ProductoCreate):
    id: int
    class Config:
        from_attributes = True

# ============================================
# SCHEMAS DE VENTA
# ============================================
class VentaCreate(BaseModel):
    fecha: date
    hora: time
    id_producto: int
    cantidad: int

class VentaResponse(VentaCreate):
    id: int
    precio_total: float
    class Config:
        from_attributes = True