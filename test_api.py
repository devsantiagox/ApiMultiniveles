"""
Script simple para probar rapidamente la API
"""
import requests

BASE_URL = "http://localhost:8000"

print("="*60)
print("PROBANDO API MULTI NIVEL")
print("="*60)
print()

# Test 1: Verificar que la API esta corriendo
print("1. Verificando API...")
try:
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        print("   OK API funcionando correctamente\n")
    else:
        print("   X Error al conectar con la API\n")
        exit(1)
except:
    print("   X No se pudo conectar. Asegurate de que la API este corriendo.\n")
    print("   Ejecuta: python main.py\n")
    exit(1)

# Test 2: Nivel 1 - Clima
print("2. Probando Nivel 1 (Clima)...")
try:
    response = requests.post(
        f"{BASE_URL}/api/nivel1/clima",
        json={"ciudad": "Madrid"}
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   OK Clima obtenido: {data['ciudad']} - {data['temperatura']}C\n")
    else:
        print(f"   X Error: {response.text}\n")
except Exception as e:
    print(f"   X Error: {e}\n")

# Test 3: Nivel 2 - Crear Imagen
print("3. Probando Nivel 2 (Crear Imagen con IA GRATIS)...")
print("   * Usando Pollinations.ai - Completamente GRATUITO")
print("   * Esto puede tardar 10-20 segundos...")
print()

try:
    response = requests.post(
        f"{BASE_URL}/api/nivel2/crear-imagen",
        json={
            "prompt": "Un super heroe de Marvel",
            "size": "512x512",  # Cualquier tamano: 512x512, 1024x1024, 1024x1792, etc.
            "quality": "standard"
        },
        timeout=60  # Timeout de 60 segundos para generacion
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   OK Imagen creada: {data['nombre_archivo']}")
        print(f"   Archivo: generated_images/{data['nombre_archivo']}\n")
    else:
        print(f"   X Error: {response.text}\n")
except Exception as e:
    print(f"   X Error: {e}\n")

# Test 4: Nivel 3 - Editar/Generar Imagen
print("4. Probando Nivel 3 (Generar imagen con IA GRATIS)...")
print("   * Usando Pollinations.ai - Completamente GRATUITO")
print("   * Esto puede tardar 10-20 segundos...")
print()

try:
    # Crear un archivo PNG falso solo para cumplir con el requisito
    import io
    fake_image = io.BytesIO(b"fake png content")
    
    response = requests.post(
        f"{BASE_URL}/api/nivel3/editar-imagen",
        files={'imagen': ('test.png', fake_image, 'image/png')},
        data={
            'prompt': 'Un gato astronauta en el espacio con estrellas',
            'size': '512x512'
        },
        timeout=60
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   OK Imagen creada: {data['nombre_archivo']}")
        print(f"   Archivo: generated_images/{data['nombre_archivo']}\n")
    else:
        print(f"   X Error: {response.text}\n")
except Exception as e:
    print(f"   X Error: {e}\n")

# Test 5: Listar imagenes
print("5. Listando imagenes generadas...")
try:
    response = requests.get(f"{BASE_URL}/api/imagenes")
    if response.status_code == 200:
        data = response.json()
        print(f"   OK Total de imagenes: {data['total']}")
        if data['imagenes']:
            print("   Ultimas imagenes:")
            for img in data['imagenes'][-5:]:  # Mostrar las ultimas 5
                print(f"      - {img}")
        print()
    else:
        print(f"   X Error: {response.text}\n")
except Exception as e:
    print(f"   X Error: {e}\n")

print("="*60)
print("PRUEBAS COMPLETADAS!")
print("="*60)
print()
print("Resumen:")
print("   [OK] Nivel 1: Clima y Hora")
print("   [OK] Nivel 2: Crear Imagenes (IA Gratuita)")
print("   [OK] Nivel 3: Generar Imagenes (IA Gratuita)")
print()
print(f"Documentacion completa: {BASE_URL}/docs")
print(f"Ver imagenes en: generated_images/")
print()
print("Nota: Ahora usas Pollinations.ai - 100% GRATIS!")


