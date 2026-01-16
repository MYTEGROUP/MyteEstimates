# TECHNICAL OVERVIEW — MYTE Seed (MyteEstimates)

This repository is the original **MYTE Seed**: a runnable, artifact-driven pipeline that converts **unstructured human intent** into **structured execution artifacts** (epics -> stories -> tasks -> estimates -> proposal outputs).  
It is intentionally **small, local-first, and auditable**.

**This is not the full Myte Cody platform.**  
The full platform adds enterprise governance (multi-tenant orgs, RBAC, approvals, audit trails, deployments, etc.).  
This seed exists so builders can study the mechanics of "software printing" in an inspectable form.

---

## What this is (high-level)
This codebase is best described as:

> **A deterministic, multi-pass "intent compiler" that produces explicit intermediate representations (IR) as JSON artifacts, with optional local UIs for review and export.**

It is **not** "chain-of-thought."  
It's **structured compilation**: each pipeline stage outputs a persistent artifact you can inspect, edit, version, and re-run.

---

## Goals
- Convert free-form intent into **structured, executable artifacts**
- Make reasoning **inspectable and replayable**
- Keep outputs **ordered**, **versionable**, and **editable**
- Enable **human review** (approve/edit/delete) before downstream outputs
- Produce real exports: **PDF proposal** + **Excel breakdown**

---

## Non-goals
- Not a production SaaS
- Not a full governance/authorization system
- Not multi-tenant
- Not autonomous execution against external systems
- Not a new model or inference algorithm

---

## Architecture at a glance

The pipeline is a set of numbered "compiler passes" that read/write JSON artifacts under `storage/`.

```

[Intent Input]
|
v

1. Vision -> Requirements (Project_Requirements.json)
   |
   v
   (vision summaries) -> ProjectSummary.json
   |
   v
   Epics -> Epics.json
   |
   v
   Stories + Tasks -> ProjectBreakdown.json / ProjectBreakdown1.json
   |
   v
   Complexity + Costing -> ProjectBreakdown1.json (enriched)
   |
   v
   Proposal (Proposal.json) -> PDF + Excel exports
   |
   v
   Human Review Gate (ApproveBreakdown UI edits ProjectBreakdown1.json)

```

**Key principle:** every stage emits a structured artifact (IR). Nothing is "hidden inside chat."

---

## Pipeline stages (what each script does)

### `1Vision2Stories.py`
**Purpose:** captures initial intent and compiles it into structured requirement sections.  
**How:** prompts the model section-by-section using a template (`project_description_template.json`) and writes outputs into `storage/`.

**Key outputs:**
- `storage/Initial_Client_Requirements.json`
- `storage/Project_Requirements.json`
- `storage/ProjectSummary.json` (vision, vertical, stakeholders, revenue models)

**Notes:**
- Uses multithreading to process template sections in parallel.
- Provides optional stakeholder editing via Tkinter.

---

### `2Stories2Tasks.py`
**Purpose:** decomposes epics/stories into granular development tasks.  
**How:** reads epics + stories and generates tasks in JSON format.

**Key outputs:**
- `storage/ProjectBreakdown1.json` (tasks assigned IDs: `T001`, `T002`, ...)

**Notes on determinism:**
- Uses `response_format: json_object` for structure.
- Uses concurrency + a semaphore as a rate-limiting primitive.

---

### `3.5ComplexityInput.py` (optional UI)
**Purpose:** local UI to set complexity weights and hourly rate used for estimating.  
**Key output:**
- `storage/Complexity.json`

---

### `3ComplexityAnalysis.py`
**Purpose:** labels each task with a complexity class and computes hours + cost.  
**How:** for each task, asks the model to choose a complexity label from a bounded set, then applies weights from `Complexity.json`.

**Key output:**
- Updates `storage/ProjectBreakdown1.json` tasks with:
  - `Complexity`
  - `Estimated Hours`
  - `Cost`

**Notes:**
- Uses worker threads + queue.
- Includes a structured complexity rubric inside the prompt to reduce variance.

---

### `4ProposalProjectDetailsCreation.py`
**Purpose:** synthesizes proposal-level narrative artifacts (title, summary, scope, deliverables) and attaches budgeting and metadata.

**Key outputs:**
- `storage/Proposal.json` (includes milestones, risks, budget totals, and cost breakdown)

---

### `5ProposalLetter.py`
**Purpose:** renders `Proposal.json` into HTML and exports a PDF using WeasyPrint.

**Key outputs:**
- `Proposal/… .pdf` (saved locally)

---

### `6ProjectBreakdownExcel.py`
**Purpose:** converts the structured plan into a styled Excel sheet for scanning and costing.

**Key output:**
- `StyledProjectBreakdown.xlsx`

---

### `7ReviewBreakdown.py` (local review gate)
**Purpose:** a human-in-the-loop approval UI for tasks/stories/epics.  
**Why it matters:** this is the governance primitive in the seed: you can **edit**, **approve**, and **delete** before downstream consumption.

**Key behavior:**
- Approve Task -> sets `approved=true`
- Approve Story -> requires all tasks approved
- Approve Epic -> requires all stories approved
- Delete Task/Story/Epic -> removes nodes from IR
- Writes edits back into `storage/ProjectBreakdown1.json`

---

## Determinism & "Why this isn't just prompt chaining"
This seed avoids "prompt soup" by enforcing:
- **Explicit schemas** (JSON artifacts at every stage)
- **Versionable intermediate representations** (`storage/*.json`)
- **Constrained outputs** (`response_format: json_object` where applicable)
- **Ordered IDs** (`E001`, `S001`, `T001`...)
- **Human validation** via a local review UI
- **Replayability**: re-run stages after editing artifacts

In short:
> The model is a transformer inside a harness. The artifacts are the truth.

---

## Storage & artifact model (IR)
All persistent artifacts default to `storage/` (configurable via `MYTE_STORAGE_DIR`).

Typical artifacts:
- `Initial_Client_Requirements.json` — raw user intent
- `Project_Requirements.json` — structured requirements sections
- `ProjectSummary.json` — vision + vertical + stakeholders + revenue models
- `Epics.json` — stakeholder-specific epics
- `ProjectBreakdown1.json` — epics -> stories -> tasks (+ cost)
- `Complexity.json` — estimation weights + hourly rate
- `Proposal.json` — proposal narrative + milestones + risks + budget totals

These artifacts are designed to be:
- inspectable
- editable
- exportable
- rerunnable

---

## Model integration
The seed uses OpenAI via `OpenAIModels/` and expects an API key in `.env`.

- `OpenAIModels/textgen.py` and `OpenAIModels/OpenAIClient.py` implement:
  - `generate_text(...)` (string output)
  - `generate_text_json(...)` (JSON-structured output)
  - optional vision + TTS/STT utilities

**Default model:** `gpt-4o` (can be changed in `OpenAIModels/textgen.py`).

**Important:** this repo is built to be *engine-agnostic* at the concept level.
To swap providers later:
- keep the artifact schemas stable
- re-implement `generate_text` / `generate_text_json` with a different backend
- preserve the JSON contracts per stage

---

## Concurrency & rate limiting
Several stages use Python threads to parallelize generation.

- `2Stories2Tasks.py` uses a `Semaphore` to rate-limit requests.
- `3ComplexityAnalysis.py` uses a worker-queue pattern.

**Note:** this is a seed-level approach; production orchestration would use durable queues, backpressure, retries, and structured tracing.

---

## Local UIs
This repo includes optional local-first interfaces:
- Tkinter: stakeholder/epic editing, voice onboarding UI (prototype)
- Flask: complexity editor, proposal preview, review/approval UI

These are intended as:
- inspection tools
- human review gates
- local operator interfaces

They are **not** hardened for public internet exposure.

---

## Glossary
- **Intent**: raw human input (text, docs, notes)
- **Pass**: one pipeline stage that transforms artifacts
- **IR (Intermediate Representation)**: JSON artifacts representing structured truth
- **Artifacts**: persisted outputs under `storage/`
- **Gate**: a validation step (human or automated) before advancing
- **Determinism (here)**: constrained, schema-bound generation + replayable artifacts (not cryptographic determinism)

---

## One-line summary for engineers
> This repo is a deterministic, artifact-driven reasoning pipeline that makes LLM cognition explicit, reviewable, and executable instead of hidden in chat.

---

Build Your Tech • Your Way.
