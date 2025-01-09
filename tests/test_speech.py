import speech_recognition as sr

def test_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Parlez maintenant...")
        try:
            audio = recognizer.listen(source)
            print("Analyse...")
            text = recognizer.recognize_google(audio, language="fr-FR")
            print(f"Vous avez dit: {text}")
        except sr.UnknownValueError:
            print("Je n'ai pas compris, veuillez essayer encore.")
        except sr.RequestError as e:
            print(f"Erreur dans le service de reconnaissance vocale: {e}")

test_microphone()