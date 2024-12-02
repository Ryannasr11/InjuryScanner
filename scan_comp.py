import os
import base64
from dotenv import load_dotenv
import openai
from openai import OpenAI

'''

TEMPORARILY DEPRECATED FEATURE, as the GPT API currently requires more tokens than are available for this feature to run
-- This could change in the future, however --

'''

# Load the API key from the .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key is not set in the .env file.")

openai.api_key = api_key

client = OpenAI()

def capture_images_in_folder(folder_path):
    """Get all images in the folder sorted by their last modification time."""
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")

    images = sorted(
        [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))],
        key=os.path.getmtime
    )
    if not images:
        raise FileNotFoundError("No images found in the folder.")
    return images

def analyze_progression_with_gpt(images):
    """Analyze progression of condition using GPT."""
    encoded_images = []
    for image_path in images:
        # Read and encode each image as base64
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            encoded_images.append(f"data:image/jpeg;base64,{encoded_image}")

    # Send all images to the model at once
    messages = [
        {
            "role": "user",
            "content": "You are a doctor tasked with analyzing the progression of a medical condition depicted in a series of images. "
                       "You will be provided all images at once. Describe what these images show in the context of a medical condition, "
                       "highlighting any noticeable progression or regression of the condition. "
                       "Provide your observations in a cohesive and detailed manner. "
                       "Remember to sound confident, avoid hedging, and stick to plain text without lists or formatting."
        }
    ]

    # Add each image as a separate message with "user" role
    for img in encoded_images:
        messages.append({
            "role": "user",
            "content": f"This is an image for analysis: {img}"
        })

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    # Return the model's response
    return completion.choices[0].message.content


def clear_folder(folder_path):
    """Delete all files in the specified folder."""
    if os.path.exists(folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
    else:
        print(f"Folder '{folder_path}' does not exist.")

def main():
    comparison_dir = "comparison_images"

    try:
        # Step 1: Capture all images in the comparison_images folder
        images = capture_images_in_folder(comparison_dir)
        print(f"Found {len(images)} images in the comparison folder.")

        # Step 2: Analyze all images simultaneously
        print("Analyzing progression...")
        progression_summary = analyze_progression_with_gpt(images)
        print("\n--- Progression Analysis ---")
        print(progression_summary)

        # Step 3: Clear the comparison_images folder
        clear_folder(comparison_dir)
        print("Cleared comparison_images folder.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
