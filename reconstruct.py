from pathlib import Path
from sour import Sour
from tqdm import tqdm

folder_path = Path("D:/spotify_dataset/audio")
output_dir = Path("D:/spotify_dataset/image_noise")
output_dir.mkdir(parents=True, exist_ok=True)

sr = Sour()
all_files = list(folder_path.iterdir())
for file in tqdm(all_files):
    save_path = output_dir / file.stem
    sr.audio_to_image(
        file_path=file,
        save_as=save_path,
        max_size=640,
        fill=True
    )
