from models.model_loader import load_model
from models.ner import extract_entities
from utils.speech_to_text import recognize_speech

def main():
    print("Début du programme...")
    # تحميل النموذج
    model, tokenizer = load_model()
    print("Modèle chargé avec succès.")

    while True:
        print("Veuillez parler maintenant...")
        # تحويل الصوت إلى نص
        text = recognize_speech()
        print(f"Texte reconnu: {text}")

        if text.lower() in ["exit", "quitter"]:
            print("Au revoir!")
            break

        # تحليل النص واستخراج المعلومات
        if "Erreur" not in text and "Je n'ai pas compris" not in text:
            entities = extract_entities(text, model, tokenizer)
            print("Résultat:", entities)
        else:
            print("Impossible d'analyser le texte. Réessayez.")

if __name__ == "__main__":
    main()