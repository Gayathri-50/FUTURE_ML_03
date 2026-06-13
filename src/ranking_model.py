"""
Ranking model module for Resume Screening System.
Uses TF-IDF Vectorization and Cosine Similarity to rank candidates.
"""
import os
import pandas as pd
import numpy as np
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass, field

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.preprocess import TextPreprocessor
from src.skill_extractor import SkillExtractor, SkillMatchResult, SKILL_REGISTRY


@dataclass
class CandidateRank:
    """Ranking result for a single candidate."""
    rank: int = 0
    candidate_name: str = ""
    resume_file: str = ""
    similarity_score: float = 0.0
    skill_match_score: float = 0.0
    combined_score: float = 0.0
    matching_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    candidate_skills: List[str] = field(default_factory=list)


class ResumeRankingModel:
    """
    ML model for ranking resumes against job descriptions.
    Uses TF-IDF + Cosine Similarity + Skill Matching.
    """

    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.skill_extractor = SkillExtractor(SKILL_REGISTRY)
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.8
        )
        self._fitted = False

    def preprocess_corpus(self, texts: List[str]) -> List[str]:
        """
        Preprocess a list of texts.
        
        Args:
            texts: List of raw text strings
            
        Returns:
            List of preprocessed text strings
        """
        return [self.preprocessor.preprocess(text) for text in texts]

    def fit_tfidf(self, corpus: List[str]):
        """
        Fit the TF-IDF vectorizer on a corpus.
        
        Args:
            corpus: List of document strings to fit on
        """
        processed = self.preprocess_corpus(corpus)
        self.tfidf_vectorizer.fit(processed)
        self._fitted = True

    def compute_similarity(self, resume_text: str, jd_text: str) -> float:
        """
        Compute TF-IDF cosine similarity between resume and job description.
        
        Args:
            resume_text: Preprocessed resume text
            jd_text: Preprocessed job description text
            
        Returns:
            Cosine similarity score (0 to 1)
        """
        if not self._fitted:
            # Fit on both texts if not already fitted
            corpus = [resume_text, jd_text]
            processed = self.preprocess_corpus(corpus)
            self.tfidf_vectorizer.fit(processed)
            self._fitted = True

        processed_resume = self.preprocessor.preprocess(resume_text)
        processed_jd = self.preprocessor.preprocess(jd_text)

        # Transform texts to TF-IDF vectors
        resume_vec = self.tfidf_vectorizer.transform([processed_resume])
        jd_vec = self.tfidf_vectorizer.transform([processed_jd])

        # Compute cosine similarity
        similarity = cosine_similarity(resume_vec, jd_vec)[0][0]
        return float(similarity)

    def rank_candidates(
        self,
        resumes: List[Dict[str, str]],
        jd_text: str,
        required_skills: Set[str],
        similarity_weight: float = 0.4,
        skill_weight: float = 0.6
    ) -> List[CandidateRank]:
        """
        Rank candidates based on TF-IDF similarity and skill match.
        
        Args:
            resumes: List of dicts with 'name', 'file', 'text' keys
            jd_text: Raw job description text
            required_skills: Set of required skills for the job
            similarity_weight: Weight for TF-IDF similarity score
            skill_weight: Weight for skill match score
            
        Returns:
            List of CandidateRank objects sorted by combined score (descending)
        """
        rankings = []
        processed_jd = self.preprocessor.preprocess(jd_text)
        jd_skills = self.skill_extractor.extract_skills(jd_text)

        # Use provided required_skills or extract from JD
        if not required_skills and jd_skills:
            required_skills = jd_skills

        for resume in resumes:
            name = resume.get('name', 'Unknown')
            resume_text = resume.get('text', '')
            resume_file = resume.get('file', '')

            # Compute TF-IDF similarity
            similarity = self.compute_similarity(resume_text, jd_text)

            # Extract candidate skills
            candidate_skills = self.skill_extractor.extract_skills(resume_text)

            # Match skills
            match_result = self.skill_extractor.match_skills(candidate_skills, required_skills)

            # Compute combined score (weighted average)
            # Normalize similarity to percentage
            similarity_pct = similarity * 100
            combined = (similarity_weight * similarity_pct) + (skill_weight * match_result.match_score)

            rank = CandidateRank(
                rank=0,
                candidate_name=name,
                resume_file=os.path.basename(resume_file),
                similarity_score=round(similarity_pct, 2),
                skill_match_score=round(match_result.match_score, 2),
                combined_score=round(combined, 2),
                matching_skills=match_result.matching_skills,
                missing_skills=match_result.missing_skills,
                candidate_skills=sorted(candidate_skills)
            )
            rankings.append(rank)

        # Sort by combined score descending
        rankings.sort(key=lambda r: r.combined_score, reverse=True)

        # Assign ranks
        for i, rank in enumerate(rankings, 1):
            rank.rank = i

        return rankings

    def batch_process(
        self,
        resume_dir: str,
        jd_file: str,
        required_skills: Set[str] = None
    ) -> Tuple[List[CandidateRank], str]:
        """
        Process all resumes in a directory against a job description file.
        
        Args:
            resume_dir: Directory containing resume files
            jd_file: Path to job description file
            required_skills: Optional set of required skills
            
        Returns:
            Tuple of (rankings list, job title)
        """
        # Read job description
        with open(jd_file, 'r', encoding='utf-8', errors='ignore') as f:
            jd_text = f.read()

        # Extract job title from first line
        jd_title = "Job Description"
        lines = jd_text.strip().split('\n')
        if lines:
            title_line = lines[0].replace(':', '').replace('Job Title', '').strip()
            if title_line:
                jd_title = title_line

        # Read all resumes
        resumes = []
        for fname in sorted(os.listdir(resume_dir)):
            if fname.endswith('.txt') or fname.endswith('.pdf'):
                fpath = os.path.join(resume_dir, fname)
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                # Extract name from file
                name_parts = fname.replace('.txt', '').replace('.pdf', '').split('_')
                # Try to get a meaningful name
                name = ' '.join(word.capitalize() for word in name_parts if not word.isdigit() and word != 'resume')
                if not name.strip():
                    name = fname

                resumes.append({
                    'name': name,
                    'file': fname,
                    'text': text
                })

        # If no required skills provided, extract from JD
        if required_skills is None:
            required_skills = self.skill_extractor.extract_skills(jd_text)

        # Fit TF-IDF on all texts
        all_texts = [r['text'] for r in resumes] + [jd_text]
        self.fit_tfidf(all_texts)

        # Rank candidates
        rankings = self.rank_candidates(resumes, jd_text, required_skills)

        return rankings, jd_title

    def save_results(self, rankings: List[CandidateRank], output_path: str):
        """
        Save ranking results to CSV.
        
        Args:
            rankings: List of CandidateRank objects
            output_path: Path to save CSV
        """
        data = []
        for r in rankings:
            data.append({
                'Rank': r.rank,
                'Candidate Name': r.candidate_name,
                'Resume File': r.resume_file,
                'Similarity Score (%)': r.similarity_score,
                'Skill Match Score (%)': r.skill_match_score,
                'Combined Score (%)': r.combined_score,
                'Matching Skills': ', '.join(r.matching_skills),
                'Missing Skills': ', '.join(r.missing_skills),
                'Total Skills Found': len(r.candidate_skills)
            })

        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False)
        print(f"Results saved to: {output_path}")
        return df


# Evaluation utilities
def generate_sample_labels(rankings: List[CandidateRank], threshold: float = 50.0) -> Tuple[List[int], List[int]]:
    """
    Generate sample ground truth labels for evaluation.
    Uses combined_score > threshold as 'selected' (1) vs 'not selected' (0).
    
    Args:
        rankings: List of ranked candidates
        threshold: Score threshold for classification
        
    Returns:
        Tuple of (y_true, y_pred) for evaluation metrics
    """
    y_true = []
    y_pred = []

    for rank in rankings:
        # Simulate ground truth: top 30% of candidates are "good"
        total = len(rankings)
        top_n = max(1, int(total * 0.3))
        # Ground truth: top rank candidates are good
        is_good_truth = 1 if rank.rank <= top_n else 0
        y_true.append(is_good_truth)

        # Prediction based on threshold
        is_good_pred = 1 if rank.combined_score >= threshold else 0
        y_pred.append(is_good_pred)

    return y_true, y_pred


def evaluate_model(y_true: List[int], y_pred: List[int]) -> Dict[str, float]:
    """
    Compute evaluation metrics: precision, recall, F1 score, accuracy.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        
    Returns:
        Dictionary with evaluation metrics
    """
    from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix

    metrics = {}

    try:
        metrics['precision'] = round(precision_score(y_true, y_pred, zero_division=0), 4)
    except Exception:
        metrics['precision'] = 0.0

    try:
        metrics['recall'] = round(recall_score(y_true, y_pred, zero_division=0), 4)
    except Exception:
        metrics['recall'] = 0.0

    try:
        metrics['f1_score'] = round(f1_score(y_true, y_pred, zero_division=0), 4)
    except Exception:
        metrics['f1_score'] = 0.0

    try:
        metrics['accuracy'] = round(accuracy_score(y_true, y_pred), 4)
    except Exception:
        metrics['accuracy'] = 0.0

    try:
        cm = confusion_matrix(y_true, y_pred)
        metrics['confusion_matrix'] = cm.tolist()
    except Exception:
        metrics['confusion_matrix'] = [[0, 0], [0, 0]]

    return metrics