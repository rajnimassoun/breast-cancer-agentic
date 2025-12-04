#!/usr/bin/env python
"""
Quick Start Script for Breast Cancer Agentic ML
================================================

This script provides an interactive menu to easily run different
modes of the breast cancer ML pipeline without remembering commands.

Usage:
    python quickstart.py
"""

import sys
import subprocess
from pathlib import Path


def clear_screen():
    """Clear the terminal screen."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_menu():
    """Display the main menu."""
    print("\n" + "="*70)
    print(" "*15 + "🩺 BREAST CANCER AGENTIC ML")
    print("="*70)
    print("\nSelect an option:\n")
    print("  [1] Run Full ML Pipeline (with interactive session)")
    print("  [2] Run Full ML Pipeline (without interactive session)")
    print("  [3] Run Agent Pipeline - All Stages")
    print("  [4] Run Agent Pipeline - EDA Only")
    print("  [5] Run Agent Pipeline - Modeling Only")
    print("  [6] Run Agent Pipeline - Explanation Only")
    print("  [7] Run Jupyter Notebooks (00_eda, 01_eda, etc.)")
    print("  [8] Run Quick Test (verify setup)")
    print("  [0] Exit")
    print("\n" + "="*70)


def run_command(mode, stage=None, no_interactive=False):
    """Execute the main.py with specified arguments."""
    python_exe = sys.executable
    cmd = [python_exe, "main.py", "--mode", mode]
    
    if stage:
        cmd.extend(["--stage", stage])
    
    if no_interactive:
        cmd.append("--no-interactive")
    
    print(f"\n🚀 Running: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error: Command failed with exit code {e.returncode}")
        return e.returncode
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user.")
        return 1


def main():
    """Main interactive menu loop."""
    # Check if main.py exists
    if not Path("main.py").exists():
        print("\n❌ Error: main.py not found in current directory!")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    while True:
        print_menu()
        
        try:
            choice = input("\nEnter your choice (0-8): ").strip()
            
            if choice == "0":
                print("\n👋 Goodbye!\n")
                sys.exit(0)
            
            elif choice == "1":
                run_command("full", no_interactive=False)
                input("\n✓ Press Enter to return to menu...")
            
            elif choice == "2":
                run_command("full", no_interactive=True)
                input("\n✓ Press Enter to return to menu...")
            
            elif choice == "3":
                run_command("agents", stage="all")
                input("\n✓ Press Enter to return to menu...")
            
            elif choice == "4":
                run_command("agents", stage="eda")
                input("\n✓ Press Enter to return to menu...")
            
            elif choice == "5":
                run_command("agents", stage="modeling")
                input("\n✓ Press Enter to return to menu...")
            
            elif choice == "6":
                run_command("agents", stage="explain")
                input("\n✓ Press Enter to return to menu...")
            
            elif choice == "7":
                run_command("notebooks")
                input("\n✓ Press Enter to return to menu...")
            
            elif choice == "8":
                run_command("test")
                input("\n✓ Press Enter to return to menu...")
            
            else:
                print("\n⚠️  Invalid choice. Please enter a number between 0 and 8.")
                input("Press Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
