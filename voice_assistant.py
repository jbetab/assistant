import speech_recognition as sr
import pyttsx3
import json
from datetime import datetime

class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.customer_data = {}
        
        # Configurar propiedades de voz
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', 'spanish')  # Intentar usar voz en español
        self.engine.setProperty('rate', 150)  # Velocidad del habla
        
    def speak(self, text):
        print(f"Asistente: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self):
        with sr.Microphone() as source:
            print("\nEscuchando...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source)
            
        try:
            # Especificar 'es-ES' para reconocimiento en español
            text = self.recognizer.recognize_google(audio, language='es-ES').lower()
            print(f"Cliente: {text}")
            return text
        except sr.UnknownValueError:
            self.speak("Lo siento, no pude entender. ¿Podrías repetirlo?")
            return self.listen()
        except sr.RequestError:
            self.speak("Estoy teniendo problemas con el servicio de reconocimiento de voz.")
            return None
            
    def save_conversation(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pedido_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.customer_data, f, indent=4, ensure_ascii=False)
        print(f"\nPedido guardado en {filename}")
        
    def print_summary(self):
        print("\n=== Resumen del Pedido ===")
        for key, value in self.customer_data.items():
            print(f"{key}: {value}")
        print("========================")
        
    def take_order(self):
        questions = {
            "nombre": "¡Hola! Bienvenido a nuestro restaurante. ¿Cuál es tu nombre?",
            "estado": "¿Cómo te encuentras hoy?",
            "ciudad": "¿De qué ciudad eres?",
            "telefono": "¿Cuál es tu número de teléfono celular?",
            "pedido": "¿Qué te gustaría ordenar hoy?",
            "solicitudes_especiales": "¿Tienes alguna solicitud especial o restricción dietética?"
        }
        
        self.speak("Bienvenido a nuestro sistema de pedidos por voz. Puedes decir 'salir' en cualquier momento para terminar.")
        
        for key, question in questions.items():
            self.speak(question)
            response = self.listen()
            
            if response and response.lower() == 'salir':
                self.speak("¡Gracias por tu visita. ¡Hasta luego!")
                return False
                
            if response:
                self.customer_data[key] = response
        
        self.speak("¡Gracias por tu pedido! Aquí está un resumen de nuestra conversación.")
        self.print_summary()
        self.save_conversation()
        self.speak("Tu pedido ha sido guardado. ¡Que tengas un excelente día!")
        return True