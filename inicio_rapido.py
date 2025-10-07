"""
Script de Inicio Rápido para API Multi Nivel

Este script verifica la configuración y ayuda a iniciar la API
"""
import os
import sys

def verificar_archivo_env():
    """Verifica si existe el archivo .env"""
    if not os.path.exists('.env'):
        print("❌ No se encontró el archivo .env")
        print("\n📝 Necesitas crear un archivo .env con tus API keys.")
        print("   Puedes copiar .env.example y llenarlo con tus datos:\n")
        print("   OPENWEATHER_API_KEY=tu_api_key")
        print("   OPENAI_API_KEY=tu_api_key")
        print("   HOST=0.0.0.0")
        print("   PORT=8000")
        print("\n🔗 Obtén tus API keys en:")
        print("   - OpenWeather: https://openweathermap.org/api")
        print("   - OpenAI: https://platform.openai.com/")
        return False
    return True

def verificar_dependencias():
    """Verifica si las dependencias están instaladas"""
    try:
        import fastapi
        import uvicorn
        import httpx
        import openai
        from dotenv import load_dotenv
        return True
    except ImportError as e:
        print(f"❌ Falta instalar dependencias: {e.name}")
        print("\n📦 Instala las dependencias con:")
        print("   pip install -r requirements.txt")
        return False

def verificar_api_keys():
    """Verifica que las API keys estén configuradas"""
    from dotenv import load_dotenv
    load_dotenv()
    
    openweather_key = os.getenv("OPENWEATHER_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    problemas = []
    
    if not openweather_key or openweather_key == "tu_api_key_de_openweather":
        problemas.append("OPENWEATHER_API_KEY no está configurada")
    
    if not openai_key or openai_key == "tu_api_key_de_openai":
        problemas.append("OPENAI_API_KEY no está configurada")
    
    if problemas:
        print("⚠️  Problemas encontrados:")
        for p in problemas:
            print(f"   • {p}")
        print("\n💡 Edita el archivo .env y agrega tus API keys válidas.")
        return False
    
    return True

def main():
    print("\n" + "="*60)
    print("     API MULTI NIVEL - INICIO RÁPIDO")
    print("="*60)
    
    print("\n🔍 Verificando configuración...\n")
    
    # Verificar archivo .env
    print("1️⃣ Verificando archivo .env...")
    if not verificar_archivo_env():
        sys.exit(1)
    print("   ✅ Archivo .env encontrado\n")
    
    # Verificar dependencias
    print("2️⃣ Verificando dependencias...")
    if not verificar_dependencias():
        sys.exit(1)
    print("   ✅ Todas las dependencias instaladas\n")
    
    # Verificar API keys
    print("3️⃣ Verificando API keys...")
    if not verificar_api_keys():
        print("\n⚠️  La API puede iniciar pero los endpoints fallarán sin API keys válidas.")
        respuesta = input("\n¿Deseas continuar de todos modos? (s/n): ")
        if respuesta.lower() != 's':
            sys.exit(1)
    else:
        print("   ✅ API keys configuradas\n")
    
    print("="*60)
    print("✅ Configuración correcta. Iniciando API...")
    print("="*60)
    print()
    
    # Iniciar la API
    try:
        import uvicorn
        from main import app
        from config import settings
        
        print(f"🚀 API corriendo en: http://{settings.HOST}:{settings.PORT}")
        print(f"📚 Documentación: http://{settings.HOST}:{settings.PORT}/docs")
        print("\n💡 Presiona Ctrl+C para detener el servidor\n")
        
        uvicorn.run(app, host=settings.HOST, port=settings.PORT)
    except KeyboardInterrupt:
        print("\n\n👋 Servidor detenido. ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error al iniciar el servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


