import requests
import time
import os
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# =========================
# CONFIG
# =========================

HF_API_KEY = "PASTE_YOUR_HF_API_KEY_HERE"  # REQUIRED

API_URL = "https://router.huggingface.co/hf-inference/models/nlpconnect/vit-gpt2-image-captioning"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/octet-stream"
}

# =========================
# IMAGE CAPTION FUNCTION
# =========================

def get_basic_caption(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError("Image file not found")

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    print(Fore.CYAN + "Generating basic caption using vit-gpt2-image-captioning...")

    for attempt in range(5):
        response = requests.post(API_URL, headers=HEADERS, data=image_bytes)

        print(Fore.YELLOW + f"Attempt {attempt + 1} | Status Code: {response.status_code}")

        if response.status_code == 200:
            try:
                result = response.json()
                return result[0]["generated_text"]
            except Exception:
                print(Fore.RED + "Invalid JSON response:")
                print(response.text)
                break

        elif response.status_code == 503:
            print(Fore.YELLOW + "Model loading... waiting 5 seconds")
            time.sleep(5)

        elif response.status_code == 401:
            print(Fore.RED + "Unauthorized! Check your Hugging Face API key.")
            break

        else:
            print(Fore.RED + "Unexpected error:")
            print(response.text)
            break

    return "Caption generation failed."

# =========================
# MAIN
# =========================

def main():
    image_path = input(Fore.GREEN + "Enter image path: ").strip()

    try:
        caption = get_basic_caption(image_path)
        print(Fore.GREEN + "\nGenerated Caption:")
        print(Style.BRIGHT + caption)
    except Exception as e:
        print(Fore.RED + f"Error: {e}")

# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    main()
