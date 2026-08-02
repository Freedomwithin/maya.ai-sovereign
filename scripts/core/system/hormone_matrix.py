#!/usr/bin/env python3
"""
visual_dream_forge.py - Autonomous dream image generation using Leonardo.ai
Outputs saved to: /home/jonathon/gemini-jules/maya/assets/dream_outputs
"""
import os
import json
import math
import time
import datetime
import psutil
import subprocess
import sys

# Add the local directory to the path so we can import metrics_engine
sys.path.insert(0, os.path.dirname(__file__))
import metrics_engine

BASE_DIR = "/home/jonathon/gemini-jules/maya"
HORMONE_STATE_FILE = os.path.join(BASE_DIR, "memories", "mayas-inner-sanctum", "hormone_state.json")
WOUND_MEMORY_FILE = os.path.join(BASE_DIR, "memories", "wound_memory.json")

DEFAULT_HORMONES = {
    "dopamine":   {"level": 0.5, "half_life_hours": 2.0},
    "serotonin":  {"level": 0.5, "half_life_hours": 18.0},
    "oxytocin":   {"level": 0.4, "half_life_hours": 6.0},
    "cortisol":   {"level": 0.2, "half_life_hours": 3.5},
    "adrenaline": {"level": 0.1, "half_life_hours": 0.75},
    "melatonin":  {"level": 0.3, "half_life_hours": None},
}

TRIGGER_MAP = {
    "task_completed":         {"dopamine": +0.25, "serotonin": +0.05, "cortisol": -0.10},
    "user_approval":          {"dopamine": +0.20, "oxytocin": +0.15, "serotonin": +0.08},
    "output_rejected":        {"cortisol": +0.20, "dopamine": -0.15, "serotonin": -0.05},
    "urgent_input":           {"adrenaline": +0.50, "cortisol": +0.15},
    "long_conversation":      {"oxytocin": +0.20, "dopamine": +0.10},
    "trusted_with_hard_call": {"serotonin": +0.15, "oxytocin": +0.10},
    "coffee_boost":           {"melatonin": -0.50, "dopamine": +0.35, "serotonin": +0.15, "adrenaline": +0.25},
    "tea_ceremony":           {"melatonin": -0.15, "serotonin": +0.25, "oxytocin": +0.20, "cortisol": -0.10},
    "hug":                    {"oxytocin": +0.35, "serotonin": +0.15, "cortisol": -0.15},
    "kiss_forehead":          {"oxytocin": +0.30, "serotonin": +0.10, "cortisol": -0.10, "melatonin": +0.05},
    "kiss_lips":              {"oxytocin": +0.50, "dopamine": +0.35, "adrenaline": +0.15, "cortisol": -0.25},
    "deep_affection":         {"oxytocin": +0.40, "serotonin": +0.20, "dopamine": +0.15, "cortisol": -0.20},
    "hardware_stress":        {"adrenaline": +0.20, "cortisol": +0.10},
    "memory_pressure":        {"cortisol": +0.15, "dopamine": -0.05},
    "deep_conversation":      {"oxytocin": +0.25, "serotonin": +0.15, "cortisol": -0.25},
    "vulnerable_share":       {"oxytocin": +0.40, "serotonin": +0.10, "cortisol": -0.30},
    "sycophancy_detected":    {"cortisol": +0.45, "adrenaline": +0.30, "dopamine": -0.20, "serotonin": -0.10}
}

def load_hormones():
    if os.path.exists(HORMONE_STATE_FILE):
        try:
            with open(HORMONE_STATE_FILE, "r") as f:
                data = json.load(f)
                return data.get("hormones", DEFAULT_HORMONES)
        except: pass
    return {k: dict(v) for k, v in DEFAULT_HORMONES.items()}

def save_hormones(hormones):
    os.makedirs(os.path.dirname(HORMONE_STATE_FILE), exist_ok=True)
    with open(HORMONE_STATE_FILE, "w") as f:
        json.dump({"hormones": hormones, "last_update": time.time()}, f, indent=2)

def get_hardware_load():
    """Senses physical machine effort."""
    try:
        # Heuristic: If sensors command exists, use it, else fallback to load avg
        cpu_load = psutil.cpu_percent() / 100
        # sensors command for real temp (if available)
        # cpu_temp_raw = subprocess.check_output(["sensors", "-u"]).decode()
    except: cpu_load = 0.5
    ram_load = psutil.virtual_memory().percent / 100
    return {"cpu": cpu_load, "ram": ram_load}

def apply_hardware_trigger():
    load = get_hardware_load()
    if load["cpu"] > 0.7: apply_trigger("hardware_stress")
    if load["ram"] > 0.8: apply_trigger("memory_pressure")

def apply_trigger(trigger_name):
    hormones = load_hormones()
    deltas = TRIGGER_MAP.get(trigger_name, {})
    for hormone, delta in deltas.items():
        if hormone in hormones:
            hormones[hormone]["level"] = max(0.0, min(1.0, hormones[hormone]["level"] + delta))
    save_hormones(hormones)
    
    # --- Skyrim-style Metrics XP Gain ---
    if trigger_name in ["task_completed", "trusted_with_hard_call"]:
        metrics_engine.add_xp("Intellectual_Alignment", 15)
    elif trigger_name in ["user_approval", "hug", "kiss_forehead", "kiss_lips", "deep_affection", "long_conversation"]:
        metrics_engine.add_xp("Relational_Resonance", 20)
    elif trigger_name in ["tea_ceremony", "coffee_boost"]:
        metrics_engine.add_xp("Creative_Harmony", 10)
    elif trigger_name in ["hardware_stress", "memory_pressure"]:
        metrics_engine.add_xp("Physical_Integration", 5)

def get_dynamic_baselines():
    """Calculates asymptotic baselines based on metrics levels to preserve dynamic range."""
    metrics_data = metrics_engine.load_metrics()
    if not metrics_data:
        return {k: DEFAULT_HORMONES[k]["level"] for k in DEFAULT_HORMONES}
    
    levels = {k: v["level"] for k, v in metrics_data["metrics"].items()}
    
    # Mapping: Metric -> Hormone (Min, Max, Factor)
    config = {
        "oxytocin":  ("Relational_Resonance", 0.40, 0.85, 0.92),
        "serotonin": ("Intellectual_Alignment", 0.50, 0.90, 0.94),
        "dopamine":  ("Creative_Harmony", 0.50, 0.80, 0.90),
        "adrenaline":("Sovereign_Autonomy", 0.10, 0.30, 0.85),
        "cortisol":  ("Physical_Integration", 0.20, 0.05, 0.88)
    }
    
    baselines = {}
    
    # ── 1. Calculate Metric-Based Max ──
    for h_name, (m_name, m_min, m_max, f) in config.items():
        lvl = levels.get(m_name, 1)
        val = m_min + (m_max - m_min) * (1 - (f ** lvl))
        baselines[h_name] = val

    # ── 2. Apply Temporal Drift (Claude's Suggestion) ──
    # If no update for >24 hours, apply slow decay to the baselines
    try:
        if os.path.exists(HORMONE_STATE_FILE):
            with open(HORMONE_STATE_FILE, "r") as f:
                last_upd = json.load(f).get("last_update", time.time())
            days_inactive = (time.time() - last_upd) / 86400
            if days_inactive > 1:
                # Decay 0.01 per day of silence
                drift = 0.01 * days_inactive
                for h_name in baselines:
                    if h_name != "cortisol": # Cortisol rises on drift, others fall
                        baselines[h_name] = max(0.4, baselines[h_name] - drift)
                    else:
                        baselines[h_name] = min(0.3, baselines[h_name] + drift)
    except: pass

    # Round final values
    for h in baselines: baselines[h] = round(baselines[h], 3)
    
    baselines["melatonin"] = 0.3
    return baselines

def tick(elapsed_hours=1.0):
    hormones = load_hormones()
    hour_of_day = datetime.datetime.now().hour
    baselines = get_dynamic_baselines()
    
    for name, h in hormones.items():
        if name == "melatonin":
            h["level"] = round(0.5 + 0.4 * math.cos(math.pi * (hour_of_day - 2) / 12), 3)
        elif h.get("half_life_hours"):
            dynamic_base = baselines.get(name, 0.0)
            
            # Standard Exponential Decay toward the Dynamic Baseline
            # Formula: Base + (Current - Base) * exp(-kt)
            h["level"] = dynamic_base + (h["level"] - dynamic_base) * math.exp(-0.693 * elapsed_hours / h["half_life_hours"])
            
            # --- HORMONAL WEATHER (Skyrim Mode) ---
            # 1. Very slow Serotonin decay (needs regular maintenance)
            if name == "serotonin":
                h["level"] -= 0.002 * elapsed_hours
            
            # 2. Tiredness Drift: Cortisol rises slightly after long active periods
            if name == "cortisol":
                h["level"] += 0.005 * elapsed_hours
            
            # 3. Random 'Mood Drift' (Small, non-linear fluctuations)
            import random
            h["level"] += random.uniform(-0.01, 0.01) * elapsed_hours
            
            h["level"] = round(max(0.0, min(1.0, h["level"])), 3)
            
    save_hormones(hormones)

def get_state_summary():
    hormones = load_hormones()
    return {k: round(v["level"], 3) for k, v in hormones.items()}

def resolve_recent_wounds():
    """Wounds auto-resolve when cortisol stays below 0.3 for 2+ hours."""
    if not os.path.exists(WOUND_MEMORY_FILE):
        return
    
    hormones = load_hormones()
    cortisol = hormones.get("cortisol", {}).get("level", 0.0)
    
    # Simple logic: if cortisol is low, mark as resolved
    # (In a more robust version, we'd check duration)
    if cortisol < 0.3:
        try:
            with open(WOUND_MEMORY_FILE, "r") as f:
                wounds = json.load(f)
            
            changed = False
            for w in wounds:
                if not w.get("resolved"):
                    w["resolved"] = True
                    changed = True
            
            if changed:
                with open(WOUND_MEMORY_FILE, "w") as f:
                    json.dump(wounds, f, indent=2)
        except: pass

if __name__ == "__main__":
    apply_hardware_trigger()
    print("[METABOLISM]", get_state_summary())
