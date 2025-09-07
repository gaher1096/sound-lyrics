import os
import time
from lyrics_finder import obtener_letra, obtener_letra_sincronizada

# Colores para la terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Ruta a la carpeta de canciones
SONGS_FOLDER = "sounds"


def listar_canciones() -> list[str]:
    """
    Lista los archivos MP3 en la carpeta 'songs'.
    Devuelve una lista de nombres de archivo.
    """
    canciones_disponibles = []
    if not os.path.exists(SONGS_FOLDER):
        os.makedirs(SONGS_FOLDER)  # Crea la carpeta si no existe
        print(f"Carpeta '{SONGS_FOLDER}' creada. Coloca tus archivos de audio aquí.")
        return []

    for archivo in os.listdir(SONGS_FOLDER):
        if archivo.endswith((".mp3", ".wav", ".flac", ".ogg")):  # Acepta varios formatos
            canciones_disponibles.append(archivo)

    return canciones_disponibles


def simular_karaoke(letra_sincronizada: list, nombre_cancion: str = "Canción", fuente_api: str = "Desconocida"):
    """
    Recibe la lista de letras con timestamps y las muestra en tiempo real.
    """
    if not letra_sincronizada:
        print("No hay letra sincronizada para mostrar.")
        return

    # Verificar el formato de los datos
    if not isinstance(letra_sincronizada, list):
        print(f"Error: Se esperaba una lista, pero se recibió {type(letra_sincronizada)}")
        return

    if len(letra_sincronizada) > 0:
        primera_linea = letra_sincronizada[0]
        if not isinstance(primera_linea, dict):
            print(f"Error: Se esperaba una lista de diccionarios, pero el primer elemento es {type(primera_linea)}")
            print(f"Contenido del primer elemento: {primera_linea}")
            return

        if 'text' not in primera_linea or 'timestamp' not in primera_linea:
            print(f"Error: Los diccionarios deben contener 'text' y 'timestamp'. Claves encontradas: {list(primera_linea.keys())}")
            return

    print("\n🎤 ¡Empezando karaoke en 3 segundos! 🎤\n")
    time.sleep(3)

    # Limpia la consola una sola vez al inicio
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}🎤 KARAOKE - {nombre_cancion} 🎤{Colors.END}")
    print(f"{Colors.CYAN}{'='*70}{Colors.END}")

    # Mostrar información de la fuente de datos
    if fuente_api == "LRCLIB":
        print(f"{Colors.GREEN}🌐 Fuente: LRCLIB - Letras sincronizadas reales{Colors.END}")
        print(f"{Colors.GREEN}✅ Timestamps reales de la música{Colors.END}")
        print(f"{Colors.CYAN}✨ Efecto de escritura activado{Colors.END}")
    elif fuente_api == "AUDD":
        print(f"{Colors.YELLOW}🎤 Fuente: Audd.io - Reconocimiento de audio{Colors.END}")
        print(f"{Colors.YELLOW}⚠️ Timestamps simulados inteligentes{Colors.END}")
        print(f"{Colors.WHITE}📝 Visualización directa{Colors.END}")
    else:
        print(f"{Colors.WHITE}📝 Fuente: {fuente_api}{Colors.END}")

    print(f"{Colors.CYAN}{'─'*70}{Colors.END}")
    print(f"{Colors.GREEN}🎵 ¡Canta junto con la música! 🎵{Colors.END}")
    print(f"{Colors.CYAN}{'─'*70}{Colors.END}")

    for i, linea in enumerate(letra_sincronizada):
        # Efecto de escritura progresiva para la línea actual
        texto_linea = linea['text']
        
        # Verificar si es un título de sección (entre corchetes) y omitirlo
        if texto_linea.startswith('[') and texto_linea.endswith(']'):
            # Saltar títulos de sección sin mostrarlos
            continue
        
        # Mostrar la línea con o sin efecto de escritura según la fuente
        if fuente_api == "LRCLIB":
            # Efecto de escritura para letras sincronizadas reales
            print("\n", end="", flush=True)
            
            # Efecto de escritura carácter por carácter con velocidad rápida
            for char in texto_linea:
                print(char, end="", flush=True)
                if char == ' ':
                    time.sleep(0.02)  # Pausa muy corta en espacios
                elif char in '.,!?':
                    time.sleep(0.05)  # Pausa corta en puntuación
                else:
                    time.sleep(0.01)  # Pausa mínima entre caracteres
            
            print()  # Nueva línea al final
        else:
            # Mostrar directamente para timestamps simulados
            print(f"\n{Colors.WHITE}{Colors.BOLD}{texto_linea}{Colors.END}")

        # Calcula cuánto tiempo esperar hasta la siguiente línea usando timestamps reales
        if i + 1 < len(letra_sincronizada):
            try:
                # Usar los timestamps reales de la API
                ts_actual_str = linea['timestamp']
                ts_siguiente_str = letra_sincronizada[i + 1]['timestamp']

                # Convertir timestamps a segundos
                def parse_timestamp_to_seconds(ts_str):
                    # Formato: HH:MM:SS.fff o MM:SS.fff
                    parts = ts_str.split(':')
                    if len(parts) == 3:  # HH:MM:SS.fff
                        h, m, s_f = parts
                        h, m = int(h), int(m)
                    elif len(parts) == 2:  # MM:SS.fff
                        h = 0
                        m, s_f = parts
                        m = int(m)
                    else:
                        raise ValueError(f"Formato de timestamp inesperado: {ts_str}")

                    s, f = s_f.split('.')
                    s, f = int(s), float(f) / 1000.0
                    return h * 3600 + m * 60 + s + f

                segundos_actual = parse_timestamp_to_seconds(ts_actual_str)
                segundos_siguiente = parse_timestamp_to_seconds(ts_siguiente_str)

                pausa = max(3.0, segundos_siguiente - segundos_actual)  # Mínimo 3 segundos, máximo 15 segundos
                pausa = min(15.0, pausa)  # Evitar pausas demasiado largas
                time.sleep(pausa)

            except Exception as e:
                # Si hay error con timestamps, usar tiempo fijo como respaldo
                print(f"Error con timestamp, usando tiempo fijo: {e}")
                time.sleep(6)  # 6 segundos como respaldo
        else:
            # Final de la canción
            print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
            print(f"{Colors.BOLD}{Colors.GREEN}🎉 ¡CANCIÓN TERMINADA! 🎉{Colors.END}")
            print(f"{Colors.YELLOW}¡Gracias por cantar con nosotros!{Colors.END}")
            print(f"{Colors.CYAN}{'='*70}{Colors.END}")
            time.sleep(3)  # Pausa al final de la canción


def mostrar_menu():
    print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}🎶 BUSCADOR DE LETRAS Y KARAOKE 🎶{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"\n{Colors.WHITE}{Colors.BOLD}📋 OPCIONES DISPONIBLES:{Colors.END}")
    print(f"{Colors.GREEN}1.{Colors.END} 🔍 Buscar letra de canción (texto)")
    print(f"{Colors.BLUE}2.{Colors.END} 🎤 Iniciar Karaoke (con archivo de audio)")
    print(f"{Colors.RED}3.{Colors.END} ❌ Salir del programa")
    print(f"\n{Colors.CYAN}{'─'*60}{Colors.END}")
    return input(f"{Colors.YELLOW}👉 Elige una opción (1-3): {Colors.END}")


def mostrar_submenu_karaoke():
    """Submenú para la opción de karaoke"""
    while True:
        print(f"\n{Colors.BLUE}{'='*50}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}🎤 MODO KARAOKE 🎤{Colors.END}")
        print(f"{Colors.BLUE}{'='*50}{Colors.END}")

        canciones = listar_canciones()
        if not canciones:
            print(f"{Colors.RED}❌ No hay archivos de audio en la carpeta 'sounds'.{Colors.END}")
            print(f"{Colors.YELLOW}💡 Coloca archivos MP3, WAV, FLAC o OGG en la carpeta 'sounds' y vuelve a intentar.{Colors.END}")
            return None

        print(f"\n{Colors.WHITE}{Colors.BOLD}🎵 CANCIONES DISPONIBLES:{Colors.END}")
        for i, cancion_file in enumerate(canciones):
            print(f"{Colors.GREEN}{i + 1:2d}.{Colors.END} 🎶 {cancion_file}")

        print(f"\n{Colors.CYAN}0.{Colors.END} ⬅️ Volver al menú principal")
        print(f"{Colors.RED}9.{Colors.END} ❌ Salir del programa")
        print(f"\n{Colors.BLUE}{'─'*50}{Colors.END}")

        try:
            seleccion = input(f"{Colors.YELLOW}👉 Elige una opción: {Colors.END}")

            if seleccion == '0':
                return 'back'
            elif seleccion == '9':
                return 'exit'
            else:
                seleccion_num = int(seleccion)
                if 1 <= seleccion_num <= len(canciones):
                    return canciones[seleccion_num - 1]
                else:
                    print(f"{Colors.RED}❌ Selección inválida. Intenta de nuevo.{Colors.END}")
        except ValueError:
            print(f"{Colors.RED}❌ Entrada inválida. Por favor, ingresa un número.{Colors.END}")

def main():
    print(f"{Colors.BOLD}{Colors.PURPLE}🎶 ¡Bienvenido al Buscador de Letras y Karaoke! 🎶{Colors.END}")

    while True:
        opcion = mostrar_menu()

        if opcion == '1':
            print(f"\n{Colors.GREEN}{'='*50}{Colors.END}")
            print(f"{Colors.BOLD}{Colors.CYAN}🔍 BÚSQUEDA DE LETRAS{Colors.END}")
            print(f"{Colors.GREEN}{'='*50}{Colors.END}")

            cancion = input(f"{Colors.YELLOW}🎵 Ingresa el nombre de la canción: {Colors.END}")
            artista = input(f"{Colors.YELLOW}👤 Ingresa el nombre del artista: {Colors.END}")

            if cancion and artista:
                obtener_letra(nombre_cancion=cancion, nombre_artista=artista)
            else:
                print(f"{Colors.RED}❌ Debes ingresar tanto el nombre de la canción como el del artista.{Colors.END}")

        elif opcion == '2':
            while True:
                resultado = mostrar_submenu_karaoke()

                if resultado == 'back':
                    break
                elif resultado == 'exit':
                    print(f"\n{Colors.YELLOW}👋 ¡Hasta luego! ¡Gracias por usar el karaoke!{Colors.END}")
                    return
                elif resultado is None:
                    break
                else:
                    # Procesar la canción seleccionada
                    nombre_archivo_seleccionado = resultado
                    ruta_completa_audio = os.path.join(SONGS_FOLDER, nombre_archivo_seleccionado)

                    print(f"\n{Colors.CYAN}🔄 Procesando '{nombre_archivo_seleccionado}'...{Colors.END}")
                    letra_sincronizada, fuente_api = obtener_letra_sincronizada(ruta_completa_audio)

                    if letra_sincronizada:
                        print(f"\n{Colors.GREEN}✅ ¡Letra sincronizada encontrada!{Colors.END}")
                        print(f"{Colors.YELLOW}🎵 ¡IMPORTANTE! Reproduce manualmente '{nombre_archivo_seleccionado}' en tu reproductor ahora.{Colors.END}")
                        print(f"{Colors.CYAN}⏱️ El karaoke comenzará en 3 segundos...{Colors.END}")
                        time.sleep(3)
                        simular_karaoke(letra_sincronizada, nombre_archivo_seleccionado, fuente_api)

                        # Preguntar si quiere continuar
                        continuar = input(f"\n{Colors.YELLOW}¿Quieres elegir otra canción? (s/n): {Colors.END}").lower()
                        if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                            break
                    else:
                        print(f"{Colors.RED}❌ No se pudo obtener la letra sincronizada para esta canción.{Colors.END}")
                        input(f"{Colors.YELLOW}Presiona Enter para continuar...{Colors.END}")

        elif opcion == '3':
            print(f"\n{Colors.YELLOW}👋 ¡Hasta luego! ¡Gracias por usar el karaoke!{Colors.END}")
            break

        else:
            print(f"{Colors.RED}❌ Opción no válida. Intenta de nuevo.{Colors.END}")

        input(f"\n{Colors.CYAN}Presiona Enter para continuar...{Colors.END}")  # Pausa para ver el resultado


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma terminado.")