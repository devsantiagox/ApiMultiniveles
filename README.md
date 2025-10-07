# API Multi Nivel 🚀

API REST desarrollada con FastAPI que implementa 3 niveles de funcionalidad:

1. **Nivel 1**: Obtener el clima y la hora según la ciudad ingresada
2. **Nivel 2**: Crear una imagen según el prompt ingresado
3. **Nivel 3**: Editar una imagen según el prompt de indicaciones dadas

## 📋 Requisitos Previos

- Python 3.8 o superior
- Cuenta de OpenWeatherMap (para API key)
- Cuenta de OpenAI (para API key)

## 🔧 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd ApiMultiNivel
```

### 2. Crear un entorno virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto (puedes copiar `.env.example`):

```env
# API Keys
OPENWEATHER_API_KEY=tu_api_key_de_openweather
OPENAI_API_KEY=tu_api_key_de_openai

# Server Config
HOST=0.0.0.0
PORT=8000
```

#### ¿Cómo obtener las API Keys?

**OpenWeather API:**
1. Ve a [OpenWeatherMap](https://openweathermap.org/api)
2. Crea una cuenta gratuita
3. Ve a "API Keys" en tu perfil
4. Copia tu API key

**OpenAI API:**
1. Ve a [OpenAI Platform](https://platform.openai.com/)
2. Crea una cuenta
3. Ve a "API Keys" en configuración
4. Crea una nueva API key y cópiala

## 🚀 Ejecutar la API

```bash
python main.py
```

O usando uvicorn directamente:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en:
- **URL Base**: http://localhost:8000
- **Documentación Interactiva**: http://localhost:8000/docs
- **Documentación Alternativa**: http://localhost:8000/redoc

## 📚 Documentación de Endpoints

### Nivel 1: Clima y Hora 🌤️

**Endpoint**: `POST /api/nivel1/clima`

Obtiene el clima actual y la hora local de una ciudad.

**Request Body:**
```json
{
  "ciudad": "Madrid"
}
```

**Response:**
```json
{
  "ciudad": "Madrid",
  "pais": "ES",
  "temperatura": 22.5,
  "descripcion": "cielo claro",
  "humedad": 65,
  "velocidad_viento": 3.5,
  "hora_local": "2024-10-07 14:30:00",
  "zona_horaria": "UTC+2"
}
```

**Ejemplo con curl:**
```bash
curl -X POST "http://localhost:8000/api/nivel1/clima" \
  -H "Content-Type: application/json" \
  -d '{"ciudad": "Buenos Aires"}'
```

---

### Nivel 2: Crear Imagen 🎨

**Endpoint**: `POST /api/nivel2/crear-imagen`

Genera una imagen usando DALL-E 3 basándose en un prompt.

**Request Body:**
```json
{
  "prompt": "Un gato astronauta flotando en el espacio, estilo cartoon",
  "size": "1024x1024",
  "quality": "standard"
}
```

**Parámetros:**
- `prompt` (requerido): Descripción de la imagen a generar
- `size` (opcional): "256x256", "512x512", o "1024x1024" (default: "1024x1024")
- `quality` (opcional): "standard" o "hd" (default: "standard")

**Response:**
```json
{
  "mensaje": "Imagen generada exitosamente",
  "prompt": "Un gato astronauta flotando en el espacio, estilo cartoon",
  "url_imagen": "https://oaidalleapiprodscus.blob.core.windows.net/...",
  "nombre_archivo": "generated_20241007_143000.png"
}
```

**Ejemplo con curl:**
```bash
curl -X POST "http://localhost:8000/api/nivel2/crear-imagen" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Un dragón volando sobre montañas nevadas",
    "size": "1024x1024",
    "quality": "standard"
  }'
```

**Obtener la imagen guardada:**
```
GET /api/nivel2/imagen/{nombre_archivo}
```

---

### Nivel 3: Editar Imagen ✏️

**Endpoint**: `POST /api/nivel3/editar-imagen`

Edita una imagen existente usando DALL-E 2 según instrucciones.

**Request (multipart/form-data):**
- `imagen`: Archivo PNG con transparencia (File)
- `prompt`: Instrucciones para editar la imagen (string)
- `size`: Tamaño de la imagen resultante (string, opcional)

**Nota importante**: DALL-E requiere que la imagen sea PNG con áreas transparentes. Las áreas transparentes son donde se aplicarán los cambios según el prompt.

**Response:**
```json
{
  "mensaje": "Imagen editada exitosamente",
  "prompt": "Agregar un sombrero de mago",
  "url_imagen": "https://oaidalleapiprodscus.blob.core.windows.net/...",
  "nombre_archivo": "edited_20241007_143500.png"
}
```

**Ejemplo con curl:**
```bash
curl -X POST "http://localhost:8000/api/nivel3/editar-imagen" \
  -F "imagen=@imagen.png" \
  -F "prompt=Agregar un sombrero de mago" \
  -F "size=1024x1024"
```

**Ejemplo con Python:**
```python
import requests

files = {'imagen': open('imagen.png', 'rb')}
data = {
    'prompt': 'Agregar un sombrero de mago',
    'size': '1024x1024'
}

response = requests.post(
    'http://localhost:8000/api/nivel3/editar-imagen',
    files=files,
    data=data
)

print(response.json())
```

**Obtener la imagen editada:**
```
GET /api/nivel3/imagen/{nombre_archivo}
```

---

### Endpoint Adicional: Listar Imágenes 📁

**Endpoint**: `GET /api/imagenes`

Lista todas las imágenes generadas y editadas.

**Response:**
```json
{
  "total": 5,
  "imagenes": [
    "generated_20241007_143000.png",
    "edited_20241007_143500.png",
    "generated_20241007_144000.png"
  ]
}
```

## 🏗️ Estructura del Proyecto

```
ApiMultiNivel/
├── main.py              # Aplicación principal con endpoints
├── config.py            # Configuración y variables de entorno
├── models.py            # Modelos de datos (Pydantic)
├── services.py          # Servicios para APIs externas
├── requirements.txt     # Dependencias del proyecto
├── .env                 # Variables de entorno (no incluir en git)
├── .env.example         # Ejemplo de variables de entorno
├── .gitignore          # Archivos a ignorar en git
├── README.md           # Documentación
└── generated_images/   # Carpeta para imágenes generadas
```

## 🧪 Probar la API

### Usando la documentación interactiva

1. Inicia la API: `python main.py`
2. Abre tu navegador en: http://localhost:8000/docs
3. Verás la interfaz Swagger UI donde puedes probar todos los endpoints
4. Haz clic en cualquier endpoint → "Try it out" → Completa los parámetros → "Execute"

### Usando Python requests

```python
import requests

# Nivel 1: Obtener clima
response = requests.post(
    'http://localhost:8000/api/nivel1/clima',
    json={'ciudad': 'París'}
)
print(response.json())

# Nivel 2: Crear imagen
response = requests.post(
    'http://localhost:8000/api/nivel2/crear-imagen',
    json={
        'prompt': 'Un atardecer en la playa con palmeras',
        'size': '1024x1024'
    }
)
print(response.json())

# Nivel 3: Editar imagen
files = {'imagen': open('mi_imagen.png', 'rb')}
data = {'prompt': 'Agregar un arcoíris en el cielo'}
response = requests.post(
    'http://localhost:8000/api/nivel3/editar-imagen',
    files=files,
    data=data
)
print(response.json())
```

## ⚠️ Notas Importantes

### Sobre el Nivel 3 (Editar Imagen)

- **Formato requerido**: La imagen debe ser PNG con áreas transparentes
- **Modelo usado**: DALL-E 2 (DALL-E 3 no soporta edición de imágenes)
- **Funcionamiento**: Las áreas transparentes de la imagen son donde se aplicarán los cambios según el prompt
- **Tamaños soportados**: 256x256, 512x512, 1024x1024

### Costos

- **OpenWeather API**: Gratis para hasta 60 llamadas por minuto
- **OpenAI API**: 
  - DALL-E 3 (Nivel 2): ~$0.040-0.080 por imagen dependiendo del tamaño y calidad
  - DALL-E 2 (Nivel 3): ~$0.020 por imagen

### Limitaciones

- Las imágenes se guardan localmente en `generated_images/`
- No hay persistencia en base de datos
- Las API keys deben mantenerse privadas y no compartirse

## 🐛 Troubleshooting

### Error: "OPENWEATHER_API_KEY no está configurada"
- Verifica que existe el archivo `.env` en la raíz del proyecto
- Asegúrate de haber copiado correctamente tu API key de OpenWeatherMap

### Error: "OPENAI_API_KEY no está configurada"
- Verifica que existe el archivo `.env` en la raíz del proyecto
- Asegúrate de haber copiado correctamente tu API key de OpenAI

### Error al editar imagen: "La imagen debe ser formato PNG con transparencia"
- Asegúrate de usar una imagen PNG
- La imagen debe tener áreas transparentes para que DALL-E pueda editarla
- Puedes usar herramientas como Photoshop, GIMP o remove.bg para crear transparencias

### Error: "No se pudo obtener el clima"
- Verifica que el nombre de la ciudad esté correctamente escrito
- Prueba con nombres en inglés si no funciona en español
- Verifica que tu API key de OpenWeather sea válida

## 📝 Licencia

Este proyecto fue creado con fines educativos basado en la clase del viernes 3 de Octubre.

## 👨‍💻 Autor

Desarrollado para el curso de API Multi Nivel.

---

**¡Disfruta usando la API! 🎉**


