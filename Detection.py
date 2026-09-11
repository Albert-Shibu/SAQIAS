from inference_sdk import InferenceHTTPClient, InferenceConfiguration
import json

ROBOFLOW_API_KEY = "lBeyq6Jn8m8DzuSZ0kFJ"

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="lBeyq6Jn8m8DzuSZ0kFJ"
).configure(
    InferenceConfiguration(
        api_key_transport="header"
    )
)


# ==============================
# 25 FOOD CLASSES
# ==============================

IDLY_FOODS = {
    "idly",
    "apple",
    "egg",
    "rice",
    # Add the rest of your IDLY-side foods here
}

SAMBAR_FOODS = {
    "sambar",
    "dal",
    "curry",
    # Add the rest of your SAMBAR-side foods here
}


def detect_sambar(image_path):

    result = client.run_workflow(
        workspace_name="albert-shibu",
        workflow_id="custom-workflow",
        images={
            "image": image_path
        },
        use_cache=False
    )

    return result


def classify_food(result):

    # Convert result to JSON so we can search through it
    data = result

    detected_food = None
    confidence = None

    # Look for prediction objects anywhere in the result
    def search_predictions(obj):

        nonlocal detected_food, confidence

        if isinstance(obj, dict):

            # Roboflow prediction usually contains class + confidence
            if "class" in obj and "confidence" in obj:
                detected_food = obj["class"]
                confidence = obj["confidence"]
                return True

            for value in obj.values():
                if search_predictions(value):
                    return True

        elif isinstance(obj, list):

            for item in obj:
                if search_predictions(item):
                    return True

        return False

    search_predictions(data)

    if detected_food is None:
        print("No food detected.")
        return

    detected_food = detected_food.lower()

    # Convert the original class into IDLY/SAMBAR
    if detected_food in IDLY_FOODS:
        category = "idly"

    elif detected_food in SAMBAR_FOODS:
        category = "sambar"

    else:
        category = "unknown"

    # Only print what you want
    print(f"Food: {category}")
    print(f"Confidence: {confidence * 100:.2f}%")


if __name__ == "__main__":

    image_path = "input/sambar2.jpg"

    try:

        result = detect_sambar(image_path)

        print("\n===== DETECTION =====")

        classify_food(result)

        print("=====================")

    except Exception as e:

        print("\nDetection failed:")
        print(e)