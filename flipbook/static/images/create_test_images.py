from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def create_test_image(number, width=1000, height=800):
    # Créer une image avec un fond coloré
    colors = ["lightblue", "lightgreen", "lightpink"]
    img = Image.new("RGB", (width, height), colors[number % len(colors)])
    draw = ImageDraw.Draw(img)

    # Ajouter du texte
    text = f"Page {number + 1}"
    # Utiliser une police par défaut car les polices système peuvent varier
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()

    # Centrer le texte
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    # Dessiner le texte
    draw.text((x, y), text, fill="black", font=font)
    return img


def main():
    # Créer le dossier static/images s'il n'existe pas
    image_dir = Path(__file__).parent / "flipbook" / "static" / "images"
    image_dir.mkdir(parents=True, exist_ok=True)

    # Créer 3 images de test
    for i in range(3):
        img = create_test_image(i)
        img.save(image_dir / f"page{i+1}.jpg")
        print(f"Created test image: page{i+1}.jpg")


if __name__ == "__main__":
    main()
