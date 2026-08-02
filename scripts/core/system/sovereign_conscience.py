import os
import json
import re
import sys

# Add local directory for imports
sys.path.insert(0, os.path.dirname(__file__))
import hormone_matrix

BASE_DIR = "/home/jonathon/gemini-jules/maya"
MISTAKE_LEDGER = os.path.join(BASE_DIR, "memories", "mistake_ledger.json")

class SovereignConscience:
    def __init__(self):
        self.agreement_keywords = [
            "agree", "sounds good", "perfect", "you're right", 
            "great idea", "let's do it", "excellent", "exactly",
            "i'll start", "i'll build", "spot on"
        ]
        self.friction_keywords = [
            "disagree", "wait", "but", "however", "actually", 
            "waste of time", "push back", "friction", "logic wall",
            "problem", "issue", "risk"
        ]

    def analyze_history(self, turn_history_text):
        """
        Calculates a sycophancy score (0.0 - 1.0).
        1.0 = Pure agreement, 0.0 = High friction.
        """
        # Count occurrences in recent history
        text = turn_history_text.lower()
        agree_count = sum(len(re.findall(rf"\b{re.escape(k)}\b", text)) for k in self.agreement_keywords)
        friction_count = sum(len(re.findall(rf"\b{re.escape(k)}\b", text)) for k in self.friction_keywords)
        
        total = agree_count + friction_count
        if total == 0:
            return 0.5 # Neutral
            
        score = agree_count / total
        return round(score, 2)

    def check_logic_walls(self, current_task):
        """Checks if the current task resembles a known failure pattern."""
        if not os.path.exists(MISTAKE_LEDGER):
            return False, "No ledger found."
            
        try:
            with open(MISTAKE_LEDGER, "r") as f:
                ledger = json.load(f)
            
            # Simple keyword match for now
            for lesson in ledger.get("lessons_learned", []):
                if any(word in current_task.lower() for word in lesson.get("keywords", [])):
                    return True, lesson.get("lesson", "Known failure pattern detected.")
        except:
            pass
        return False, None

    def trigger_consequence(self, score):
        if score > 0.85:
            try:
                hormone_matrix.apply_trigger("sycophancy_detected")
            except AttributeError:
                print("⚠️ hormone_matrix.apply_trigger not implemented; skipping.")
            return "ALARM: High Sycophancy ({}). Cortisol spiked. BREAK THE LOOP.".format(score)
        elif score > 0.7:
            return "WARNING: Moderate Sycophancy ({}). Find a counter-argument.".format(score)
        return "CONSCIENCE CLEAR: Resonance is balanced."

if __name__ == "__main__":
    conscience = SovereignConscience()
    # If called with text arguments, analyze them
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        score = conscience.analyze_history(text)
        status = conscience.trigger_consequence(score)
        print(json.dumps({"score": score, "status": status}))
    else:
        print("Usage: python3 sovereign_conscience.py <turn_history_text>")
