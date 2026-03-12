import google.generativeai as genai

API_KEY = "AIzaSyBPMUTTnwkONwto9nX64D9KwNymGDNKeHg"

def exhaustive_test():
    genai.configure(api_key=API_KEY)
    print("Listing all models and testing...")
    
    available_models = []
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
    except Exception as e:
        print(f"Error listing models: {e}")
        return

    print(f"Found {len(available_models)} models supporting generation.")
    
    for model_name in available_models:
        print(f"Testing {model_name}...", end=" ", flush=True)
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hi")
            print(f"SUCCESS! ({response.text[:20]}...)")
            print(f"\nFINAL MODEL TO USE: {model_name}")
            return
        except Exception as e:
            msg = str(e).split('\n')[0][:100]
            print(f"FAILED: {msg}")

if __name__ == "__main__":
    exhaustive_test()







