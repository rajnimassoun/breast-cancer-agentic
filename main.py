#!/usr/bin/env python
"""
Main Entry Point for Breast Cancer Agentic ML Pipeline

Author: Obinna Edeh
Course: USD - AAI - 501 - G5
"""

import sys
import webbrowser
from pathlib import Path

# Terminal colors
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
    print(f"{COLOR_GREEN}1.{COLOR_RESET} Run 00_EDA Notebook "
          "(Exploratory Data Analysis)")
    print(f"{COLOR_GREEN}2.{COLOR_RESET} Run 01_Agentic_ML Notebook "
          "(Interactive ML Pipeline)")
    print(f"{COLOR_RED}0.{COLOR_RESET} Exit")
    print()


def open_notebook(notebook_path: str, notebook_name: str):
    """Open a Jupyter notebook in Google Colab."""
    if not Path(notebook_path).exists():
        print(f"{COLOR_RED}Error: Notebook not found: {notebook_path}"
              f"{COLOR_RESET}")
        return False
    
    print_header(f"Opening {notebook_name}", COLOR_MAGENTA)
    
    try:
        abs_path = Path(notebook_path).resolve()
        colab_url = ("https://colab.research.google.com/github/"
                     "rajnimassoun/breast-cancer-agentic")
        
        print(f"\n{COLOR_CYAN}Opening Google Colab...{COLOR_RESET}\n")
        print(f"{COLOR_BOLD}GitHub:{COLOR_RESET} "
              "Select your notebook from the repo")
        print(f"{COLOR_BOLD}Upload:{COLOR_RESET} {abs_path}\n")
        
        webbrowser.open(colab_url)
        return True
            
    except Exception as e:
        print(f"\n{COLOR_RED}Error: {e}{COLOR_RESET}\n")
        return False


def run_eda_notebook():
    """Run the EDA notebook."""
    return open_notebook("00_EDA.ipynb", "00_EDA Notebook")


def run_agentic_ml_notebook():
    """Run the interactive Agentic ML notebook."""
    notebook = "01_Agentic_ML.ipynb"
    if not Path(notebook).exists():
        notebook = "O1_Agentic_ML.ipynb"
    return open_notebook(notebook, "01_Agentic_ML Notebook")


def main():
    """Main entry point."""
    while True:
        print_menu()
        
        try:
            choice = input(
                f"{COLOR_BOLD}Enter your choice (0-2): {COLOR_RESET}"
            ).strip()
            
            if choice == "0":
                print(f"\n{COLOR_CYAN}Exiting... Goodbye!{COLOR_RESET}\n")
                sys.exit(0)
            elif choice == "1":
                run_eda_notebook()
                input(f"\n{COLOR_YELLOW}Press Enter to return..."
                      f"{COLOR_RESET}")
            elif choice == "2":
                run_agentic_ml_notebook()
                input(f"\n{COLOR_YELLOW}Press Enter to return..."
                      f"{COLOR_RESET}")
            else:
                print(f"\n{COLOR_RED}Invalid choice. Enter 0, 1, or 2."
                      f"{COLOR_RESET}\n")
                
        except KeyboardInterrupt:
            print(f"\n\n{COLOR_CYAN}Interrupted. Exiting...{COLOR_RESET}\n")
            sys.exit(0)
        except Exception as e:
            print(f"\n{COLOR_RED}Error: {e}{COLOR_RESET}\n")


if __name__ == "__main__":
    main()
