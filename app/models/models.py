from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, LargeBinary, event, func, select, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base


# Modelo Cuadrilla
class Cuadrilla(Base):
    __tablename__ = "cuadrillas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    clave = Column(String(20), nullable=True)
    responsable = Column(String(50), nullable=False)
    localidad = Column(String(100), nullable=False)

    # Relación 1:N con Recolector
    # Relación 1:N con Recolector. Un objeto Cuadrilla tiene muchos objetos Recolector.
    # La relación se establece en el campo id_cuadrilla de la tabla Recolector.
    # El parámetro back_populates se utiliza para establecer la relación inversa.
    # En este caso, permite acceder a los objetos Cuadrilla desde un objeto Recolector
    # a través de la propiedad cuadrilla. Por ejemplo, recolector.cuadrilla returns the
    # related Cuadrilla object.
    recolectores = relationship("Recolector", back_populates="cuadrilla")

# Modelo Recolector
class Recolector(Base):
    __tablename__ = "recolectores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    clave = Column(String(20), nullable=True)
    nombre_completo = Column(String(100), nullable=False)
    encoder = Column(String(200), nullable=False)
    foto = Column(LargeBinary)
    localidad = Column(String(100))
    tel = Column(String(20))
    id_cuadrilla = Column(Integer, ForeignKey("cuadrillas.id"), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.now)
    acceso = Column(Boolean, default=True)

    # Relaciones
    cuadrilla = relationship("Cuadrilla", back_populates="recolectores")
    
# Event listeners para generación automática de claves
@event.listens_for(Cuadrilla, "after_insert")
def generar_clave_cuadrilla(mapper, connection, target):
    if target.clave is None:
        target.clave = f"CUA{target.id}"
        connection.execute(
            mapper.mapped_table.update()
            .where(mapper.mapped_table.c.id == target.id)
            .values(clave=target.clave)
        )

@event.listens_for(Recolector, "after_insert")
def generar_clave_recolector(mapper, connection, target):
    if target.clave is None:
        target.clave = f"REC{target.id}"
        connection.execute(
            mapper.mapped_table.update()
            .where(mapper.mapped_table.c.id == target.id)
            .values(clave=target.clave)
        )
