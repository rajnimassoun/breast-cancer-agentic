#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main Entry Point for Breast Cancer Agentic ML Pipeline
=======================================================

This script provides a simple menu interface to run the ML pipeline notebooks.

Usage:
------
    python main.py

Author: Obinna Edeh
Course: USD - AAI - 501 - G5
"""

import sys
import subprocess
from pathlib import Path


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


def print_menu():
    """Display the main menu."""
    print_header("Breast Cancer Agentic ML Pipeline", COLOR_CYAN)
    print(f"{COLOR_BOLD}Select an option:{COLOR_RESET}\n")
    print(f"{COLOR_GREEN}1.{COLOR_RESET} Run 01_EDA Notebook (Exploratory Data Analysis)")
    print(f"{COLOR_GREEN}2.{COLOR_RESET} Run 02_Agentic_ML Notebook (Interactive ML Pipeline)")
    print(f"{COLOR_RED}0.{COLOR_RESET} Exit")
    print()


def open_notebook(notebook_path: str, notebook_name: str):
    """
    Open a Jupyter notebook in Google Colab.
    
    Args:
        notebook_path: Path to the notebook file
        notebook_name: Display name of the notebook
    """
    if not Path(notebook_path).exists():
        print(f"{COLOR_RED}Error: Notebook not found: {notebook_path}{COLOR_RESET}")
        return False
    
    print_header(f"Opening {notebook_name}", COLOR_MAGENTA)
    print(f"{COLOR_YELLOW}Opening notebook in Google Colab: {notebook_path}{COLOR_RESET}")
    
    try:
        # Get absolute path
        abs_path = Path(notebook_path).resolve()
        
        # Check if the file is in a GitHub repo
        print(f"\n{COLOR_CYAN}To open this notebook in Google Colab:{COLOR_RESET}")
        print(f"{COLOR_BOLD}Option 1 - Via GitHub:{COLOR_RESET}")
        print(f"  1. Make sure your notebook is pushed to GitHub")
        print(f"  2. Go to: https://colab.research.google.com/")
        print(f"  3. Click 'GitHub' tab")
        print(f"  4. Enter: rajnimassoun/breast-cancer-agentic")
        print(f"  5. Select your notebook\n")
        
        print(f"{COLOR_BOLD}Option 2 - Upload directly:{COLOR_RESET}")
        print(f"  1. Go to: https://colab.research.google.com/")
        print(f"  2. Click 'Upload' tab")
        print(f"  3. Upload: {abs_path}\n")
        
        # Try to open Colab in browser
        import webbrowser
        
        # Open Colab GitHub interface with the repo
        colab_url = "https://colab.research.google.com/github/rajnimassoun/breast-cancer-agentic"
        print(f"{COLOR_GREEN}Opening Google Colab in browser...{COLOR_RESET}\n")
        webbrowser.open(colab_url)
        
        print(f"{COLOR_CYAN}Local file location: {abs_path}{COLOR_RESET}")
        
        return True
            
    except Exception as e:
        print(f"\n{COLOR_RED}✗ Error opening {notebook_name}: {e}{COLOR_RESET}\n")
        return False


def run_eda_notebook():
    """Run the EDA notebook."""
    notebook_path = "notebooks/01_eda.ipynb"
    return open_notebook(notebook_path, "01_EDA Notebook")


def run_agentic_ml_notebook():
    """Run the interactive Agentic ML notebook."""
    notebook_path = "02_Agentic_ML.ipynb"
    if not Path(notebook_path).exists():
        # Try alternative name
        notebook_path = "OEDEH_Agentic_ML.ipynb"
    return open_notebook(notebook_path, "02_Agentic_ML Notebook (Interactive)")


def main():
    """Main entry point."""
    while True:
        print_menu()
        
        try:
            choice = input(f"{COLOR_BOLD}Enter your choice (0-2): {COLOR_RESET}").strip()
            
            if choice == "0":
                print(f"\n{COLOR_CYAN}Exiting... Goodbye!{COLOR_RESET}\n")
                sys.exit(0)
            
            elif choice == "1":
                run_eda_notebook()
                input(f"\n{COLOR_YELLOW}Press Enter to return to menu...{COLOR_RESET}")
            
            elif choice == "2":
                run_agentic_ml_notebook()
                input(f"\n{COLOR_YELLOW}Press Enter to return to menu...{COLOR_RESET}")
            
            else:
                print(f"\n{COLOR_RED}Invalid choice. Please enter 0, 1, or 2.{COLOR_RESET}\n")
                
        except KeyboardInterrupt:
            print(f"\n\n{COLOR_CYAN}Interrupted. Exiting...{COLOR_RESET}\n")
            sys.exit(0)
        except Exception as e:
            print(f"\n{COLOR_RED}Error: {e}{COLOR_RESET}\n")


if __name__ == "__main__":
    main()
