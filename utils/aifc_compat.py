"""
Совместимость с модулем aifc для Python 3.13+
"""
import wave

# Определяем базовые функции, которые использует speech_recognition
def open(f, mode=None):
    """Эмуляция aifc.open с использованием wave модуля"""
    return wave.open(f, mode)

Error = wave.Error
