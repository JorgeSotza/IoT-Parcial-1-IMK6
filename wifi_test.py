import network
import time
import urequests  # Librería para hacer solicitudes HTTP
import machine

# 🔹 Configuración de Wi-Fi
SSID = "Casa Pinos 2G"  # Reemplaza con el nombre de tu red
PASSWORD = "jsruz4040"   # Reemplaza con tu contraseña

# 🔹 Configuración de ThingSpeak
THINGSPEAK_API_KEY = "E1NSFB1YJ5X7LT4X"  # Reemplaza con tu API Key de escritura
THINGSPEAK_URL = "https://api.thingspeak.com/update?api_key=E1NSFB1YJ5X7LT4X&field1=0"

# 🔹 Configuración del sensor LM35
adc = machine.ADC(28)  # Usando GP28 (ADC2)

# 🔹 Función para conectar a Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando a Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        tiempo_inicio = time.time()
        while not wlan.isconnected():
            if time.time() - tiempo_inicio > 10:
                print("❌ No se pudo conectar a Wi-Fi")
                return False
            time.sleep(1)
    print("✅ Conectado a Wi-Fi:", wlan.ifconfig())
    return True

# 🔹 Función para leer el LM35 y enviar datos a ThingSpeak
def enviar_a_thingspeak():
    while True:
        lectura = adc.read_u16()  # Leer ADC (0-65535)
        voltaje = lectura * (3.3 / 65535)  # Convertir a voltaje (0-3.3V)
        temperatura = voltaje * 100  # Convertir a °C (LM35: 10mV/°C)
        
        print(f"🌡️ Temperatura: {temperatura:.2f} °C")

        # Crear la URL con los datos
        url = f"{THINGSPEAK_URL}?api_key={THINGSPEAK_API_KEY}&field1={temperatura}"

        # Enviar datos a ThingSpeak
        try:
            respuesta = urequests.get(url)
            print(f"✅ Enviado a ThingSpeak: {respuesta.text}")
            respuesta.close()
        except Exception as e:
            print(f"❌ Error al enviar datos: {e}")

        time.sleep(15)  # ThingSpeak permite envíos cada 15 segundos

# 🔹 Ejecutar el código
if connect_wifi():
    enviar_a_thingspeak()
else:
    print("❌ No se pudo conectar a Wi-Fi")
