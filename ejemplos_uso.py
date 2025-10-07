"""
Ejemplos de uso de la API Multi Nivel

Estos scripts muestran cómo consumir cada uno de los 3 niveles de la API
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def ejemplo_nivel_1():
    """
    Ejemplo Nivel 1: Obtener clima y hora de una ciudad
    """
    print("\n" + "="*50)
    print("NIVEL 1: Clima y Hora")
    print("="*50)
    
    ciudades = ["Madrid", "Buenos Aires", "Ciudad de México", "Tokio"]
    
    for ciudad in ciudades:
        print(f"\n🌍 Consultando clima de {ciudad}...")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/nivel1/clima",
                json={"ciudad": ciudad}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Ciudad: {data['ciudad']}, {data['pais']}")
                print(f"   🌡️  Temperatura: {data['temperatura']}°C")
                print(f"   ☁️  Clima: {data['descripcion']}")
                print(f"   💧 Humedad: {data['humedad']}%")
                print(f"   💨 Viento: {data['velocidad_viento']} m/s")
                print(f"   🕐 Hora local: {data['hora_local']}")
                print(f"   🌐 Zona horaria: {data['zona_horaria']}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"❌ Error de conexión: {e}")


def ejemplo_nivel_2():
    """
    Ejemplo Nivel 2: Crear una imagen con DALL-E
    """
    print("\n" + "="*50)
    print("NIVEL 2: Crear Imagen")
    print("="*50)
    
    prompts = [
        "Un gato astronauta flotando en el espacio con estrellas de colores",
        "Un paisaje de montañas al atardecer con un lago cristalino",
        "Un robot amigable jugando con niños en un parque"
    ]
    
    for idx, prompt in enumerate(prompts, 1):
        print(f"\n🎨 Generando imagen {idx}...")
        print(f"   Prompt: '{prompt}'")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/nivel2/crear-imagen",
                json={
                    "prompt": prompt,
                    "size": "1024x1024",
                    "quality": "standard"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {data['mensaje']}")
                print(f"   📁 Archivo: {data['nombre_archivo']}")
                print(f"   🔗 URL: {data['url_imagen'][:60]}...")
                print(f"   📥 Ver localmente: {BASE_URL}/api/nivel2/imagen/{data['nombre_archivo']}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"❌ Error de conexión: {e}")


def ejemplo_nivel_3():
    """
    Ejemplo Nivel 3: Editar una imagen existente
    """
    print("\n" + "="*50)
    print("NIVEL 3: Editar Imagen")
    print("="*50)
    
    print("\n⚠️  Para usar este ejemplo, necesitas una imagen PNG con transparencia.")
    print("   Puedes crear una usando herramientas como:")
    print("   - remove.bg (para eliminar fondos)")
    print("   - Photoshop / GIMP (para crear áreas transparentes)")
    print("   - Canva (herramienta online)")
    
    imagen_path = "imagen_ejemplo.png"  # Cambia esto por tu imagen
    
    print(f"\n✏️  Editando imagen: {imagen_path}")
    print("   Prompt: 'Agregar un sombrero de mago y una varita mágica'")
    
    try:
        # Verificar si existe la imagen
        import os
        if not os.path.exists(imagen_path):
            print(f"\n❌ No se encontró la imagen: {imagen_path}")
            print("   Coloca una imagen PNG en la raíz del proyecto para probar este ejemplo.")
            return
        
        # Abrir la imagen y enviarla
        with open(imagen_path, 'rb') as img_file:
            files = {'imagen': img_file}
            data = {
                'prompt': 'Agregar un sombrero de mago y una varita mágica',
                'size': '1024x1024'
            }
            
            response = requests.post(
                f"{BASE_URL}/api/nivel3/editar-imagen",
                files=files,
                data=data
            )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['mensaje']}")
            print(f"   📁 Archivo: {result['nombre_archivo']}")
            print(f"   🔗 URL: {result['url_imagen'][:60]}...")
            print(f"   📥 Ver localmente: {BASE_URL}/api/nivel3/imagen/{result['nombre_archivo']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error: {e}")


def listar_imagenes():
    """
    Lista todas las imágenes generadas
    """
    print("\n" + "="*50)
    print("LISTAR IMÁGENES GENERADAS")
    print("="*50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/imagenes")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📁 Total de imágenes: {data['total']}")
            
            if data['imagenes']:
                print("\nImágenes disponibles:")
                for img in data['imagenes']:
                    print(f"   • {img}")
            else:
                print("\nNo hay imágenes generadas aún.")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")


def verificar_api():
    """
    Verifica que la API esté funcionando
    """
    print("\n" + "="*50)
    print("VERIFICANDO API")
    print("="*50)
    
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API funcionando correctamente")
            print(f"   Versión: {data['version']}")
            print(f"   Niveles disponibles: {len(data['niveles'])}")
            return True
        else:
            print(f"❌ API no responde correctamente: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ No se puede conectar a la API en {BASE_URL}")
        print("   Asegúrate de que la API esté ejecutándose con: python main.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def menu():
    """
    Menú interactivo para probar los ejemplos
    """
    print("\n" + "="*70)
    print("   API MULTI NIVEL - EJEMPLOS DE USO")
    print("="*70)
    
    if not verificar_api():
        return
    
    while True:
        print("\n📋 Selecciona una opción:")
        print("   1. Nivel 1 - Obtener clima y hora de ciudades")
        print("   2. Nivel 2 - Crear imágenes con DALL-E")
        print("   3. Nivel 3 - Editar imagen existente")
        print("   4. Listar todas las imágenes generadas")
        print("   5. Probar todos los niveles")
        print("   0. Salir")
        
        opcion = input("\n👉 Opción: ").strip()
        
        if opcion == "1":
            ejemplo_nivel_1()
        elif opcion == "2":
            ejemplo_nivel_2()
        elif opcion == "3":
            ejemplo_nivel_3()
        elif opcion == "4":
            listar_imagenes()
        elif opcion == "5":
            ejemplo_nivel_1()
            ejemplo_nivel_2()
            ejemplo_nivel_3()
            listar_imagenes()
        elif opcion == "0":
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("\n❌ Opción no válida. Intenta de nuevo.")
        
        input("\n⏎ Presiona Enter para continuar...")


if __name__ == "__main__":
    menu()


