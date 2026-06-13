"""
Resume / Candidate Screening System - Main Entry Point

An ATS-style Resume Screening System that:
- Accepts multiple resumes and job descriptions
- Extracts skills from resumes
- Matches resume skills with job requirements
- Calculates matching scores
- Identifies missing skills
- Ranks candidates
- Generates visual reports

Usage:
    python main.py
    python main.py --resume-dir data/resumes --jd-file data/job_descriptions/jd_data_scientist.txt
"""
import os
import sys
import argparse
import pandas as pd
from typing import List, Set

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.preprocess import TextPreprocessor
from src.skill_extractor import SkillExtractor, SKILL_REGISTRY, JOB_ROLE_SKILLS
from src.ranking_model import ResumeRankingModel, CandidateRank, generate_sample_labels, evaluate_model
from src.visualization import generate_all_charts


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Resume / Candidate Screening System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py
  python main.py --resume-dir data/resumes --jd-file data/job_descriptions/jd_data_scientist.txt
  python main.py --jd-file data/job_descriptions/jd_ml_engineer.txt --job-role "Machine Learning Engineer"
        """
    )
    parser.add_argument(
        '--resume-dir', type=str, default='data/resumes',
        help='Directory containing resume files (default: data/resumes)'
    )
    parser.add_argument(
        '--jd-file', type=str, default='data/job_descriptions/jd_data_scientist.txt',
        help='Path to job description file (default: data/job_descriptions/jd_data_scientist.txt)'
    )
    parser.add_argument(
        '--job-role', type=str, default=None,
        help='Job role for predefined skill sets (Data Scientist, ML Engineer, Data Analyst, Python Developer)'
    )
    parser.add_argument(
        '--output-dir', type=str, default='outputs',
        help='Directory for output files (default: outputs)'
    )
    return parser.parse_args()


def display_header():
    """Display the application header."""
    print("\n")
    print("=" * 70)
    print("      RESUME / CANDIDATE SCREENING SYSTEM")
    print("      ATS-Style Resume Screening & Ranking Engine")
    print("=" * 70)
    print()


def display_ranking_table(rankings: List[CandidateRank], top_n: int = 10):
    """
    Display a formatted ranking table.
    
    Args:
        rankings: List of ranked candidates
        top_n: Number of top candidates to display
    """
    print("\n" + "=" * 80)
    print(f"TOP {min(top_n, len(rankings))} CANDIDATE RANKINGS")
    print("=" * 80)
    print(f"{'Rank':<6} {'Candidate Name':<25} {'Similarity':<12} {'Skill Match':<12} {'Combined':<10}")
    print("-" * 80)
    
    for rank in rankings[:top_n]:
        name = rank.candidate_name[:24]
        print(f"{rank.rank:<6} {name:<25} {rank.similarity_score:<10.2f}%  {rank.skill_match_score:<10.2f}%  {rank.combined_score:<8.2f}%")
    
    print("-" * 80)
    print(f"Total candidates processed: {len(rankings)}")
    print()


def display_skill_gap(rankings: List[CandidateRank], top_n: int = 5):
    """
    Display skill gap analysis for top candidates.
    
    Args:
        rankings: List of ranked candidates
        top_n: Number of top candidates to display
    """
    print("\n" + "=" * 80)
    print(f"SKILL GAP ANALYSIS - TOP {min(top_n, len(rankings))} CANDIDATES")
    print("=" * 80)
    
    for rank in rankings[:top_n]:
        print(f"\n{'─' * 70}")
        print(f"  Rank #{rank.rank}: {rank.candidate_name}")
        print(f"  Combined Score: {rank.combined_score:.2f}%")
        print(f"{'─' * 70}")
        
        if rank.matching_skills:
            print(f"  ✅ Matching Skills ({len(rank.matching_skills)}):")
            for skill in rank.matching_skills[:10]:
                print(f"     - {skill}")
            if len(rank.matching_skills) > 10:
                print(f"     ... and {len(rank.matching_skills) - 10} more")
        else:
            print("  ⚠️  No matching skills found")
        
        if rank.missing_skills:
            print(f"  ❌ Missing Skills ({len(rank.missing_skills)}):")
            for skill in rank.missing_skills[:10]:
                print(f"     - {skill}")
            if len(rank.missing_skills) > 10:
                print(f"     ... and {len(rank.missing_skills) - 10} more")
        else:
            print("  ✅ No missing skills!")
    
    print()


def display_evaluation_metrics(metrics: dict):
    """
    Display evaluation metrics.
    
    Args:
        metrics: Dictionary with evaluation metrics
    """
    print("\n" + "=" * 70)
    print("MODEL EVALUATION METRICS")
    print("=" * 70)
    print(f"  Precision:    {metrics.get('precision', 0):.4f}")
    print(f"  Recall:       {metrics.get('recall', 0):.4f}")
    print(f"  F1 Score:     {metrics.get('f1_score', 0):.4f}")
    print(f"  Accuracy:     {metrics.get('accuracy', 0):.4f}")
    
    cm = metrics.get('confusion_matrix', [[0, 0], [0, 0]])
    print(f"\n  Confusion Matrix:")
    print(f"                    Predicted")
    print(f"                    No    Yes")
    print(f"  Actual No       {cm[0][0]:5d}  {cm[0][1]:5d}")
    print(f"         Yes      {cm[1][0]:5d}  {cm[1][1]:5d}")
    print()


def main():
    """Main entry point for the Resume Screening System."""
    args = parse_arguments()
    display_header()
    
    # Validate paths
    if not os.path.exists(args.resume_dir):
        print(f"❌ Error: Resume directory '{args.resume_dir}' not found.")
        print("   Run 'python data/generate_sample_data.py' first to create sample data.")
        sys.exit(1)
    
    if not os.path.exists(args.jd_file):
        print(f"❌ Error: Job description file '{args.jd_file}' not found.")
        print("   Run 'python data/generate_sample_data.py' first to create sample data.")
        sys.exit(1)
    
    # Determine required skills
    required_skills = None
    if args.job_role and args.job_role in JOB_ROLE_SKILLS:
        required_skills = JOB_ROLE_SKILLS[args.job_role]
        print(f"📋 Using predefined skill set for: {args.job_role}")
    
    print(f"📁 Resume Directory: {args.resume_dir}")
    print(f"📄 Job Description:  {args.jd_file}")
    print(f"📂 Output Directory: {args.output_dir}")
    print()
    
    # Initialize ranking model
    print("🚀 Initializing Resume Ranking Model...")
    model = ResumeRankingModel()
    
    # Process resumes
    print("📊 Processing resumes and computing rankings...")
    rankings, jd_title = model.batch_process(
        resume_dir=args.resume_dir,
        jd_file=args.jd_file,
        required_skills=required_skills
    )
    
    # Extract required skills from JD for display
    skill_extractor = SkillExtractor(SKILL_REGISTRY)
    with open(args.jd_file, 'r', encoding='utf-8', errors='ignore') as f:
        jd_text = f.read()
    jd_skills = skill_extractor.extract_skills(jd_text)
    if required_skills:
        jd_skills = required_skills
    
    # Display results
    print(f"\n✅ Processing complete! Matching candidates for: {jd_title}")
    print(f"   Total candidates: {len(rankings)}")
    print(f"   Required skills identified: {len(jd_skills)}")
    
    display_ranking_table(rankings, top_n=10)
    display_skill_gap(rankings, top_n=5)
    
    # Save results to CSV
    output_csv = os.path.join(args.output_dir, 'ranking_results.csv')
    df = model.save_results(rankings, output_csv)
    
    # Generate evaluation metrics
    print("📈 Computing evaluation metrics...")
    y_true, y_pred = generate_sample_labels(rankings, threshold=50.0)
    metrics = evaluate_model(y_true, y_pred)
    display_evaluation_metrics(metrics)
    
    # Generate visualizations
    print("🎨 Generating visualizations...")
    charts = generate_all_charts(
        rankings=rankings,
        required_skills=sorted(jd_skills),
        evaluation_metrics=metrics,
        chart_dir=os.path.join(args.output_dir, 'charts')
    )
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Job Title:           {jd_title}")
    print(f"  Total Candidates:    {len(rankings)}")
    print(f"  Skills Identified:   {len(jd_skills)}")
    print(f"  Top Candidate:       {rankings[0].candidate_name} ({rankings[0].combined_score:.2f}%)")
    print(f"  Bottom Candidate:    {rankings[-1].candidate_name} ({rankings[-1].combined_score:.2f}%)")
    print()
    print(f"  📄 Ranking Results:  {output_csv}")
    print(f"  📊 Charts Generated: {len(charts)}")
    for name, path in charts.items():
        if path:
            print(f"     - {name}: {path}")
    print()
    print("=" * 70)
    print("✅ Resume Screening Complete!")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()