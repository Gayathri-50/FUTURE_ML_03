"""
Script to generate sample resumes and job descriptions for the Resume Screening System.
Run this script first to create sample data files.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESUMES_DIR = os.path.join(BASE_DIR, "resumes")
JOBS_DIR = os.path.join(BASE_DIR, "job_descriptions")

os.makedirs(RESUMES_DIR, exist_ok=True)
os.makedirs(JOBS_DIR, exist_ok=True)

resumes = [
    {
        "name": "Alice Johnson",
        "file": "resume_01_alice_johnson.txt",
        "text": """Alice Johnson
Email: alice.johnson@email.com | Phone: +1-555-0101

Professional Summary:
Data Scientist with 5 years of experience in building machine learning models and statistical analysis. Proficient in Python, SQL, and deep learning frameworks.

Skills:
- Python, SQL, R
- Machine Learning, Deep Learning
- TensorFlow, PyTorch
- NLP, Computer Vision
- Statistics, Data Analysis
- Scikit-learn, Pandas, NumPy
- Power BI, Tableau
- Excel, Data Visualization

Experience:
Senior Data Scientist at TechCorp (2021-Present)
- Developed ML models for customer churn prediction achieving 94% accuracy
- Built NLP pipeline for sentiment analysis using BERT
- Created interactive dashboards using Power BI

Data Scientist at DataSolve (2019-2021)
- Performed statistical analysis on large datasets
- Implemented recommendation systems using collaborative filtering
- Automated data preprocessing pipelines

Education:
M.S. in Data Science, Stanford University (2019)
B.S. in Computer Science, MIT (2017)
"""
    },
    {
        "name": "Bob Smith",
        "file": "resume_02_bob_smith.txt",
        "text": """Bob Smith
Email: bob.smith@email.com | Phone: +1-555-0102

Professional Summary:
Machine Learning Engineer with strong background in deploying scalable ML systems. Expert in Python, TensorFlow, and cloud platforms.

Skills:
- Python, Java, C++
- Machine Learning, Deep Learning
- TensorFlow, PyTorch, Keras
- Docker, Kubernetes, AWS
- CI/CD, MLOps
- SQL, NoSQL Databases
- Scikit-learn, Pandas
- REST APIs, Microservices

Experience:
ML Engineer at CloudAI (2020-Present)
- Deployed ML models to production using Docker and Kubernetes
- Built automated ML pipelines reducing deployment time by 60%
- Optimized model inference using TensorRT

Junior ML Engineer at AI Labs (2018-2020)
- Developed computer vision models for object detection
- Implemented data augmentation pipelines
- Created monitoring dashboards for model performance

Education:
M.S. in Computer Science, Carnegie Mellon University (2018)
B.S. in Computer Engineering, Georgia Tech (2016)
"""
    },
    {
        "name": "Carol Davis",
        "file": "resume_03_carol_davis.txt",
        "text": """Carol Davis
Email: carol.davis@email.com | Phone: +1-555-0103

Professional Summary:
Data Analyst with expertise in transforming raw data into actionable insights. Skilled in SQL, Excel, Power BI, and statistical analysis.

Skills:
- SQL, Excel, Power BI
- Data Analysis, Data Visualization
- Statistics, A/B Testing
- Tableau, Python
- R, SAS
- Business Intelligence
- Data Cleaning, ETL

Experience:
Data Analyst at MarketInsights (2021-Present)
- Created weekly sales dashboards using Power BI
- Conducted A/B tests for marketing campaigns
- Analyzed customer behavior patterns using SQL

Junior Data Analyst at RetailCorp (2019-2021)
- Maintained data quality and performed data cleaning
- Generated monthly performance reports in Excel
- Assisted in building Tableau dashboards

Education:
B.S. in Statistics, University of Michigan (2019)
"""
    },
    {
        "name": "David Wilson",
        "file": "resume_04_david_wilson.txt",
        "text": """David Wilson
Email: david.wilson@email.com | Phone: +1-555-0104

Professional Summary:
Python Developer with 4 years of experience building web applications and data pipelines. Strong knowledge of Python frameworks and database systems.

Skills:
- Python, Django, Flask
- SQL, PostgreSQL, MongoDB
- REST APIs, GraphQL
- Git, Docker, CI/CD
- Pandas, NumPy
- AWS, Cloud Computing
- JavaScript, HTML, CSS
- Data Analysis, ETL

Experience:
Python Developer at WebSolutions (2020-Present)
- Built RESTful APIs using Django REST Framework
- Designed and implemented data pipelines
- Deployed applications on AWS EC2 and Lambda

Junior Developer at StartUpInc (2018-2020)
- Developed web scrapers for data collection
- Created automated testing frameworks
- Maintained PostgreSQL databases

Education:
B.S. in Computer Science, UC Berkeley (2018)
"""
    },
    {
        "name": "Eve Martinez",
        "file": "resume_05_eve_martinez.txt",
        "text": """Eve Martinez
Email: eve.martinez@email.com | Phone: +1-555-0105

Professional Summary:
Data Scientist with PhD in Machine Learning. Specialized in NLP and deep learning with publications in top conferences.

Skills:
- Python, PyTorch, TensorFlow
- NLP, Transformers, BERT
- Deep Learning, Neural Networks
- Machine Learning, Statistics
- SQL, Big Data
- Scikit-learn, Pandas, NumPy
- Research, Experiment Design
- Data Visualization

Experience:
Senior Research Scientist at NLP Labs (2022-Present)
- Led research team developing state-of-the-art NLP models
- Published papers at ACL and EMNLP conferences
- Built large-scale language models

Data Scientist at BigData Corp (2019-2022)
- Developed text classification and entity extraction systems
- Built recommendation engines using deep learning
- Analyzed user behavior using statistical methods

Education:
Ph.D. in Machine Learning, MIT (2019)
M.S. in Computer Science, Stanford University (2015)
"""
    },
    {
        "name": "Frank Brown",
        "file": "resume_06_frank_brown.txt",
        "text": """Frank Brown
Email: frank.brown@email.com | Phone: +1-555-0106

Professional Summary:
Machine Learning Engineer experienced in building end-to-end ML systems. Expert in TensorFlow, PyTorch, and MLOps practices.

Skills:
- Python, TensorFlow, PyTorch
- Machine Learning, Deep Learning
- Docker, Kubernetes, Kubeflow
- AWS, GCP, Azure
- MLOps, CI/CD
- SQL, BigQuery
- Scikit-learn, Pandas
- Data Engineering, ETL

Experience:
ML Engineer at CloudML (2021-Present)
- Built automated ML pipelines using Kubeflow
- Deployed models on AWS SageMaker
- Implemented model versioning and monitoring

ML Engineer at DataPlatform (2019-2021)
- Developed fraud detection models
- Built feature stores for ML systems
- Created data pipelines using Apache Airflow

Education:
M.S. in Data Science, Columbia University (2019)
B.S. in Mathematics, UCLA (2017)
"""
    },
    {
        "name": "Grace Lee",
        "file": "resume_07_grace_lee.txt",
        "text": """Grace Lee
Email: grace.lee@email.com | Phone: +1-555-0107

Professional Summary:
Data Analyst skilled in SQL, Excel, and data visualization. Passionate about turning data into business insights.

Skills:
- SQL, Excel, Python
- Data Analysis, Reporting
- Power BI, Tableau
- Statistics, A/B Testing
- Data Cleaning, Data Quality
- Business Intelligence
- Google Analytics
- Communication, Presentation

Experience:
Data Analyst at Ecommerce Inc (2020-Present)
- Analyzed sales data to identify growth opportunities
- Created automated reports using SQL and Python
- Built executive dashboards in Tableau

Analyst Intern at FinanceCorp (2019-2020)
- Assisted in financial data analysis
- Created weekly performance reports
- Participated in data quality initiatives

Education:
B.S. in Business Analytics, University of Texas (2020)
"""
    },
    {
        "name": "Henry Clark",
        "file": "resume_08_henry_clark.txt",
        "text": """Henry Clark
Email: henry.clark@email.com | Phone: +1-555-0108

Professional Summary:
Python Developer and Data Engineer with expertise in building scalable data pipelines and ETL processes.

Skills:
- Python, SQL, PySpark
- ETL, Data Pipelines
- Apache Spark, Hadoop
- Pandas, NumPy
- AWS S3, Redshift, Lambda
- Docker, Airflow
- Django, Flask
- Git, Linux

Experience:
Data Engineer at DataStream (2021-Present)
- Designed and built real-time data pipelines
- Optimized Spark jobs for large-scale processing
- Implemented data quality monitoring systems

Python Developer at TechStartup (2019-2021)
- Developed ETL pipelines using Python and Airflow
- Built REST APIs using Flask
- Managed AWS infrastructure for data processing

Education:
B.S. in Computer Science, University of Washington (2019)
"""
    },
    {
        "name": "Ivy Wang",
        "file": "resume_09_ivy_wang.txt",
        "text": """Ivy Wang
Email: ivy.wang@email.com | Phone: +1-555-0109

Professional Summary:
Data Scientist with expertise in deep learning and computer vision. Experienced in deploying models for production use cases.

Skills:
- Python, PyTorch, TensorFlow
- Computer Vision, OpenCV
- Deep Learning, CNNs, GANs
- Machine Learning, Statistics
- SQL, MongoDB
- Docker, AWS
- Scikit-learn, Pandas
- Research, Technical Writing

Experience:
Computer Vision Engineer at VisionTech (2021-Present)
- Developed object detection models using YOLO and Detectron2
- Built face recognition systems achieving 99% accuracy
- Deployed models using TensorFlow Serving

Data Scientist at AI Solutions (2019-2021)
- Built image classification models for medical imaging
- Implemented data augmentation strategies
- Created visualization dashboards for model metrics

Education:
Ph.D. in Computer Vision, Stanford University (2019)
M.S. in Electrical Engineering, MIT (2015)
"""
    },
    {
        "name": "Jack Taylor",
        "file": "resume_10_jack_taylor.txt",
        "text": """Jack Taylor
Email: jack.taylor@email.com | Phone: +1-555-0110

Professional Summary:
Data Analyst with strong background in statistical analysis and business intelligence. Proficient in SQL, Python, and Tableau.

Skills:
- SQL, Python, R
- Statistics, Data Analysis
- Tableau, Power BI
- Excel, Google Sheets
- A/B Testing, Hypothesis Testing
- Data Visualization
- Business Intelligence
- Data Cleaning

Experience:
Data Analyst at HealthData Inc (2020-Present)
- Analyzed patient data to identify health trends
- Built interactive dashboards for healthcare metrics
- Conducted statistical analysis for clinical studies

Junior Analyst at MarketResearch (2018-2020)
- Performed market research and competitor analysis
- Created data visualizations using Tableau
- Assisted in building predictive models

Education:
B.S. in Statistics, University of Florida (2018)
"""
    },
    {
        "name": "Karen White",
        "file": "resume_11_karen_white.txt",
        "text": """Karen White
Email: karen.white@email.com | Phone: +1-555-0111

Professional Summary:
Machine Learning Engineer specializing in NLP and recommendation systems. Strong background in mathematics and algorithm design.

Skills:
- Python, TensorFlow, PyTorch
- NLP, Text Mining, Transformers
- Machine Learning, Deep Learning
- Recommendation Systems
- SQL, NoSQL
- AWS, Docker, Kubernetes
- Scikit-learn, Pandas
- Statistics, Probability

Experience:
ML Engineer at RecommendAI (2022-Present)
- Built personalized recommendation systems
- Developed NLP models for content understanding
- Optimized ranking algorithms for relevance

Data Scientist at Ecommerce Giant (2020-2022)
- Developed product recommendation engines
- Built customer segmentation models
- Improved search relevance using ML

Education:
M.S. in Machine Learning, Georgia Tech (2020)
B.S. in Mathematics, Cornell University (2018)
"""
    },
    {
        "name": "Liam Harris",
        "file": "resume_12_liam_harris.txt",
        "text": """Liam Harris
Email: liam.harris@email.com | Phone: +1-555-0112

Professional Summary:
Python Developer with expertise in backend development and data engineering. Skilled in building scalable applications and APIs.

Skills:
- Python, Django, FastAPI
- SQL, PostgreSQL, Redis
- REST APIs, GraphQL
- Docker, Kubernetes
- AWS, GCP
- Pandas, NumPy
- Git, CI/CD
- Microservices Architecture

Experience:
Backend Developer at FastTech (2021-Present)
- Designed and implemented microservices architecture
- Built high-performance APIs handling 10K+ requests/second
- Optimized database queries reducing latency by 40%

Python Developer at DevShop (2019-2021)
- Developed web applications using Django
- Implemented caching strategies using Redis
- Created automated deployment pipelines

Education:
B.S. in Software Engineering, University of Illinois (2019)
"""
    },
    {
        "name": "Mia Robinson",
        "file": "resume_13_mia_robinson.txt",
        "text": """Mia Robinson
Email: mia.robinson@email.com | Phone: +1-555-0113

Professional Summary:
Data Scientist experienced in applying ML to business problems. Strong skills in Python, SQL, and statistical modeling.

Skills:
- Python, SQL, R
- Machine Learning, Statistics
- Deep Learning, Neural Networks
- NLP, Text Analytics
- Power BI, Tableau
- Excel, Data Analysis
- Scikit-learn, Pandas
- A/B Testing, Experimentation

Experience:
Data Scientist at FinTech Corp (2020-Present)
- Built credit risk models using ensemble methods
- Developed fraud detection system using XGBoost
- Created customer lifetime value prediction models

Data Analyst at BankInc (2018-2020)
- Performed financial data analysis and reporting
- Built dashboards for risk management
- Assisted in regulatory compliance reporting

Education:
M.S. in Data Science, Harvard University (2020)
B.S. in Economics, Brown University (2018)
"""
    },
    {
        "name": "Noah Garcia",
        "file": "resume_14_noah_garcia.txt",
        "text": """Noah Garcia
Email: noah.garcia@email.com | Phone: +1-555-0114

Professional Summary:
Machine Learning Engineer focused on MLOps and deploying ML systems at scale. Experience with cloud platforms and containerization.

Skills:
- Python, TensorFlow, PyTorch
- Docker, Kubernetes, Terraform
- AWS, GCP, Azure
- MLOps, CI/CD, GitOps
- SQL, Redis, MongoDB
- Scikit-learn, XGBoost
- Data Pipelines, Airflow
- Monitoring, Logging

Experience:
MLOps Engineer at CloudScale (2021-Present)
- Built ML platform for model deployment and monitoring
- Implemented automated model retraining pipelines
- Reduced model deployment time by 80% using CI/CD

ML Engineer at DataPlatform (2019-2021)
- Developed ML models for predictive maintenance
- Built feature engineering pipelines
- Created monitoring dashboards for model performance

Education:
M.S. in Computer Science, University of Michigan (2019)
B.S. in Electrical Engineering, Ohio State (2017)
"""
    },
    {
        "name": "Olivia Martinez",
        "file": "resume_15_olivia_martinez.txt",
        "text": """Olivia Martinez
Email: olivia.martinez@email.com | Phone: +1-555-0115

Professional Summary:
Data Analyst specializing in marketing analytics and customer insights. Expert in SQL, Excel, and data visualization tools.

Skills:
- SQL, Excel, Python
- Tableau, Power BI
- Data Analysis, Reporting
- Google Analytics, HubSpot
- A/B Testing, Experimentation
- Statistics, Data Visualization
- Marketing Analytics
- CRM Systems

Experience:
Marketing Analyst at BrandCorp (2021-Present)
- Analyzed marketing campaign performance using SQL
- Built customer segmentation models
- Created dashboards tracking KPIs and ROI

Data Analyst at AgencyX (2019-2021)
- Performed web analytics using Google Analytics
- Created monthly client reports and presentations
- Assisted in A/B testing for website optimization

Education:
B.S. in Marketing Analytics, University of Illinois (2019)
"""
    },
    {
        "name": "Peter Anderson",
        "file": "resume_16_peter_anderson.txt",
        "text": """Peter Anderson
Email: peter.anderson@email.com | Phone: +1-555-0116

Professional Summary:
Python Developer and Data Scientist with expertise in building ML-powered applications. Full-stack experience with Python frameworks.

Skills:
- Python, Django, Flask
- Machine Learning, Deep Learning
- TensorFlow, PyTorch, Scikit-learn
- React, JavaScript, HTML/CSS
- SQL, PostgreSQL
- Docker, AWS
- Pandas, NumPy
- REST APIs, GraphQL

Experience:
Full Stack ML Developer at AppGenius (2021-Present)
- Built ML-powered web applications using Django
- Deployed models as REST APIs on AWS
- Developed interactive data visualization components

Python Developer at CodeWorks (2019-2021)
- Developed backend services using Flask
- Integrated ML models into production systems
- Built data processing pipelines

Education:
B.S. in Computer Science, University of Texas (2019)
Bootcamp in Data Science, General Assembly (2019)
"""
    },
    {
        "name": "Quinn Thompson",
        "file": "resume_17_quinn_thompson.txt",
        "text": """Quinn Thompson
Email: quinn.thompson@email.com | Phone: +1-555-0117

Professional Summary:
Senior Data Scientist with 7 years of experience in ML and AI. Published author in top-tier journals and conferences.

Skills:
- Python, R, Julia
- Machine Learning, Deep Learning
- TensorFlow, PyTorch, JAX
- NLP, Transformers, LLMs
- Computer Vision, GANs
- Statistics, Bayesian Methods
- Big Data, Spark
- Research, Publications

Experience:
Principal Data Scientist at AI Research (2020-Present)
- Led research in large language models
- Published 10+ papers in NeurIPS, ICML, ICLR
- Mentored junior researchers and interns

Senior Data Scientist at TechGiant (2017-2020)
- Built production ML systems serving millions of users
- Developed novel algorithms for content recommendation
- Led team of 5 data scientists

Education:
Ph.D. in Machine Learning, MIT (2017)
M.S. in Computer Science, Stanford University (2013)
"""
    },
    {
        "name": "Rachel Kim",
        "file": "resume_18_rachel_kim.txt",
        "text": """Rachel Kim
Email: rachel.kim@email.com | Phone: +1-555-0118

Professional Summary:
Data Analyst experienced in healthcare analytics and operations. Skilled in SQL, Python, and business intelligence tools.

Skills:
- SQL, Python, SAS
- Excel, Power BI, Tableau
- Data Analysis, Reporting
- Statistics, Hypothesis Testing
- Healthcare Analytics
- Data Quality, Data Governance
- ETL, Data Warehousing
- Communication, Collaboration

Experience:
Healthcare Data Analyst at MedInsights (2021-Present)
- Analyzed patient outcomes data using SQL and Python
- Built dashboards for hospital performance metrics
- Conducted statistical analysis for clinical research

Data Analyst at HealthCorp (2019-2021)
- Maintained data quality in healthcare databases
- Created regulatory compliance reports
- Assisted in building data warehouse systems

Education:
M.S. in Health Informatics, Johns Hopkins University (2021)
B.S. in Biology, University of Pennsylvania (2019)
"""
    },
    {
        "name": "Samuel Jackson",
        "file": "resume_19_samuel_jackson.txt",
        "text": """Samuel Jackson
Email: samuel.jackson@email.com | Phone: +1-555-0119

Professional Summary:
Machine Learning Engineer experienced in building real-time ML systems. Expert in TensorFlow, Kafka, and stream processing.

Skills:
- Python, TensorFlow, PyTorch
- Spark, Kafka, Flink
- Real-time ML, Streaming
- Docker, Kubernetes
- AWS Kinesis, Lambda
- SQL, Cassandra
- Scikit-learn, XGBoost
- Data Engineering

Experience:
ML Engineer at RealTimeAI (2021-Present)
- Built real-time fraud detection system using Kafka and TensorFlow
- Implemented streaming feature engineering pipelines
- Deployed models using TensorFlow Serving and Kubernetes

Data Engineer at StreamData (2019-2021)
- Built real-time data pipelines using Kafka
- Implemented stream processing using Apache Flink
- Maintained production data infrastructure

Education:
M.S. in Data Engineering, University of Wisconsin (2019)
B.S. in Computer Science, Purdue University (2017)
"""
    },
    {
        "name": "Tina Brown",
        "file": "resume_20_tina_brown.txt",
        "text": """Tina Brown
Email: tina.brown@email.com | Phone: +1-555-0120

Professional Summary:
Data Scientist with expertise in NLP and deep learning. Passionate about using AI for social good and ethical AI.

Skills:
- Python, TensorFlow, PyTorch
- NLP, Transformers, BERT
- Deep Learning, Neural Networks
- Machine Learning, Statistics
- SQL, BigQuery
- Fairness in AI, Ethics
- Scikit-learn, Pandas, NumPy
- Data Visualization

Experience:
Data Scientist at SocialGood AI (2021-Present)
- Developed NLP models for content moderation
- Built bias detection and fairness evaluation tools
- Created educational resources for ethical AI

Data Scientist at ResearchLab (2019-2021)
- Applied ML to environmental sustainability projects
- Built text classification systems for document analysis
- Collaborated on interdisciplinary research projects

Education:
M.S. in Data Science, UC Berkeley (2019)
B.S. in Statistics, Duke University (2017)
"""
    },
    {
        "name": "Uma Patel",
        "file": "resume_21_uma_patel.txt",
        "text": """Uma Patel
Email: uma.patel@email.com | Phone: +1-555-0121

Professional Summary:
Python Developer with experience in machine learning and data engineering. Full-stack capabilities with Python and JavaScript.

Skills:
- Python, JavaScript, TypeScript
- Django, FastAPI, Flask
- SQL, PostgreSQL, MySQL
- React, Node.js
- Docker, AWS, GCP
- Pandas, NumPy, Scikit-learn
- Git, CI/CD
- REST APIs, GraphQL

Experience:
Full Stack Developer at WebDev Pro (2021-Present)
- Built full-stack web applications using Django and React
- Implemented data visualization features using D3.js
- Deployed applications on AWS using Docker

Python Developer at CodeHouse (2019-2021)
- Developed backend microservices using FastAPI
- Built data processing scripts using Pandas
- Integrated third-party APIs and services

Education:
B.S. in Computer Science, University of Texas (2019)
"""
    },
    {
        "name": "Victor Chen",
        "file": "resume_22_victor_chen.txt",
        "text": """Victor Chen
Email: victor.chen@email.com | Phone: +1-555-0122

Professional Summary:
Data Analyst with expertise in financial analysis and risk modeling. Strong analytical skills with Python, SQL, and Excel.

Skills:
- SQL, Python, VBA
- Excel, Power BI, Tableau
- Financial Analysis, Risk Modeling
- Statistics, Econometrics
- Data Analysis, Reporting
- A/B Testing
- Data Cleaning, ETL
- Bloomberg Terminal

Experience:
Financial Analyst at InvestmentBank (2021-Present)
- Built financial models for investment decisions
- Analyzed market trends using Python and SQL
- Created automated reporting dashboards

Data Analyst at FinanceCorp (2019-2021)
- Performed risk analysis using statistical models
- Generated quarterly performance reports
- Assisted in building predictive models for stock prices

Education:
M.S. in Financial Engineering, NYU (2021)
B.S. in Finance, University of Chicago (2019)
"""
    },
    {
        "name": "Wendy Foster",
        "file": "resume_23_wendy_foster.txt",
        "text": """Wendy Foster
Email: wendy.foster@email.com | Phone: +1-555-0123

Professional Summary:
Machine Learning Engineer specializing in NLP and text analytics. Experienced in building production-ready ML systems.

Skills:
- Python, TensorFlow, PyTorch
- NLP, SpaCy, NLTK
- Transformers, BERT, GPT
- Machine Learning, Deep Learning
- SQL, MongoDB, Elasticsearch
- Docker, AWS, GCP
- Scikit-learn, Pandas, NumPy
- Data Pipelines, Airflow

Experience:
NLP Engineer at TextAnalytics (2021-Present)
- Built document classification and information extraction systems
- Developed question-answering systems using BERT
- Implemented semantic search using Elasticsearch

ML Engineer at SearchEngine (2019-2021)
- Developed search relevance models
- Built text preprocessing and feature extraction pipelines
- Improved search ranking algorithms

Education:
M.S. in Computational Linguistics, Stanford University (2019)
B.S. in Linguistics, UC San Diego (2017)
"""
    },
]

job_descriptions = [
    {
        "title": "Data Scientist",
        "file": "jd_data_scientist.txt",
        "text": """Job Title: Data Scientist

Company: TechCorp
Location: San Francisco, CA
Employment Type: Full-time

Job Description:
We are looking for a talented Data Scientist to join our team. You will work on solving complex business problems using machine learning and statistical methods.

Responsibilities:
- Analyze large datasets to extract actionable insights
- Build and deploy machine learning models
- Design and conduct A/B experiments
- Communicate findings to stakeholders
- Collaborate with engineering teams to implement solutions

Required Skills:
- Python, SQL, R
- Machine Learning, Statistics
- Deep Learning, Neural Networks
- NLP, Text Analytics
- TensorFlow, PyTorch
- Scikit-learn, Pandas, NumPy
- Data Analysis, Data Visualization
- Power BI, Tableau
- Excel
- A/B Testing, Experimentation

Qualifications:
- MS or PhD in Data Science, Statistics, or related field
- 3+ years of experience in data science
- Strong communication and presentation skills
"""
    },
    {
        "title": "Machine Learning Engineer",
        "file": "jd_ml_engineer.txt",
        "text": """Job Title: Machine Learning Engineer

Company: AI Innovations
Location: New York, NY
Employment Type: Full-time

Job Description:
We are seeking a Machine Learning Engineer to design, build, and deploy ML systems at scale.

Responsibilities:
- Design and implement ML pipelines
- Deploy models to production environments
- Optimize model performance and latency
- Build monitoring and alerting for ML systems
- Collaborate with data scientists on model development

Required Skills:
- Python, TensorFlow, PyTorch
- Machine Learning, Deep Learning
- Docker, Kubernetes
- AWS, GCP or Azure
- SQL, NoSQL Databases
- Scikit-learn, Pandas, NumPy
- MLOps, CI/CD
- Data Pipelines, Airflow
- REST APIs, Microservices
- Git, Linux

Qualifications:
- MS in Computer Science, Machine Learning, or related field
- 3+ years of ML engineering experience
- Experience with production ML systems
"""
    },
    {
        "title": "Data Analyst",
        "file": "jd_data_analyst.txt",
        "text": """Job Title: Data Analyst

Company: Business Insights Inc
Location: Chicago, IL
Employment Type: Full-time

Job Description:
We are looking for a Data Analyst to help us make data-driven decisions. You will analyze data, create reports, and provide actionable insights.

Responsibilities:
- Collect and analyze data from multiple sources
- Create dashboards and reports using BI tools
- Identify trends and patterns in data
- Present findings to stakeholders
- Maintain data quality and documentation

Required Skills:
- SQL, Excel, Python
- Data Analysis, Data Visualization
- Power BI, Tableau
- Statistics, A/B Testing
- Data Cleaning, Data Quality
- Business Intelligence
- Communication, Presentation
- Google Analytics

Qualifications:
- BS in Statistics, Mathematics, Economics, or related field
- 2+ years of data analysis experience
- Strong analytical and problem-solving skills
"""
    },
    {
        "title": "Python Developer",
        "file": "jd_python_developer.txt",
        "text": """Job Title: Python Developer

Company: Software Solutions
Location: Seattle, WA
Employment Type: Full-time

Job Description:
We are seeking a skilled Python Developer to build and maintain our backend systems and applications.

Responsibilities:
- Develop and maintain Python applications
- Build REST APIs and microservices
- Design and optimize database schemas
- Write clean, testable, and efficient code
- Participate in code reviews and architecture discussions

Required Skills:
- Python, Django, Flask, FastAPI
- SQL, PostgreSQL, MySQL
- REST APIs, GraphQL
- Docker, Kubernetes
- AWS, GCP
- Git, CI/CD
- Pandas, NumPy
- Data Analysis, ETL
- JavaScript, HTML, CSS (Optional)
- Microservices Architecture

Qualifications:
- BS in Computer Science or related field
- 3+ years of Python development experience
- Strong understanding of software engineering principles
"""
    },
]

def write_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {filepath}")

def main():
    print("=" * 60)
    print("Generating Sample Resumes and Job Descriptions")
    print("=" * 60)

    # Write resumes
    print(f"\nGenerating {len(resumes)} resumes...")
    for r in resumes:
        filepath = os.path.join(RESUMES_DIR, r["file"])
        write_file(filepath, r["text"])

    # Write job descriptions
    print(f"\nGenerating {len(job_descriptions)} job descriptions...")
    for jd in job_descriptions:
        filepath = os.path.join(JOBS_DIR, jd["file"])
        write_file(filepath, jd["text"])

    print("\n" + "=" * 60)
    print("Sample data generation complete!")
    print(f"Resumes: {len(resumes)} files in {RESUMES_DIR}")
    print(f"Job Descriptions: {len(job_descriptions)} files in {JOBS_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    main()