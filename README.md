# nFactorial-AI-Cup-2025
# Car Diagnostics Assistant

## Overview
The Car Diagnostics Assistant is an intelligent web application that helps users diagnose car problems by analyzing text descriptions, photos, and audio recordings. The application leverages LLM technology through the Groq API to provide accurate diagnoses, recommended actions, and possible causes of car issues.

## Features
- **Multi-input diagnosis**: Text descriptions, photos, and/or audio recordings
- **Drag-and-drop file upload**: Easy file uploading with preview
- **Speech recognition**: Automatic transcription of audio recordings
- **Comprehensive diagnosis**: Provides malfunction description, recommended actions, and possible causes
- **Diagnostic history**: Stores all past diagnoses for future reference
- **History search**: Filter history by keywords
- **Feedback system**: Mark diagnoses as helpful or not helpful
- **Dark/Light theme**: Toggle between dark and light mode
- **Multilingual support**: English and Russian interfaces
- **Mobile-friendly**: Responsive design for all screen sizes

## Technical Stack
- **Backend**: Python, Flask
- **Frontend**: HTML, Tailwind CSS, Alpine.js
- **LLM Integration**: Groq API
- **Data Storage**: JSON-based history (easily extendable to databases)
- **File Processing**: Support for multiple image and audio formats

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Groq API key

### Deployment

https://dayio.onrender.com

### Presentation

https://docs.google.com/presentation/d/1V_H7VSw9B5-2uTvw6xNMgujWsIy5wFk3LdujPQ8GWuI/edit?usp=sharing
### Project Structure
- `main.py`: Main Flask application
- `llm_client.py`: Groq API integration
- `history.py`: History management module
- `utils/file_processor.py`: File handling utilities
- `templates/`: HTML templates for the web interface
- `static/`: Static assets
- `uploads/`: Directory for uploaded files (created automatically)
- `history.json`: Diagnostic history storage (created automatically)

## Future Enhancements
- Integration with computer vision models for direct image analysis
- More sophisticated audio analysis for mechanical sounds
- Integration with a proper database
- User accounts and authentication
- Export/import of diagnostic history
- Integration with repair manuals and parts catalogs
