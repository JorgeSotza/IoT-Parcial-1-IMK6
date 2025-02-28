import network  # Librería para manejar la conexión Wi-Fi
import time  # Librería para manejar tiempos y pausas
import urequests  # Librería para hacer solicitudes HTTP a ThingSpeak
import machine  # Librería para manejar el hardware de la Raspberry Pi Pico W

# 🔹 Configuración de Wi-Fi
SSID = "Casa Pinos 2G"  # Nombre de la red Wi-Fi (SSID)
PASSWORD = "jsruz4040"   # Contraseña de la red Wi-Fi

# 🔹 Configuración de ThingSpeak
THINGSPEAK_API_KEY = "E1NSFB1YJ5X7LT4X"  # API Key para escribir en ThingSpeak
THINGSPEAK_URL = "https://api.thingspeak.com/update?api_key=E1NSFB1YJ5X7LT4X&field1=0"  # URL base para enviar datos a ThingSpeak

# 🔹 Configuración del sensor LM35
adc = machine.ADC(28)  # Configura el ADC en el pin GP28 (ADC2) para leer el sensor LM35

# 🔹 Función para conectar a Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)  # Configura la Wi-Fi en modo estación
    wlan.active(True)  # Activa la Wi-Fi
    if not wlan.isconnected():  # Si no está conectada
        print("Conectando a Wi-Fi...")
        wlan.connect(SSID, PASSWORD)  # Intenta conectar con las credenciales dadas
        tiempo_inicio = time.time()  # Guarda el tiempo de inicio de la conexión
        while not wlan.isconnected():  # Espera hasta que se conecte
            if time.time() - tiempo_inicio > 10:  # Si tarda más de 10 segundos
                print("❌ No se pudo conectar a Wi-Fi")  # Muestra error
                return False  # Retorna falso si no se conecta
            time.sleep(1)  # Espera 1 segundo antes de volver a intentar
    print("✅ Conectado a Wi-Fi:", wlan.ifconfig())  # Muestra la IP asignada
    return True  # Retorna verdadero si la conexión fue exitosa

# 🔹 Función para leer el LM35 y enviar datos a ThingSpeak
def enviar_a_thingspeak():
    while True:  # Bucle infinito para seguir enviando datos
        lectura = adc.read_u16()  # Lee el valor del ADC (0-65535)
        voltaje = lectura * (3.3 / 65535)  # Convierte el valor leído a voltaje (0-3.3V)
        temperatura = voltaje * 100  # Convierte el voltaje en temperatura (°C)

        print(f"🌡️ Temperatura: {temperatura:.2f} °C")  # Muestra la temperatura en la consola

        # Construye la URL con la temperatura medida
        url = f"{THINGSPEAK_URL}?api_key={THINGSPEAK_API_KEY}&field1={temperatura}"

        # Intenta enviar los datos a ThingSpeak
        try:
            respuesta = urequests.get(url)  # Hace la solicitud HTTP GET a ThingSpeak
            print(f"✅ Enviado a ThingSpeak: {respuesta.text}")  # Muestra la respuesta del servidor
            respuesta.close()  # Cierra la conexión HTTP
        except Exception as e:  # Captura cualquier error en la solicitud
            print(f"❌ Error al enviar datos: {e}")  # Muestra el error

        time.sleep(60)  # Espera 60 segundos antes de enviar el siguiente dato

# 🔹 Ejecutar el código principal
if connect_wifi():  # Si se conecta a Wi-Fi correctamente
    enviar_a_thingspeak()  # Comienza a leer la temperatura y enviarla a ThingSpeak
else:
    print("❌ No se pudo conectar a Wi-Fi")  # Muestra error si no hay conexión

