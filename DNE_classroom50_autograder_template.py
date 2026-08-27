#!/usr/bin/env python3
"""
Classroom 50 autograder entry point.

INSTRUCTOR ONLY. This file and _due_dates.csv beside it are installed in the solution
repository with a leading underscore, marking them as files to delete before handing the
repository to students. They carry no DO-NOT-EDIT banner because no student ever
receives them: they live in your private classroom50 config repository.

Install by copying this file into that repository as

    <classroom>/autograders/<assignment>/autograder.py

renaming it to autograder.py, which is the name the runner looks for, and putting
_due_dates.csv beside it. Everything under that directory is bundled and published to
Pages, and the runner unpacks it before grading. Because this file only bootstraps, it
never needs reinstalling when the grading logic changes: the real work lives in the
solution repository's auto_grader submodule.

The runner executes this from inside the student's checkout, so the working directory is
the repository root. No secrets are used or needed.
"""

import os
import pathlib
import runpy
import subprocess
import sys

bundle = pathlib.Path(__file__).resolve().parent
checkout = pathlib.Path.cwd()

# The runner executes this file from the unpacked bundle, so sys.path[0] is the bundle
# directory, not the repository. Without this the grading scripts run but cannot import
# their own neighbours: "No module named 'DNE_assignment_info'".
sys.path.insert(0, str(checkout))

# Point the grader at the due dates bundled beside this file. Keeping them here rather
# than in the student repository means a due date can be changed with a single push to
# the config repo, with no student repository to sync.
due_dates = bundle / "_due_dates.csv"
if due_dates.is_file():
    os.environ["AUTOGRADER_DUE_DATES"] = str(due_dates)
    print(f"autograder: using due dates from {due_dates}")
else:
    print("autograder: no _due_dates.csv in the bundle; no late penalties will be projected")

# The grader imports from the auto_grader submodule, which actions/checkout does not
# fetch by default.
subprocess.run(["git", "submodule", "update", "--init", "--recursive"], check=False)

# Install the assignment's dependencies. Not quiet on purpose: when a grading run fails,
# the install log is the first thing worth reading.
subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=False)
install = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                         check=False)
if install.returncode != 0:
    print("::warning::pip install failed; grading will probably fail to import its dependencies")

# Grade. This writes ./result.json and ./release-body.md for the runner to publish.
entry_point = checkout / "DNE_github_grade_on_push.py"
if not entry_point.is_file():
    sys.exit(f"autograder: {entry_point} not found. The working directory is {checkout}, "
             f"which does not look like the student's checkout.")
runpy.run_path(str(entry_point), run_name="__main__")
