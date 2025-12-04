#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main Entry Point for Breast Cancer Agentic ML Pipeline
=======================================================

This script provides a unified interface to run the breast cancer diagnostic
ML pipeline with multiple execution modes:

1. Full ML Pipeline (obiedeh_breast_cancer_agentic_ml.py)
2. Agent-based Pipeline (orchestrator.py with individual agents)
3. Individual stages (EDA, Feature Engineering, Modeling, Explanation)

Usage:
------
    # Run the full ML pipeline with interactive session
    python main.py --mode full

    # Run the agent-based pipeline (all stages)
    python main.py --mode agents --stage all

    # Run specific agent stage
    python main.py --mode agents --stage eda
    python main.py --mode agents --stage modeling
    python main.py --mode agents --stage explain

    # Run full pipeline without interactive session
    python main.py --mode full --no-interactive

Author: Obinna Edeh
Course: USD - AAI - 501 - G5
"""

import argparse
import sys
import os
import subprocess
from pathlib import Path
import json


# Terminal colors for better UX
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"
COLOR_GREEN = "\033[92m"
COLOR_CYAN = "\033[96m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_MAGENTA = "\033[95m"


def print_header(text: str, color: str = COLOR_CYAN):
    """Print a formatted header."""
    print(f"\n{color}{COLOR_BOLD}{'='*80}")
    print(f"{text:^80}")
    print(f"{'='*80}{COLOR_RESET}\n")


def print_section(text: str):
    """Print a formatted section header."""
    print(f"\n{COLOR_BOLD}{COLOR_GREEN}▶ {text}{COLOR_RESET}")


def check_dependencies():
    """Check if required files and dependencies exist."""
    required_files = [
        "obiedeh_breast_cancer_agentic_ml.py",
        "orchestrator.py",
        "config.yaml",
        "requirements.txt"
    ]
    
    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
    
    if missing:
        print(f"{COLOR_RED}Error: Missing required files:{COLOR_RESET}")
        for file in missing:
            print(f"  - {file}")
        return False
    
    return True


def run_full_pipeline(interactive: bool = True):
    """
    Run the complete ML pipeline from obiedeh_breast_cancer_agentic_ml.py
    
    Args:
        interactive: If True, runs the interactive agent session at the end
    """
    print_header("Running Full ML Pipeline", COLOR_CYAN)
    
    # Import and run the main ML script
    try:
        print_section("Importing ML pipeline module...")
        
        # Add current directory to path if not already there
        if os.getcwd() not in sys.path:
            sys.path.insert(0, os.getcwd())
        
        # Import the module
        import obiedeh_breast_cancer_agentic_ml as ml_pipeline
        
        print_section("Step 1: Loading breast cancer data...")
        ml_pipeline.load_breast_data()
        
        print_section("Step 2: Training and tuning all models...")
        ml_pipeline.run_all_models()
        
        print_section("Step 3: Running RFECV and XGBoost optimization...")
        ml_pipeline.run_rfecv_and_xgb()
        
        print_section("Step 4: Selecting best model...")
        ml_pipeline.summarize_and_choose_model(preferred="XGBoost")
        
        print_section("Step 5: Setting up SHAP explainer...")
        ml_pipeline.setup_shap_explainer()
        
        if interactive:
            print_section("Step 6: Starting interactive agent session...")
            print(f"{COLOR_YELLOW}Type 'exit' to quit the interactive session{COLOR_RESET}")
            ml_pipeline.interactive_agent_session()
        else:
            print_section("Pipeline completed successfully (non-interactive mode)")
        
        print(f"\n{COLOR_GREEN}{COLOR_BOLD}✓ Full pipeline completed successfully!{COLOR_RESET}\n")
        
    except ImportError as e:
        print(f"{COLOR_RED}Error importing module: {e}{COLOR_RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{COLOR_RED}Error running pipeline: {e}{COLOR_RESET}")
        sys.exit(1)


def run_notebooks(notebooks: list = None):
    """
    Run Jupyter notebooks using nbconvert.
    
    Args:
        notebooks: List of notebook paths to run. If None, runs all notebooks in order.
    """
    print_header("Running Jupyter Notebooks", COLOR_MAGENTA)
    
    # Default notebook execution order: 00_eda (1), 01_eda, then obiedeh_breast_cancer_agentic_ML
    if notebooks is None:
        notebooks = [
            "00_eda (1).ipynb",
            "notebooks/01_eda.ipynb",
            "obiedeh_breast_cancer_agentic_ML.ipynb",
        ]
    
    # Filter to only existing notebooks
    existing_notebooks = [nb for nb in notebooks if Path(nb).exists()]
    
    if not existing_notebooks:
        print(f"{COLOR_YELLOW}Warning: No notebooks found to execute{COLOR_RESET}")
        return
    
    print(f"Found {len(existing_notebooks)} notebook(s) to execute\n")
    
    # Check if jupyter/nbconvert is available
    try:
        result = subprocess.run(
            [sys.executable, "-m", "jupyter", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"{COLOR_YELLOW}Jupyter not found. Installing...{COLOR_RESET}")
            subprocess.run([sys.executable, "-m", "pip", "install", "jupyter", "nbconvert"], check=True)
    except Exception:
        print(f"{COLOR_YELLOW}Installing Jupyter for notebook execution...{COLOR_RESET}")
        subprocess.run([sys.executable, "-m", "pip", "install", "jupyter", "nbconvert"], check=True)
    
    # Execute each notebook
    for i, notebook_path in enumerate(existing_notebooks, 1):
        print_section(f"Executing Notebook {i}/{len(existing_notebooks)}: {notebook_path}")
        
        try:
            # Use nbconvert to execute the notebook
            cmd = [
                sys.executable, "-m", "jupyter", "nbconvert",
                "--to", "notebook",
                "--execute",
                "--inplace",
                notebook_path
            ]
            
            print(f"{COLOR_YELLOW}Executing: {Path(notebook_path).name}{COLOR_RESET}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout per notebook
            )
            
            if result.returncode == 0:
                print(f"{COLOR_GREEN}✓ {Path(notebook_path).name} completed successfully{COLOR_RESET}")
            else:
                print(f"{COLOR_RED}✗ {Path(notebook_path).name} failed{COLOR_RESET}")
                if result.stderr:
                    print(f"{COLOR_RED}Error: {result.stderr[:500]}{COLOR_RESET}")
                
        except subprocess.TimeoutExpired:
            print(f"{COLOR_RED}✗ {Path(notebook_path).name} timed out (>10 minutes){COLOR_RESET}")
        except Exception as e:
            print(f"{COLOR_RED}✗ Error executing {Path(notebook_path).name}: {e}{COLOR_RESET}")
    
    print(f"\n{COLOR_GREEN}{COLOR_BOLD}✓ Notebook execution completed!{COLOR_RESET}\n")


def run_agent_pipeline(stage: str = "all"):
    """
    Run the agent-based pipeline using orchestrator.py
    
    Args:
        stage: Which stage to run ('eda', 'modeling', 'explain', 'all')
    """
    print_header("Running Agent-Based Pipeline", COLOR_CYAN)
    
    print(f"{COLOR_BOLD}Stage: {stage.upper()}{COLOR_RESET}")
    
    # Use the current Python interpreter
    python_exe = sys.executable
    
    cmd = [python_exe, "orchestrator.py", "--stage", stage]
    
    print(f"{COLOR_YELLOW}Executing: {' '.join(cmd)}{COLOR_RESET}\n")
    
    try:
        result = subprocess.run(cmd, check=True, text=True)
        print(f"\n{COLOR_GREEN}{COLOR_BOLD}✓ Agent pipeline completed successfully!{COLOR_RESET}\n")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"{COLOR_RED}Error running agent pipeline: {e}{COLOR_RESET}")
        sys.exit(e.returncode)


def run_quick_test():
    """Run a quick test to verify the setup."""
    print_header("Running Quick Test", COLOR_YELLOW)
    
    try:
        print_section("Testing imports...")
        import numpy as np
        import pandas as pd
        import sklearn
        print(f"  ✓ NumPy version: {np.__version__}")
        print(f"  ✓ Pandas version: {pd.__version__}")
        print(f"  ✓ Scikit-learn version: {sklearn.__version__}")
        
        print_section("Testing data loading...")
        from sklearn.datasets import load_breast_cancer
        data = load_breast_cancer()
        print(f"  ✓ Dataset loaded: {data.data.shape[0]} samples, {data.data.shape[1]} features")
        
        print_section("Verifying directory structure...")
        dirs = ["artifacts", "data", "agents"]
        for dir_name in dirs:
            if Path(dir_name).exists():
                print(f"  ✓ {dir_name}/ exists")
            else:
                print(f"  ⚠ {dir_name}/ missing (will be created)")
        
        print(f"\n{COLOR_GREEN}{COLOR_BOLD}✓ Quick test passed!{COLOR_RESET}\n")
        
    except Exception as e:
        print(f"{COLOR_RED}✗ Quick test failed: {e}{COLOR_RESET}")
        sys.exit(1)


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Breast Cancer Agentic ML Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --mode full                    # Run full ML pipeline with interactive session
  %(prog)s --mode full --no-interactive   # Run full ML pipeline without interaction
  %(prog)s --mode agents --stage all      # Run all agent stages
  %(prog)s --mode agents --stage eda      # Run only EDA stage
  %(prog)s --mode notebooks               # Run all Jupyter notebooks
  %(prog)s --mode notebooks --notebooks notebooks/00_eda.ipynb  # Run specific notebook
  %(prog)s --mode test                    # Run quick setup test
        """
    )
    
    parser.add_argument(
        "--mode",
        choices=["full", "agents", "notebooks", "test"],
        default="full",
        help="Execution mode: 'full' for complete ML pipeline, 'agents' for orchestrated agents, 'notebooks' for Jupyter notebooks, 'test' for quick test"
    )
    
    parser.add_argument(
        "--stage",
        choices=["eda", "modeling", "explain", "all"],
        default="all",
        help="Stage to run when using agent mode (default: all)"
    )
    
    parser.add_argument(
        "--no-interactive",
        action="store_true",
        help="Skip interactive session in full mode"
    )
    
    parser.add_argument(
        "--notebooks",
        nargs="*",
        help="Specific notebooks to run (optional, runs all if not specified)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="Breast Cancer Agentic ML v1.0"
    )
    
    args = parser.parse_args()
    
    # Print welcome message
    print_header("Breast Cancer Agentic ML Pipeline", COLOR_BOLD + COLOR_GREEN)
    print(f"{COLOR_CYAN}Mode: {args.mode.upper()}{COLOR_RESET}")
    if args.mode == "agents":
        print(f"{COLOR_CYAN}Stage: {args.stage.upper()}{COLOR_RESET}")
    
    # Check dependencies
    if args.mode != "test":
        if not check_dependencies():
            print(f"\n{COLOR_RED}Please ensure all required files are present.{COLOR_RESET}")
            sys.exit(1)
    
    # Execute based on mode
    try:
        if args.mode == "test":
            run_quick_test()
        elif args.mode == "full":
            run_full_pipeline(interactive=not args.no_interactive)
        elif args.mode == "agents":
            run_agent_pipeline(stage=args.stage)
        elif args.mode == "notebooks":
            run_notebooks(notebooks=args.notebooks)
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        print(f"\n\n{COLOR_YELLOW}Operation cancelled by user.{COLOR_RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{COLOR_RED}Unexpected error: {e}{COLOR_RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
