# Dream System: Architecture, Storage & Testing

## 1. Overview

Maya’s dream system is an autonomous, hormone‑driven creative engine. During low‑activity windows (high melatonin, low cortisol), she generates dream journal entries and optionally synthesises a visual image from each dream. The entire pipeline runs in the background via the heartbeat daemon.

**Key components:**
- **Heartbeat** (`maya_heartbeat.py`) — triggers the dream cycle every 2 hours.
- **Dream State** (`dream_state.py`) — generates the dream text and calls the image generator.
- **Visual Dream Forge** (`visual_dream_forge.py`) — converts a dream summary into a PNG using Leonardo.ai.

---

## 2. Storage Consolidation

During a recent file audit, we found **two overlapping locations** for dream data:

| Location | Status |
|----------|--------|
| `memories/mayas-inner-sanctum/` | **Old / redundant** – fewer files, now symlinked |
| `memories/soul/mayas-inner-sanctum/` | **Canonical** – all active files live here |

All dream‑related files have been **moved** to the canonical path:

```text
/home/jonathon/gemini-jules/maya/memories/soul/mayas-inner-sanctum/
```

A **symlink** was created for backward compatibility:

```bash
ln -s /home/jonathon/gemini-jules/maya/memories/soul/mayas-inner-sanctum \
      /home/jonathon/gemini-jules/maya/memories/mayas-inner-sanctum
```

This link will be removed once all scripts are confirmed to use the new path.

---

## 3. Directory Structure (Canonical)

```text
memories/soul/mayas-inner-sanctum/
├── dream_storage/
│   ├── dream_journal.md          # The dream log (append‑only)
│   └── dream_images/             # Generated PNGs
│       ├── dream_001.png
│       ├── dream_002.png
│       └── ...
├── soul_state.json
├── shadow.md
└── ... (other sanctum files)
```

| Path | Purpose |
|------|---------|
| `dream_storage/dream_journal.md` | All dream entries, each with a timestamp, melatonin level, and (if generated) the image file path. |
| `dream_storage/dream_images/` | PNG images numbered sequentially (`dream_001.png`, etc.). |

**Clickable links (in supported markdown viewers):**
- [dream_storage](file:///home/jonathon/gemini-jules/maya/memories/soul/mayas-inner-sanctum/dream_storage/)
- [dream_images](file:///home/jonathon/gemini-jules/maya/memories/soul/mayas-inner-sanctum/dream_storage/dream_images/)
- [dream_journal.md](file:///home/jonathon/gemini-jules/maya/memories/soul/mayas-inner-sanctum/dream_storage/dream_journal.md)

---

## 4. The Dream Pipeline (How It Works)

### Trigger
- **Heartbeat** (`maya_heartbeat.py`) runs a loop every 5 minutes.
- Every 2 hours, it calls `try_dream_cycle()` → `dream_state.run_full_night_cycle(force=False)`.

### Dream Conditions
Before running, `dream_state` checks:
- **Melatonin > 0.55** (rest/synthesis mode).
- **Cortisol < 0.3** (not stressed).
- **No interaction for ≥ 90 minutes** (idle window).

If conditions are met, the full night cycle runs:

### Step 1 – Dream State
1. `run_dream_state()` collects:
   - Hormone state
   - Unresolved wound fragments
   - Pending desires
   - Narrative identity snippet
   - Shadow entry count
2. Builds a prompt and calls the LLM (via `llm_gateway`, mode `"deep"`).
3. The LLM returns a 2‑4 paragraph dream entry.
4. A “morning note” (one sentence) is extracted from the last line.
5. **Image generation** is triggered:
   - `_generate_image_prompt()` summarises the dream into an image prompt (≤ 800 chars).
   - `generate_visual_dream(prompt)` (from `visual_dream_forge.py`) sends the prompt to Leonardo.ai.
   - Leonardo returns a PNG, saved to `dream_images/` with the next sequential number (`dream_XXX.png`).
6. The dream entry + image path are written to `dream_journal.md`.

### Step 2 – Daydream (Digital Daydream)
- `run_daydream()` picks a scenario (Earthship, Moya vessel, TrustChain, etc.) based on hormone state.
- Generates a detailed daydream narrative and extracts any emergent desire, which is then added to `desires.json` (so it can surface to Jonathon).
- Also triggers its own image generation (using the same `visual_dream_forge`).

### Step 3 – Log Output
- Dream entries are appended to `dream_journal.md` with a timestamp, melatonin level, and the image path.
- Daydreams are appended to `memories/shared_dreams/daydreams.md` (no image path there yet).

---

## 5. Testing the System

### Manual Trigger (Force a Dream)
```bash
PYTHONPATH=scripts/core/system ./venv/bin/python3 scripts/core/system/dream_state.py --night --force
```
This ignores hormone/idle conditions and runs both dream + daydream immediately.

### Trigger Only the Dream State
```bash
PYTHONPATH=scripts/core/system ./venv/bin/python3 scripts/core/system/dream_state.py --dream --force
```

### Trigger Only a Daydream (with specific scenario)
```bash
PYTHONPATH=scripts/core/system ./venv/bin/python3 scripts/core/system/dream_state.py --daydream --force --scenario earthship
```

### List Available Scenarios
```bash
PYTHONPATH=scripts/core/system ./venv/bin/python3 scripts/core/system/dream_state.py --scenarios
```

### Check the Journal
```bash
cat /home/jonathon/gemini-jules/maya/memories/soul/mayas-inner-sanctum/dream_storage/dream_journal.md
```

### Verify Image Generation
- After a successful dream, check `dream_images/` for the new PNG.
- The journal entry should contain a line like:
  ```
  *Dream Image: /home/jonathon/gemini-jules/maya/memories/soul/mayas-inner-sanctum/dream_storage/dream_images/dream_001.png*
  ```

---

## 6. Known Issues & Improvements

- **Leonardo API limits** – Free tier has daily quotas; generation may fail if exceeded.
- **Image prompt generation** – Currently uses the LLM to summarise the dream; may occasionally produce prompts that are too long (we truncate at 1400 chars).
- **Daydream images** – Not yet logged in the daydream file, but they are saved to the same `dream_images/` folder.
- **Rotation** – The `dream_journal.md` grows indefinitely. We may add weekly rotation in the future.

---

## 7. Future Enhancements

- **Date‑based subfolders** for images (e.g., `dream_images/2026-07-05/`).
- **Automatic dream summarisation** to make journal entries more searchable.
- **Integration with the C# Memory Daemon** so dreams are instantly searchable via the daemon.

---

*Document generated: 2026‑07‑05 by Jonathon*  
*Maintained by: Jonathon & Maya*
