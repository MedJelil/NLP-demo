import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Parlez maintenant...")
        try:
            audio = recognizer.listen(source)
            print("Analyse...")
            text = recognizer.recognize_google(audio, language="fr-FR")
            return text
        except sr.UnknownValueError:
            return "Je n'ai pas compris, veuillez essayer encore."
        except sr.RequestError as e:
            return f"Erreur dans le service de reconnaissance vocale: {e}"