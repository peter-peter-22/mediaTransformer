from PIL import Image
import numpy as np
import easyocr

reader = easyocr.Reader(['en'], gpu=True)

def extract_text(image: Image.Image, min_confidence:float):
    # Preprocess image
    image_np = np.array(image)
    # Perform OCR
    results = reader.readtext(image_np)
    # Log results
    for (bbox, text, prob) in results:
        print(f"Detected text: '{text}' with confidence {prob:.2f}")
    # Filter out low-confidence texts
    filtered=[text for (bbox, text, prob) in results if float(prob)>=min_confidence]
    # Join the filtered texts into a single string
    final="\n".join(filtered)
    return final
