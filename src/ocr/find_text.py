from src.common.device import device
from PIL import Image
import doctr.models as models
import numpy as np
from typing import List

model = models.ocr_predictor(
    det_arch="db_resnet50",
    reco_arch = 'crnn_vgg16_bn',
    pretrained=True
).to(device)

def extract_text(image:Image.Image,min_confidence:float)->str:
    """
    Read the texts from the image, preserve the lines, filter out inconfident results.
    Args:
        image (PIL.Image): The input image
        min_confidence (float): Filter out line below this confidence level.
    Returns:
        str: The predicted text with linebraks.
    """
    # Prepare the image for the mode
    img_array=np.asarray(image)
    # Predict
    results=model([img_array])
    # Convert the json result to one string
    lines = []
    for page in results.pages:
        for block in page.blocks:
            for line in block.lines:
                # Preserve the lines
                words_in_line:List[str]=[]
                too_inconfident=False
                for word in line.words:
                    if word.confidence < min_confidence:
                        # If one word is too inconfident, skip the whole line
                        too_inconfident=True
                        break 
                    words_in_line.append(word.value)
                if too_inconfident:
                    continue
                # Add a space between each word
                lines.append(' '.join(words_in_line))
    # Add line breaks between lines
    return '\n'.join(lines)
                