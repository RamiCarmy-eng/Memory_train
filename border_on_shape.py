from pathlib import Path

from PIL import Image, ImageFilter


def apply_border_to_shape(image_path, border_color=(100, 100, 100), width=3):
    """מוסיף מסגרת לקווי המתאר של הצורה עצמה"""
    with Image.open(image_path) as img:
        img = img.convert("RGBA")

        # הפרדת ערוץ האלפא (שקיפות) - אם אין שקיפות, נתייחס ללבן כאל שקיפות
        alpha = img.split()[3]

        # אם התמונה אטומה לגמרי (לבנה), נהפוך את הלבן לשקיפות כדי למצוא את הצורה
        if alpha.getextrema() == (255, 255):
            # הפיכת כל מה שקרוב ללבן לשקוף
            grayscale = img.convert("L")
            alpha = grayscale.point(lambda x: 255 if x < 250 else 0)
            img.putalpha(alpha)

        # יצירת מסיכה של קווי המתאר
        # אנחנו מרחיבים את הצורה מעט ואז מחסירים את המקור
        edge = alpha.filter(ImageFilter.MaxFilter(width * 2 + 1))

        # יצירת תמונה חדשה למסגרת
        new_img = Image.new("RGBA", img.size, border_color + (0,))
        # הדבקת הצבע של המסגרת לפי המסיכה של הקצוות
        result = Image.composite(Image.new("RGBA", img.size, border_color + (255,)), img, edge)

        # הדבקת התמונה המקורית מעל המסגרת
        final = Image.alpha_composite(result, img)

        # שמירה כ-PNG (כדי לשמור על השקיפות והמסגרת)
        final.save(image_path, "PNG")


def process_all():
    folders = [Path.cwd() / "training_shapes", Path.cwd() / "training_images"]
    for folder in folders:
        if not folder.exists(): continue
        print(f"מעבד צורות בתיקייה: {folder.name}")
        for f in list(folder.glob("*.png")) + list(folder.glob("*.jpg")):
            apply_border_to_shape(f)
            print(f"בוצע: {f.name}")


if __name__ == "__main__":
    process_all()
