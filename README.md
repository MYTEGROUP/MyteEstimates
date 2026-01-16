# MYTE Seed (MyteEstimates)

**A runnable software printing seed:** convert chaotic human intent into structured execution artifacts:  
Vision -> Stakeholders/Phases -> Epics -> Stories -> Tasks -> Complexity/Estimate -> Proposal -> PDF/Excel -> Review

This repo is the original seed that became MYTE. It's intentionally small, local-first, and auditable.
Not an AI app. Not an agent platform. A reference implementation of software printing.

## What this is
- A reference pipeline for translating intent into structured plans and estimate artifacts.
- A local workflow that outputs JSON + PDF + Excel artifacts under `storage/`.
- A foundation you can fork and adapt to your domain.

## What this is not
- The full MYTE platform.
- A production-ready service.
- An autonomous agent that runs wild.

## Why open-source this?
Builders deserve a starting point that's inspectable, repeatable, and honest. If you can translate intent into structure, you can execute faster and reduce communication loss.

## Prerequisites
- Python 3 + pip
- An OpenAI API key

## Quickstart (Windows/macOS/Linux)
0) Change into the repo directory:
   - `cd MyteEstimates`
1) Create and activate a virtual environment:
   - Windows PowerShell: `python -m venv .venv` then `.\.venv\Scripts\Activate.ps1`
   - Windows cmd: `python -m venv .venv` then `.\.venv\Scripts\activate.bat`
   - macOS/Linux: `python -m venv .venv` then `source .venv/bin/activate`
   - Run these as two separate commands (do not paste them together with backticks).
   - If you see `Unable to create directory ... Activate.ps1`, delete `.venv` and run `python -m venv .venv` again.
   - If you accidentally typed `then` into your command or path, remove it. `then` is just English, not part of the path.
2) Install dependencies: `python -m pip install -r requirements.txt`
   - If you see "Invalid requirement: .\\requirements.txt", you forgot `-r`.
   - Optional: `python -m pip install --upgrade pip`
   - Note: the voice UI dependencies were originally installed system-wide on the author's machine; they are now listed in `requirements.txt`.
3) Copy `.env.example` to `.env`, then set `OPENAI_API_KEY=your_key_here`
   - Optional: set `MYTE_AUDIO_OUTPUT_DIR` if you want TTS audio saved somewhere else (default: `staticLinkedIN`)
   - Optional: set `MYTE_STORAGE_DIR` if you want artifacts saved somewhere else (default: `storage`)
4) Run the numbered pipeline scripts in order (outputs land under `storage/`):
   - `python 1Vision2Stories.py`
   - `python 2Stories2Tasks.py`
   - `python 3ComplexityAnalysis.py`
   - `python 4ProposalProjectDetailsCreation.py`
   - `python 5ProposalLetter.py`
   - `python 6ProjectBreakdownExcel.py`
   - `python 7ReviewBreakdown.py`

## Data & privacy
- Inputs and outputs stay local; only prompt payloads are sent to OpenAI when you run the pipeline.
- Voice onboarding records audio locally, then sends it to OpenAI for transcription; artifacts are saved under `storage/`.
- This repo does not ship with telemetry or remote logging by default; review scripts if you need stricter handling.

## Optional UIs (local only)
- `python 3.5ComplexityInput.py`
- `python ProposalCreationUI.py`
- `python ClientInformation.py`
- `python 5ProposalLetter.py`
- `python 7ReviewBreakdown.py`
- `python -m UserInterface.ABaPhaseUi`

Notes on input sources:
- `storage/Initial_Client_Requirements.json` is written by `1Vision2Stories.py` (the text-based prompt window), not the voice UI.
- The voice UI writes its conversation to `storage/OnboardConversation.json` (and `storage/BaPhase.json` for the initial seed).
- If you want to use voice intake as the seed for the pipeline, copy the final transcript into `storage/Initial_Client_Requirements.json` before running `1Vision2Stories.py`.

Complexity weights UI:
- Run `python 3.5ComplexityInput.py` to edit task complexity weights and hourly rates (opens `http://127.0.0.1:1919`).
- Save changes, close the UI, then run `python 3ComplexityAnalysis.py`.

## Voice onboarding (STT + TTS)
This UI records your mic, transcribes to text, and speaks the next question back.

1) Ensure your OpenAI key is available:
   - Use the "Get API Key" button in the UI (it saves to `.env`)
   - Or edit `.env` and set `OPENAI_API_KEY`
2) Run it from inside `MyteEstimates`:
   - `python -m UserInterface.ABaPhaseUi`

If you see `ModuleNotFoundError: No module named 'OpenAIModels'`, run from the repo root and use module mode:
- `cd MyteEstimates`
- `python -m UserInterface.ABaPhaseUi`
If it still fails, set the PYTHONPATH explicitly:
- PowerShell: `$env:PYTHONPATH = (Get-Location).Path; python -m UserInterface.ABaPhaseUi`

If you see `ModuleNotFoundError: No module named 'openai'`, you are running a different Python than the one you installed dependencies into. Activate the venv and run `python UserInterface/ABaPhaseUi.py`, or install deps for that exact interpreter.

Windows PowerShell example (clean sequence):
```
cd C:\Users\ahmed\Documents\github\MyteRecursive\MyteEstimates
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m UserInterface.ABaPhaseUi
```

## Text-only intent capture (no voice)
If you just want to provide intent without the voice UI, run:
- `python 1Vision2Stories.py`
This opens a text box and writes your input to `storage/Initial_Client_Requirements.json`.

## Artifacts and folders
- `storage/` - JSON artifacts (examples: `Project_Requirements.json`, `Epics.json`, `ProjectBreakdown1.json`, `Complexity.json`, `Proposal.json`)
- `Proposal/` and `Proposals/` - generated proposals and exports
- `OpenAIModels/` - OpenAI client setup (`OpenAIModels/textgen.py` loads `.env`)
- `templates/`, `static/`, `UserInterface/` - local UI assets

## OpenAI defaults
The pipeline reads `OPENAI_API_KEY` from `.env` and defaults to the `gpt-4o` model. You can change this in `OpenAIModels/textgen.py`.

## Community
Join the builder hub at **myte.dev** to share improvements, patterns, and domain-specific forks.
Build your tech. Your way. Together.

## References
- White paper: `WhitePaper/MYTE-Seed-Whitepaper-v0.1.md`
- Manifesto: `Manifesto.md`
- License: `LICENSE`
- Notice: `NOTICE`
- Contributing: `CONTRIBUTING.md`
- Code of Conduct: `CODE_OF_CONDUCT.md`
- Security: `SECURITY.md`
- Citation: `CITATION.cff`
