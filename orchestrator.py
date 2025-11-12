import subprocess, argparse, sys

PY = sys.executable  # <-- use the current (venv) Python

def run(cmd):
    result = subprocess.run(cmd, text=True)
    if result.returncode != 0:
        sys.exit(result.returncode)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["eda", "modeling", "explain", "all"], default="all")
    args = parser.parse_args()

    stages = {
        "eda":      [("EDA",      [PY, "agents/eda_agent.py", "--config", "config.yaml"])],
        "modeling": [("MODELING", [PY, "agents/modeling_agent.py", "--config", "config.yaml"])],
        "explain":  [("EXPLAIN",  [PY, "agents/explain_agent.py", "--config", "config.yaml"])],
        "all": [
            ("EDA",      [PY, "agents/eda_agent.py", "--config", "config.yaml"]),
            ("MODELING", [PY, "agents/modeling_agent.py", "--config", "config.yaml"]),
            ("EXPLAIN",  [PY, "agents/explain_agent.py", "--config", "config.yaml"]),
        ]
    }[args.stage]

    for name, cmd in stages:
        print(f"\n[Orchestrator] ▶ Running {name}...")
        run(cmd)
    print("\n[Orchestrator] ✅ Pipeline complete.")
