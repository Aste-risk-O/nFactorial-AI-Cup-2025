import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import json
from datetime import datetime

# Import custom modules
from llm_client import LLMClient
from history import add_record, get_history, delete_record, clear_history, search_history, update_feedback, get_feedback_stats
from utils.file_processor import process_uploaded_files, allowed_file, ALLOWED_IMAGE_EXTENSIONS, ALLOWED_AUDIO_EXTENSIONS

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

# Создаем директории, если они не существуют
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Создаем поддиректории для разных типов файлов
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'images'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'audio'), exist_ok=True)

# Initialize LLM client
llm_client = LLMClient()

# Supported languages
LANGUAGES = {
    'en': 'English',
    'ru': 'Russian'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    diagnosis_result = None
    error_message = None
    
    if request.method == 'POST':
        try:
            # Get user description
            description = request.form.get('description', '')
            
            # Get uploaded files
            files = request.files.getlist('files')
            
            # Process uploaded files
            image_descriptions, audio_files, transcription = process_uploaded_files(
                files, app.config['UPLOAD_FOLDER']
            )
            
            # Get diagnosis from LLM if we have at least some input
            if description or image_descriptions or audio_files:
                
                # Get diagnosis
                diagnosis = llm_client.get_car_diagnosis(
                    description=description,
                    image_descriptions=image_descriptions if image_descriptions else None,
                    audio_transcription=transcription
                )
                
                # Save to history
                uploaded_filenames = [os.path.basename(f) for f in image_files + audio_files]
                record = add_record(description, diagnosis, uploaded_filenames)
                
                diagnosis_result = {
                    'record_id': record['id'],
                    'diagnosis': diagnosis,
                    'transcription': transcription
                }
            else:
                error_message = "Please provide at least a description, photo, or audio recording."
                
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
    
    return render_template('index.html', 
                           diagnosis_result=diagnosis_result, 
                           error_message=error_message,
                           allowed_image_extensions=", ".join(ALLOWED_IMAGE_EXTENSIONS),
                           allowed_audio_extensions=", ".join(ALLOWED_AUDIO_EXTENSIONS),
                           languages=LANGUAGES)

@app.route('/history')
def history():
    query = request.args.get('query', '')
    if query:
        records = search_history(query)
    else:
        records = get_history()
    
    return render_template('history.html', 
                           records=records, 
                           search_query=query,
                           languages=LANGUAGES)

@app.route('/stats')
def stats():
    """Отображает страницу статистики с информацией об обратной связи."""
    feedback_stats = get_feedback_stats()
    return render_template('stats.html',
                          stats=feedback_stats,
                          languages=LANGUAGES)

@app.route('/api/delete_record/<record_id>', methods=['POST'])
def api_delete_record(record_id):
    success = delete_record(record_id)
    return jsonify({'success': success})

@app.route('/api/clear_history', methods=['POST'])
def api_clear_history():
    clear_history()
    return jsonify({'success': True})

@app.route('/api/feedback/<record_id>', methods=['POST'])
def api_feedback(record_id):
    data = request.json
    feedback = data.get('helpful', None)
    
    if feedback is not None:
        success = update_feedback(record_id, feedback)
        return jsonify({'success': success})
    
    return jsonify({'success': False, 'error': 'Invalid feedback data'})

@app.route('/api/toggle_theme', methods=['POST'])
def toggle_theme():
    # This would typically store the theme preference in a session or cookie
    # For simplicity, we'll just return success
    return jsonify({'success': True})

@app.route('/api/change_language', methods=['POST'])
def change_language():
    # This would typically store the language preference in a session or cookie
    # For simplicity, we'll just return success
    return jsonify({'success': True})

@app.route('/api/export_history')
def export_history():
    """Экспортирует историю диагностики в формате JSON для скачивания."""
    history = get_history()
    response = jsonify(history)
    response.headers.set('Content-Disposition', 'attachment', filename='car_diagnostics_history.json')
    return response

@app.route('/api/import_history', methods=['POST'])
def import_history():
    """Импортирует историю диагностики из загруженного JSON-файла."""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'})
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})
        
    if not file.filename.endswith('.json'):
        return jsonify({'success': False, 'error': 'File must be a JSON file'})
        
    try:
        # Чтение данных из файла
        content = file.read()
        imported_history = json.loads(content)
        
        # Проверка структуры данных
        if not isinstance(imported_history, list):
            return jsonify({'success': False, 'error': 'Invalid history format'})
            
        # Сохранение импортированной истории
        save_history(imported_history)
        
        return jsonify({'success': True, 'message': 'History imported successfully', 'count': len(imported_history)})
    except json.JSONDecodeError:
        return jsonify({'success': False, 'error': 'Invalid JSON format'})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error importing history: {str(e)}'})


if __name__ == '__main__':
    app.run(debug=True)
