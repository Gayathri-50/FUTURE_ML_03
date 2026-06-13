"""
Resume / Candidate Screening System - Modern ATS SaaS Dashboard
A professional interactive web dashboard for ATS-style Resume Screening.
Allows recruiters and HR managers to:
- Upload and screen resumes against job descriptions
- View ranked candidate lists with detailed scoring
- Analyze skill gaps and missing skills
- Generate visual reports
- Export results

Usage:
    streamlit run app.py
"""

import os
import sys
import io
import base64
import pandas as pd
import numpy as np
from typing import List, Set, Dict, Optional
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config MUST be first Streamlit command
st.set_page_config(
    page_title="SkillMatch AI - Resume Screening Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

from src.preprocess import TextPreprocessor
from src.skill_extractor import SkillExtractor, SKILL_REGISTRY, JOB_ROLE_SKILLS, SkillMatchResult
from src.ranking_model import ResumeRankingModel, CandidateRank, generate_sample_labels, evaluate_model
from src.visualization import (
    plot_top_candidate_scores,
    plot_skill_distribution,
    plot_match_percentage_chart,
    plot_missing_skills_heatmap,
    plot_confusion_matrix,
    ensure_chart_dir
)

# ============================================================
# CONSTANTS & CONFIGURATION
# ============================================================
SKILL_COLORS = {
    "Python": "#3776AB", "SQL": "#E38C00", "Machine Learning": "#FF6F00",
    "Deep Learning": "#4CAF50", "TensorFlow": "#FF6F00", "PyTorch": "#EE4C2C",
    "NLP": "#9C27B0", "Statistics": "#2196F3", "Power BI": "#F2C811",
    "Tableau": "#E97627", "Excel": "#217346", "Data Analysis": "#00ACC1",
    "Scikit-learn": "#F7931E", "Pandas": "#130654", "NumPy": "#013243",
    "Docker": "#2496ED", "Kubernetes": "#326CE5", "AWS": "#FF9900",
    "GCP": "#4285F4", "Azure": "#0089D6", "Computer Vision": "#E91E63",
    "Spark": "#E25A1C", "Git": "#F05032"
}

AVAILABLE_JOB_ROLES = list(JOB_ROLE_SKILLS.keys())
AVAILABLE_JD_FILES = {
    "Data Scientist": "data/job_descriptions/jd_data_scientist.txt",
    "Machine Learning Engineer": "data/job_descriptions/jd_ml_engineer.txt",
    "Data Analyst": "data/job_descriptions/jd_data_analyst.txt",
    "Python Developer": "data/job_descriptions/jd_python_developer.txt"
}

# ============================================================
# MODERN CSS WITH GLASSMORPHISM & DARK THEME
# ============================================================

def load_css():
    """Load custom CSS with dark theme and glassmorphism."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
        
        .stApp {
            background: #0F172A;
            background-image: 
                radial-gradient(ellipse at 20% 50%, rgba(59, 130, 246, 0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 20%, rgba(20, 184, 166, 0.06) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 80%, rgba(99, 102, 241, 0.05) 0%, transparent 50%);
        }
        
        .section-title {
            font-size: 1.3rem; font-weight: 700; color: #F1F5F9;
            margin-bottom: 1rem; padding-bottom: 0.5rem;
            border-bottom: 1px solid rgba(255,255,255,0.06);
            letter-spacing: -0.01em;
        }
        .section-subtitle {
            font-size: 0.85rem; color: #94A3B8;
            margin-top: -0.5rem; margin-bottom: 1.5rem;
        }

        /* Hero Section */
        .hero-section {
            background: linear-gradient(135deg, rgba(15,23,42,0.95) 0%, rgba(30,41,59,0.85) 100%);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px; padding: 2.5rem 3rem;
            margin-bottom: 2rem; position: relative; overflow: hidden;
        }
        .hero-section::before {
            content: '';
            position: absolute; top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: conic-gradient(from 0deg, transparent, rgba(59,130,246,0.03), transparent, rgba(20,184,166,0.03), transparent);
            animation: rotate 20s linear infinite;
        }
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .hero-content { position: relative; z-index: 1; }
        .hero-badge {
            display: inline-flex; align-items: center; gap: 0.4rem;
            background: rgba(59,130,246,0.15);
            border: 1px solid rgba(59,130,246,0.25);
            border-radius: 100px; padding: 0.3rem 1rem;
            font-size: 0.75rem; font-weight: 600; color: #60A5FA;
            margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.05em;
        }
        .hero-title {
            font-size: 2.8rem; font-weight: 800; color: #F1F5F9;
            margin: 0 0 0.8rem 0; line-height: 1.15; letter-spacing: -0.03em;
        }
        .hero-title .highlight {
            background: linear-gradient(135deg, #3B82F6, #14B8A6);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .hero-subtitle {
            font-size: 1.05rem; color: #94A3B8;
            margin: 0 0 1.5rem 0; line-height: 1.6; max-width: 650px;
        }
        .hero-stats { display: flex; gap: 2rem; flex-wrap: wrap; }
        .hero-stat {
            display: flex; align-items: center; gap: 0.5rem;
            color: #CBD5E1; font-size: 0.85rem;
        }
        .hero-stat .stat-icon {
            width: 32px; height: 32px; border-radius: 8px;
            display: flex; align-items: center; justify-content: center; font-size: 0.9rem;
        }
        .hero-stat .stat-icon.blue { background: rgba(59,130,246,0.15); }
        .hero-stat .stat-icon.teal { background: rgba(20,184,166,0.15); }
        .hero-stat .stat-icon.purple { background: rgba(99,102,241,0.15); }
        .hero-stat .stat-icon.amber { background: rgba(245,158,11,0.15); }

        /* KPI Cards */
        .kpi-card {
            background: rgba(30,41,59,0.6);
            backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 16px; padding: 1.5rem;
            transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
            position: relative; overflow: hidden;
        }
        .kpi-card::before {
            content: '';
            position: absolute; top: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, #3B82F6, #14B8A6);
            opacity: 0; transition: opacity 0.3s ease;
        }
        .kpi-card:hover {
            transform: translateY(-4px);
            border-color: rgba(255,255,255,0.12);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        .kpi-card:hover::before { opacity: 1; }
        .kpi-card .kpi-header {
            display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.8rem;
        }
        .kpi-card .kpi-icon {
            width: 42px; height: 42px; border-radius: 12px;
            display: flex; align-items: center; justify-content: center; font-size: 1.2rem;
        }
        .kpi-card .kpi-icon.blue { background: rgba(59,130,246,0.15); }
        .kpi-card .kpi-icon.teal { background: rgba(20,184,166,0.15); }
        .kpi-card .kpi-icon.purple { background: rgba(99,102,241,0.15); }
        .kpi-card .kpi-icon.amber { background: rgba(245,158,11,0.15); }
        .kpi-card .kpi-icon.green { background: rgba(34,197,94,0.15); }
        .kpi-card .kpi-icon.red { background: rgba(239,68,68,0.15); }
        .kpi-card .kpi-label {
            font-size: 0.8rem; font-weight: 500; color: #94A3B8;
            text-transform: uppercase; letter-spacing: 0.05em;
        }
        .kpi-card .kpi-value {
            font-size: 2rem; font-weight: 800; color: #F1F5F9;
            letter-spacing: -0.02em; line-height: 1.2;
        }
        .kpi-card .kpi-value .unit { font-size: 1rem; font-weight: 500; color: #64748B; }
        .kpi-card .kpi-change {
            display: inline-flex; align-items: center; gap: 0.25rem;
            font-size: 0.75rem; font-weight: 600; margin-top: 0.3rem;
            padding: 0.15rem 0.5rem; border-radius: 100px;
        }
        .kpi-card .kpi-change.positive { color: #22C55E; background: rgba(34,197,94,0.1); }
        .kpi-card .kpi-change.neutral { color: #94A3B8; background: rgba(148,163,184,0.1); }

        /* Glass Card */
        .glass-card {
            background: rgba(30,41,59,0.6);
            backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem;
            transition: all 0.3s ease;
        }
        .glass-card:hover { border-color: rgba(255,255,255,0.1); }
        .glass-card .card-header {
            display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;
        }
        .glass-card .card-title { font-size: 1rem; font-weight: 600; color: #F1F5F9; }

        /* Candidate Cards */
        .candidate-card-modern {
            background: rgba(30,41,59,0.5);
            backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 14px; padding: 1.2rem; margin-bottom: 0.7rem;
            transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
        }
        .candidate-card-modern:hover {
            transform: translateX(4px);
            border-color: rgba(59,130,246,0.3);
            box-shadow: 0 8px 24px rgba(0,0,0,0.2);
            background: rgba(30,41,59,0.7);
        }
        .candidate-card-modern .cand-header { display: flex; align-items: center; gap: 0.8rem; }
        .candidate-card-modern .rank-circle {
            width: 36px; height: 36px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-weight: 700; font-size: 0.85rem; flex-shrink: 0;
        }
        .rank-circle.gold {
            background: linear-gradient(135deg, #F59E0B, #D97706);
            color: #1E293B; box-shadow: 0 0 20px rgba(245,158,11,0.3);
        }
        .rank-circle.silver {
            background: linear-gradient(135deg, #94A3B8, #64748B);
            color: #0F172A; box-shadow: 0 0 20px rgba(148,163,184,0.2);
        }
        .rank-circle.bronze {
            background: linear-gradient(135deg, #CD7F32, #A0522D);
            color: #1E293B; box-shadow: 0 0 20px rgba(205,127,50,0.2);
        }
        .rank-circle.default {
            background: rgba(59,130,246,0.15);
            color: #60A5FA; border: 1px solid rgba(59,130,246,0.2);
        }
        .candidate-card-modern .cand-name { font-weight: 600; color: #F1F5F9; font-size: 0.95rem; }
        .candidate-card-modern .cand-file { font-size: 0.75rem; color: #64748B; }
        .candidate-card-modern .cand-score { text-align: right; }
        .candidate-card-modern .cand-score-value { font-size: 1.4rem; font-weight: 700; letter-spacing: -0.02em; }
        .candidate-card-modern .cand-score-label { font-size: 0.7rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; }
        .candidate-card-modern .cand-details { display: flex; gap: 1.5rem; margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(255,255,255,0.05); }
        .candidate-card-modern .cand-detail-item { font-size: 0.8rem; color: #94A3B8; }
        .candidate-card-modern .cand-detail-item strong { color: #E2E8F0; }

        /* Skill Tags */
        .skill-tag-modern {
            display: inline-flex; align-items: center; gap: 0.3rem;
            padding: 0.2rem 0.7rem; border-radius: 100px;
            font-size: 0.75rem; font-weight: 500; margin: 0.15rem;
        }
        .skill-tag-modern.match {
            background: rgba(34,197,94,0.12); color: #4ADE80;
            border: 1px solid rgba(34,197,94,0.2);
        }
        .skill-tag-modern.missing {
            background: rgba(239,68,68,0.12); color: #F87171;
            border: 1px solid rgba(239,68,68,0.2);
        }
        .skill-tag-modern.extra {
            background: rgba(99,102,241,0.12); color: #818CF8;
            border: 1px solid rgba(99,102,241,0.2);
        }

        /* ATS Gauge */
        .ats-gauge-container {
            background: rgba(30,41,59,0.6);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 16px; padding: 1.5rem; text-align: center;
        }
        .ats-gauge-container .gauge-title {
            font-size: 0.85rem; font-weight: 600; color: #94A3B8;
            text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;
        }

        /* Leaderboard */
        .leaderboard-item {
            display: flex; align-items: center; gap: 0.8rem;
            padding: 0.7rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);
            transition: all 0.2s ease;
        }
        .leaderboard-item:last-child { border-bottom: none; }
        .leaderboard-item:hover { padding-left: 0.5rem; }
        .leaderboard-item .lb-rank { width: 24px; font-weight: 700; font-size: 0.8rem; color: #64748B; text-align: center; }
        .leaderboard-item .lb-rank.gold { color: #F59E0B; }
        .leaderboard-item .lb-rank.silver { color: #94A3B8; }
        .leaderboard-item .lb-rank.bronze { color: #CD7F32; }
        .leaderboard-item .lb-avatar {
            width: 32px; height: 32px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-weight: 600; font-size: 0.75rem; flex-shrink: 0;
        }
        .leaderboard-item .lb-avatar.gold { background: linear-gradient(135deg,#F59E0B,#D97706); color: #0F172A; }
        .leaderboard-item .lb-avatar.silver { background: linear-gradient(135deg,#94A3B8,#64748B); color: #0F172A; }
        .leaderboard-item .lb-avatar.bronze { background: linear-gradient(135deg,#CD7F32,#A0522D); color: #0F172A; }
        .leaderboard-item .lb-avatar.default { background: rgba(59,130,246,0.15); color: #60A5FA; }
        .leaderboard-item .lb-name { flex: 1; font-weight: 500; font-size: 0.85rem; color: #E2E8F0; }
        .leaderboard-item .lb-score { font-weight: 700; font-size: 0.9rem; }

        /* Progress bar */
        .progress-bar-modern {
            width: 100%; height: 6px; background: rgba(255,255,255,0.06);
            border-radius: 100px; overflow: hidden; margin: 0.3rem 0;
        }
        .progress-bar-modern .progress-fill {
            height: 100%; border-radius: 100px; transition: width 1s ease;
            background: linear-gradient(90deg, #3B82F6, #14B8A6);
        }

        /* Status boxes */
        .status-box {
            border-radius: 12px; padding: 0.8rem 1rem; margin: 0.5rem 0;
            font-size: 0.85rem; border-left: 3px solid;
        }
        .status-box.info { background: rgba(59,130,246,0.08); border-left-color: #3B82F6; color: #93C5FD; }
        .status-box.success { background: rgba(34,197,94,0.08); border-left-color: #22C55E; color: #86EFAC; }
        .status-box.warning { background: rgba(245,158,11,0.08); border-left-color: #F59E0B; color: #FCD34D; }
        .status-box.error { background: rgba(239,68,68,0.08); border-left-color: #EF4444; color: #FCA5A5; }

        /* Tabs */
        .stTabs { margin-bottom: 1.5rem; }
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background: rgba(30,41,59,0.4);
            border-radius: 14px; padding: 0.3rem;
            border: 1px solid rgba(255,255,255,0.06);
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px; padding: 0.5rem 1.2rem;
            font-weight: 500; font-size: 0.85rem;
            color: #94A3B8; transition: all 0.2s ease; background: transparent;
        }
        .stTabs [aria-selected="true"] {
            background: rgba(59,130,246,0.15) !important;
            color: #60A5FA !important;
            border: 1px solid rgba(59,130,246,0.2) !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] { background: #0F172A; border-right: 1px solid rgba(255,255,255,0.06); }
        .sidebar-brand {
            text-align: center; padding: 1.5rem 1rem;
            border-bottom: 1px solid rgba(255,255,255,0.06); margin-bottom: 1rem;
        }
        .sidebar-brand .brand-icon { font-size: 2.2rem; margin-bottom: 0.3rem; }
        .sidebar-brand .brand-name { font-size: 1.2rem; font-weight: 700; color: #F1F5F9; }
        .sidebar-brand .brand-tagline { font-size: 0.75rem; color: #64748B; }
        .sidebar-section {
            padding: 0 1rem 0.5rem;
            font-size: 0.7rem; font-weight: 600; color: #64748B;
            text-transform: uppercase; letter-spacing: 0.08em;
        }

        /* Buttons */
        .stButton button {
            border-radius: 10px !important; font-weight: 600 !important;
            font-size: 0.85rem !important; padding: 0.5rem 1.2rem !important;
            transition: all 0.3s ease !important; border: none !important;
        }
        .stButton button[kind="primary"] {
            background: linear-gradient(135deg, #3B82F6, #2563EB) !important;
            color: white !important;
            box-shadow: 0 4px 15px rgba(59,130,246,0.3) !important;
        }
        .stButton button[kind="primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(59,130,246,0.4) !important;
        }
        .stButton button[kind="primary"]:disabled { opacity: 0.4 !important; }

        /* Select, Input, Radio */
        .stSelectbox label, .stRadio label, .stCheckbox label { color: #94A3B8 !important; font-weight: 500 !important; }
        div[data-baseweb="select"] > div {
            background: rgba(30,41,59,0.6) !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 10px !important; color: #E2E8F0 !important;
        }
        div[data-baseweb="select"] > div:hover { border-color: rgba(59,130,246,0.3) !important; }
        .stTextInput input {
            background: rgba(30,41,59,0.6) !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 10px !important; color: #E2E8F0 !important;
        }
        .stTextInput input:focus {
            border-color: #3B82F6 !important;
            box-shadow: 0 0 0 2px rgba(59,130,246,0.15) !important;
        }
        .stSlider label { color: #94A3B8 !important; }
        div[data-testid="stThumbValue"] { background: #3B82F6 !important; color: white !important; }
        div[role="radiogroup"] {
            background: rgba(30,41,59,0.4); border-radius: 10px; padding: 0.3rem;
            border: 1px solid rgba(255,255,255,0.06);
        }
        div[role="radiogroup"] label {
            border-radius: 8px !important; padding: 0.4rem 1rem !important; color: #94A3B8 !important;
        }
        div[role="radiogroup"] label[aria-checked="true"] {
            background: rgba(59,130,246,0.15) !important; color: #60A5FA !important;
        }

        /* Dataframes */
        .stDataFrame { border-radius: 12px !important; overflow: hidden !important; }
        .stDataFrame [data-testid="stTable"] { background: rgba(30,41,59,0.4) !important; }
        .stDataFrame table { background: transparent !important; }
        .stDataFrame th {
            background: rgba(30,41,59,0.8) !important; color: #94A3B8 !important;
            font-weight: 600 !important; font-size: 0.8rem !important;
            text-transform: uppercase !important; letter-spacing: 0.05em !important;
            border-bottom: 1px solid rgba(255,255,255,0.06) !important;
        }
        .stDataFrame td {
            color: #E2E8F0 !important;
            border-bottom: 1px solid rgba(255,255,255,0.03) !important;
        }
        .stMetric label { color: #94A3B8 !important; }
        .stMetric .css-1wivap2 { color: #F1F5F9 !important; }
        .stFileUploader div {
            background: rgba(30,41,59,0.4) !important;
            border: 1px dashed rgba(255,255,255,0.1) !important;
            border-radius: 12px !important;
        }
        .stFileUploader div:hover { border-color: rgba(59,130,246,0.3) !important; }
        .stSpinner > div { border-color: #3B82F6 !important; }
        .st-emotion-cache-1dj0hjr {
            background: rgba(30,41,59,0.4) !important;
            border: 1px solid rgba(255,255,255,0.06) !important;
            border-radius: 12px !important;
        }
        .footer-modern {
            text-align: center; padding: 1.5rem; color: #475569;
            font-size: 0.8rem; border-top: 1px solid rgba(255,255,255,0.05); margin-top: 2rem;
        }
        .chart-container {
            background: rgba(30,41,59,0.4); border-radius: 14px;
            padding: 1rem; border: 1px solid rgba(255,255,255,0.06); margin-bottom: 1rem;
        }
        @keyframes shimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        .loading-skeleton {
            background: linear-gradient(90deg, rgba(30,41,59,0.4) 25%, rgba(30,41,59,0.6) 50%, rgba(30,41,59,0.4) 75%);
            background-size: 200% 100%; animation: shimmer 1.5s infinite;
            border-radius: 12px; height: 100px; margin-bottom: 1rem;
        }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: rgba(15,23,42,0.5); }
        ::-webkit-scrollbar-thumb { background: rgba(59,130,246,0.3); border-radius: 100px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(59,130,246,0.5); }
        </style>
    """, unsafe_allow_html=True)


def get_base64_encoded_image(image_path: str) -> str:
    """Get base64 encoded string from an image file."""
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def render_skill_tags_modern(skills: List[str], skill_type: str = "match") -> str:
    """Render HTML for modern skill tags."""
    if not skills:
        return "<span style='color:#64748B;font-size:0.8rem;'>None</span>"
    tags = []
    for skill in skills[:12]:
        color = SKILL_COLORS.get(skill, "#5C6BC0")
        tags.append(
            f'<span class="skill-tag-modern {skill_type}" style="background:{color}22;border-color:{color}44;color:{color};">{skill}</span>'
        )
    if len(skills) > 12:
        tags.append(f'<span style="font-size:0.75rem;color:#64748B;">+{len(skills)-12} more</span>')
    return " ".join(tags)


def get_rank_circle_class(rank: int) -> str:
    """Get CSS class for rank circle."""
    if rank == 1: return "gold"
    elif rank == 2: return "silver"
    elif rank == 3: return "bronze"
    return "default"


def get_score_color(score: float) -> str:
    """Get color based on score."""
    if score >= 80: return "#4ADE80"
    elif score >= 60: return "#60A5FA"
    elif score >= 40: return "#FBBF24"
    else: return "#F87171"


def scrape_jd_from_text(text: str) -> tuple:
    """Extract job title and skills from JD text."""
    lines = text.strip().split('\n')
    title = "Custom Job Description"
    for line in lines[:5]:
        if 'job title' in line.lower():
            title = line.split(':', 1)[-1].strip()
            break
    extractor = SkillExtractor(SKILL_REGISTRY)
    skills = extractor.extract_skills(text)
    return title, sorted(skills)


def initialize_session_state():
    """Initialize session state variables."""
    if 'rankings' not in st.session_state:
        st.session_state.rankings = None
    if 'jd_title' not in st.session_state:
        st.session_state.jd_title = ""
    if 'required_skills' not in st.session_state:
        st.session_state.required_skills = []
    if 'model_initialized' not in st.session_state:
        st.session_state.model_initialized = False
    if 'processing_done' not in st.session_state:
        st.session_state.processing_done = False
    if 'metrics' not in st.session_state:
        st.session_state.metrics = None
    if 'tab' not in st.session_state:
        st.session_state.tab = "Screening"


def render_hero_section():
    """Render modern hero section."""
    st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <div class="hero-badge">🚀 Next-Gen ATS Platform</div>
            <h1 class="hero-title">AI Resume <span class="highlight">Screening Platform</span></h1>
            <p class="hero-subtitle">Automatically screen, rank and analyze candidates using Natural Language Processing and Machine Learning. Make data-driven hiring decisions with intelligent ATS scoring.</p>
            <div class="hero-stats">
                <div class="hero-stat">
                    <div class="stat-icon blue">🤖</div>
                    <span>NLP-Powered Analysis</span>
                </div>
                <div class="hero-stat">
                    <div class="stat-icon teal">🎯</div>
                    <span>Smart ATS Scoring</span>
                </div>
                <div class="hero-stat">
                    <div class="stat-icon purple">📊</div>
                    <span>Skill Gap Analysis</span>
                </div>
                <div class="hero-stat">
                    <div class="stat-icon amber">⚡</div>
                    <span>Real-time Ranking</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_kpi_card(icon_class: str, label: str, value: str, change: str = "", change_class: str = ""):
    """Render a KPI card with glassmorphism."""
    return f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <div class="kpi-icon {icon_class}">{icon_class.replace('blue','📊').replace('teal','🎯').replace('purple','🧠').replace('amber','⭐').replace('green','📈').replace('red','🔍')[:2]}</div>
        </div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {'<div class="kpi-change ' + change_class + '">' + change + '</div>' if change else ''}
    </div>
    """


def render_ats_gauge(score: float, label: str = "ATS Score"):
    """Render an ATS score gauge using plotly."""
    # Determine color
    if score >= 80: color = "#4ADE80"
    elif score >= 60: color = "#60A5FA"
    elif score >= 40: color = "#FBBF24"
    else: color = "#F87171"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        number={"font": {"size": 36, "color": "#F1F5F9"}, "suffix": "%"},
        delta={"reference": 50, "font": {"size": 14}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#64748B", "tickfont": {"size": 10, "color": "#94A3B8"}},
            "bar": {"color": color, "thickness": 0.4},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 30], "color": "rgba(239,68,68,0.15)"},
                {"range": [30, 60], "color": "rgba(251,191,36,0.15)"},
                {"range": [60, 80], "color": "rgba(96,165,250,0.15)"},
                {"range": [80, 100], "color": "rgba(74,222,128,0.15)"},
            ],
            "threshold": {
                "line": {"color": "#F1F5F9", "width": 2},
                "thickness": 0.6,
                "value": score
            }
        },
        title={"text": label, "font": {"size": 14, "color": "#94A3B8"}}
    ))
    fig.update_layout(
        height=220,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#94A3B8"}
    )
    return fig


def render_leaderboard_item(rank: int, name: str, score: float, is_current_user: bool = False):
    """Render a leaderboard item."""
    rank_class = "gold" if rank == 1 else ("silver" if rank == 2 else ("bronze" if rank == 3 else "default"))
    initials = "".join([w[0] for w in name.split()[:2]]).upper()
    score_color = get_score_color(score)
    return f"""
    <div class="leaderboard-item">
        <div class="lb-rank {rank_class}">#{rank}</div>
        <div class="lb-avatar {rank_class}">{initials}</div>
        <div class="lb-name">{name}</div>
        <div class="lb-score" style="color:{score_color};">{score:.1f}%</div>
    </div>
    """


def render_ranking_table(rankings: List[CandidateRank]):
    """Render the ranking table with modern styling using plotly."""
    df_table = pd.DataFrame([{
        'Rank': r.rank,
        'Candidate': r.candidate_name,
        'ATS Score': round(r.combined_score, 1),
        'Match %': round(r.skill_match_score, 1),
        'Similarity': round(r.similarity_score, 1),
        'Missing Skills': len(r.missing_skills),
        'Total Skills': len(r.candidate_skills)
    } for r in rankings])
    
    return df_table


def show_plotly_chart(fig, use_container_width=True):
    """Display a plotly chart with proper styling."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#94A3B8", "family": "Inter, sans-serif"},
        title_font={"color": "#F1F5F9", "size": 14},
        legend={"font": {"color": "#94A3B8"}},
        xaxis={"gridcolor": "rgba(255,255,255,0.05)", "zerolinecolor": "rgba(255,255,255,0.05)"},
        yaxis={"gridcolor": "rgba(255,255,255,0.05)", "zerolinecolor": "rgba(255,255,255,0.05)"}
    )
    st.plotly_chart(fig, use_container_width=use_container_width)


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():
    """Main application entry point."""
    initialize_session_state()
    load_css()
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand">
            <div class="brand-icon">🎯</div>
            <div class="brand-name">SkillMatch AI</div>
            <div class="brand-tagline">Intelligent Resume Screening</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-section">Configuration</div>', unsafe_allow_html=True)
        
        # Job role selection
        st.markdown("#### 📋 Job Role")
        role_option = st.selectbox(
            "Job Role",
            ["Custom (Upload JD)"] + AVAILABLE_JOB_ROLES,
            label_visibility="collapsed"
        )
        
        # JD selection
        st.markdown("#### 📄 Job Description")
        jd_text = ""
        jd_file_path = None
        
        if role_option == "Custom (Upload JD)":
            uploaded_jd = st.file_uploader(
                "Upload JD (.txt)",
                type=['txt'],
                label_visibility="collapsed"
            )
            if uploaded_jd:
                jd_text = uploaded_jd.getvalue().decode('utf-8')
                st.markdown(f'<div class="status-box success">✅ Loaded: {uploaded_jd.name}</div>', unsafe_allow_html=True)
        else:
            jd_file_path = AVAILABLE_JD_FILES.get(role_option)
            if jd_file_path and os.path.exists(jd_file_path):
                with open(jd_file_path, 'r', encoding='utf-8') as f:
                    jd_text = f.read()
                st.markdown(f'<div class="status-box success">✅ Using: {role_option}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-box error">❌ JD file not found</div>', unsafe_allow_html=True)
        
        # Resume selection
        st.markdown("#### 📁 Resumes")
        resume_source = st.radio(
            "Resume Source",
            ["Sample Resumes (23)", "Upload Custom"],
            label_visibility="collapsed"
        )
        
        resume_dir = "data/resumes"
        custom_resumes = []
        
        if resume_source == "Upload Custom":
            uploaded_files = st.file_uploader(
                "Upload resumes (.txt, .pdf)",
                type=['txt', 'pdf'],
                accept_multiple_files=True,
                label_visibility="collapsed"
            )
            if uploaded_files:
                for f in uploaded_files:
                    custom_resumes.append({
                        'name': f.name.replace('.txt', '').replace('.pdf', '').replace('_', ' ').title(),
                        'file': f.name,
                        'text': f.getvalue().decode('utf-8')
                    })
                st.markdown(f'<div class="status-box success">✅ {len(custom_resumes)} uploaded</div>', unsafe_allow_html=True)
        
        # Job role skills checkbox
        use_predefined_skills = False
        if role_option in AVAILABLE_JOB_ROLES:
            use_predefined_skills = st.checkbox(
                f"Use {role_option} skill set",
                value=True
            )
        
        # Run button
        st.markdown("---")
        run_button = st.button(
            "🎯 SCREEN CANDIDATES",
            type="primary",
            use_container_width=True,
            disabled=(not jd_text)
        )
        
        if not jd_text:
            st.markdown('<div class="status-box info">ℹ️ Select a role or upload a JD</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(
            '<div style="font-size:0.75rem;color:#475569;text-align:center;">'
            'Built with ❤️ using Python & Streamlit<br>'
            'FUTURE_ML_03'
            '</div>',
            unsafe_allow_html=True
        )
    
    # Main content
    render_hero_section()
    
    # Run screening
    if run_button and jd_text:
        with st.spinner("🔄 Processing resumes..."):
            try:
                # Set required skills
                required_skills = None
                if role_option in AVAILABLE_JOB_ROLES and use_predefined_skills:
                    required_skills = JOB_ROLE_SKILLS[role_option]
                
                # Determine resume list
                if resume_source == "Upload Custom" and custom_resumes:
                    resume_list = custom_resumes
                    resume_dir_actual = None
                else:
                    resume_list = None
                    resume_dir_actual = resume_dir
                
                # Initialize model
                model = ResumeRankingModel()
                
                if resume_list:
                    if required_skills is None:
                        extractor = SkillExtractor(SKILL_REGISTRY)
                        required_skills = extractor.extract_skills(jd_text)
                    
                    jd_title = "Custom Job Description"
                    lines = jd_text.strip().split('\n')
                    for line in lines[:5]:
                        if 'job title' in line.lower():
                            jd_title = line.split(':', 1)[-1].strip()
                            break
                    
                    all_texts = [r['text'] for r in resume_list] + [jd_text]
                    model.fit_tfidf(all_texts)
                    rankings = model.rank_candidates(resume_list, jd_text, required_skills or set())
                else:
                    jd_file = jd_file_path or "data/job_descriptions/temp_jd.txt"
                    if role_option == "Custom (Upload JD)":
                        os.makedirs("data/job_descriptions", exist_ok=True)
                        jd_file = "data/job_descriptions/temp_jd.txt"
                        with open(jd_file, 'w', encoding='utf-8') as f:
                            f.write(jd_text)
                    
                    rankings, jd_title = model.batch_process(
                        resume_dir=resume_dir_actual,
                        jd_file=jd_file,
                        required_skills=required_skills
                    )
                
                # Store in session state
                st.session_state.rankings = rankings
                st.session_state.jd_title = jd_title
                st.session_state.processing_done = True
                
                if required_skills:
                    jd_skills = sorted(required_skills)
                else:
                    extractor = SkillExtractor(SKILL_REGISTRY)
                    jd_skills = sorted(extractor.extract_skills(jd_text))
                st.session_state.required_skills = jd_skills
                
                y_true, y_pred = generate_sample_labels(rankings, threshold=50.0)
                st.session_state.metrics = evaluate_model(y_true, y_pred)
                
                st.markdown(f'<div class="status-box success">✅ Screening complete! {len(rankings)} candidates processed for "{jd_title}"</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.markdown(f'<div class="status-box error">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
                st.exception(e)
    
    # Display results if available
    if st.session_state.processing_done and st.session_state.rankings:
        rankings = st.session_state.rankings
        jd_title = st.session_state.jd_title
        required_skills = st.session_state.required_skills
        metrics = st.session_state.metrics
        
        # KPI Cards Row
        st.markdown('<div class="section-title">📊 Screening Overview</div>', unsafe_allow_html=True)
        kpi_cols = st.columns(5)
        
        # Calculate KPIs
        avg_combined = np.mean([r.combined_score for r in rankings])
        avg_skill = np.mean([r.skill_match_score for r in rankings])
        avg_similarity = np.mean([r.similarity_score for r in rankings])
        top_score = rankings[0].combined_score
        
        with kpi_cols[0]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <div class="kpi-icon amber">🏆</div>
                </div>
                <div class="kpi-label">Top Candidate</div>
                <div class="kpi-value">{rankings[0].candidate_name[:15]}..</div>
                <div class="kpi-change positive">Score: {top_score:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with kpi_cols[1]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <div class="kpi-icon blue">📊</div>
                </div>
                <div class="kpi-label">Avg Combined Score</div>
                <div class="kpi-value">{avg_combined:.1f}<span class="unit">%</span></div>
                <div class="kpi-change neutral">Across {len(rankings)} candidates</div>
            </div>
            """, unsafe_allow_html=True)
        
        with kpi_cols[2]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <div class="kpi-icon teal">🧠</div>
                </div>
                <div class="kpi-label">Avg Skill Match</div>
                <div class="kpi-value">{avg_skill:.1f}<span class="unit">%</span></div>
                <div class="kpi-change positive">+{avg_skill - avg_similarity:.1f}% vs TF-IDF</div>
            </div>
            """, unsafe_allow_html=True)
        
        with kpi_cols[3]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <div class="kpi-icon purple">📈</div>
                </div>
                <div class="kpi-label">Score Range</div>
                <div class="kpi-value">{rankings[-1].combined_score:.0f}-{top_score:.0f}<span class="unit">%</span></div>
                <div class="kpi-change neutral">Spread: {top_score - rankings[-1].combined_score:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with kpi_cols[4]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <div class="kpi-icon green">🔍</div>
                </div>
                <div class="kpi-label">Required Skills</div>
                <div class="kpi-value">{len(required_skills)}</div>
                <div class="kpi-change neutral">Skills tracked</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🏆 Rankings", "🔍 Skill Analysis", "📈 Charts", 
            "📊 Evaluation", "📥 Export"
        ])
        
        with tab1:
            show_rankings_tab(rankings, jd_title, required_skills)
        
        with tab2:
            show_skill_analysis_tab(rankings, required_skills)
        
        with tab3:
            show_visualizations_tab(rankings, required_skills, metrics)
        
        with tab4:
            show_evaluation_tab(metrics, rankings)
        
        with tab5:
            show_export_tab(rankings, required_skills, metrics)
    
    else:
        show_welcome_screen()
    
    # Footer
    st.markdown('<div class="footer-modern">SkillMatch AI &copy; 2026 | Built with Python, Streamlit & Scikit-learn | NLP-Powered Resume Screening</div>', unsafe_allow_html=True)


# ============================================================
# TAB FUNCTIONS
# ============================================================

def show_welcome_screen():
    """Show welcome screen when no results are available."""
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color:#F1F5F9;margin:0 0 0.8rem 0;">👋 Welcome to SkillMatch AI</h3>
            <p style="color:#94A3B8;font-size:0.9rem;line-height:1.6;">
            This AI-powered platform helps recruiters and HR managers automatically screen, 
            score, and rank candidates based on job requirements. It uses <strong>Natural Language 
            Processing (NLP)</strong> and <strong>Machine Learning</strong> to evaluate resume fit.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        features_col1, features_col2 = st.columns(2)
        with features_col1:
            st.markdown("""
            <div class="glass-card" style="padding:1rem;">
                <div style="font-size:1.2rem;margin-bottom:0.3rem;">📄</div>
                <div style="font-weight:600;color:#F1F5F9;font-size:0.9rem;">Resume Parsing</div>
                <div style="color:#64748B;font-size:0.8rem;">Extract text from TXT/PDF</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class="glass-card" style="padding:1rem;">
                <div style="font-size:1.2rem;margin-bottom:0.3rem;">🧠</div>
                <div style="font-weight:600;color:#F1F5F9;font-size:0.9rem;">Skill Extraction</div>
                <div style="color:#64748B;font-size:0.8rem;">Auto-identify 35+ skills</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class="glass-card" style="padding:1rem;">
                <div style="font-size:1.2rem;margin-bottom:0.3rem;">🔬</div>
                <div style="font-weight:600;color:#F1F5F9;font-size:0.9rem;">TF-IDF Analysis</div>
                <div style="color:#64748B;font-size:0.8rem;">Semantic similarity scoring</div>
            </div>
            """, unsafe_allow_html=True)
        with features_col2:
            st.markdown("""
            <div class="glass-card" style="padding:1rem;">
                <div style="font-size:1.2rem;margin-bottom:0.3rem;">📊</div>
                <div style="font-weight:600;color:#F1F5F9;font-size:0.9rem;">Smart Ranking</div>
                <div style="color:#64748B;font-size:0.8rem;">40% TF-IDF + 60% Skills</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class="glass-card" style="padding:1rem;">
                <div style="font-size:1.2rem;margin-bottom:0.3rem;">🔍</div>
                <div style="font-weight:600;color:#F1F5F9;font-size:0.9rem;">Skill Gap Analysis</div>
                <div style="color:#64748B;font-size:0.8rem;">Identify missing skills</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class="glass-card" style="padding:1rem;">
                <div style="font-size:1.2rem;margin-bottom:0.3rem;">📥</div>
                <div style="font-weight:600;color:#F1F5F9;font-size:0.9rem;">Export Reports</div>
                <div style="color:#64748B;font-size:0.8rem;">Download CSV summaries</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:2rem;">
            <div style="font-size:3rem;margin-bottom:1rem;">🎯</div>
            <h3 style="color:#F1F5F9;margin:0 0 1rem 0;">Getting Started</h3>
            <div style="color:#94A3B8;font-size:0.85rem;line-height:1.6;">
            1. Select a job role from the sidebar<br>
            2. Configure your screening preferences<br>
            3. Click "Screen Candidates"<br>
            4. Review rankings and insights
            </div>
            <div style="margin-top:1.5rem;padding:1rem;background:rgba(59,130,246,0.08);border-radius:12px;">
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;">
                    <div><div style="font-size:1.8rem;font-weight:700;color:#F1F5F9;">23</div><div style="font-size:0.75rem;color:#64748B;">Sample Resumes</div></div>
                    <div><div style="font-size:1.8rem;font-weight:700;color:#F1F5F9;">4</div><div style="font-size:0.75rem;color:#64748B;">Job Roles</div></div>
                    <div><div style="font-size:1.8rem;font-weight:700;color:#F1F5F9;">35+</div><div style="font-size:0.75rem;color:#64748B;">Skills Tracked</div></div>
                    <div><div style="font-size:1.8rem;font-weight:700;color:#F1F5F9;">5</div><div style="font-size:0.75rem;color:#64748B;">Chart Types</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def show_rankings_tab(rankings: List[CandidateRank], jd_title: str, required_skills: List[str]):
    """Display candidate rankings with modern UI."""
    st.markdown(f'<div class="section-title">🏆 Candidate Rankings for: {jd_title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle">Total Candidates: {len(rankings)} · Required Skills: {len(required_skills)}</div>', unsafe_allow_html=True)
    
    # Left: ATS Gauge + Leaderboard | Right: Ranking Table
    rank_col1, rank_col2 = st.columns([1, 2])
    
    with rank_col1:
        # ATS Gauge for top candidate
        st.markdown('<div class="ats-gauge-container">', unsafe_allow_html=True)
        fig = render_ats_gauge(rankings[0].combined_score, f"🏆 {rankings[0].candidate_name}")
        show_plotly_chart(fig)
        
        # Top 5 Leaderboard
        st.markdown("""
        <div style="margin-top:0.5rem;">
            <div style="font-size:0.85rem;font-weight:600;color:#94A3B8;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.5rem;">
                🥇 Top Candidates
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        for r in rankings[:5]:
            st.markdown(render_leaderboard_item(r.rank, r.candidate_name, r.combined_score), unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with rank_col2:
        # Filter bar
        col_f1, col_f2 = st.columns([1, 1])
        with col_f1:
            search_term = st.text_input("🔍", placeholder="Search candidate...", label_visibility="collapsed")
        with col_f2:
            min_score = st.slider("Min ATS Score", 0, 100, 0, label_visibility="collapsed")
        
        # Filter
        display_rankings = rankings
        if search_term:
            display_rankings = [r for r in rankings if search_term.lower() in r.candidate_name.lower()]
        if min_score > 0:
            display_rankings = [r for r in display_rankings if r.combined_score >= min_score]
        
        # Ranking table
        df_table = render_ranking_table(display_rankings)
        
        # Color rank column
        def color_rank(val):
            if val == 1: return 'color: #F59E0B; font-weight: 800;'
            elif val == 2: return 'color: #94A3B8; font-weight: 700;'
            elif val == 3: return 'color: #CD7F32; font-weight: 700;'
            return 'color: #64748B;'
        
        def color_score(val):
            if val >= 80: return 'color: #4ADE80; font-weight: 700;'
            elif val >= 60: return 'color: #60A5FA; font-weight: 600;'
            elif val >= 40: return 'color: #FBBF24; font-weight: 600;'
            return 'color: #F87171; font-weight: 600;'
        
        styled_df = df_table.style.applymap(color_rank, subset=['Rank'])\
                                  .applymap(color_score, subset=['ATS Score'])\
                                  .applymap(color_score, subset=['Match %'])\
                                  .applymap(color_score, subset=['Similarity'])
        
        st.dataframe(styled_df, use_container_width=True, height=min(400, 35 * len(display_rankings)))
        
        # Export button for rankings
        csv_data = df_table.to_csv(index=False)
        b64_csv = base64.b64encode(csv_data.encode()).decode()
        st.markdown(f'''
        <div style="text-align:right;margin-top:0.5rem;">
            <a href="data:file/csv;base64,{b64_csv}" download="candidate_rankings.csv" style="
                display:inline-flex;align-items:center;gap:0.4rem;
                background:rgba(59,130,246,0.1);color:#60A5FA;
                padding:0.4rem 1rem;border-radius:8px;
                font-size:0.8rem;font-weight:500;text-decoration:none;
                border:1px solid rgba(59,130,246,0.2);
                transition:all 0.2s ease;
            " onmouseover="this.style.background='rgba(59,130,246,0.2)'" onmouseout="this.style.background='rgba(59,130,246,0.1)'">
            📥 Export CSV
            </a>
        </div>
        ''', unsafe_allow_html=True)
    
    # Candidate detail cards
    st.markdown(f'<div class="section-title" style="margin-top:1rem;">👤 Candidate Profiles</div>', unsafe_allow_html=True)
    
    top_n = st.selectbox("Show top N candidates", [3, 5, 10, 15, 20], index=1, label_visibility="collapsed")
    
    for rank in display_rankings[:top_n]:
        score_color = get_score_color(rank.combined_score)
        rank_class = get_rank_circle_class(rank.rank)
        
        st.markdown(f"""
        <div class="candidate-card-modern">
            <div class="cand-header">
                <div class="rank-circle {rank_class}">#{rank.rank}</div>
                <div style="flex:1;">
                    <div class="cand-name">{rank.candidate_name}</div>
                    <div class="cand-file">{rank.resume_file if rank.resume_file else 'Uploaded Resume'}</div>
                </div>
                <div class="cand-score">
                    <div class="cand-score-value" style="color:{score_color};">{rank.combined_score:.1f}%</div>
                    <div class="cand-score-label">ATS Score</div>
                </div>
            </div>
            <div class="cand-details">
                <div class="cand-detail-item">TF-IDF: <strong>{rank.similarity_score:.1f}%</strong></div>
                <div class="cand-detail-item">Skill Match: <strong>{rank.skill_match_score:.1f}%</strong></div>
                <div class="cand-detail-item">Skills: <strong>{len(rank.candidate_skills)}</strong></div>
                <div class="cand-detail-item">Match: <strong>{len(rank.matching_skills)}</strong></div>
                <div class="cand-detail-item">Gap: <strong>{len(rank.missing_skills)}</strong></div>
            </div>
            <div style="margin-top:0.5rem;">
                <span style="font-size:0.75rem;color:#64748B;">✅ Matching:</span><br>
                {render_skill_tags_modern(rank.matching_skills, "match")}
            </div>
            <div style="margin-top:0.3rem;">
                <span style="font-size:0.75rem;color:#64748B;">❌ Missing:</span><br>
                {render_skill_tags_modern(rank.missing_skills, "missing")}
            </div>
        </div>
        """, unsafe_allow_html=True)


def show_skill_analysis_tab(rankings: List[CandidateRank], required_skills: List[str]):
    """Display skill analysis with modern charts."""
    st.markdown('<div class="section-title">🔍 Skill Gap Analysis</div>', unsafe_allow_html=True)
    
    # Aggregate skill statistics
    all_candidate_skills = {}
    for r in rankings:
        for s in r.candidate_skills:
            all_candidate_skills[s] = all_candidate_skills.get(s, 0) + 1
    
    if required_skills:
        # Skill Coverage - Plotly horizontal bar
        coverage_data = []
        for skill in required_skills:
            count = all_candidate_skills.get(skill, 0)
            pct = round(count / len(rankings) * 100, 1)
            coverage_data.append({"Skill": skill, "Count": count, "Coverage": pct})
        
        df_coverage = pd.DataFrame(coverage_data).sort_values("Coverage", ascending=True)
        
        colors_coverage = ['#4ADE80' if c >= 50 else '#FBBF24' if c >= 25 else '#F87171' for c in df_coverage['Coverage'].values]
        
        fig_coverage = go.Figure(go.Bar(
            x=df_coverage['Coverage'],
            y=df_coverage['Skill'],
            orientation='h',
            marker=dict(color=colors_coverage, line=dict(color='rgba(255,255,255,0.1)', width=1)),
            text=df_coverage['Coverage'].apply(lambda x: f'{x:.1f}%'),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Coverage: %{x:.1f}%<br>Count: %{customdata[0]}/{total}<extra></extra>',
            customdata=df_coverage[['Count']],
        ))
        
        fig_coverage.update_layout(
            title="Required Skills Coverage Across All Candidates",
            xaxis=dict(title="Coverage (%)", range=[0, 110]),
            yaxis=dict(title=""),
            height=max(300, len(required_skills) * 30),
            margin=dict(l=10, r=30, t=30, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#94A3B8", "family": "Inter"},
        )
        
        show_plotly_chart(fig_coverage)
    
    # Skill Gap per Candidate
    st.markdown(f'<div class="section-title" style="margin-top:1rem;">🎯 Candidate Skill Analysis</div>', unsafe_allow_html=True)
    
    candidate_selector = st.selectbox(
        "Select a candidate to analyze",
        [r.candidate_name for r in rankings],
        label_visibility="collapsed"
    )
    
    selected = [r for r in rankings if r.candidate_name == candidate_selector]
    if selected:
        rank = selected[0]
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="status-box success">
                <strong>✅ Matching Skills ({len(rank.matching_skills)})</strong><br>
                {render_skill_tags_modern(rank.matching_skills, "match")}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="status-box warning">
                <strong>❌ Missing Skills ({len(rank.missing_skills)})</strong><br>
                {render_skill_tags_modern(rank.missing_skills, "missing")}
            </div>
            """, unsafe_allow_html=True)
        
        # Extra skills
        extra_skills = set(rank.candidate_skills) - set(required_skills)
        if extra_skills:
            st.markdown(f"""
            <div class="status-box info">
                <strong>➕ Extra Skills (Present but not Required):</strong><br>
                {render_skill_tags_modern(sorted(extra_skills), "extra")}
            </div>
            """, unsafe_allow_html=True)
        
        # Score breakdown
        st.markdown("""
        <div style="display:flex;gap:1rem;margin:1rem 0;">
        """, unsafe_allow_html=True)
        
        score_cols = st.columns(3)
        with score_cols[0]:
            st.metric("TF-IDF Similarity", f"{rank.similarity_score:.1f}%")
        with score_cols[1]:
            st.metric("Skill Match", f"{rank.skill_match_score:.1f}%")
        with score_cols[2]:
            st.metric("Combined Score", f"{rank.combined_score:.1f}%")
        
        # Skill status chart - plotly
        if required_skills:
            skill_data = []
            for s in required_skills[:15]:
                skill_data.append({
                    "Skill": s,
                    "Status": "Has Skill" if s in rank.matching_skills else "Missing"
                })
            
            df_skills = pd.DataFrame(skill_data)
            status_colors = {'Has Skill': '#4ADE80', 'Missing': '#F87171'}
            
            fig_skills = go.Figure(go.Bar(
                x=[1] * len(df_skills),
                y=df_skills['Skill'],
                orientation='h',
                marker=dict(
                    color=[status_colors[s] for s in df_skills['Status']],
                    line=dict(color='rgba(255,255,255,0.1)', width=1),
                    opacity=0.7
                ),
                text=df_skills['Status'],
                textposition='inside',
                hovertemplate='<b>%{y}</b><br>%{text}<extra></extra>'
            ))
            
            fig_skills.update_layout(
                title=f"Skill Status for {rank.candidate_name}",
                xaxis=dict(showticklabels=False, range=[0, 1.5]),
                yaxis=dict(title=""),
                height=max(300, len(df_skills) * 28),
                margin=dict(l=10, r=10, t=30, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "#94A3B8", "family": "Inter"},
                showlegend=False,
            )
            
            show_plotly_chart(fig_skills)
    
    # Missing skills heatmap
    st.markdown(f'<div class="section-title" style="margin-top:1rem;">🔥 Missing Skills Matrix</div>', unsafe_allow_html=True)
    
    top_n_heatmap = st.slider("Number of candidates", 5, min(20, len(rankings)), 10, label_visibility="collapsed")
    
    if required_skills:
        n_candidates = min(top_n_heatmap, len(rankings))
        skills_to_show = required_skills[:20]
        
        heatmap_data = []
        candidate_names = []
        
        for r in rankings[:n_candidates]:
            row = [1 if s in r.missing_skills else 0 for s in skills_to_show]
            heatmap_data.append(row)
            candidate_names.append(r.candidate_name[:20])
        
        df_heatmap = pd.DataFrame(heatmap_data, index=candidate_names, columns=skills_to_show)
        
        fig_heat = go.Figure(data=go.Heatmap(
            z=df_heatmap.values,
            x=df_heatmap.columns,
            y=df_heatmap.index,
            colorscale=[[0, 'rgba(34,197,94,0.3)'], [1, 'rgba(239,68,68,0.6)']],
            text=df_heatmap.values,
            texttemplate="%{text}",
            textfont={"size": 10, "color": "#F1F5F9"},
            hovertemplate='<b>%{y}</b><br>Skill: %{x}<br>Status: %{z} (1=Missing)<extra></extra>',
            showscale=True,
            colorbar=dict(
                title="Missing",
                tickvals=[0, 1],
                ticktext=["Has", "Missing"],
                tickfont={"color": "#94A3B8"},
                titlefont={"color": "#94A3B8"}
            )
        ))
        
        fig_heat.update_layout(
            title="Missing Skills Heatmap",
            xaxis=dict(tickangle=45, tickfont={"size": 9}),
            yaxis=dict(tickfont={"size": 9}),
            height=max(300, n_candidates * 35),
            margin=dict(l=10, r=30, t=30, b=80),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#94A3B8", "family": "Inter"},
        )
        
        show_plotly_chart(fig_heat)


def show_visualizations_tab(rankings: List[CandidateRank], required_skills: List[str], metrics: Dict):
    """Display visualizations with plotly."""
    st.markdown('<div class="section-title">📈 Visual Reports & Analytics</div>', unsafe_allow_html=True)
    
    # Row 1: Skill Match Distribution + ATS Score Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        # Skill Match Distribution
        skill_scores = [r.skill_match_score for r in rankings]
        fig_skill_dist = go.Figure()
        
        fig_skill_dist.add_trace(go.Histogram(
            x=skill_scores,
            nbinsx=12,
            marker=dict(color='rgba(74,222,128,0.5)', line=dict(color='#4ADE80', width=1)),
            name="Skill Match",
            opacity=0.8
        ))
        
        mean_skill = np.mean(skill_scores)
        fig_skill_dist.add_vline(x=mean_skill, line=dict(color="#FBBF24", width=2, dash="dash"),
                                annotation_text=f"Mean: {mean_skill:.1f}%",
                                annotation_position="top left",
                                annotation_font=dict(color="#FBBF24", size=11))
        
        fig_skill_dist.update_layout(
            title="Skill Match Distribution",
            xaxis=dict(title="Score (%)", range=[0, 100]),
            yaxis=dict(title="Number of Candidates"),
            height=300,
            margin=dict(l=10, r=10, t=40, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#94A3B8", "family": "Inter"},
            bargap=0.05,
        )
        
        show_plotly_chart(fig_skill_dist)
    
    with col2:
        # ATS Score Distribution
        combined_scores = [r.combined_score for r in rankings]
        fig_ats_dist = go.Figure()
        
        fig_ats_dist.add_trace(go.Histogram(
            x=combined_scores,
            nbinsx=12,
            marker=dict(color='rgba(96,165,250,0.5)', line=dict(color='#60A5FA', width=1)),
            name="ATS Score",
            opacity=0.8
        ))
        
        mean_ats = np.mean(combined_scores)
        median_ats = np.median(combined_scores)
        
        fig_ats_dist.add_vline(x=mean_ats, line=dict(color="#FBBF24", width=2, dash="dash"),
                              annotation_text=f"Mean: {mean_ats:.1f}%",
                              annotation_position="top left",
                              annotation_font=dict(color="#FBBF24", size=11))
        fig_ats_dist.add_vline(x=median_ats, line=dict(color="#4ADE80", width=2, dash="dot"),
                              annotation_text=f"Median: {median_ats:.1f}%",
                              annotation_position="top right",
                              annotation_font=dict(color="#4ADE80", size=11))
        
        fig_ats_dist.update_layout(
            title="ATS Score Distribution",
            xaxis=dict(title="Score (%)", range=[0, 100]),
            yaxis=dict(title="Number of Candidates"),
            height=300,
            margin=dict(l=10, r=10, t=40, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#94A3B8", "family": "Inter"},
            bargap=0.05,
        )
        
        show_plotly_chart(fig_ats_dist)
    
    # Row 2: Candidate Comparison + Skill Gap Analysis
    col3, col4 = st.columns(2)
    
    with col3:
        # Candidate Comparison (Top 10)
        top10 = rankings[:10]
        names = [r.candidate_name[:12] for r in top10]
        
        fig_compare = go.Figure()
        fig_compare.add_trace(go.Bar(
            name="TF-IDF",
            x=names,
            y=[r.similarity_score for r in top10],
            marker=dict(color='rgba(96,165,250,0.7)', line=dict(color='#60A5FA', width=1)),
        ))
        fig_compare.add_trace(go.Bar(
            name="Skill Match",
            x=names,
            y=[r.skill_match_score for r in top10],
            marker=dict(color='rgba(74,222,128,0.7)', line=dict(color='#4ADE80', width=1)),
        ))
        fig_compare.add_trace(go.Bar(
            name="Combined",
            x=names,
            y=[r.combined_score for r in top10],
            marker=dict(color='rgba(251,191,36,0.7)', line=dict(color='#FBBF24', width=1)),
        ))
        
        fig_compare.update_layout(
            title="Candidate Comparison (Top 10)",
            xaxis=dict(title=""),
            yaxis=dict(title="Score (%)", range=[0, 100]),
            height=350,
            margin=dict(l=10, r=10, t=40, b=60),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#94A3B8", "family": "Inter"},
            barmode='group',
            legend=dict(orientation="h", y=-0.2, font=dict(size=10)),
        )
        
        show_plotly_chart(fig_compare)
    
    with col4:
        # Skill Gap Analysis
        if required_skills:
            # Count how many candidates are missing each skill
            skill_gap_data = []
            for skill in required_skills[:15]:
                missing_count = sum(1 for r in rankings if skill in r.missing_skills)
                has_count = len(rankings) - missing_count
                skill_gap_data.append({"Skill": skill, "Has": has_count, "Missing": missing_count})
            
            df_gap = pd.DataFrame(skill_gap_data).sort_values("Missing", ascending=True)
            
            fig_gap = go.Figure()
            fig_gap.add_trace(go.Bar(
                name="Has Skill",
                y=df_gap['Skill'],
                x=df_gap['Has'],
                orientation='h',
                marker=dict(color='rgba(74,222,128,0.6)', line=dict(color='#4ADE80', width=1)),
                text=df_gap['Has'],
                textposition='inside',
            ))
            fig_gap.add_trace(go.Bar(
                name="Missing",
                y=df_gap['Skill'],
                x=df_gap['Missing'],
                orientation='h',
                marker=dict(color='rgba(239,68,68,0.4)', line=dict(color='#F87171', width=1)),
                text=df_gap['Missing'],
                textposition='inside',
            ))
            
            fig_gap.update_layout(
                title="Skill Gap Analysis",
                xaxis=dict(title="Number of Candidates"),
                yaxis=dict(title=""),
                height=350,
                margin=dict(l=10, r=10, t=40, b=30),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "#94A3B8", "family": "Inter"},
                barmode='stack',
                legend=dict(orientation="h", y=-0.2, font=dict(size=10)),
            )
            
            show_plotly_chart(fig_gap)


def show_evaluation_tab(metrics: Dict, rankings: List[CandidateRank]):
    """Display evaluation metrics."""
    st.markdown('<div class="section-title">📊 Model Evaluation</div>', unsafe_allow_html=True)
    
    eval_cols = st.columns(4)
    
    metrics_data = [
        ("🎯", "Precision", metrics.get("precision", 0), "blue"),
        ("📡", "Recall", metrics.get("recall", 0), "teal"),
        ("⚖️", "F1 Score", metrics.get("f1_score", 0), "purple"),
        ("✅", "Accuracy", metrics.get("accuracy", 0), "green"),
    ]
    
    for i, (icon, label, value, color) in enumerate(metrics_data):
        with eval_cols[i]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <div class="kpi-icon {color}">{icon}</div>
                </div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value:.3f}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Confusion Matrix
    st.markdown(f'<div class="section-title" style="margin-top:1rem;">📋 Confusion Matrix</div>', unsafe_allow_html=True)
    
    cm = metrics.get('confusion_matrix', [[0, 0], [0, 0]])
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Plotly confusion matrix
        fig_cm = go.Figure(data=go.Heatmap(
            z=cm,
            x=['Not Selected', 'Selected'],
            y=['Not Selected', 'Selected'],
            text=[[str(cm[0][0]), str(cm[0][1])], [str(cm[1][0]), str(cm[1][1])]],
            texttemplate="%{text}",
            textfont={"size": 18, "color": "#F1F5F9", "family": "Inter"},
            colorscale=[[0, 'rgba(34,197,94,0.3)'], [0.5, 'rgba(96,165,250,0.3)'], [1, 'rgba(239,68,68,0.3)']],
            showscale=False,
            hovertemplate='Actual: %{y}<br>Predicted: %{x}<br>Count: %{z}<extra></extra>'
        ))
        
        fig_cm.update_layout(
            title="Confusion Matrix",
            xaxis=dict(title="Predicted", side="bottom"),
            yaxis=dict(title="Actual", autorange="reversed"),
            height=350,
            width=400,
            margin=dict(l=10, r=10, t=40, b=40),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#94A3B8", "family": "Inter"},
        )
        
        show_plotly_chart(fig_cm)
    
    with col2:
        total = sum(sum(row) for row in cm)
        correct = cm[0][0] + cm[1][1]
        
        st.markdown(f"""
        <div class="glass-card" style="height:350px;display:flex;flex-direction:column;justify-content:center;">
            <h4 style="color:#F1F5F9;margin:0 0 1rem 0;">📊 Matrix Interpretation</h4>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
                <div style="padding:0.8rem;background:rgba(34,197,94,0.08);border-radius:10px;">
                    <div style="font-size:1.5rem;font-weight:700;color:#4ADE80;">{cm[0][0]}</div>
                    <div style="font-size:0.8rem;color:#94A3B8;">True Negatives (TN)</div>
                    <div style="font-size:0.7rem;color:#64748B;">Correctly rejected</div>
                </div>
                <div style="padding:0.8rem;background:rgba(239,68,68,0.08);border-radius:10px;">
                    <div style="font-size:1.5rem;font-weight:700;color:#F87171;">{cm[0][1]}</div>
                    <div style="font-size:0.8rem;color:#94A3B8;">False Positives (FP)</div>
                    <div style="font-size:0.7rem;color:#64748B;">Incorrectly selected</div>
                </div>
                <div style="padding:0.8rem;background:rgba(239,68,68,0.08);border-radius:10px;">
                    <div style="font-size:1.5rem;font-weight:700;color:#F87171;">{cm[1][0]}</div>
                    <div style="font-size:0.8rem;color:#94A3B8;">False Negatives (FN)</div>
                    <div style="font-size:0.7rem;color:#64748B;">Missed good candidates</div>
                </div>
                <div style="padding:0.8rem;background:rgba(34,197,94,0.08);border-radius:10px;">
                    <div style="font-size:1.5rem;font-weight:700;color:#4ADE80;">{cm[1][1]}</div>
                    <div style="font-size:0.8rem;color:#94A3B8;">True Positives (TP)</div>
                    <div style="font-size:0.7rem;color:#64748B;">Correctly selected</div>
                </div>
            </div>
            <div style="margin-top:1rem;padding:0.8rem;background:rgba(59,130,246,0.08);border-radius:10px;text-align:center;">
                <span style="font-size:1.2rem;font-weight:700;color:#60A5FA;">{correct}/{total}</span>
                <span style="color:#94A3B8;font-size:0.85rem;"> correct predictions ({correct/total*100:.1f}%)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Scoring methodology
    st.markdown(f'<div class="section-title" style="margin-top:1rem;">⚙️ Scoring Methodology</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <p style="color:#E2E8F0;font-weight:600;">Combined Score = <span style="color:#60A5FA;">40% × TF-IDF Similarity</span> + <span style="color:#4ADE80;">60% × Skill Match Percentage</span></p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem;">
            <div style="padding:0.8rem;background:rgba(59,130,246,0.08);border-radius:10px;">
                <div style="font-size:0.9rem;font-weight:600;color:#60A5FA;">📄 TF-IDF Similarity</div>
                <div style="font-size:0.8rem;color:#94A3B8;margin-top:0.3rem;">
                Measures semantic similarity between resume and JD using TF-IDF vectorization and cosine similarity.
                </div>
            </div>
            <div style="padding:0.8rem;background:rgba(34,197,94,0.08);border-radius:10px;">
                <div style="font-size:0.9rem;font-weight:600;color:#4ADE80;">🧠 Skill Match Percentage</div>
                <div style="font-size:0.8rem;color:#94A3B8;margin-top:0.3rem;">
                Percentage of required skills the candidate possesses, extracted via NLP keyword matching against 35+ skills.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Score Distribution
    st.markdown(f'<div class="section-title" style="margin-top:1rem;">📊 Score Distribution</div>', unsafe_allow_html=True)
    
    scores = [r.combined_score for r in rankings]
    fig_dist = go.Figure()
    
    fig_dist.add_trace(go.Histogram(
        x=scores,
        nbinsx=15,
        marker=dict(color='rgba(96,165,250,0.5)', line=dict(color='#60A5FA', width=1)),
        name="Combined Score",
        opacity=0.8
    ))
    
    fig_dist.add_vline(x=np.mean(scores), line=dict(color="#FBBF24", width=2, dash="dash"),
                      annotation_text=f"Mean: {np.mean(scores):.1f}%",
                      annotation_font=dict(color="#FBBF24", size=11))
    fig_dist.add_vline(x=np.median(scores), line=dict(color="#4ADE80", width=2, dash="dot"),
                      annotation_text=f"Median: {np.median(scores):.1f}%",
                      annotation_font=dict(color="#4ADE80", size=11))
    
    fig_dist.update_layout(
        title="Distribution of Combined Scores",
        xaxis=dict(title="Score (%)"),
        yaxis=dict(title="Number of Candidates"),
        height=350,
        margin=dict(l=10, r=10, t=40, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#94A3B8", "family": "Inter"},
        bargap=0.05,
    )
    
    show_plotly_chart(fig_dist)


def show_export_tab(rankings: List[CandidateRank], required_skills: List[str], metrics: Dict):
    """Display the export tab."""
    st.markdown('<div class="section-title">📥 Export Results</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Download screening results in CSV format for your HR systems.</div>', unsafe_allow_html=True)
    
    # Prepare data
    df_results = pd.DataFrame([{
        'Rank': r.rank,
        'Candidate Name': r.candidate_name,
        'Resume File': r.resume_file,
        'TF-IDF Similarity (%)': round(r.similarity_score, 1),
        'Skill Match Score (%)': round(r.skill_match_score, 1),
        'Combined Score (%)': round(r.combined_score, 1),
        'Matching Skills': ', '.join(r.matching_skills),
        'Missing Skills': ', '.join(r.missing_skills),
        'Total Skills Found': len(r.candidate_skills),
        'Match Count': len(r.matching_skills),
        'Gap Count': len(r.missing_skills)
    } for r in rankings])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card" style="text-align:center;">
            <div style="font-size:2rem;margin-bottom:0.5rem;">📄</div>
            <div style="font-weight:600;color:#F1F5F9;font-size:1rem;">CSV Export</div>
            <div style="color:#64748B;font-size:0.8rem;margin-bottom:1rem;">
            Full ranking details including scores and skill data.
            </div>
        """, unsafe_allow_html=True)
        
        csv_data = df_results.to_csv(index=False)
        b64_csv = base64.b64encode(csv_data.encode()).decode()
        st.markdown(f'''
        <a href="data:file/csv;base64,{b64_csv}" download="candidate_rankings.csv" style="
            display:inline-flex;align-items:center;gap:0.5rem;
            background:linear-gradient(135deg,#3B82F6,#2563EB);color:white;
            padding:0.6rem 1.5rem;border-radius:10px;
            font-size:0.9rem;font-weight:600;text-decoration:none;
            box-shadow:0 4px 15px rgba(59,130,246,0.3);
            transition:all 0.3s ease;
        " onmouseover="this.style.boxShadow='0 6px 20px rgba(59,130,246,0.4)'" 
           onmouseout="this.style.boxShadow='0 4px 15px rgba(59,130,246,0.3)'">
        ⬇️ Download CSV Report
        </a>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <div style="font-weight:600;color:#F1F5F9;font-size:1rem;margin-bottom:0.8rem;">📊 Summary Report</div>
        """, unsafe_allow_html=True)
        
        summary_data = {
            'Metric': [
                'Job Title', 'Total Candidates', 'Required Skills', 
                'Top Candidate', 'Top Score', 'Average Score',
                'Precision', 'Recall', 'F1 Score', 'Accuracy'
            ],
            'Value': [
                st.session_state.jd_title,
                len(rankings),
                len(required_skills),
                rankings[0].candidate_name,
                f"{rankings[0].combined_score:.2f}%",
                f"{np.mean([r.combined_score for r in rankings]):.2f}%",
                f"{metrics.get('precision', 0):.4f}" if metrics else "N/A",
                f"{metrics.get('recall', 0):.4f}" if metrics else "N/A",
                f"{metrics.get('f1_score', 0):.4f}" if metrics else "N/A",
                f"{metrics.get('accuracy', 0):.4f}" if metrics else "N/A"
            ]
        }
        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Preview
    st.markdown(f'<div class="section-title" style="margin-top:1rem;">👁️ Preview</div>', unsafe_allow_html=True)
    st.dataframe(df_results.head(10), use_container_width=True, hide_index=True)
    st.caption(f"Showing 10 of {len(df_results)} rows")
    
    # Skill gap report
    st.markdown(f'<div class="section-title" style="margin-top:1rem;">📝 Skill Gap Report</div>', unsafe_allow_html=True)
    
    if required_skills:
        gap_data = []
        for r in rankings[:10]:
            gap_data.append({
                'Rank': r.rank,
                'Candidate': r.candidate_name,
                **{s: '✅' if s in r.matching_skills else ('❌' if s in r.missing_skills else '➖') 
                   for s in required_skills[:15]}
            })
        
        df_gaps = pd.DataFrame(gap_data)
        st.dataframe(df_gaps, use_container_width=True, hide_index=True)
        
        csv_gaps = df_gaps.to_csv(index=False)
        b64_gaps = base64.b64encode(csv_gaps.encode()).decode()
        st.markdown(f'''
        <div style="text-align:right;margin-top:0.5rem;">
        <a href="data:file/csv;base64,{b64_gaps}" download="skill_gap_report.csv" style="
            display:inline-flex;align-items:center;gap:0.4rem;
            background:rgba(59,130,246,0.1);color:#60A5FA;
            padding:0.4rem 1rem;border-radius:8px;
            font-size:0.8rem;font-weight:500;text-decoration:none;
            border:1px solid rgba(59,130,246,0.2);
        ">⬇️ Download Skill Gap Report</a>
        </div>
        ''', unsafe_allow_html=True)


if __name__ == "__main__":
    main()