from machine import Pin, PWM
import time

# Configura el pin del buzzer como una salida de PWM
buzzer = PWM(Pin(5))

# Configuración de los botones
buttons = {
    28: Pin(28, Pin.IN, Pin.PULL_UP),
    22: Pin(22, Pin.IN, Pin.PULL_UP),
    21: Pin(21, Pin.IN, Pin.PULL_UP),
    18: Pin(18, Pin.IN, Pin.PULL_UP)
}

# Frecuencias de las notas (en Hz)
tones = {
    'C4': 261,
    'D4': 294,
    'E4': 329,
    'F4': 349,
    'G4': 392,
    'A4': 440,
    'B4': 493,
    'C5': 523,
    'D5': 587,
    'E5': 659,
    'F5': 698,
    'G5': 784,
    'A5': 880,
    'B5': 987,
    'C6': 1046,
    'D6': 1174,
    'E6': 1318,
    'F6': 1396,
    'G6': 1567,
    'A6': 1760,
    'B6': 1975,
    'C7': 2093,
    'P': 0  # Pausa
}

# Melodías
melodies = {
    28: [  # Kirby - Gourmet Race
        ('C5', 0.2), ('D5', 0.2), ('E5', 0.2), ('G5', 0.2), ('C6', 0.2),
        ('C6', 0.1), ('B5', 0.1), ('A5', 0.1), ('G5', 0.2), ('F5', 0.2), 
        ('E5', 0.2), ('F5', 0.2), ('G5', 0.2), ('A5', 0.2), ('C6', 0.2), 
        ('P', 0.2), ('A5', 0.1), ('B5', 0.1), ('C6', 0.2), ('D6', 0.2),
        ('C6', 0.2), ('B5', 0.2), ('A5', 0.2), ('G5', 0.2), ('F5', 0.2),
        ('E5', 0.2), ('D5', 0.2), ('C5', 0.2)
    ],
    22: [  # Mario Bros
        ('E5', 0.2), ('E5', 0.2), ('P', 0.2), ('E5', 0.2), ('P', 0.2), 
        ('C5', 0.2), ('E5', 0.2), ('G5', 0.2), ('P', 0.2), ('G4', 0.2),
        ('P', 0.2), ('C5', 0.2), ('G4', 0.2), ('P', 0.2), ('E4', 0.2),
        ('A4', 0.2), ('B4', 0.2), ('A4', 0.2), ('A4', 0.2), ('G4', 0.2),
        ('E4', 0.2), ('P', 0.2), ('E5', 0.2), ('C5', 0.2), ('G4', 0.2)
    ],
    21: [  # Zelda
        ('E4', 0.2), ('G4', 0.2), ('A4', 0.2), ('P', 0.2), ('A4', 0.2),
        ('G4', 0.2), ('E4', 0.2), ('C4', 0.2), ('P', 0.2), ('E4', 0.2),
        ('G4', 0.2), ('A4', 0.2), ('P', 0.2), ('A4', 0.2), ('G4', 0.2),
        ('E4', 0.2), ('C4', 0.2), ('P', 0.2), ('C4', 0.2), ('D4', 0.2),
        ('E4', 0.2), ('P', 0.2), ('E4', 0.2), ('D4', 0.2), ('C4', 0.2)
    ],
    18: [  # Kirby - Candy Mountain
        ('C5', 0.2), ('E5', 0.2), ('G5', 0.2), ('C6', 0.2), ('E6', 0.2),
        ('G6', 0.2), ('C7', 0.2), ('P', 0.2), ('C7', 0.2), ('G6', 0.2),
        ('E6', 0.2), ('C6', 0.2), ('G5', 0.2), ('E5', 0.2), ('C5', 0.2),
        ('P', 0.2), ('C5', 0.2), ('D5', 0.2), ('E5', 0.2), ('G5', 0.2),
        ('C6', 0.2), ('E6', 0.2), ('G6', 0.2), ('C7', 0.2), ('P', 0.2)
    ]
}

# Variable para controlar la interrupción de la melodía
current_button = None
stop_playing = False  # Variable para detener la canción actual

# Función para reproducir la melodía con interrupción
def play_melody(melody, pin):
    global current_button, stop_playing
    stop_playing = False  # Resetear la variable de detener

    for note, duration in melody:
        if stop_playing:  # Si se ha presionado otro botón, se interrumpe la reproducción
            break
        
        if note == 'P':  # Pausa
            time.sleep(duration)
        else:
            buzzer.freq(tones[note])  # Establece la frecuencia de la nota
            buzzer.duty_u16(32768)    # 50% duty cycle
            time.sleep(duration)
            buzzer.duty_u16(0)  # Detiene la nota
        
        time.sleep(0.02)  # Pausa mínima entre notas

        # Verificar si se presiona otro botón después de la nota
        if detect_button_press():  # Si se presiona otro botón, salir inmediatamente
            return

# Función para detectar si algún botón ha sido presionado
def detect_button_press():
    global current_button, stop_playing
    for new_pin, button in buttons.items():
        if button.value() == 0:  # Si se presiona cualquier botón
            if current_button != new_pin:  # Si es un botón diferente
                current_button = new_pin  # Cambia la melodía de inmediato
                stop_playing = True  # Detiene la melodía actual
                print(f"Button {new_pin} pressed, playing new theme.")
            return True
    return False

# Función principal para detectar la presión de los botones
def check_buttons():
    global current_button, stop_playing
    while True:
        if detect_button_press():  # Detectar si cualquier botón es presionado
            stop_playing = True  # Detiene la melodía actual
            time.sleep(0.05)  # Pequeña pausa para evitar múltiples activaciones rápidas
            play_melody(melodies[current_button], current_button)  # Reproducir la melodía correspondiente

# Ejecuta el bucle de detección de botones
check_buttons()