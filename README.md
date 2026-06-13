# Resume / Candidate Screening System

An ATS-style Resume Screening System that uses Machine Learning to automatically screen, rank, and match candidates against job descriptions. Built with Python, Scikit-learn, NLTK, and modern data science tools.

## 🚀 Overview

This system automates the candidate screening process by:
- Extracting and preprocessing text from resumes
- Identifying skills using keyword-based skill extraction
- Computing TF-IDF cosine similarity between resumes and job descriptions
- Calculating skill match percentages
- Ranking candidates by combined score (similarity + skill match)
- Generating detailed skill gap analysis
- Creating visual reports and evaluation metrics

## ✨ Features

### Core Features
- **Streamlit Web App**: Interactive dashboard for recruiters and HR managers
- **Resume Parsing**: Extract text from `.txt` and `.pdf` files
- **Text Preprocessing**: Cleaning, stopword removal, lemmatization (NLTK)
- **Skill Extraction**: 35+ predefined skills with keyword-based matching
- **TF-IDF Vectorization**: Machine learning-based text similarity
- **Cosine Similarity**: Measure document similarity
- **Candidate Ranking**: Weighted scoring system (40% similarity + 60% skill match)
- **Skill Gap Analysis**: Identify missing and matching skills per candidate
- **Visual Reports**: 5 types of charts for data-driven insights
- **Export Results**: Download CSV reports and skill gap analyses

### Technical Features
- **Streamlit Dashboard** with 5 interactive tabs (Rankings, Skill Analysis, Visualizations, Evaluation, Export)
- Modular Python architecture (separation of concerns)
- Type hints and comprehensive docstrings
- Error handling for missing files and dependencies
- Configurable skill registry and job role skill sets
- CSV export of ranking results
- Evaluation metrics: Precision, Recall, F1 Score, Confusion Matrix
- Jupyter Notebook for interactive analysis
- Session state management for persistent results

### Supported Job Roles (Predefined Skill Sets)
- Data Scientist
- Machine Learning Engineer
- Data Analyst
- Python Developer

### Supported Skills (35+)
Python, SQL, Machine Learning, Deep Learning, TensorFlow, PyTorch, NLP, Statistics, Power BI, Tableau, Excel, Data Analysis, Scikit-learn, Pandas, NumPy, Docker, Kubernetes, AWS, GCP, Azure, Computer Vision, Spark, Kafka, Airflow, and more.

## 📁 Project Structure

```
FUTURE_ML_03/
│
├── data/
│   ├── resumes/                    # Resume files (.txt)
│   │   ├── resume_01_alice_johnson.txt
│   │   ├── resume_02_bob_smith.txt
│   │   └── ... (23 resumes)
│   ├── job_descriptions/           # Job description files (.txt)
│   │   ├── jd_data_scientist.txt
│   │   ├── jd_ml_engineer.txt
│   │   ├── jd_data_analyst.txt
│   │   └── jd_python_developer.txt
│   └── generate_sample_data.py     # Script to generate sample data
│
├── notebooks/
│   └── Resume_Screening_System.ipynb  # Interactive Jupyter Notebook
│
├── src/
│   ├── preprocess.py               # Text preprocessing (cleaning, stopwords, lemmatization)
│   ├── skill_extractor.py          # Skill extraction and matching
│   ├── ranking_model.py            # TF-IDF, Cosine Similarity, Ranking
│   └── visualization.py            # Chart generation (Matplotlib + Seaborn)
│
├── outputs/
│   ├── ranking_results.csv         # Ranking results in CSV format
│   └── charts/                     # Generated visualizations
│       ├── top_10_candidates.png
│       ├── skill_distribution.png
│       ├── match_percentage.png
│       ├── missing_skills_heatmap.png
│       └── confusion_matrix.png
│
├── requirements.txt                # Python dependencies
├── main.py                         # Main entry point (CLI)
├── app.py                          # Streamlit web application (NEW!)
└── README.md                       # Project documentation
```

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/FUTURE_ML_03.git
cd FUTURE_ML_03
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Generate Sample Data
```bash
python data/generate_sample_data.py
```

This creates:
- 23 sample resumes with diverse skill sets
- 4 job descriptions for different roles

## 🎯 Usage

### Command Line Interface

#### Basic Usage (Data Scientist screening)
```bash
python main.py
```

#### Screen for a specific job role
```bash
python main.py --jd-file data/job_descriptions/jd_ml_engineer.txt
```

#### Use predefined skill sets
```bash
python main.py --jd-file data/job_descriptions/jd_data_analyst.txt --job-role "Data Analyst"
```

#### Custom resume directory
```bash
python main.py --resume-dir data/resumes --jd-file data/job_descriptions/jd_python_developer.txt
```

### 🌐 Streamlit Web Application (Recommended)

The easiest way to interact with the system - a professional dashboard for recruiters:

```bash
streamlit run app.py
```

This launches an interactive web app with **5 tabs**:
- **🏆 Rankings** - View ranked candidate table with search, filter, and detailed cards
- **🔍 Skill Analysis** - Analyze skill coverage, per-candidate gaps, and missing skills matrix
- **📈 Visualizations** - 5 types of professional charts (scores, distribution, match, heatmap, confusion)
- **📊 Evaluation** - Model metrics with confusion matrix and score distribution
- **📥 Export** - Download CSV reports and skill gap analyses

Features:
- Select from 4 predefined job roles or upload custom job descriptions
- Use sample resumes (23 candidates) or upload your own
- Search and filter candidates by name or score
- Color-coded skill tags for matching, missing, and extra skills
- Professional UI with gradient cards, progress bars, and interactive controls

### Jupyter Notebook

Launch the interactive notebook for analysis:
```bash
jupyter notebook notebooks/Resume_Screening_System.ipynb
```

Or using Jupyter Lab:
```bash
jupyter lab notebooks/Resume_Screening_System.ipynb
```

### Python API

```python
from src.ranking_model import ResumeRankingModel

# Initialize model
model = ResumeRankingModel()

# Process resumes against a job description
rankings, job_title = model.batch_process(
    resume_dir='data/resumes',
    jd_file='data/job_descriptions/jd_data_scientist.txt',
    required_skills=None  # Auto-extract from JD
)

# View top candidate
top = rankings[0]
print(f"Top Candidate: {top.candidate_name} ({top.combined_score:.2f}%)")
print(f"Matching Skills: {top.matching_skills}")
print(f"Missing Skills: {top.missing_skills}")

# Save results to CSV
model.save_results(rankings, 'outputs/ranking_results.csv')
```

## 📊 Sample Output

### Terminal Output
```
======================================================================
      RESUME / CANDIDATE SCREENING SYSTEM
      ATS-Style Resume Screening & Ranking Engine
======================================================================

================================================================================
TOP 10 CANDIDATE RANKINGS
================================================================================
Rank   Candidate Name            Similarity   Skill Match  Combined
--------------------------------------------------------------------------------
1      Alice Johnson             20.20%       94.44%       64.74%
2      Mia Robinson              20.57%       77.78%       54.89%
3      Eve Martinez              18.26%       66.67%       47.30%
4      Tina Brown                13.02%       66.67%       45.21%
5      Wendy Foster              8.67%        61.11%       40.13%
...
--------------------------------------------------------------------------------
Total candidates processed: 23
```

### Skill Gap Analysis
```
──────────────────────────────────────────────────────────────────────
  Rank #1: Alice Johnson
  Combined Score: 64.74%
──────────────────────────────────────────────────────────────────────
  ✅ Matching Skills (17):
     - Business Intelligence, Data Analysis, Data Visualization,
       Deep Learning, Excel, Machine Learning, NLP, NumPy,
       Pandas, Power BI, Python, R, Scikit-learn, SQL, Statistics,
       Tableau, TensorFlow
  ❌ Missing Skills (1):
     - A/B Testing
```

### Evaluation Metrics
```
======================================================================
MODEL EVALUATION METRICS
======================================================================
  Precision:    1.0000
  Recall:       0.3333
  F1 Score:     0.5000
  Accuracy:     0.8261
```

## 📈 Visualizations

### 1. Top Candidate Scores
![Top Candidate Scores](outputs/charts/top_10_candidates.png)

Horizontal bar chart showing the top 10 candidates ranked by combined score.

### 2. Skill Distribution
![Skill Distribution](outputs/charts/skill_distribution.png)

Bar chart showing how many candidates possess each skill across the entire pool.

### 3. Resume Match Percentage
![Match Percentage](outputs/charts/match_percentage.png)

Grouped bar chart comparing TF-IDF similarity, skill match, and combined scores for all candidates.

### 4. Missing Skills Heatmap
![Missing Skills Heatmap](outputs/charts/missing_skills_heatmap.png)

Heatmap displaying missing skills per candidate. Green = has skill, Red = missing skill.

### 5. Confusion Matrix
![Confusion Matrix](outputs/charts/confusion_matrix.png)

Model evaluation confusion matrix showing classification performance.

## 🧠 Machine Learning Component

### TF-IDF Feature Extraction
- Uses `sklearn.feature_extraction.text.TfidfVectorizer`
- Configuration: max 5000 features, unigrams + bigrams, English stopwords
- Transforms resume and JD text into numerical feature vectors

### Cosine Similarity Ranking
- Measures document similarity between each resume and the job description
- Score range: 0 (completely different) to 1 (identical)

### Combined Scoring
```
Combined Score = (0.4 × Similarity %) + (0.6 × Skill Match %)
```

### Classification-Ready Architecture
- `generate_sample_labels()` creates ground truth labels based on ranking position
- `evaluate_model()` computes precision, recall, F1 score, and confusion matrix
- Ready for integration with supervised learning classifiers

## 📋 Results

### Performance Summary
- 23 candidates processed in under 2 seconds
- 35+ skills automatically extracted and matched
- 5 visualization charts generated
- Precision: 1.0, Accuracy: 0.83 (with sample threshold-based evaluation)

### Key Findings
| Job Role | Top Candidate | Score |
|----------|--------------|-------|
| Data Scientist | Alice Johnson | 64.74% |
| ML Engineer | Bob Smith | High Docker/MLOps match |
| Data Analyst | Carol Davis | Strong SQL/Excel/Power BI |
| Python Developer | David Wilson | Full-stack Python expertise |

## 🔧 Future Improvements

1. **Advanced Skill Extraction**
   - Integrate spaCy for Named Entity Recognition (NER)
   - Extract skills from unstructured text using pre-trained models
   - Add experience level detection (years of experience per skill)

2. **Enhanced Ranking**
   - Weighted skill scoring based on required vs. nice-to-have
   - Experience level normalization
   - Education and certification parsing and scoring

3. **PDF Support**
   - Full PDF resume parsing with PyPDF2 or PDFPlumber
   - Table extraction for structured data

4. **ML Enhancements**
   - Train a classifier on labeled resume data
   - Implement BERT-based semantic similarity
   - Add cross-validation for more robust evaluation

5. **Scalability**
   - Batch processing for large resume pools
   - Database integration for persistent storage
   - REST API for integration with HR systems

6. **User Interface**
   - Web-based dashboard using Streamlit or Flask
   - Interactive filtering and sorting
   - Resume upload functionality

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Gayathri**
- Project: FUTURE_ML_03 - Resume/Candidate Screening System
- Built as part of Machine Learning Internship

## 🙏 Acknowledgments

- Scikit-learn documentation and community
- NLTK project for NLP utilities
- Matplotlib and Seaborn for visualization tools