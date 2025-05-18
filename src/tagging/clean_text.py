def clean_text(text:str):
    """Keep only the first sentence of the generated text."""
    text = text.split(":")[-1].strip()
    text = text.split(".")[0]+"."
    return text
