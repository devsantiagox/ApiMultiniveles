"""
API Multi Nivel - Proyecto de API REST con FastAPI
Creado en base a la clase del viernes 3 de Octubre

Niveles:
1. Obtener el clima y la hora según la ciudad ingresada
2. Crear una imagen según el prompt ingresado  
3. Editar una imagen según el prompt de indicaciones dadas
"""
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os

from models import (
    WeatherRequest, WeatherResponse,
    ImageCreateRequest, ImageCreateResponse,
    ImageEditRequest, ImageEditResponse,
    ErrorResponse
)
from services import WeatherService, ImageService
from config import settings

# Crear la aplicación FastAPI
app = FastAPI(
    title="API Multi Nivel",
    description="API con 3 niveles: Clima/Hora, Creación de Imágenes y Edición de Imágenes",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instanciar servicios
weather_service = WeatherService()


@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "mensaje": "Bienvenido a la API Multi Nivel",
        "Autor": "David Santiago Ruiz Patarroyo",
        "Correo": "davidsantiagoruiz@ucompensar.edu.co",
        "version": "1.0.0",
        "niveles": [
            {
                "nivel": 1,
                "nombre": "Clima y Hora",
                "endpoint": "/api/nivel1/clima",
                "descripcion": "Obtiene el clima y la hora según la ciudad ingresada"
            },
            {
                "nivel": 2,
                "nombre": "Crear Imagen",
                "endpoint": "/api/nivel2/crear-imagen",
                "descripcion": "Crea una imagen según el prompt ingresado"
            },
            {
                "nivel": 3,
                "nombre": "Editar Imagen",
                "endpoint": "/api/nivel3/editar-imagen",
                "descripcion": "Edita una imagen según el prompt de indicaciones dadas"
            }
        ]
    }


# ============================================
# NIVEL 1: OBTENER CLIMA Y HORA POR CIUDAD
# ============================================

@app.post("/api/nivel1/clima", response_model=WeatherResponse, tags=["Nivel 1 - Clima y Hora"])
async def obtener_clima(request: WeatherRequest):
    """
    Nivel 1: Obtiene el clima actual y la hora local de una ciudad
    
    - **ciudad**: Nombre de la ciudad (ej: "Madrid", "Buenos Aires", "Ciudad de México")
    
    Retorna información del clima incluyendo:
    - Temperatura actual
    - Descripción del clima
    - Humedad
    - Velocidad del viento
    - Hora local de la ciudad
    - Zona horaria
    """
    try:
        resultado = await weather_service.get_weather_and_time(request.ciudad)
        return WeatherResponse(**resultado)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"No se pudo obtener el clima: {str(e)}")


# ============================================
# NIVEL 2: CREAR IMAGEN CON PROMPT
# ============================================

@app.post("/api/nivel2/crear-imagen", response_model=ImageCreateResponse, tags=["Nivel 2 - Crear Imagen"])
async def crear_imagen(request: ImageCreateRequest):
    """
    Nivel 2: Genera una imagen usando IA GRATUITA (Pollinations.ai - Stable Diffusion)
    
    - **prompt**: Descripción de la imagen que deseas generar
    - **size**: Tamaño de la imagen (cualquier tamaño WxH, ej: 1024x1024, 512x512, 1024x1792)
    - **quality**: Calidad de la imagen (standard, hd) - nota: en versión gratuita se usa calidad mejorada por defecto
    
    ✨ COMPLETAMENTE GRATIS - Sin límites ni API keys necesarias
    
    Retorna:
    - URL de la imagen generada
    - Nombre del archivo guardado localmente
    """
    try:
        image_service = ImageService()
        resultado = image_service.create_image(
            prompt=request.prompt,
            size=request.size,
            quality=request.quality
        )
        
        return ImageCreateResponse(
            mensaje="Imagen generada exitosamente",
            prompt=request.prompt,
            url_imagen=resultado["url_imagen"],
            nombre_archivo=resultado["nombre_archivo"]
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear imagen: {str(e)}")


@app.get("/api/nivel2/imagen/{filename}", tags=["Nivel 2 - Crear Imagen"])
async def obtener_imagen(filename: str):
    """
    Obtiene una imagen generada por nombre de archivo
    """
    filepath = os.path.join(settings.IMAGES_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return FileResponse(filepath)


# ============================================
# NIVEL 3: EDITAR IMAGEN CON PROMPT
# ============================================

@app.post("/api/nivel3/editar-imagen", response_model=ImageEditResponse, tags=["Nivel 3 - Editar Imagen"])
async def editar_imagen(
    imagen: UploadFile = File(..., description="Imagen a editar (opcional en versión gratuita)"),
    prompt: str = Form(..., description="Instrucciones para generar/editar la imagen"),
    size: str = Form("1024x1024", description="Tamaño de la imagen resultante")
):
    """
    Nivel 3: Genera una imagen según instrucciones usando IA GRATUITA
    
    - **imagen**: Archivo de imagen (en esta versión gratuita, se genera nueva imagen basada en prompt)
    - **prompt**: Descripción detallada de lo que quieres generar
    - **size**: Tamaño de la imagen resultante (cualquier WxH, ej: 512x512, 1024x1024)
    
    ✨ COMPLETAMENTE GRATIS - Usa Pollinations.ai (Stable Diffusion)
    
    Nota: En la versión gratuita, se genera una nueva imagen basada en tu prompt
    en lugar de editar la imagen original (limitación de APIs gratuitas).
    
    Retorna:
    - URL de la imagen generada
    - Nombre del archivo guardado localmente
    """
    try:
        # Validar que sea PNG
        if not imagen.filename.lower().endswith('.png'):
            raise HTTPException(
                status_code=400,
                detail="La imagen debe ser formato PNG con transparencia"
            )
        
        # Guardar imagen temporal
        temp_filename = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        temp_filepath = os.path.join(settings.IMAGES_DIR, temp_filename)
        
        with open(temp_filepath, "wb") as buffer:
            content = await imagen.read()
            buffer.write(content)
        
        # Editar imagen
        image_service = ImageService()
        resultado = image_service.edit_image(
            image_path=temp_filepath,
            prompt=prompt,
            size=size
        )
        
        # Eliminar archivo temporal
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        
        return ImageEditResponse(
            mensaje="Imagen editada exitosamente",
            prompt=prompt,
            url_imagen=resultado["url_imagen"],
            nombre_archivo=resultado["nombre_archivo"]
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al editar imagen: {str(e)}")


@app.get("/api/nivel3/imagen/{filename}", tags=["Nivel 3 - Editar Imagen"])
async def obtener_imagen_editada(filename: str):
    """
    Obtiene una imagen editada por nombre de archivo
    """
    filepath = os.path.join(settings.IMAGES_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return FileResponse(filepath)


# ============================================
# ENDPOINT ADICIONAL: LISTAR IMÁGENES
# ============================================

@app.get("/api/imagenes", tags=["Utilidades"])
async def listar_imagenes():
    """
    Lista todas las imágenes generadas y editadas
    """
    if not os.path.exists(settings.IMAGES_DIR):
        return {"imagenes": []}
    
    archivos = os.listdir(settings.IMAGES_DIR)
    imagenes = [f for f in archivos if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    return {
        "total": len(imagenes),
        "imagenes": imagenes
    }


# Importar datetime para el nivel 3
from datetime import datetime


if __name__ == "__main__":
    import uvicorn
    print(f"Iniciando API Multi Nivel en http://{settings.HOST}:{settings.PORT}")
    print(f"Documentacion disponible en http://{settings.HOST}:{settings.PORT}/docs")
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)

