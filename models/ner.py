from transformers import pipeline
import speech_recognition as sr

from transformers import pipeline

def extract_entities(text, model, tokenizer):
    # تحليل النص باستخدام النموذج
    ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    results = ner_pipeline(text)

    # قوائم الكلمات المفتاحية
    boissons = ["café", "thé", "jus", "eau", "vin"]
    sports = ["football", "tennis", "basketball", "natation"]
    activites = ["manger", "lire", "jouer", "courir"]
    temps = ["matin", "soir", "nuit", "après-midi", "lundi", "mardi"]

    # خريطة التصنيفات
    entity_mapping = {
        "PER": "personne",    # الأشخاص
        "ORG": "organisation", # المنظمات
        "LOC": "lieu",         # الأماكن
        "MISC": "autre",       # كيانات أخرى
    }

    # تنظيم النتائج
    analysis = {}
    words = text.split()
    classified_words = []

    for entity in results:
        entity_type = entity["entity_group"]
        word = entity["word"]
        classified_words.append(word)
        key = entity_mapping.get(entity_type, "autre")
        if key not in analysis:
            analysis[key] = []
        analysis[key].append(word)

    # إضافة الكلمات غير المصنفة باستخدام القوائم المخصصة
    for word in words:
        if word not in classified_words:
            if word.lower() in boissons:
                if "boisson" not in analysis:
                    analysis["boisson"] = []
                analysis["boisson"].append(word)
            elif word.lower() in sports:
                if "sport" not in analysis:
                    analysis["sport"] = []
                analysis["sport"].append(word)
            elif word.lower() in activites:
                if "activité" not in analysis:
                    analysis["activité"] = []
                analysis["activité"].append(word)
            elif word.lower() in temps:
                if "temps" not in analysis:
                    analysis["temps"] = []
                analysis["temps"].append(word)
            else:
                if "autre" not in analysis:
                    analysis["autre"] = []
                analysis["autre"].append(word)

    return analysis


# تحميل النموذج المدرب مسبقًا
def load_ner_model():
    model_name = "Jean-Baptiste/camembert-ner"  # نموذج مدرب على الفرنسية
    ner_pipeline = pipeline("ner", model=model_name, tokenizer=model_name, aggregation_strategy="simple")
    return ner_pipeline

# تحويل الصوت إلى نص
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Parlez maintenant...")
        try:
            audio = recognizer.listen(source)
            print("Analyse du son...")
            text = recognizer.recognize_google(audio, language="fr-FR")
            return text
        except sr.UnknownValueError:
            return "Je n'ai pas compris, veuillez essayer encore."
        except sr.RequestError as e:
            return f"Erreur dans le service de reconnaissance vocale: {e}"

# تحليل النص وتصنيف الكلمات
def analyze_text(text, ner_pipeline):
    # تحليل النص لاستخراج الكيانات
    results = ner_pipeline(text)

    # خريطة التصنيفات
    entity_mapping = {
        "PER": "personne",    # الأشخاص
        "ORG": "organisation", # المنظمات
        "LOC": "lieu",         # الأماكن
        "MISC": "autre",       # كيانات أخرى
    }

    # تنظيم النتائج
    analysis = {}
    for entity in results:
        entity_type = entity["entity_group"]
        word = entity["word"]
        if entity_type in entity_mapping:
            key = entity_mapping[entity_type]
            if key not in analysis:
                analysis[key] = []
            analysis[key].append(word)

    # إضافة كلمات أخرى غير مصنفة
    words = text.split()
    classified_words = [entity["word"] for entity in results]
    for word in words:
        if word not in classified_words:
            if "autre" not in analysis:
                analysis["autre"] = []
            analysis["autre"].append(word)

    return analysis

# طباعة النتائج بتنسيق
def print_analysis(analysis):
    print("\n--- Résultat de l'analyse ---")
    for key, words in analysis.items():
        for word in words:
            print(f"{key} : {word}")

# البرنامج الرئيسي
def main():
    print("Chargement du modèle...")
    ner_pipeline = load_ner_model()
    print("Modèle chargé avec succès.\n")

    while True:
        print("Veuillez parler (ou dites 'quitter' pour terminer):")
        text = recognize_speech()
        if text.lower() in ["quitter", "exit"]:
            print("Au revoir!")
            break

        print(f"Texte reconnu: {text}")
        analysis = analyze_text(text, ner_pipeline)
        print_analysis(analysis)

if __name__ == "__main__":
    main()