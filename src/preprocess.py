"""
Text preprocessing module for Resume Screening System.
Handles text extraction, cleaning, stopword removal, and lemmatization.
"""
import re
import os
from typing import List, Dict, Optional

# Try importing NLTK - gracefully fallback if not available
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False


class TextPreprocessor:
    """
    Text preprocessor for cleaning and normalizing resume/job description text.
    """

    def __init__(self, language: str = 'english'):
        self.language = language
        self.lemmatizer = None
        self.stop_words = set()

        if NLTK_AVAILABLE:
            try:
                self.stop_words = set(stopwords.words(language))
                self.lemmatizer = WordNetLemmatizer()
            except LookupError:
                self._download_nltk_data()
                try:
                    self.stop_words = set(stopwords.words(language))
                    self.lemmatizer = WordNetLemmatizer()
                except LookupError:
                    self.stop_words = set()
                    self.lemmatizer = None
        else:
            # Fallback basic stopwords if NLTK not available
            self.stop_words = {
                'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
                'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were',
                'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
                'will', 'would', 'could', 'should', 'may', 'might', 'shall',
                'can', 'need', 'dare', 'ought', 'used', 'this', 'that', 'these',
                'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me',
                'him', 'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our',
                'their', 'mine', 'yours', 'hers', 'its', 'ours', 'theirs'
            }

    def _download_nltk_data(self):
        """Download required NLTK data packages."""
        if not NLTK_AVAILABLE:
            return
        packages = ['stopwords', 'wordnet', 'punkt']
        for package in packages:
            try:
                nltk.download(package, quiet=True)
            except Exception:
                pass

    def extract_text_from_file(self, filepath: str) -> Optional[str]:
        """
        Extract text from a file. Supports .txt and .pdf files.
        
        Args:
            filepath: Path to the resume file
            
        Returns:
            Extracted text as string, or None if extraction fails
        """
        if not os.path.exists(filepath):
            return None

        ext = os.path.splitext(filepath)[1].lower()

        if ext == '.txt':
            return self._extract_from_txt(filepath)
        elif ext == '.pdf':
            return self._extract_from_pdf(filepath)
        else:
            return None

    def _extract_from_txt(self, filepath: str) -> str:
        """Extract text from a .txt file."""
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

    def _extract_from_pdf(self, filepath: str) -> Optional[str]:
        """Extract text from a .pdf file using PyPDF2."""
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(filepath)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except ImportError:
            print("Warning: PyPDF2 not installed. Cannot extract text from PDF.")
            return None
        except Exception as e:
            print(f"Error extracting text from PDF {filepath}: {e}")
            return None

    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text.
        
        Args:
            text: Raw text string
            
        Returns:
            Cleaned text string
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove phone numbers
        text = re.sub(r'\b[\d\s\-\(\)\+\.]{7,}\b', '', text)
        
        # Remove special characters but keep letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def remove_stopwords(self, text: str) -> str:
        """
        Remove stopwords from text.
        
        Args:
            text: Cleaned text string
            
        Returns:
            Text with stopwords removed
        """
        words = text.split()
        filtered_words = [w for w in words if w not in self.stop_words and len(w) > 1]
        return ' '.join(filtered_words)

    def lemmatize_text(self, text: str) -> str:
        """
        Lemmatize words in text using NLTK WordNetLemmatizer.
        
        Args:
            text: Text string
            
        Returns:
            Lemmatized text string
        """
        if self.lemmatizer is None:
            return text
        
        words = text.split()
        lemmatized_words = [self.lemmatizer.lemmatize(w) for w in words]
        return ' '.join(lemmatized_words)

    def preprocess(self, text: str) -> str:
        """
        Full preprocessing pipeline: clean -> remove stopwords -> lemmatize.
        
        Args:
            text: Raw text string
            
        Returns:
            Fully preprocessed text string
        """
        text = self.clean_text(text)
        text = self.remove_stopwords(text)
        text = self.lemmatize_text(text)
        return text

    def preprocess_file(self, filepath: str) -> Optional[str]:
        """
        Read a file and apply full preprocessing pipeline.
        
        Args:
            filepath: Path to the file
            
        Returns:
            Preprocessed text or None if extraction fails
        """
        text = self.extract_text_from_file(filepath)
        if text is None:
            return None
        return self.preprocess(text)


# Convenience functions
def preprocess_text(text: str) -> str:
    """Convenience function to preprocess text."""
    preprocessor = TextPreprocessor()
    return preprocessor.preprocess(text)


def preprocess_file(filepath: str) -> Optional[str]:
    """Convenience function to preprocess a file."""
    preprocessor = TextPreprocessor()
    return preprocessor.preprocess_file(filepath)