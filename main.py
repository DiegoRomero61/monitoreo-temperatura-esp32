import network
import urequests
import time
import dht
from machine import Pin


SSID = "Totalplay-1AA2"
PASSWORD = "1AA2197UTtNej9w"

sensor = dht.DHT22(Pin(4))
buzzer = Pin(15, Pin.OUT)

SERVER_URL = "http://192.168.100.100/insertar.php"

def conectar_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)

    while not wifi.isconnected():
        time.sleep(1)
    
    print("Conectado:", wifi.ifconfig())

def enviar_datos(temp, hum):
    try:
        data = {
            "temperatura": temp,
            "humedad": hum
        }
        r = urequests.post(SERVER_URL, json=data)
        r.close()
    except:
        print("Error enviando datos")

conectar_wifi()

while True:
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()

    print(temp, hum)
    
    if temp > 35:
        buzzer.on()
    else:
        buzzer.off()

    enviar_datos(temp, hum)

    time.sleep(5)
