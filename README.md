# 🎤 Sound Lyrics - Buscador de Letras y Karaoke

Un buscador de letras y karaoke con letras sincronizadas usando LRCLIB y Audd.io.

## ✨ Características

- **🔍 Búsqueda de letras**: Encuentra letras de canciones por texto
- **🎤 Modo Karaoke**: Reproduce letras sincronizadas con archivos de audio
- **🌐 Múltiples fuentes**: LRCLIB para letras sincronizadas reales, Audd.io como respaldo
- **✨ Efectos visuales**: Efecto de escritura para letras sincronizadas reales
- **🎵 Sincronización inteligente**: Timestamps reales o simulados según disponibilidad

## 📦 Repositorio

Encuéntralo en GitHub: `https://github.com/gaher1096/sound-lyrics`

## 🚀 Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/gaher1096/sound-lyrics
   cd sound-lyrics
   ```

2. **Crea un entorno virtual**:
   ```bash
   python -m venv venv
   ```

3. **Activa el entorno virtual**:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac**:
     ```bash
     source venv/bin/activate
     ```

4. **Instala las dependencias**:
   ```bash
   pip install -e .
   ```

5. **Configura las variables de entorno**:
   Copia el archivo `.env.example` a `.env` y completa los valores:
   ```bash
   cp .env.example .env
   ```
   Variables disponibles:
   ```env
   # Token de Audd.io para reconocimiento/búsqueda de letras
   API_TOKEN=
   ```

6. **Crea la carpeta de audio**:
   Crea la carpeta `sounds/` en la raíz del proyecto y coloca allí tus archivos `.mp3` (y otros formatos soportados). Recomendado nombrar archivos como:
   - `Canción - Artista.mp3`
   - `Artista - Canción.mp3`
   
   Nota: Usar ese formato mejora la extracción automática de artista y canción en el modo karaoke, ya que `lyrics_finder.py` detecta el patrón " - " para separar los campos.

## 📋 Uso

### Ejecutar el programa:
```bash
python main.py
```

### Opciones disponibles:
1. **🔍 Buscar letra de canción**: Busca letras por texto
2. **🎤 Iniciar Karaoke**: Reproduce letras sincronizadas con archivos de audio
3. **❌ Salir del programa**

## 🎵 Modo Karaoke

### Fuentes de letras:

#### **🌐 LRCLIB (Preferida)**
- Letras sincronizadas reales con timestamps precisos
- Efecto de escritura carácter por carácter
- Sincronización perfecta con la música

#### **🎤 Audd.io (Respaldo)**
- Reconocimiento de audio automático
- Timestamps simulados inteligentes
- Visualización directa

### Archivos de audio soportados:
- MP3
- WAV
- FLAC
- M4A

## 📁 Estructura del proyecto

```
sound-lyrics/
├── main.py              # Programa principal
├── lyrics_finder.py     # Lógica de búsqueda de letras
├── pyproject.toml       # Configuración del proyecto
├── .env                 # Variables de entorno
├── .env.example         # Ejemplo de variables de entorno
├── .gitignore          # Archivos ignorados por Git
├── README.md           # Este archivo
├── sounds/             # Directorio para archivos de audio
└── venv/               # Entorno virtual (no incluido en Git)
```

## 🔧 Dependencias

- **requests**: Para llamadas a APIs
- **python-dotenv**: Para variables de entorno
- **lrcup**: Para integración con LRCLIB

## 📝 Configuración

### Token de Audd.io
1. Regístrate en [Audd.io](https://audd.io/)
2. Obtén tu token de API
3. Agrégalo al archivo `.env`:
   ```env
   API_TOKEN=tu_token_aqui
   ```

### LRCLIB
No requiere configuración adicional. Se instala automáticamente con las dependencias.

## 🎯 Características técnicas

- **Sincronización real**: Usa timestamps de LRCLIB cuando están disponibles
- **Fallback inteligente**: Cambia automáticamente a Audd.io si LRCLIB no tiene la canción
- **Timestamps simulados**: Genera timestamps inteligentes basados en el contenido
- **Efectos visuales**: Efecto de escritura para letras sincronizadas reales
- **Logging**: Registra todas las respuestas de API para debugging

## 🐛 Solución de problemas

### Error: "No module named 'lrcup'"
```bash
pip install lrcup
```

### Error: "API_TOKEN not found"
Asegúrate de crear el archivo `.env` con tu token de Audd.io.

### Letras no sincronizadas
El programa usará timestamps simulados si no encuentra letras sincronizadas reales.

## 📄 Licencia

Este proyecto está licenciado bajo **GPL-3.0**. Revisa el archivo `LICENSE` en la raíz del repositorio para más detalles.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar el proyecto, no dudes en crear un pull request.

---

¡Disfruta cantando! 🎤🎵
