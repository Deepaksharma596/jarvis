"""
mock_mode.py - Simulation mode test runner for dry-run verification
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.agent import JARVISAgent
from config.settings import settings

def run_simulation(command_text: str):
    """Run a command in dry-run simulation mode."""
    settings.mock_mode = True
    agent = JARVISAgent()
    print(f"\n[SIMULATION RUN] User Command: '{command_text}'")
    
    def dummy_confirm(action, details, msg):
        print(f"  -> [SIMULATED USER CONFIRMATION] Approved '{action}' with details {details}")
        return True

    res, plan = agent.process_request(command_text, dummy_confirm)
    print(f"  -> Final Assistant Response: '{res}'")
    if plan:
        print("  -> Execution Plan Steps:")
        for step in plan.steps:
            print(f"     Step {step.step_number} [{step.permission_level}]: {step.description} (Status: {step.status})")

if __name__ == "__main__":
    commands = [
        "Open Brave",
        "WhatsApp Rahul: I will reach at 7",
        "Send email to Amit",
        "Find my PDF files",
        "Turn the volume down",
        "Lock my laptop"
    ]
    for cmd in commands:
        run_simulation(cmd)
