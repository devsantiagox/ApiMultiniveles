"""
Modelos de datos para la API
"""
from pydantic import BaseModel, Field
from typing import Optional

# Nivel 1: Clima y Hora
class WeatherRequest(BaseModel):
    """Request para obtener clima y hora de una ciudad"""
    ciudad: str = Field(..., description="Nombre de la ciudad", example="Bogota")

class WeatherResponse(BaseModel):
    """Response con información del clima y hora"""
    ciudad: str
    pais: str
    temperatura: float
    descripcion: str
    humedad: int
    velocidad_viento: float
    hora_local: str
    zona_horaria: str

# Nivel 2: Crear Imagen
class ImageCreateRequest(BaseModel):
    """Request para crear una imagen con IA gratuita"""
    prompt: str = Field(..., description="Descripción de la imagen a generar", 
                       example="Un gato astronauta en el espacio")
    size: Optional[str] = Field("1024x1024", description="Tamaño de la imagen (ej: 512x512, 1024x1024, 1024x1792)")
    quality: Optional[str] = Field("standard", description="Calidad de la imagen (standard, hd)")

class ImageCreateResponse(BaseModel):
    """Response con la imagen generada"""
    mensaje: str
    prompt: str
    url_imagen: str
    nombre_archivo: str

# Nivel 3: Editar Imagen
class ImageEditRequest(BaseModel):
    """Request para editar una imagen"""
    prompt: str = Field(..., description="Instrucciones para editar la imagen",
                       example="Agregar un sombrero de mago")
    size: Optional[str] = Field("1024x1024", description="Tamaño de la imagen (256x256, 512x512, 1024x1024)")

class ImageEditResponse(BaseModel):
    """Response con la imagen editada"""
    mensaje: str
    prompt: str
    url_imagen: str
    nombre_archivo: str

# Respuestas generales
class ErrorResponse(BaseModel):
    """Response de error"""
    error: str
    detalle: Optional[str] = None


