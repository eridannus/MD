from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import os
import time

# Inicializa el I2C y la pantalla OLED
i2c = I2C(0, sda=Pin(0), scl=Pin(1))
oled = SSD1306_I2C(128, 64, i2c)

# Invierte los colores
oled.invert(False)

# Funciones para voltear la pantalla
def flip_horizontal(oled, flip):
    if flip:
        oled.write_cmd(0xA1)  # Volteo horizontal
    else:
        oled.write_cmd(0xA0)  # Orientación horizontal normal

def flip_vertical(oled, flip):
    if flip:
        oled.write_cmd(0xC8)  # Volteo vertical
    else:
        oled.write_cmd(0xC0)  # Orientación vertical normal

# Configura las opciones de volteo
voltear_horizontal = False  # Cambia a True para voltear horizontalmente
voltear_vertical = False    # Cambia a True para voltear verticalmente

# Aplica las configuraciones de volteo
flip_horizontal(oled, voltear_horizontal)
flip_vertical(oled, voltear_vertical)

# Función para extraer el número de frame del nombre del archivo
def extract_frame_number(filename):
    name_part = filename[len('frame_'):-len('.bin')]
    return int(name_part)

# Obtiene y ordena la lista de archivos de frames
frame_files = [f for f in os.listdir() if f.startswith('frame_') and f.endswith('.bin')]
frame_files.sort(key=extract_frame_number)  # Ordena numéricamente

while True:
    for frame_file in frame_files:
        with open(frame_file, 'rb') as f:
            frame_data = f.read()
        # Convertir frame_data a bytearray
        fb = framebuf.FrameBuffer(bytearray(frame_data), 128, 64, framebuf.MONO_HLSB)
        oled.fill(0)
        oled.blit(fb, 0, 0)
        oled.show()
        time.sleep(0.1)  # Ajusta el retraso según sea necesario