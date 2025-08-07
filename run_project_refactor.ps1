# run_project_refactor.ps1
# Wrapper for MetaGPT to refactor slide-to-notion project with master prompt

param(
    [string]$PromptFile = "meta_prompt.txt"
)

# Ensure virtual environment is active
Write-Host "=== Starting MetaGPT Project Refactor ==="

# If meta_prompt.txt doesn't exist, create it
if (-not (Test-Path $PromptFile)) {
    @"
I have a project called "slide-to-notion" and I need a complete refactor and polish to production-grade quality. Please act as an experienced Engineering Director with a proactive mindset.

## Goals

1. **Folder Structure**
   - Ensure the folder structure is clean and optimal.
   - Keep only one canonical implementation folder (e.g. `google_slides_to_notion`).
   - Remove or merge redundant or duplicate work (e.g. old `slides_to_notion`, `code_optimization`, `task_manager`).
   - Delete unnecessary junk (venv, metagpt_env, __pycache__, .idea, duplicate .git, timestamped snapshots).

2. **Code Architecture & Structure**
   - Gather full context from ALL files before making any changes.
   - Review each file to determine if it contributes meaningfully to the goal; if not, remove or merge it.
   - Follow modular, maintainable architecture: each module has a clear single responsibility.
   - Confirm or rebuild final file list:
     - main.py
     - converter.py
     - ui.py
     - file_manager.py
     - environment_manager.py
     - api_handler.py
     - sync.py
     - google_slides_to_notion.py
     - notion_page_wizard.py
     - data_aggregator.py

3. **Primary Functional Goal**
   - Convert Google Slides decks → Notion pages/blocks with highest possible 1:1 visual fidelity.
   - Preserve fonts, alignment, colors, images, lists.
   - QA must validate visually:
     - If deviations from original slides are required, document them and justify.
   - Include at least 2 test conversions, one of which is the example deck:
     https://docs.google.com/presentation/d/1BftmE4rYIMuyDDpFY3DYCMQ2G5Nm_BIY7JkoeYds6bI/edit?usp=sharing

4. **Cost Awareness**
   - Minimize API calls that incur costs (Google Slides API, Notion API).
   - Use caching, batching, and dry-run modes where possible.
   - Always keep the goal of top-quality results in mind when deciding when to call APIs.

5. **Documentation**
   - Provide minimal but clear docs for each file:
     - Purpose of the file
     - Why it matters in achieving the goal
   - Create a polished README.md with step-by-step usage instructions for non-technical users.
   - Include “before and after” visual examples of converting the example deck.
   - Document wizard usage if it works.

6. **Engineering Director Review**
   - Before finalizing, proactively review ALL code for:
     - Bug risks
     - Portability across environments
     - Professional readability & maintainability
   - Suggest improvements based on anticipating problems before they occur.
   - Ensure the final version is portable enough to pass real-world code reviews at work.

7. **Final Deliverables**
   - A cleaned and reorganized project folder tree.
   - Fully working, polished code that runs end-to-end with ONE command.
   - Example tests (with the provided Google Slides deck and one additional).
   - A README.md with setup + usage instructions.
   - QA notes on fidelity and acceptable deviations.
   - Minimal per-file documentation.

Constraints:
- Always gather and understand ALL context before making adjustments.
- Once you have the context, you may change any file as needed to meet the goals.
- Prioritize simplicity, maintainability, and accuracy.
- Ensure portability for professional review.

Please deliver the final refactored project in the cleanest, most production-ready state possible.
"@ | Set-Content $PromptFile -Encoding UTF8
    Write-Host "Created default prompt file at $PromptFile"
}

# Run MetaGPT with the master prompt
Write-Host "=== Running MetaGPT with Master Prompt ==="
python run_metagpt.py (Get-Content $PromptFile -Raw)

Write-Host "=== MetaGPT run complete ==="
