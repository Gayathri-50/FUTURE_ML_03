"""
Skill extraction module for Resume Screening System.
Extracts predefined skills from resume text and matches against job requirements.
"""
import re
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass, field


# Predefined skill set for extraction
SKILL_REGISTRY: Dict[str, List[str]] = {
    "Python": ["python"],
    "SQL": ["sql", "sql server", "mysql", "postgresql", "sqlite", "bigquery"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning", "dl"],
    "TensorFlow": ["tensorflow", "tf"],
    "PyTorch": ["pytorch", "torch"],
    "NLP": ["nlp", "natural language processing", "text analytics", "text mining"],
    "Statistics": ["statistics", "statistical", "statistical analysis", "hypothesis testing"],
    "Power BI": ["power bi", "powerbi", "power-bi"],
    "Tableau": ["tableau"],
    "Excel": ["excel", "microsoft excel", "vba", "spreadsheet"],
    "Data Analysis": ["data analysis", "data analytics", "analytics"],
    "Scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy", "num-py"],
    "R": ["r programming", " r ", "r stats"],
    "Docker": ["docker", "containerization", "container"],
    "Kubernetes": ["kubernetes", "k8s"],
    "AWS": ["aws", "amazon web services", "ec2", "s3", "lambda", "sagemaker"],
    "GCP": ["gcp", "google cloud", "google cloud platform"],
    "Azure": ["azure", "microsoft azure"],
    "Computer Vision": ["computer vision", "cnn", "yolo", "opencv"],
    "Spark": ["spark", "apache spark", "pyspark"],
    "Kafka": ["kafka", "apache kafka"],
    "Airflow": ["airflow", "apache airflow"],
    "Data Visualization": ["data visualization", "visualization"],
    "A/B Testing": ["a/b testing", "ab testing", "experimentation", "a b testing"],
    "Business Intelligence": ["business intelligence", "bi"],
    "Django": ["django"],
    "Flask": ["flask"],
    "FastAPI": ["fastapi"],
    "ETL": ["etl", "data pipeline", "data pipelines"],
    "Git": ["git", "github", "gitlab"],
    "MLOps": ["mlops", "ml ops", "model deployment"],
    "NLTK": ["nltk"],
    "SpaCy": ["spacy"],
    "Transformers": ["transformers", "bert", "gpt", "llm", "large language model"],
}


@dataclass
class SkillMatchResult:
    """Result of skill matching between a candidate and a job."""
    candidate_name: str = ""
    match_score: float = 0.0
    matching_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    candidate_skills: List[str] = field(default_factory=list)
    required_skills: List[str] = field(default_factory=list)
    similarity_score: float = 0.0


class SkillExtractor:
    """
    Extracts skills from text using keyword matching with skill registry.
    """

    def __init__(self, skill_registry: Dict[str, List[str]] = None):
        self.skill_registry = skill_registry or SKILL_REGISTRY
        # Compile patterns for each skill
        self._patterns = self._compile_patterns()

    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for each skill."""
        patterns = {}
        for skill_name, keywords in self.skill_registry.items():
            # Create a pattern that matches any of the keywords as whole words
            escaped_keywords = [re.escape(kw) for kw in keywords]
            # Sort by length descending to match longer phrases first
            escaped_keywords.sort(key=len, reverse=True)
            pattern_str = r'\b(?:' + '|'.join(escaped_keywords) + r')\b'
            patterns[skill_name] = re.compile(pattern_str, re.IGNORECASE)
        return patterns

    def extract_skills(self, text: str) -> Set[str]:
        """
        Extract skills from text using pattern matching.
        
        Args:
            text: Text to search for skills
            
        Returns:
            Set of skill names found in the text
        """
        text_lower = text.lower()
        found_skills = set()

        for skill_name, pattern in self._patterns.items():
            if pattern.search(text_lower):
                found_skills.add(skill_name)

        return found_skills

    def extract_skills_from_file(self, filepath: str) -> Set[str]:
        """
        Extract skills from a file.
        
        Args:
            filepath: Path to the file
            
        Returns:
            Set of skill names found in the file
        """
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            return self.extract_skills(text)
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            return set()

    def match_skills(self, candidate_skills: Set[str], required_skills: Set[str]) -> SkillMatchResult:
        """
        Match candidate skills against required job skills.
        
        Args:
            candidate_skills: Set of skills possessed by the candidate
            required_skills: Set of skills required by the job
            
        Returns:
            SkillMatchResult with matching/missing skills and match percentage
        """
        result = SkillMatchResult()
        result.candidate_skills = sorted(candidate_skills)
        result.required_skills = sorted(required_skills)
        result.matching_skills = sorted(candidate_skills & required_skills)
        result.missing_skills = sorted(required_skills - candidate_skills)

        if len(required_skills) > 0:
            result.match_score = (len(result.matching_skills) / len(required_skills)) * 100
        else:
            result.match_score = 0.0

        return result

    def get_skill_gap_analysis(self, candidate_skills: Set[str], required_skills: Set[str]) -> Dict:
        """
        Perform detailed skill gap analysis.
        
        Args:
            candidate_skills: Skills possessed by candidate
            required_skills: Skills required by job
            
        Returns:
            Dictionary with detailed gap analysis
        """
        matching = candidate_skills & required_skills
        missing = required_skills - candidate_skills
        extra = candidate_skills - required_skills

        return {
            "matching_skills": sorted(matching),
            "missing_skills": sorted(missing),
            "extra_skills": sorted(extra),
            "match_count": len(matching),
            "missing_count": len(missing),
            "total_required": len(required_skills),
            "match_percentage": round((len(matching) / len(required_skills)) * 100, 2) if required_skills else 0,
            "gaps_filled_message": f"Candidate has {len(matching)}/{len(required_skills)} required skills ({round((len(matching)/len(required_skills))*100, 1)}%)"
        }


# Predefined skill sets for common job roles
JOB_ROLE_SKILLS: Dict[str, Set[str]] = {
    "Data Scientist": {
        "Python", "SQL", "Machine Learning", "Deep Learning",
        "TensorFlow", "PyTorch", "NLP", "Statistics",
        "Power BI", "Tableau", "Excel", "Data Analysis",
        "Scikit-learn", "Pandas", "NumPy", "Data Visualization",
        "A/B Testing", "R", "Spark"
    },
    "Machine Learning Engineer": {
        "Python", "SQL", "Machine Learning", "Deep Learning",
        "TensorFlow", "PyTorch", "Scikit-learn", "Pandas",
        "NumPy", "Docker", "Kubernetes", "AWS",
        "GCP", "Azure", "MLOps", "Git",
        "REST APIs", "Microservices", "Data Pipelines"
    },
    "Data Analyst": {
        "SQL", "Excel", "Python", "Tableau", "Power BI",
        "Statistics", "Data Analysis", "Data Visualization",
        "Business Intelligence", "A/B Testing", "Data Cleaning",
        "ETL", "R"
    },
    "Python Developer": {
        "Python", "Django", "Flask", "FastAPI", "SQL",
        "PostgreSQL", "MySQL", "REST APIs", "GraphQL",
        "Docker", "Kubernetes", "AWS", "GCP",
        "Git", "CI/CD", "Pandas", "NumPy",
        "Data Analysis", "ETL", "Microservices"
    }
}


# Convenience functions
def extract_skills(text: str) -> Set[str]:
    """Convenience function to extract skills from text."""
    extractor = SkillExtractor()
    return extractor.extract_skills(text)


def match_skills(candidate_skills: Set[str], required_skills: Set[str]) -> SkillMatchResult:
    """Convenience function to match skills."""
    extractor = SkillExtractor()
    return extractor.match_skills(candidate_skills, required_skills)