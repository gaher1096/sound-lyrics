import os
import requests
import json
import datetime
import re
from dotenv import load_dotenv

try:
    from lrcup import LRCLib
    LRCLIB_AVAILABLE = True
    print("✅ LRCLIB disponible - Letras sincronizadas reales habilitadas")
except ImportError:
    LRCLIB_AVAILABLE = False
    print("⚠️ LRCLIB no está disponible. Instala con: pip install lrcup")

# Carga las variables del archivo .env
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

# Configuración de logging
LOG_FILE = "api_responses.log"


def parse_lrc_lyrics(lrc_text):
    """
    Parsea texto LRC y lo convierte al formato esperado por el karaoke.
    """
    lines = []
    for line in lrc_text.strip().split("\n"):
        if not line.strip():
            continue

        # Buscar timestamp en formato [mm:ss.xx] o [mm:ss]
        timestamp_match = re.match(r"\[(\d{2}):(\d{2})(?:\.(\d{2}))?\]", line)
        if timestamp_match:
            minutes = int(timestamp_match.group(1))
            seconds = int(timestamp_match.group(2))
            centiseconds = int(timestamp_match.group(3) or 0)

            # Convertir a segundos totales
            total_seconds = minutes * 60 + seconds + centiseconds / 100.0

            # Extraer el texto de la línea (después del timestamp)
            text = line[timestamp_match.end() :].strip()

            if text:  # Solo agregar si hay texto
                # Formatear timestamp como HH:MM:SS.fff
                timestamp = f"00:{minutes:02d}:{seconds:02d}.{centiseconds:02d}0"
                lines.append({"text": text, "timestamp": timestamp})

    return lines


def obtener_letra_sincronizada_lrclib(nombre_cancion, nombre_artista, duracion=None):
    """
    Obtiene letras sincronizadas usando LRCLIB API.
    """
    if not LRCLIB_AVAILABLE:
        print("❌ LRCLIB no está disponible. Usando método alternativo.")
        return None

    try:
        lrclib = LRCLib()

        # Log de la consulta
        request_data = {
            "track": nombre_cancion,
            "artist": nombre_artista,
            "duration": duracion,
        }

        print(f"🔍 Buscando en la base de datos de LRCLIB...")
        print(f"   📝 Canción: '{nombre_cancion}'")
        print(f"   👤 Artista: {nombre_artista}")

        # Buscar letras sincronizadas
        if duracion:
            cancion = lrclib.get(
                track=nombre_cancion, artist=nombre_artista, duration=duracion
            )
        else:
            resultados = lrclib.search(track=nombre_cancion, artist=nombre_artista)
            cancion = resultados[0] if resultados else None

        if cancion and hasattr(cancion, "syncedLyrics") and cancion.syncedLyrics:
            # Log de la respuesta exitosa
            log_api_response(
                endpoint="lrclib_search",
                request_data=request_data,
                response_data={"syncedLyrics": cancion.syncedLyrics, "found": True},
                status="success",
            )

            print("🎉 ¡ENCONTRADO! Letras sincronizadas reales disponibles")
            print("✅ Timestamps reales de la música")
            print("✅ Sincronización perfecta garantizada")
            print(f"📝 Respuesta guardada en el archivo de log: {LOG_FILE}")

            # Parsear las letras LRC
            return parse_lrc_lyrics(cancion.syncedLyrics), "LRCLIB"
        else:
            # Log de no resultados
            log_api_response(
                endpoint="lrclib_search",
                request_data=request_data,
                response_data={"found": False},
                status="no_results",
            )

            print("❌ No se encontraron letras sincronizadas en LRCLIB")
            print("   💡 Esta canción no está en la base de datos de LRCLIB")
            return None, None

    except Exception as e:
        # Log del error
        log_api_response(
            endpoint="lrclib_search",
            request_data=request_data,
            response_data={"error": str(e)},
            status="error",
        )

        print(f"❌ Error al consultar LRCLIB: {e}")
        return None, None


def log_api_response(endpoint, request_data, response_data, status="success"):
    """
    Guarda la respuesta de la API en un archivo de log con timestamp.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = {
        "timestamp": timestamp,
        "endpoint": endpoint,
        "request": request_data,
        "response": response_data,
        "status": status,
    }

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"TIMESTAMP: {timestamp}\n")
            f.write(f"ENDPOINT: {endpoint}\n")
            f.write(f"STATUS: {status}\n")
            f.write(
                f"REQUEST: {json.dumps(request_data, indent=2, ensure_ascii=False)}\n"
            )
            f.write(
                f"RESPONSE: {json.dumps(response_data, indent=2, ensure_ascii=False)}\n"
            )
            f.write(f"{'='*80}\n")
    except Exception as e:
        print(f"Error al escribir en el log: {e}")


def crear_timestamps_inteligentes(lines):
    """
    Crea timestamps inteligentes basados en el contenido de las líneas.
    Ajusta los tiempos según la longitud, tipo de línea y patrones musicales.
    """
    timestamps = []
    tiempo_actual = 0

    for i, line in enumerate(lines):
        # Calcular tiempo basado en el contenido de la línea
        tiempo_linea = calcular_tiempo_linea(line, i, lines)

        # Crear timestamp en formato HH:MM:SS.fff
        minutos = int(tiempo_actual // 60)
        segundos = int(tiempo_actual % 60)
        milisegundos = int((tiempo_actual % 1) * 1000)

        timestamp = f"00:{minutos:02d}:{segundos:02d}.{milisegundos:03d}"
        timestamps.append({"text": line, "timestamp": timestamp})

        # Avanzar el tiempo para la siguiente línea
        tiempo_actual += tiempo_linea

    return timestamps


def calcular_tiempo_linea(line, index, all_lines):
    """
    Calcula el tiempo apropiado para una línea basándose en su contenido.
    """
    # Tiempo base
    tiempo_base = 4.0

    # Ajustar por longitud de la línea
    longitud = len(line)
    if longitud < 20:
        tiempo_extra = 2.0
    elif longitud < 40:
        tiempo_extra = 4.0
    elif longitud < 60:
        tiempo_extra = 6.0
    else:
        tiempo_extra = 8.0

    # Ajustar por tipo de línea
    if line.startswith("[") and line.endswith("]"):
        # Títulos de sección - tiempo corto
        return 1.0
    elif any(
        word in line.lower() for word in ["chorus", "refrain", "coro", "estribillo"]
    ):
        # Coros - tiempo más largo para repetir
        return tiempo_base + tiempo_extra + 3.0
    elif any(word in line.lower() for word in ["verse", "verso", "strophe", "estrofa"]):
        # Versos - tiempo normal
        return tiempo_base + tiempo_extra
    elif line.count(" ") > 8:  # Líneas muy largas
        return tiempo_base + tiempo_extra + 2.0
    elif line.count(" ") < 3:  # Líneas muy cortas
        return tiempo_base + tiempo_extra - 1.0
    else:
        return tiempo_base + tiempo_extra


def obtener_letra(nombre_cancion: str, nombre_artista: str):
    """
    Busca una canción y obtiene su letra usando la API de Audd.io.
    """
    if not API_TOKEN:
        print("Error: No se encontró el API_TOKEN. Revisa tu archivo .env.")
        return

    print(f"Buscando '{nombre_cancion}' de {nombre_artista}...")

    params = {
        "q": f"{nombre_artista} {nombre_cancion}",
        # 'return': 'lyrics' ya no es necesario con este endpoint,
        # pero no hace daño dejarlo.
        "api_token": API_TOKEN,
    }

    try:
        response = requests.get("https://api.audd.io/findLyrics/", params=params)

        response.raise_for_status()
        datos = response.json()

        # Log de la respuesta de la API
        log_api_response(
            endpoint="findLyrics",
            request_data=params,
            response_data=datos,
            status="success" if datos.get("status") == "success" else "no_results",
        )
        print(f"📝 Respuesta guardada en el archivo de log: {LOG_FILE}")

        # El formato de respuesta de findLyrics es un poco diferente
        if datos.get("status") == "success" and datos.get("result"):
            # El resultado es una lista, tomamos el primer elemento
            resultado = datos["result"][0]

            print("\n--- ¡Letra encontrada! ---")
            print(f"\nCanción: {resultado['title']}")
            print(f"Artista: {resultado['artist']}")
            print("-" * 25)
            print(resultado["lyrics"])  # La letra viene directamente en 'lyrics'

        else:
            print("No se encontró ninguna canción que coincida en los resultados.")
            print("Respuesta completa de la API:", datos)

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        # Log del error
        log_api_response(
            endpoint="findLyrics",
            request_data=params,
            response_data={"error": str(e)},
            status="connection_error",
        )
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")
        # Log del error
        log_api_response(
            endpoint="findLyrics",
            request_data=params,
            response_data={"error": str(e)},
            status="unexpected_error",
        )


# --- Función para obtener letra sincronizada (reconocimiento de audio) ---
def obtener_letra_sincronizada(ruta_archivo_audio: str):
    """
    Obtiene letras sincronizadas usando LRCLIB como primera opción,
    y Audd.io como respaldo.
    """
    # Extraer nombre del archivo sin extensión para usar como nombre de canción
    nombre_archivo = os.path.basename(ruta_archivo_audio)
    nombre_sin_extension = os.path.splitext(nombre_archivo)[0]

    # Intentar extraer artista y canción del nombre del archivo
    # Formato esperado: "Artista - Canción.mp3" o "Canción - Artista.mp3"
    if " - " in nombre_sin_extension:
        partes = nombre_sin_extension.split(" - ")
        if len(partes) >= 2:
            # Tomar la última parte como artista (más común)
            artista = partes[-1].strip()
            cancion = " - ".join(partes[:-1]).strip()
        else:
            artista = partes[0].strip()
            cancion = partes[1].strip()
    else:
        # Si no hay separador, usar el nombre completo como canción
        artista = "Unknown"
        cancion = nombre_sin_extension

    print(f"🎵 Buscando letras para: '{cancion}' de {artista}")
    print("=" * 60)

    # Primera opción: Intentar con LRCLIB
    if LRCLIB_AVAILABLE:
        print("🌐 OPCIÓN 1: LRCLIB (Letras sincronizadas reales)")
        print("   ✅ Timestamps reales de la música")
        print("   ✅ Sincronización perfecta")
        print("   ✅ Formato LRC estándar")
        print("-" * 40)
        letras_lrclib, fuente = obtener_letra_sincronizada_lrclib(cancion, artista)
        if letras_lrclib:
            print("🎉 ¡ÉXITO! Usando letras sincronizadas reales de LRCLIB")
            print("=" * 60)
            return letras_lrclib, fuente
        print("❌ LRCLIB no encontró letras para esta canción")
        print("-" * 40)
    else:
        print("⚠️ LRCLIB no disponible - Saltando a Audd.io")
        print("-" * 40)

    # Segunda opción: Audd.io (reconocimiento de audio)
    if not API_TOKEN:
        print("❌ Error: No se encontró el API_TOKEN. Revisa tu archivo .env.")
        return None

    print("🎤 OPCIÓN 2: Audd.io (Reconocimiento de audio)")
    print("   ⚠️ Timestamps simulados inteligentes")
    print("   ⚠️ Sincronización aproximada")
    print("   ⚠️ Basado en análisis del contenido")
    print("-" * 40)
    print(f"🎤 Enviando '{ruta_archivo_audio}' para reconocimiento...")

    data = {
        "return": "lyrics",
        "api_token": API_TOKEN,
    }

    try:
        with open(ruta_archivo_audio, "rb") as f:  # Abrimos el archivo en modo binario
            files = {"file": f}
            response = requests.post("https://api.audd.io/", data=data, files=files)

        response.raise_for_status()
        datos = response.json()

        # Log de la respuesta de la API
        log_api_response(
            endpoint="recognize_audio",
            request_data={"file": ruta_archivo_audio, "return": "lyrics"},
            response_data=datos,
            status="success" if datos.get("status") == "success" else "no_results",
        )
        print(f"📝 Respuesta guardada en el archivo de log: {LOG_FILE}")

        print("Respuesta completa de la API:")
        print(datos)

        if datos.get("status") == "success" and datos.get("result"):
            if datos["result"].get("lyrics"):
                print("🎉 ¡ÉXITO! Letras encontradas con Audd.io")
                print("⚠️ NOTA: Usando timestamps simulados inteligentes")
                print("=" * 60)
                lyrics_data = datos["result"]["lyrics"]
                print(f"Tipo de datos de letra: {type(lyrics_data)}")

                # Si las letras vienen como string, las convertimos a una lista simple
                # para que el karaoke funcione (sin timestamps)
                if isinstance(lyrics_data, str):
                    print(
                        "⚠️ Advertencia: Las letras vienen como texto plano, sin timestamps."
                    )
                    print("El karaoke mostrará las líneas con timestamps inteligentes.")
                    lines = [
                        line.strip() for line in lyrics_data.split("\n") if line.strip()
                    ]
                    # Crear timestamps inteligentes basados en el contenido
                    return crear_timestamps_inteligentes(lines), "AUDD"
                elif isinstance(lyrics_data, list):
                    print("Formato: lista de diccionarios")
                    return lyrics_data, "AUDD"
                elif isinstance(lyrics_data, dict) and "lyrics" in lyrics_data:
                    print("Formato: diccionario con clave 'lyrics'")
                    lyrics_text = lyrics_data["lyrics"]
                    if isinstance(lyrics_text, str):
                        print(
                            "⚠️ Advertencia: Las letras vienen como texto plano, sin timestamps."
                        )
                        print(
                            "El karaoke mostrará las líneas con timestamps inteligentes."
                        )
                        lines = [
                            line.strip()
                            for line in lyrics_text.split("\n")
                            if line.strip()
                        ]
                        # Crear timestamps inteligentes basados en el contenido
                        return crear_timestamps_inteligentes(lines), "AUDD"
                    else:
                        return lyrics_text, "AUDD"
                else:
                    print("Formato de letra no reconocido:", type(lyrics_data))
                    print("Contenido:", lyrics_data)
                    return None, None

        print("❌ No se encontró letra sincronizada para esta canción.")
        print("Respuesta de la API:", datos)
        return None, None

    except FileNotFoundError:
        print(
            f"❌ Error: El archivo de audio '{ruta_archivo_audio}' no fue encontrado."
        )
        # Log del error
        log_api_response(
            endpoint="recognize_audio",
            request_data={"file": ruta_archivo_audio, "return": "lyrics"},
            response_data={"error": f"File not found: {ruta_archivo_audio}"},
            status="file_not_found",
        )
        return None, None
    except Exception as e:
        print(f"❌ Ocurrió un error al procesar el audio: {e}")
        # Log del error
        log_api_response(
            endpoint="recognize_audio",
            request_data={"file": ruta_archivo_audio, "return": "lyrics"},
            response_data={"error": str(e)},
            status="processing_error",
        )
        return None, None
