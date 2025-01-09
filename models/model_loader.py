from transformers import AutoTokenizer, AutoModelForTokenClassification

def load_model():
    model_name = "Jean-Baptiste/camembert-ner"
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)  # تعطيل fast tokenizer
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    return model, tokenizer