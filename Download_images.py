from pathlib import Path

import requests


def download_training_images(num_images=100):
    folder = Path("training_images")
    folder.mkdir(exist_ok=True)

    print(f"מתחיל להוריד {num_images} תמונות... זה עשוי לקחת רגע.")
    for i in range(1, num_images + 1):
        try:
            # הורדת תמונה אקראית בנושאי טבע/חפצים
            img_url = f"https://picsum.photos/200/200?random={i}"
            img_data = requests.get(img_url).content
            with open(folder / f"img_{i}.png", 'wb') as f:
                f.write(img_data)
            if i % 10 == 0: print(f"הורדו {i} תמונות...")
        except Exception as e:
            print(f"שגיאה בהורדת תמונה {i}: {e}")
    print("הורדה הושלמה! תיקיית 'training_images' מוכנה.")


if __name__ == "__main__":
    download_training_images()
