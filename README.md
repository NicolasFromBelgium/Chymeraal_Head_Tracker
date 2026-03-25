# TDD Python Project Template (by Nicolas Leyssens)

**A professional template to start any Python project using Test Driven Development (TDD)**

This template contains everything you need to practice **real TDD** from the very first commit:

- Modern `src/` project structure

- pre-commit (black + ruff)

- Complete GitHub Actions CI (lint + type checking + tests on Python 3.11/3.12)

- 2 demo tests to force you to follow the Red → Green → Refactor cycle

## How to Use This Template

1. Click **"Use this template"** → "Create a new repository" on GitHub

2. Clone your new repository

3. `python -m venv venv && source venv/bin/activate` (if Windows : venv\Scripts\activate)

4. `pip install -r requirements-dev.txt`

5. `pre-commit install`

6. `git add . && git commit -m "chore: initial TDD template setup"`

7. **Run the tests**: `pytest` 

8. Test 1 should pass if installation went fine

9. Test 2 should fail, it's NORMAL (it tests if there is a file in src/tdd_template/)

10. Do not change anything. Commit and push the template to your github repo

11. Go to your Github repo, check actions, you will see a workflow on failed (because the test 2 failed!)

12. Now go to directory : src/tdd_template (cd tdd_template)

13. Create a file main.py(nano main.py), write some valid python 

14. commit and push again, the new workflow action should be on PASSED (test 2 is now OK)

15. BINGO, you did your first Test Driven Development workflow

The existing 2 Demo CI tests are here : tests/unit/test_demo.py

## The 2 Demo Tests (Essential for Understanding TDD)

1. **`test_project_has_at_least_one_test`** → **Always passes**  

   (There are already 2 tests in the project, it will confirm that CI is functional.)

2. **`test_project_has_new_files`** → **Intentionally fails at the beginning**  

   Clear message:  

  

   > Remember the TDD rule: **Write the TEST before the code!**"

 > "Create src/tdd_template/main.py (or any new file) to make this test pass

## The TDD Rule

**Red** (write a failing test) → **Green** (write the minimal code to make it pass) → **Refactor**



## Important config files

pyproject.toml : central config (packaging, clack, ruff, mypy)

.pre-commit-config.yaml : will execute black and ruff before any commit

.github/workflows/ci.yml : Pipeline Github Actions (CI TDD core)



## Useful Commands

\`\`\`bash

(when you launch pytest it will scan and launch files with test_ or _test.py)

pytest                  # run all tests

pre-commit run --all-files

pytest --cov=src        # with coverage

pytest # run everything (what you usually execute)

pytest -v # verbose mode (see each test individually)

pytest tests/unit/ # run only unit tests (recommended during development)

pytest --cov=src # run tests with code coverage report

pytest -k "demo" # run only tests that contain "demo" in their name

\`\`\`

Run these commands in the windows command line interface (CLI), copy the output of the last command and paste it in your github ssh key manager
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub

## On Windows
Open Git Bash
cd to working folder (e.g an empty folder TDD_project01 you just created)
git clone repo
cd repo
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
pytest
git add .
git commit -m "message"
git push


This template is open-source (MIT license) 


