import machine
import time

# Configurar el pin ADC donde conectaste el LM35 (GP28 - ADC2)
adc = machine.ADC(28)  

while True:
    lectura = adc.read_u16()  # Leer ADC (valor entre 0 y 65535)
    voltaje = lectura * (3.3 / 65535)  # Convertir a voltaje (0-3.3V)
    temperatura = voltaje * 100  # LM35 da 10mV/°C, por lo que 1V = 100°C
    print(f"Temperatura: {temperatura:.2f} °C")
    time.sleep(2)  # Leer cada 2 segundos
