import machine
import utime

# Configura el pin 5 como una salida de PWM
buzzer = machine.PWM(machine.Pin(5))

# Frecuencias de las notas (en Hz)
tones = {
    'C': 261,
    'D': 294,
    'E': 329,
    'F': 349,
    'G': 392,
    'A': 440,
    'B': 493,
    'C_high': 523
}

# Melodía de "Twinkle Twinkle Little Star"
melody = [
    ('C', 0.5), ('C', 0.5), ('G', 0.5), ('G', 0.5),
    ('A', 0.5), ('A', 0.5), ('G', 1),
    ('F', 0.5), ('F', 0.5), ('E', 0.5), ('E', 0.5),
    ('D', 0.5), ('D', 0.5), ('C', 1)
]

def play_tone(note, duration):
    if note == 'P':  # 'P' for pause
        utime.sleep(duration)
    else:
        buzzer.freq(tones[note])
        buzzer.duty_u16(32768)  # 50% duty cycle
        utime.sleep(duration)
        buzzer.duty_u16(0)  # Stop the tone

# Reproducir la melodía
for note, duration in melody:
    play_tone(note, duration)
    utime.sleep(0.1)  # Pausa entre notas

# Detener el buzzer
buzzer.deinit()