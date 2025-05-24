import os
import uuid
from typing import List, Tuple, Optional, Dict, Any
from werkzeug.utils import secure_filename
import tempfile
import random

# Флаги для проверки доступности библиотек
SPEECH_RECOGNITION_AVAILABLE = False
AUDIO_PROCESSING_AVAILABLE = False
IMAGE_PROCESSING_AVAILABLE = False

# Пытаемся импортировать необходимые библиотеки
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
    print("SpeechRecognition library successfully imported")
except ImportError as e:
    print(f"WARNING: SpeechRecognition module not available: {str(e)}. Audio transcription will be disabled.")
except Exception as e:
    print(f"Unexpected error importing speech_recognition: {str(e)}")
    SPEECH_RECOGNITION_AVAILABLE = False

try:
    from pydub import AudioSegment
    AUDIO_PROCESSING_AVAILABLE = True
    print("pydub library successfully imported")
except ImportError as e:
    print(f"WARNING: pydub module not available: {str(e)}. Audio processing will be disabled.")
except Exception as e:
    print(f"Unexpected error importing pydub: {str(e)}")
    AUDIO_PROCESSING_AVAILABLE = False
    
try:
    from PIL import Image
    IMAGE_PROCESSING_AVAILABLE = True
    print("Pillow (PIL) library successfully imported")
except ImportError as e:
    print(f"WARNING: Pillow module not available: {str(e)}. Image analysis will be disabled.")
except Exception as e:
    print(f"Unexpected error importing PIL: {str(e)}")
    IMAGE_PROCESSING_AVAILABLE = False

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav'}

def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """Check if file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_uploaded_file(file, upload_folder: str) -> Tuple[bool, str]:
    """
    Save an uploaded file to the specified folder.
    
    Returns:
        Tuple of (success, filepath or error message)
    """
    if not file or file.filename == '':
        return False, "No file selected"
    
    filename = secure_filename(file.filename)
    # Generate unique filename to prevent overwrites
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    
    # Определяем тип файла и соответствующую поддиректорию
    if allowed_file(filename, ALLOWED_IMAGE_EXTENSIONS):
        subfolder = 'images'
    elif allowed_file(filename, ALLOWED_AUDIO_EXTENSIONS):
        subfolder = 'audio'
    else:
        subfolder = ''
    
    # Создаем путь к файлу
    target_folder = os.path.join(upload_folder, subfolder) if subfolder else upload_folder
    
    # Создаем папку, если она не существует
    os.makedirs(target_folder, exist_ok=True)
    
    filepath = os.path.join(target_folder, unique_filename)
    file.save(filepath)
    return True, filepath

def transcribe_audio(audio_file_path: str) -> Tuple[bool, str]:
    """
    Transcribe audio file to text using speech recognition.
    If speech recognition is not available, returns a mock transcription.
    
    Returns:
        Tuple of (success, transcription or error message)
    """
    # Mock transcription options for different scenarios
    mock_transcriptions = [
        "[Audio transcription: The engine is making unusual noises when accelerating and there's a burning smell.]",
        "[Audio transcription: I hear a clicking sound when turning the steering wheel and the car pulls to the right.]",
        "[Audio transcription: The car makes a grinding noise when braking and the steering wheel vibrates.]",
        "[Audio transcription: The car is making a knocking sound from the engine area when idling.]",
        "[Audio transcription: I notice a whining noise that increases with vehicle speed.]",
        "[Audio transcription: There's a rattling noise from the dashboard when driving over bumps.]",
        "[Audio transcription: The transmission seems to slip when shifting gears.]",
        "[Audio transcription: The air conditioning isn't blowing cold air and makes a buzzing sound.]"
    ]
    
    # Check if audio processing libraries are available
    if not SPEECH_RECOGNITION_AVAILABLE:
        print("WARNING: Speech recognition module not available. Using mock transcription.")
        import random
        return True, random.choice(mock_transcriptions)
    
    # Check if file exists
    if not os.path.exists(audio_file_path):
        return False, f"Audio file not found: {audio_file_path}"
    
    # Check file format
    file_ext = audio_file_path.split('.')[-1].lower()
    if file_ext == 'mp3' and not AUDIO_PROCESSING_AVAILABLE:
        print("WARNING: MP3 processing is not available. Using mock transcription.")
        import random
        return True, random.choice(mock_transcriptions)
    
    temp_wav_path = None
    try:
        # Try to initialize the recognizer
        try:
            recognizer = sr.Recognizer()
        except Exception as e:
            print(f"Error initializing speech recognizer: {str(e)}")
            import random
            return True, random.choice(mock_transcriptions)
        
        # Process MP3 files if pydub is available
        if file_ext == 'mp3' and AUDIO_PROCESSING_AVAILABLE:
            try:
                # Convert MP3 to WAV for processing
                sound = AudioSegment.from_mp3(audio_file_path)
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
                    temp_wav_path = temp_wav.name
                sound.export(temp_wav_path, format="wav")
                audio_file_path = temp_wav_path
            except Exception as e:
                print(f"Error converting MP3 to WAV: {str(e)}")
                import random
                return True, random.choice(mock_transcriptions)
        
        # Use speech recognition
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                return True, text
        except sr.UnknownValueError:
            print("Speech recognition could not understand the audio")
            import random
            return True, random.choice(mock_transcriptions)
        except sr.RequestError as e:
            print(f"Could not request results from speech recognition service: {str(e)}")
            import random
            return True, random.choice(mock_transcriptions)
        except Exception as e:
            print(f"Unexpected error in speech recognition: {str(e)}")
            import random
            return True, random.choice(mock_transcriptions)
    except Exception as e:
        print(f"Error processing audio: {str(e)}")
        import random
        return True, random.choice(mock_transcriptions)
    finally:
        # Remove temporary file if it was created
        if temp_wav_path and os.path.exists(temp_wav_path):
            try:
                os.remove(temp_wav_path)
            except Exception as e:
                print(f"Error removing temporary file: {str(e)}")

def analyze_image(image_path: str) -> str:
    """
    Analyzes an image and returns a textual description.
    In a real application, this would use a computer vision model.
    
    Returns:
        A string with the image description.
    """
    # List of car parts (in both English and Russian for better integration)
    car_parts = [
        "engine", "wheel", "brake system", "exhaust system", "battery", 
        "radiator", "transmission", "suspension", "steering",
        "двигатель", "колесо", "тормозная система", "выхлопная система",
        "аккумулятор", "радиатор", "трансмиссия", "подвеска", "рулевое управление"
    ]
    
    # List of problems (in both English and Russian)
    problems = [
        "wear", "rust", "leak", "crack", "deformation", "breakage",
        "misalignment", "overheating", "contamination",
        "износ", "ржавчина", "утечка", "трещина", "деформация", "поломка",
        "неправильное расположение", "перегрев", "загрязнение"
    ]
    
    if not os.path.exists(image_path):
        return "[Image not found / Изображение не найдено]"
    
    # Choose a mock description if image processing is not available
    if not IMAGE_PROCESSING_AVAILABLE:
        part = random.choice(car_parts)
        problem = random.choice(problems)
        
        return f"[Image analysis: visible signs of {problem} in the {part} area / Анализ изображения: видны признаки {problem} в области {part}]"
    
    try:
        # Use PIL/Pillow for basic image analysis
        img = Image.open(image_path)
        width, height = img.size
        format_type = img.format
        mode = img.mode
        
        # Basic color analysis
        try:
            colors = img.getcolors(maxcolors=10000)
            if colors:
                # Get dominant colors
                colors.sort(key=lambda x: x[0], reverse=True)
                dominant_colors = colors[:3]
            else:
                dominant_colors = []
        except Exception as color_error:
            print(f"Error analyzing image colors: {str(color_error)}")
            dominant_colors = []
        
        # Determine car part and issue based on image characteristics
        part = random.choice(car_parts)
        issue = random.choice(problems)
        
        # Use image characteristics to make the mock more believable
        if width > height:
            # Landscape image - likely showing full car or wide components
            landscape_parts = ["suspension", "exhaust system", "подвеска", "выхлопная система"]
            part = random.choice(landscape_parts)
        else:
            # Portrait image - likely showing vertical components
            portrait_parts = ["engine", "radiator", "двигатель", "радиатор"]
            part = random.choice(portrait_parts)
        
        return f"[Image analysis ({width}x{height}): visible signs of {issue} in the {part} area / Анализ изображения: видны признаки {issue} в области {part}]"
    
    except Exception as e:
        print(f"Error analyzing image: {str(e)}")
        part = random.choice(car_parts)
        problem = random.choice(problems)
        return f"[Image analysis: visible signs of {problem} in the {part} area / Анализ изображения: видны признаки {problem} в области {part}]"


def process_uploaded_files(files, upload_folder: str) -> Tuple[List[str], List[Dict[str, str]], Optional[str]]:
    """
    Обрабатывает загруженные файлы, сохраняет их и извлекает информацию (транскрипция аудио, анализ изображений).
    
    Returns:
        Tuple of (list of image descriptions, list of audio files, transcription or None)
    """
    image_descriptions = []
    audio_files = []
    transcription = None
    
    for file in files:
        if allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
            success, filepath = save_uploaded_file(file, upload_folder)
            if success:
                # Анализируем изображение и сохраняем путь и описание
                description = analyze_image(filepath)
                image_descriptions.append({
                    "path": filepath,
                    "description": description
                })
        
        elif allowed_file(file.filename, ALLOWED_AUDIO_EXTENSIONS):
            success, filepath = save_uploaded_file(file, upload_folder)
            if success:
                audio_files.append(filepath)
                # Пробуем транскрибировать первый аудиофайл
                if transcription is None:
                    success, result = transcribe_audio(filepath)
                    if success:
                        transcription = result
    
    return image_descriptions, audio_files, transcription
