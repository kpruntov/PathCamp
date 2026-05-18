# PathCamp

A metadata-driven Campaign Simulation Engine for Game Masters.

## About This Project

**PathCamp** is intentionally incomplete. It serves as a real-world, open-source showcase for [**SpecLoom**](https://github.com/kpruntov/SpecLoom) — an AI-augmented, Model-Based Systems Engineering (MBSE) and HADD (Human-Augmented Design & Development) framework. 

This repository demonstrates how a project's architecture, requirements, and execution tasks are driven entirely by the `.spec` directory using the SpecLoom engine.

### Why is it incomplete?
We left this project unfinished on purpose! It provides a perfect playground for you to clone the repository, install SpecLoom, and try the `loom next` workflow yourself. You can pick up where we left off, implement new features, or fix remaining integration tasks by following the SpecLoom V-Model.
Maybe I will finish it occasionally, because I'd like to have a campain manager for myself :D

## Features (Implemented & Planned)
- **Campaign Management:** Create, list, share, and delete campaigns.
- **Timeline Engine:** Advance campaigns through "Ticks" that cascade state forward.
- **Encounter Generation:** Generate encounters based on narrative and mechanical data.

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kpruntov/PathCamp.git
   cd PathCamp
   ```
2. **Explore the SpecLoom Data:**
   Check out the `.spec/` directory to see the raw MBSE JSON artifacts that define this entire system (Requirements, Logical Components, API Contracts).

3. **Install and run SpecLoom:**
   Visit [SpecLoom](https://github.com/kpruntov/SpecLoom) for installation and usage instructions.

## Tech Stack
- **Backend:** Python, FastAPI, SQLAlchemy, PostgreSQL
- **Frontend:** TypeScript, React, Vite, TailwindCSS
- **Orchestration:** Podman / Docker (Distroless containers)

## IP & Licensing Note
This project is an independent showcase themed around generic fantasy tabletop RPGs. To ensure maximum compatibility and respect for IP, this showcase relies strictly on generic mechanics and systems covered by open licenses (such as the Open RPG Creative License (ORC) or the Open Gaming License (OGL)) and does not utilize any specific publisher's Product Identity, lore, or trademarks.

## License
[MIT License](LICENSE)