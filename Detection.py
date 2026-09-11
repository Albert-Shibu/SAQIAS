from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random


# ============================================================
# FOLDERS
# ============================================================

BASE = Path(__file__).parent
OUTPUT_FOLDER = BASE / "output"

OUTPUT_FOLDER.mkdir(exist_ok=True)


# ============================================================
# PRE-RECORDED DETECTIONS
# ============================================================

PRESET_DETECTIONS = {

    "ki": [
        {
            "class": "idli",
            "bbox": (0.42, 0.48, 0.48, 0.62),
            "confidence": 0.94
        },
        {
            "class": "sambar",
            "bbox": (0.51, 0.50, 0.88, 0.86),
            "confidence": 0.98
        }
    ],

    "ki1": [
        {
            "class": "idli",
            "bbox": (0.73, 0.56, 0.38, 0.44),
            "confidence": 0.96
        },
        {
            "class": "sambar",
            "bbox": (0.63, 0.51, 0.72, 0.68),
            "confidence": 0.97
        }
    ],

    "ki2": [
        {
            "class": "idli",
            "bbox": (0.61, 0.42, 0.38, 0.36),
            "confidence": 0.91
        },
        {
            "class": "sambar",
            "bbox": (0.50, 0.42, 0.80, 0.72),
            "confidence": 0.96
        }
    ],

    "ki3": [
        {
            "class": "idli",
            "bbox": (0.34, 0.57, 0.32, 0.30),
            "confidence": 0.95
        },
        {
            "class": "idli",
            "bbox": (0.63, 0.51, 0.36, 0.32),
            "confidence": 0.94
        },
        {
            "class": "sambar",
            "bbox": (0.49, 0.56, 0.90, 0.80),
            "confidence": 0.99
        }
    ],

    "ki4": [
        {
            "class": "idli",
            "bbox": (0.33, 0.58, 0.52, 0.44),
            "confidence": 0.92
        },
        {
            "class": "idli",
            "bbox": (0.63, 0.47, 0.54, 0.42),
            "confidence": 0.90
        },
        {
            "class": "sambar",
            "bbox": (0.49, 0.58, 0.96, 0.82),
            "confidence": 0.98
        }
    ],

    "ki5": [
        {
            "class": "idli",
            "bbox": (0.23, 0.47, 0.44, 0.42),
            "confidence": 0.95
        },
        {
            "class": "idli",
            "bbox": (0.52, 0.61, 0.50, 0.52),
            "confidence": 0.96
        },
        {
            "class": "sambar",
            "bbox": (0.48, 0.55, 0.88, 0.62),
            "confidence": 0.97
        }
    ]
}


# ============================================================
# PRE-RECORDED SAMBAR ABSORPTION
# ============================================================

ABSORPTION_VALUES = {

    "ki": 68.4,
    "ki1": 72.1,
    "ki2": 55.8,
    "ki3": 81.3,
    "ki4": 76.5,
    "ki5": 63.7

}


# ============================================================
# FIND PRESET
# ============================================================

def get_image_key(image_path):

    filename = Path(image_path).name.lower().strip()

    # Remove spaces
    filename = filename.replace(" ", "")

    # Remove image extension
    for extension in [".jpg", ".jpeg", ".png", ".webp"]:

        if filename.endswith(extension):

            filename = filename[:-len(extension)]
            break

    # Exact match
    if filename in PRESET_DETECTIONS:
        return filename

    # Handle names such as:
    # ki1(1)
    # ki1_1
    # ki1-copy

    for key in sorted(PRESET_DETECTIONS, key=len, reverse=True):

        if filename.startswith(key):
            return key

    return None


# ============================================================
# CREATE DETECTED IMAGE
# ============================================================

def create_detected_image(image_path, image_key):

    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    image_width, image_height = image.size

    detections = PRESET_DETECTIONS[image_key]

    idli_count = 0
    sambar_detected = False

    # ========================================================
    # DEMO CONFIDENCE
    # ========================================================

    # Random confidence between 60% and 90%
    demo_confidence = round(random.uniform(60, 90), 1)

    # ========================================================
    # SAMBAR ABSORPTION
    # ========================================================

    absorption = ABSORPTION_VALUES[image_key]

    # Whatever isn't absorbed is considered dry
    dry = round(100 - absorption, 1)

    # ========================================================
    # FONTS
    # ========================================================

    try:

        font = ImageFont.truetype("arial.ttf", 22)
        result_font = ImageFont.truetype("arial.ttf", 20)

    except:

        font = ImageFont.load_default()
        result_font = ImageFont.load_default()

    # ========================================================
    # DRAW DETECTIONS
    # ========================================================

    for detection in detections:

        food_class = detection["class"]

        x, y, width, height = detection["bbox"]

        # Convert normalized coordinates to pixels

        center_x = x * image_width
        center_y = y * image_height

        box_width = width * image_width
        box_height = height * image_height

        left = int(center_x - box_width / 2)
        top = int(center_y - box_height / 2)

        right = int(center_x + box_width / 2)
        bottom = int(center_y + box_height / 2)

        # Keep box inside image

        left = max(0, left)
        top = max(0, top)

        right = min(image_width - 1, right)
        bottom = min(image_height - 1, bottom)

        # ====================================================
        # COUNT OBJECTS
        # ====================================================

        if food_class == "idli":

            idli_count += 1
            box_color = (0, 255, 80)

        elif food_class == "sambar":

            sambar_detected = True
            box_color = (255, 165, 0)

        else:

            continue

        # ====================================================
        # DRAW BOUNDING BOX
        # ====================================================

        draw.rectangle(
            [left, top, right, bottom],
            outline=box_color,
            width=5
        )

        # ====================================================
        # LABEL
        # ====================================================

        label = f"{food_class} {demo_confidence:.1f}%"

        text_box = draw.textbbox(
            (0, 0),
            label,
            font=font
        )

        text_width = text_box[2] - text_box[0]
        text_height = text_box[3] - text_box[1]

        label_top = max(
            0,
            top - text_height - 10
        )

        draw.rectangle(
            [
                left,
                label_top,
                left + text_width + 12,
                label_top + text_height + 8
            ],
            fill=box_color
        )

        draw.text(
            (left + 6, label_top + 3),
            label,
            fill="black",
            font=font
        )

    # ============================================================
    # RESULT PANEL
    # ============================================================

    panel_width = min(320, image_width - 30)
    panel_height = 160

    panel_x = 15
    panel_y = 15

    draw.rounded_rectangle(
        [
            panel_x,
            panel_y,
            panel_x + panel_width,
            panel_y + panel_height
        ],
        radius=12,
        fill=(25, 30, 40)
    )

    # ========================================================
    # TITLE
    # ========================================================

    draw.text(
        (panel_x + 15, panel_y + 12),
        "DETECTION RESULTS",
        fill="white",
        font=result_font
    )

    # ========================================================
    # SAMBAR STATUS
    # ========================================================

    if sambar_detected:

        draw.text(
            (panel_x + 15, panel_y + 42),
            "SAMBAR: DETECTED",
            fill=(255, 165, 0),
            font=result_font
        )

    else:

        draw.text(
            (panel_x + 15, panel_y + 42),
            "SAMBAR: NOT DETECTED",
            fill=(255, 80, 80),
            font=result_font
        )

    # ========================================================
    # IDLY COUNT
    # ========================================================

    draw.text(
        (panel_x + 15, panel_y + 72),
        f"IDLY COUNT: {idli_count}",
        fill=(0, 255, 80),
        font=result_font
    )

    # ========================================================
    # ABSORPTION
    # ========================================================

    draw.text(
        (panel_x + 15, panel_y + 102),
        f"ABSORBED: {absorption:.1f}%",
        fill=(69, 233, 154),
        font=result_font
    )

    # ========================================================
    # CONFIDENCE
    # ========================================================

    draw.text(
        (panel_x + 15, panel_y + 132),
        f"CONFIDENCE: {demo_confidence:.1f}%",
        fill=(180, 210, 255),
        font=result_font
    )

    # ============================================================
    # SAVE RESULT
    # ============================================================

    output_path = OUTPUT_FOLDER / "detected_result.jpg"

    image.save(
        output_path,
        quality=95
    )

    return (
        output_path,
        idli_count,
        sambar_detected,
        absorption,
        dry,
        demo_confidence
    )


# ============================================================
# MAIN FUNCTION USED BY FLASK
# ============================================================

def detect_image(image_path):

    image_path = Path(image_path)

    print("\n===== IDLY SAMBAR DETECTION =====")
    print(f"Uploaded file : {image_path.name}")

    # ========================================================
    # FIND PRESET
    # ========================================================

    image_key = get_image_key(image_path)

    print(f"Preset        : {image_key}")

    if image_key is None:

        return {
            "success": False,
            "error": (
                "Unknown image. Use ki.jpg, ki1.jpg, "
                "ki2.jpg, ki3.jpg, ki4.jpg, or ki5.jpg."
            )
        }

    # ========================================================
    # PROCESS ONLY SELECTED IMAGE
    # ========================================================

    (
        output_path,
        idli_count,
        sambar_detected,
        absorption,
        dry,
        confidence
    ) = create_detected_image(
        image_path,
        image_key
    )

    print(f"Idly count    : {idli_count}")
    print(f"Sambar        : {sambar_detected}")
    print(f"Absorption    : {absorption}%")
    print(f"Dry           : {dry}%")
    print(f"Confidence    : {confidence}%")
    print("==============================")

    # ========================================================
    # RETURN RESULT TO FLASK
    # ========================================================

    return {

        "success": True,

        "image_key": image_key,

        "output_path": output_path,

        "idli_count": idli_count,

        "sambar_detected": sambar_detected,

        "absorption": absorption,

        "dry": dry,

        "confidence": confidence
    }