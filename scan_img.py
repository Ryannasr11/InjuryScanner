import os
import openai
from dotenv import load_dotenv
import base64
from openai import OpenAI

# Load the API key from the .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key is not set in the .env file.")

openai.api_key = api_key

client = OpenAI()


def capture_latest_image():
    # Specify the directory where images are saved
    output_dir = "captured_images"
    if not os.path.exists(output_dir):
        raise FileNotFoundError("Captured images directory does not exist.")
    
    # Find the most recent image in the directory
    images = sorted(os.listdir(output_dir), reverse=True)
    if not images:
        raise FileNotFoundError("No images found in the directory.")
    
    return os.path.join(output_dir, images[0])

def analyze_image_with_gpt(image_path):
    # Read the image and encode it as base64
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    # Use the ChatCompletion API for multimodal interaction
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "You are a doctor, and your job is to do two things: "
                "First, give your best guess as to what medical issue the picture depicts. "
                "It could be anything from a physical injury to a disease. "
                "Second, list possible treatment options for this issue. You will be given a picture and you must return with a diagnosis and treatment plan. "
                "DO NOT MENTION that you cannot analyze images directly."
                "If your response would have been \"Based on the description,\", then simply omit the start and go into your response. "
                "Sound confident in your response, and do not mention that you are guessing. For example, say \"This image depicts\" instead of \"this image likely depicts\". "
                "Try your hardest to provide a diagnosis and treatment plan, even if you are not sure. If there is no clear issue, then communicate this clearly and communicate what you know of the image anyway."
                "You also cannot use bold text, italics, or any other formatting. Your response must come in plain text sentences."
                "Do not use \' or \". Simply omit them from your response. For example, write \" its ...\" instead of \"it\'s ...\". "
                "Again, absolutely zero use of bolded words. no **this** or __that__."
                "No bullet points or lists. If you would have used a list, simply write the items in a sentence. "
                "Do not ask for more details, as the user cannot provide them. "
                },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"

                        }
                    },
                ],
            }
        ],
    )

    return completion

def clear_captured_images_folder():
    folder_path = "captured_images"
    if os.path.exists(folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
    else:
        print("Folder 'captured_images' does not exist.")

def main():
    try:
        # Get the latest captured image
        image_path = capture_latest_image()
        #print(f"Processing image: {image_path}")
        
        # Analyze the image using ChatGPT API
        response = analyze_image_with_gpt(image_path)
        
        # Print the API's response
        #print("\n--- GPT-4o Mini Response ---")
        print(response.choices[0].message.content)

        # Clear the captured_images folder
        clear_captured_images_folder()
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()



