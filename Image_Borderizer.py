from pathlib import Path

from PIL import Image, ImageOps


def add_border_to_folders():
    # הגדרת התיקיות
    folders = [
        Path.cwd() / "training_shapes",
        Path.cwd() / "training_images"
    ]

    border_color = (100, 100, 100)  # אפור כהה (כדי שייראה גם על לבן וגם על שחור)
    border_width = 4  # עובי המסגרת בפיקסלים

    for folder in folders:
        if not folder.exists():
            print(f"התיקייה {folder.name} לא קיימת, מדלג...")
            continue

        print(f"מתחיל לעבוד על תיקיית: {folder.name}")

        # עובר על כל קבצי התמונות
        for img_path in list(folder.glob("*.png")) + list(folder.glob("*.jpg")):
            try:
                with Image.open(img_path) as img:
                    # המרה ל-RGBA כדי לוודא תמיכה בשקיפות אם יש
                    img = img.convert("RGBA")

                    # הוספת מסגרת (מצמצם את התמונה המקורית מעט ומוסיף מסגרת מסביב)
                    bordered_img = ImageOps.expand(img, border=border_width, fill=border_color)

                    # שמירה מחדש באותו נתיב
                    bordered_img.save(img_path)
                    print(f"עובד: {img_path.name}")
            except Exception as e:
                print(f"שגיאה בעיבוד {img_path.name}: {e}")

    print("\nסיימתי! כל התמונות עכשיו עם מסגרת קבועה.")


if __name__ == "__main__":
    # ודא שהתקנת את Pillow בעזרת: pip install Pillow
    add_border_to_folders()
