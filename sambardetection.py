from inference_sdk import InferenceHTTPClient, InferenceConfiguration

ROBOFLOW_API_KEY = "lBeyq6Jn8m8DzuSZ0kFJ"

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key= "lBeyq6Jn8m8DzuSZ0kFJ"
).configure(
    InferenceConfiguration(
        api_key_transport="header"
    )
)


def detect_sambar(image_path):
    result = client.run_workflow(
        workspace_name="albert-shibu",
        workflow_id="custom-workflow",
        images={
            "image": image_path
        },
        use_cache=True
    )

    return result


if __name__ == "__main__":
    image_path = "input/sambar1.jpg"

    try:
        result = detect_sambar(image_path)

        print("\n===== SAMBAR DETECTION =====")
        print(result)
        print("============================")

    except Exception as e:
        print("\nDetection failed:")
        print(e)