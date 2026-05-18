from PIL import Image
import sys
import os

def extract_frames(gif_path):
    frames = []
    with Image.open(gif_path) as im:
        for frame_index in range(im.n_frames):
            im.seek(frame_index)
            frame = im.convert('1')  # Convertir a monocromático
            frame = frame.resize((128, 64))
            frames.append(frame)
    return frames

def save_frames_to_files(frames):
    if not os.path.exists('frames'):
        os.makedirs('frames')
    total_frames = len(frames)
    padding_width = len(str(total_frames - 1))  # Calcula el ancho del padding
    for idx, frame in enumerate(frames):
        # Transponer la imagen si es necesario
        frame = frame.transpose(Image.FLIP_TOP_BOTTOM)
        # Obtener los datos en el formato adecuado
        frame_data = frame.tobytes()
        # Formatear el índice con ceros a la izquierda
        idx_str = str(idx).zfill(padding_width)
        filename = os.path.join('frames', f'frame_{idx_str}.bin')
        with open(filename, 'wb') as f:
            f.write(frame_data)
    print(f"Se han guardado {len(frames)} frames en la carpeta 'frames'.")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python gif_to_files.py /ruta/al/gif")
        sys.exit(1)

    gif_path = sys.argv[1]

    frames = extract_frames(gif_path)
    save_frames_to_files(frames)
