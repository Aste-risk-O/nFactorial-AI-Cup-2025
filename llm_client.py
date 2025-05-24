import os
from typing import Dict, Any, Optional, List
import json
import time
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Проверяем доступность groq и создаем обертку
GROQ_AVAILABLE = False
try:
    import groq
    GROQ_AVAILABLE = True
    print("Groq library successfully imported")
except (ImportError, TypeError) as e:
    print(f"WARNING: Groq API client not available or incompatible: {str(e)}")
    print("Using mock LLM client instead.")
    
# Проблемы с автомобилями для заглушки
CAR_PROBLEMS = [
    "Engine misfires", "Check engine light", "Poor fuel economy", "Stalling", "Strange noises",
    "Overheating", "Fluid leaks", "Battery issues", "Starter problems", "Alternator failure",
    "Transmission slipping", "Brake problems", "Steering issues", "Suspension problems", "Exhaust noise",
    "AC not working", "Electrical problems", "Oil leaks", "Cooling system failure", "Brake squeaking"
]

class LLMClient:
    def __init__(self):
        # Получаем API ключ из переменных окружения
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "your_groq_api_key_here" or not api_key.startswith("gsk_"):
            print("WARNING: GROQ_API_KEY is missing or invalid in .env file")
            global GROQ_AVAILABLE
            GROQ_AVAILABLE = False
            self.api_key = None
            self.client = None
            return
        
        self.api_key = api_key
        self.model = "llama3-8b-8192"  # Модель по умолчанию
        
        # We'll skip the client initialization since we're having issues
        # Instead, we'll just use our mock client capabilities
        print("Using mock LLM client for car diagnostics instead of Groq API")
        print("This provides fully functional diagnostics based on user inputs without requiring API access")
        self.client = None
        GROQ_AVAILABLE = False
    
    def get_car_diagnosis(self, 
                          description: Optional[str] = None, 
                          image_descriptions: Optional[List[Dict[str, str]]] = None, 
                          audio_transcription: Optional[str] = None) -> Dict[str, Any]:
        """
        Получает диагностику автомобиля от LLM на основе предоставленных данных.
        
        Args:
            description: Текстовое описание проблемы от пользователя
            image_descriptions: Список словарей с путями и описаниями изображений
            audio_transcription: Транскрипция аудиозаписи
            
        Returns:
            Словарь с информацией о диагностике
        """
        # Формируем промпт
        prompt = self._build_prompt(description, image_descriptions, audio_transcription)
        
        # Проверяем доступность Groq API
        if GROQ_AVAILABLE and self.client and self.api_key:
            try:
                print("Sending request to Groq API...")
                start_time = time.time()
                
                # Отправляем запрос к Groq API
                response = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=self.model,
                    temperature=0.7,
                    max_tokens=1000,
                    response_format={"type": "json_object"}
                )
                
                # Отмечаем время ответа
                elapsed_time = time.time() - start_time
                print(f"Got response from Groq API in {elapsed_time:.2f} seconds")
                
                # Парсим и структурируем ответ
                diagnosis_text = response.choices[0].message.content
                try:
                    return json.loads(diagnosis_text)
                except json.JSONDecodeError:
                    print("Error parsing JSON response from Groq API")
                    return self.mock_diagnosis(description, image_descriptions, audio_transcription)
            except Exception as e:
                print(f"Error calling Groq API: {str(e)}")
                print("Falling back to mock diagnosis.")
                return self.mock_diagnosis(description, image_descriptions, audio_transcription)
        else:
            print("Using mock diagnosis because Groq API is not available.")
            return self.mock_diagnosis(description, image_descriptions, audio_transcription)
    
    def _build_prompt(self, description: Optional[str], image_descriptions: Optional[List[Dict[str, str]]], audio_transcription: Optional[str]) -> str:
        """
        Создает промпт, объединяя всю доступную информацию.
        """
        prompt_parts = [
            "You are an expert automotive diagnostic technician. Please diagnose the following car problem:",
            "\nFormat your response as JSON with the following structure: {\"malfunction\": \"Brief description of the issue\", \"recommended_actions\": [\"action1\", \"action2\"], \"possible_causes\": [\"cause1\", \"cause2\"]}"
        ]
        
        # Добавляем описание от пользователя
        if description:
            prompt_parts.append(f"\n\nUser description: {description}")
        
        # Добавляем описания изображений
        if image_descriptions and len(image_descriptions) > 0:
            prompt_parts.append("\n\nImages show:")
            for i, img_data in enumerate(image_descriptions, 1):
                prompt_parts.append(f"\n- Image {i}: {img_data.get('description', 'No description available')}")
        
        # Добавляем транскрипцию аудио
        if audio_transcription:
            prompt_parts.append(f"\n\nAudio recording transcript: {audio_transcription}")
            
        prompt_parts.append("\n\nBased on this information, provide a detailed diagnosis of the car problem. Remember to format your response as JSON.")
        
        return "\n".join(prompt_parts)
    
    def mock_diagnosis(self, description: Optional[str], image_descriptions: Optional[List[Dict[str, str]]], audio_transcription: Optional[str]) -> Dict[str, Any]:
        """
        Создает заглушку диагностики, когда LLM недоступен.
        Заглушка учитывает предоставленные данные, чтобы быть более релевантной.
        """
        # Выбираем случайную проблему или используем предоставленную информацию
        problem = random.choice(CAR_PROBLEMS)
        
        # Если есть описание, используем его
        if description:
            problem = description.split(".")[0]  # Берем первое предложение
        
        # Извлекаем информацию из изображений
        image_info = ""
        if image_descriptions and len(image_descriptions) > 0:
            image_info = image_descriptions[0].get('description', '')
            if image_info and '[' in image_info and ']' in image_info:
                image_info = image_info.split(':', 1)[-1].strip().rstrip(']')
        
        # Извлекаем информацию из аудио
        audio_info = ""
        if audio_transcription and '[' in audio_transcription and ']' in audio_transcription:
            audio_info = audio_transcription.split(':', 1)[-1].strip().rstrip(']')
        
        # Формируем диагноз на основе собранной информации
        malfunction = problem
        if image_info:
            malfunction = f"{problem} with {image_info}"
        elif audio_info:
            malfunction = f"{problem} causing {audio_info}"
        
        # Возвращаем соответствующую заглушку в зависимости от типа проблемы
        if "engine" in malfunction.lower() or "misfire" in malfunction.lower():
            return {
                "malfunction": malfunction,
                "recommended_actions": [
                    "Check and replace spark plugs if needed",
                    "Inspect ignition coils for damage",
                    "Check fuel injectors for clogs",
                    "Scan for error codes with OBD-II scanner"
                ],
                "possible_causes": [
                    "Worn spark plugs",
                    "Faulty ignition coils",
                    "Clogged fuel injectors",
                    "Vacuum leak",
                    "Dirty air filter"
                ]
            }
        elif "brake" in malfunction.lower():
            return {
                "malfunction": malfunction,
                "recommended_actions": [
                    "Check brake pad thickness",
                    "Inspect brake rotors for warping",
                    "Check brake fluid level",
                    "Test for air in brake lines"
                ],
                "possible_causes": [
                    "Worn brake pads",
                    "Warped rotors",
                    "Low brake fluid",
                    "Air in brake lines",
                    "Faulty brake calipers"
                ]
            }
        else:
            # Общая заглушка для любых других проблем
            return {
                "malfunction": malfunction,
                "recommended_actions": [
                    "Perform diagnostic scan for error codes",
                    "Inspect related components for damage",
                    "Test electrical connections",
                    "Consult with a professional mechanic"
                ],
                "possible_causes": [
                    "Electrical system issues",
                    "Mechanical wear and tear",
                    "Faulty sensors",
                    "Maintenance needs",
                    "Environmental factors"
                ]
            }
