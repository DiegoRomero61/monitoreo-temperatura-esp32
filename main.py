import network
import time
import urequests
from machine import Pin, I2C
import dht
import ssd1306

ssid = "ESP32test"
password = "12345678"

server_url = "http://192.168.100.120/insertar.php"

sensor = dht.DHT22(Pin(4)) 

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

if not wifi.isconnected():
    print("Conectando...")
    wifi.connect(ssid, password)

    timeout = 10
    while not wifi.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1

if wifi.isconnected():
    print("Conectado!")
    print(wifi.ifconfig())
else:
    print("Error de conexión WiFi")

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        print("Temp:", temp)
        print("Hum:", hum)

        oled.fill(0)
        oled.text("Temp: {:.1f} C".format(temp), 0, 10)
        oled.text("Hum: {:.1f} %".format(hum), 0, 30)

        if temp > 30:
            oled.text("ALERTA!", 0, 50)
        else:
            oled.text("Normal", 0, 50)

        oled.show()

        url = "{}?temp={}&hum={}".format(server_url, temp, hum)

        try:
            response = urequests.get(url)
            print("Enviado:", response.text)
            response.close()
        except Exception as e:
            print("Error envio:", e)

    except Exception as e:
        print("Error sensor:", e)

    time.sleep(5)
