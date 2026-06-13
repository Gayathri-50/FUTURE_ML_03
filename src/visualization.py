"""
Visualization module for Resume Screening System.
Generates charts and visual reports for candidate analysis.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Optional, Tuple

from src.ranking_model import CandidateRank

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def ensure_chart_dir(chart_dir: str = 'outputs/charts'):
    """Ensure the charts output directory exists."""
    os.makedirs(chart_dir, exist_ok=True)
    return chart_dir


def plot_top_candidate_scores(
    rankings: List[CandidateRank],
    top_n: int = 10,
    title: str = "Top Candidate Scores",
    save_path: str = None
) -> str:
    """
    Bar chart of top candidate combined scores.
    
    Args:
        rankings: List of ranked candidates
        top_n: Number of top candidates to show
        title: Chart title
        save_path: Path to save the figure
        
    Returns:
        Path to saved figure
    """
    ensure_chart_dir()
    
    # Take top N candidates
    top = rankings[:top_n]
    
    names = [r.candidate_name[:20] for r in top]
    scores = [r.combined_score for r in top]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars = ax.barh(range(len(names)), scores, color=sns.color_palette("viridis", len(names)))
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names)
    ax.set_xlabel('Combined Score (%)')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    
    # Add score labels on bars
    for i, (bar, score) in enumerate(zip(bars, scores)):
        ax.text(score + 0.5, bar.get_y() + bar.get_height()/2,
                f'{score:.1f}%', va='center', fontsize=9)
    
    plt.tight_layout()
    
    if save_path is None:
        save_path = f'outputs/charts/top_{top_n}_candidates.png'
    
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")
    return save_path


def plot_skill_distribution(
    rankings: List[CandidateRank],
    title: str = "Skill Distribution Across Candidates",
    save_path: str = None
) -> str:
    """
    Bar chart showing how many candidates possess each skill.
    
    Args:
        rankings: List of ranked candidates
        title: Chart title
        save_path: Path to save the figure
        
    Returns:
        Path to saved figure
    """
    ensure_chart_dir()
    
    # Count skill occurrences
    skill_counts = {}
    for rank in rankings:
        for skill in rank.candidate_skills:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
    
    if not skill_counts:
        print("No skills found to visualize.")
        return ""
    
    # Sort by count descending
    sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)
    skills, counts = zip(*sorted_skills)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    bars = ax.bar(skills, counts, color=sns.color_palette("mako", len(skills)))
    ax.set_xlabel('Skills')
    ax.set_ylabel('Number of Candidates')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(skills)))
    ax.set_xticklabels(skills, rotation=45, ha='right', fontsize=9)
    
    # Add count labels on bars
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                str(count), ha='center', fontsize=9)
    
    plt.tight_layout()
    
    if save_path is None:
        save_path = 'outputs/charts/skill_distribution.png'
    
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")
    return save_path


def plot_match_percentage_chart(
    rankings: List[CandidateRank],
    title: str = "Resume Match Percentage",
    save_path: str = None
) -> str:
    """
    Grouped bar chart showing similarity score, skill match, and combined score.
    
    Args:
        rankings: List of ranked candidates
        title: Chart title
        save_path: Path to save the figure
        
    Returns:
        Path to saved figure
    """
    ensure_chart_dir()
    
    names = [r.candidate_name[:15] for r in rankings]
    similarity_scores = [r.similarity_score for r in rankings]
    skill_scores = [r.skill_match_score for r in rankings]
    combined_scores = [r.combined_score for r in rankings]
    
    x = np.arange(len(names))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.bar(x - width, similarity_scores, width, label='TF-IDF Similarity', color='#3498db')
    ax.bar(x, skill_scores, width, label='Skill Match', color='#2ecc71')
    ax.bar(x + width, combined_scores, width, label='Combined Score', color='#e74c3c')
    
    ax.set_xlabel('Candidates')
    ax.set_ylabel('Score (%)')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
    ax.legend(loc='upper right')
    ax.set_ylim(0, 110)
    
    plt.tight_layout()
    
    if save_path is None:
        save_path = 'outputs/charts/match_percentage.png'
    
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")
    return save_path


def plot_missing_skills_heatmap(
    rankings: List[CandidateRank],
    required_skills: List[str] = None,
    title: str = "Missing Skills Heatmap",
    save_path: str = None
) -> str:
    """
    Heatmap showing missing skills for each candidate.
    
    Args:
        rankings: List of ranked candidates
        required_skills: List of all required skills for the job
        title: Chart title
        save_path: Path to save the figure
        
    Returns:
        Path to saved figure
    """
    ensure_chart_dir()
    
    # Get all unique required skills across all candidates
    if required_skills is None:
        all_required = set()
        for r in rankings:
            all_required.update(r.missing_skills)
            all_required.update(r.matching_skills)
        required_skills = sorted(all_required)
    
    if not required_skills:
        print("No skills to visualize in heatmap.")
        return ""
    
    # Build matrix: 1 = missing, 0 = has skill
    n_candidates = min(len(rankings), 20)  # Limit to top 20
    data_matrix = []
    candidate_names = []
    
    for r in rankings[:n_candidates]:
        row = []
        for skill in required_skills:
            # 1 if skill is missing, 0 if candidate has it
            row.append(1 if skill in r.missing_skills else 0)
        data_matrix.append(row)
        candidate_names.append(r.candidate_name[:20])
    
    df_heatmap = pd.DataFrame(data_matrix, index=candidate_names, columns=required_skills)
    
    fig, ax = plt.subplots(figsize=(max(10, len(required_skills) * 0.8), max(6, n_candidates * 0.5)))
    
    sns.heatmap(df_heatmap, annot=True, fmt='d', cmap='RdYlGn_r',
                cbar_kws={'label': 'Missing (1) / Has Skill (0)'},
                linewidths=0.5, ax=ax, vmin=0, vmax=1)
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel('Required Skills')
    ax.set_ylabel('Candidates')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=8)
    
    plt.tight_layout()
    
    if save_path is None:
        save_path = 'outputs/charts/missing_skills_heatmap.png'
    
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")
    return save_path


def plot_confusion_matrix(
    cm: List[List[int]],
    title: str = "Confusion Matrix",
    save_path: str = None
) -> str:
    """
    Plot confusion matrix heatmap.
    
    Args:
        cm: Confusion matrix as 2x2 list
        title: Chart title
        save_path: Path to save the figure
        
    Returns:
        Path to saved figure
    """
    ensure_chart_dir()
    
    fig, ax = plt.subplots(figsize=(6, 5))
    
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Not Selected', 'Selected'],
                yticklabels=['Not Selected', 'Selected'],
                ax=ax, cbar_kws={'label': 'Count'})
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    
    plt.tight_layout()
    
    if save_path is None:
        save_path = 'outputs/charts/confusion_matrix.png'
    
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")
    return save_path


def generate_all_charts(
    rankings: List[CandidateRank],
    required_skills: List[str] = None,
    evaluation_metrics: Dict = None,
    chart_dir: str = 'outputs/charts'
) -> Dict[str, str]:
    """
    Generate all standard charts for the resume screening system.
    
    Args:
        rankings: List of ranked candidates
        required_skills: List of required skills
        evaluation_metrics: Optional evaluation metrics dict with confusion_matrix
        chart_dir: Directory to save charts
        
    Returns:
        Dictionary mapping chart names to file paths
    """
    charts = {}
    
    charts['top_candidates'] = plot_top_candidate_scores(rankings, top_n=min(10, len(rankings)))
    charts['skill_distribution'] = plot_skill_distribution(rankings)
    charts['match_percentage'] = plot_match_percentage_chart(rankings)
    
    if required_skills:
        charts['missing_skills'] = plot_missing_skills_heatmap(rankings, required_skills)
    else:
        charts['missing_skills'] = plot_missing_skills_heatmap(rankings)
    
    if evaluation_metrics and 'confusion_matrix' in evaluation_metrics:
        charts['confusion_matrix'] = plot_confusion_matrix(evaluation_metrics['confusion_matrix'])
    
    return charts