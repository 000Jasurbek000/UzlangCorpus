"""
PDF va matn tahlil uchun utility funksiyalar
"""
import PyPDF2
import re
from pathlib import Path


def extract_text_from_pdf(pdf_path):
    """
    PDF fayldan matnni ajratib olish
    """
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"PDF o'qishda xatolik: {e}")
        return ""


def analyze_text(text):
    """
    Matnni tahlil qilish va statistikani qaytarish
    """
    if not text:
        return {
            'total_words': 0,
            'total_characters': 0,
            'total_characters_no_spaces': 0,
            'total_sentences': 0,
            'total_paragraphs': 0,
            'unique_words': 0
        }
    
    # Belgilar soni
    total_characters = len(text)
    total_characters_no_spaces = len(text.replace(' ', '').replace('\n', '').replace('\t', ''))
    
    # So'zlar
    words = re.findall(r'\b\w+\b', text.lower())
    total_words = len(words)
    unique_words = len(set(words))
    
    # Gaplar (nuqta, savol, undov belgisidan keyin)
    sentences = re.split(r'[.!?]+', text)
    total_sentences = len([s for s in sentences if s.strip()])
    
    # Paragraflar (ikki yoki undan ko'p qator oralig'i)
    paragraphs = re.split(r'\n\s*\n', text)
    total_paragraphs = len([p for p in paragraphs if p.strip()])
    
    return {
        'total_words': total_words,
        'total_characters': total_characters,
        'total_characters_no_spaces': total_characters_no_spaces,
        'total_sentences': total_sentences,
        'total_paragraphs': total_paragraphs,
        'unique_words': unique_words
    }


def get_pdf_page_count(pdf_path):
    """
    PDF sahifalar sonini olish
    """
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            return len(pdf_reader.pages)
    except Exception as e:
        print(f"PDF sahifalarni hisoblashda xatolik: {e}")
        return 0
