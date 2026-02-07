import os

from PIL import Image, ImageDraw


def generate_colored_shapes():
    # יצירת התיקייה אם היא לא קיימת
    folder = "training_shapes"
    if not os.path.exists(folder):
        os.makedirs(folder)

    shapes = {
        "ellipse": {"color": "blue", "points": [10, 30, 190, 170]},
        "rectangle": {"color": "red", "points": [20, 40, 180, 160]},
        "pentagon": {"color": "green", "points": [(100, 10), (190, 80), (160, 180), (40, 180), (10, 80)]},
        "hexagon": {"color": "orange", "points": [(100, 10), (185, 55), (185, 145), (100, 190), (15, 145), (15, 55)]}
    }

    for name, data in shapes.items():
        # יצירת תמונה שקופה (RGBA)
        img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        if name == "ellipse":
            draw.ellipse(data["points"], fill=data["color"], outline="black", width=3)
        elif name == "rectangle":
            draw.rectangle(data["points"], fill=data["color"], outline="black", width=3)
        else:  # פוליגונים (מחומש ומשושה)
            draw.polygon(data["points"], fill=data["color"], outline="black", width=3)

        # שמירה כ-PNG (חשוב לשקיפות)
        img.save(os.path.join(folder, f"{name}.png"))
        print(f"נוצר קובץ: {name}.png בתיקיית {folder}")


if __name__ == "__main__":
    generate_colored_shapes()
