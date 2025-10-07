"""
Configuración de la aplicación
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Settings:
    """Configuración de la aplicación"""
    
    # API Keys
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Server Config
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # OpenWeather API
    OPENWEATHER_BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather"
    
    # Carpeta para imágenes generadas
    IMAGES_DIR: str = "generated_images"
    
    def __init__(self):
        # Crear directorio de imágenes si no existe
        if not os.path.exists(self.IMAGES_DIR):
            os.makedirs(self.IMAGES_DIR)

settings = Settings()


