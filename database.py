

# Conexión a la base de datos + Modelos (tablas)


from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


# CONEXIÓN A LA BASE DE DATOS

engine = create_engine("sqlite:///database.db")
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# TABLA: PRODUCTOS

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)

    # Relación: un producto tiene muchas ventas
    ventas = relationship("Venta", back_populates="producto")


# TABLA: VENTAS

class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    cantidad = Column(Integer, nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id"), nullable=False)
    precio_total = Column(Float, nullable=False)

    # Relación: una venta pertenece a un producto
    producto = relationship("Producto", back_populates="ventas")



# CREAR LAS TABLAS

Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=True)
