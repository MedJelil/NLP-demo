from transformers import pipeline

# تحميل النموذج
model_name = "Jean-Baptiste/camembert-ner"
ner_pipeline = pipeline("ner", model=model_name, tokenizer=model_name, aggregation_strategy="simple")

# نص الاختبار
text = "Je bois un café à Paris"
results = ner_pipeline(text)
print("Résultats du modèle:", results)