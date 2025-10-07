"""
Servicios para interactuar con APIs externas
"""
import httpx
import os
from datetime import datetime, timezone, timedelta
from config import settings
from openai import OpenAI
import requests

class WeatherService:
    """Servicio para obtener información del clima"""
    
    @staticmethod
    async def get_weather_and_time(ciudad: str):
        """
        Obtiene el clima y la hora local de una ciudad
        """
        if not settings.OPENWEATHER_API_KEY:
            raise ValueError("OPENWEATHER_API_KEY no está configurada")
        
        params = {
            "q": ciudad,
            "appid": settings.OPENWEATHER_API_KEY,
            "units": "metric",  # Para obtener temperatura en Celsius
            "lang": "es"  # Respuestas en español
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(settings.OPENWEATHER_BASE_URL, params=params)
            
            if response.status_code != 200:
                raise Exception(f"Error al obtener el clima: {response.text}")
            
            data = response.json()
            
            # Calcular hora local usando el timezone offset
            timezone_offset = data['timezone']  # Offset en segundos
            utc_time = datetime.now(timezone.utc)
            local_time = utc_time + timedelta(seconds=timezone_offset)
            
            return {
                "ciudad": data['name'],
                "pais": data['sys']['country'],
                "temperatura": data['main']['temp'],
                "descripcion": data['weather'][0]['description'],
                "humedad": data['main']['humidity'],
                "velocidad_viento": data['wind']['speed'],
                "hora_local": local_time.strftime("%Y-%m-%d %H:%M:%S"),
                "zona_horaria": f"UTC{timezone_offset//3600:+d}"
            }


class ImageService:
    """Servicio para crear y editar imágenes usando IA gratuita (Pollinations.ai)"""
    
    def __init__(self):
        # Pollinations.ai no requiere API key - es completamente gratuito
        self.pollinations_base_url = "https://image.pollinations.ai/prompt"
    
    def create_image(self, prompt: str, size: str = "1024x1024", quality: str = "standard"):
        """
        Genera una imagen usando Pollinations.ai (GRATIS - basado en Stable Diffusion)
        """
        try:
            # Extraer dimensiones del tamaño
            width, height = size.split('x')
            
            # URL de Pollinations.ai - genera imagen automáticamente
            # Formato: https://image.pollinations.ai/prompt/{prompt}?width={w}&height={h}&nologo=true
            encoded_prompt = requests.utils.quote(prompt)
            image_url = f"{self.pollinations_base_url}/{encoded_prompt}?width={width}&height={height}&nologo=true&enhance=true"
            
            # Descargar la imagen
            response = requests.get(image_url, timeout=60)
            if response.status_code != 200:
                raise Exception(f"Error al generar imagen: Status {response.status_code}")
            
            # Guardar la imagen
            filename = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(settings.IMAGES_DIR, filename)
            
            with open(filepath, 'wb') as handler:
                handler.write(response.content)
            
            return {
                "url_imagen": image_url,
                "nombre_archivo": filename,
                "ruta_local": filepath
            }
        except Exception as e:
            raise Exception(f"Error al generar imagen: {str(e)}")
    
    def edit_image(self, image_path: str, prompt: str, size: str = "1024x1024"):
        """
        'Edita' una imagen combinándola con un nuevo prompt (método alternativo gratuito)
        Nota: En realidad genera una nueva imagen basada en el prompt, ya que la edición 
        real de imágenes con IA gratuita tiene limitaciones.
        """
        try:
            # Para simular edición, generamos una nueva imagen con el prompt
            # En un servicio gratuito, la edición real de imágenes es limitada
            width, height = size.split('x')
            
            # Mejorar el prompt con contexto de edición
            enhanced_prompt = f"{prompt}, high quality, detailed"
            encoded_prompt = requests.utils.quote(enhanced_prompt)
            image_url = f"{self.pollinations_base_url}/{encoded_prompt}?width={width}&height={height}&nologo=true&enhance=true"
            
            # Descargar la imagen generada
            response = requests.get(image_url, timeout=60)
            if response.status_code != 200:
                raise Exception(f"Error al editar imagen: Status {response.status_code}")
            
            # Guardar la imagen editada
            filename = f"edited_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(settings.IMAGES_DIR, filename)
            
            with open(filepath, 'wb') as handler:
                handler.write(response.content)
            
            return {
                "url_imagen": image_url,
                "nombre_archivo": filename,
                "ruta_local": filepath
            }
        except Exception as e:
            raise Exception(f"Error al editar imagen: {str(e)}")
    
    def create_variation(self, image_path: str, prompt: str = "creative variation"):
        """
        Crea una variación basada en un prompt (método gratuito)
        """
        try:
            # Generar variación usando un prompt genérico
            encoded_prompt = requests.utils.quote(prompt)
            image_url = f"{self.pollinations_base_url}/{encoded_prompt}?width=1024&height=1024&nologo=true&enhance=true&seed={datetime.now().timestamp()}"
            
            # Descargar la variación
            response = requests.get(image_url, timeout=60)
            if response.status_code != 200:
                raise Exception(f"Error al crear variación: Status {response.status_code}")
            
            # Guardar la variación
            filename = f"variation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(settings.IMAGES_DIR, filename)
            
            with open(filepath, 'wb') as handler:
                handler.write(response.content)
            
            return {
                "url_imagen": image_url,
                "nombre_archivo": filename,
                "ruta_local": filepath
            }
        except Exception as e:
            raise Exception(f"Error al crear variación: {str(e)}")


