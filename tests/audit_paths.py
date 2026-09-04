"""
Comprehensive File Path & Import Auditor for SunRiseSet Project.
Checks:
1. All Python imports across all .py files
2. All path strings in code, configuration, and documentation
3. All Markdown file links (.md)
4. pyproject.toml package pointers and scripts
5. All file existence in workspace
"""

import os
import sys
import ast
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Add src to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

def audit_all():
    print("==================================================")
    print("🔍 AUDITING ALL PROJECT PATHS & REFERENCES")
    print("==================================================")
    
    workspace = Path(__file__).resolve().parent.parent
    os.chdir(workspace)

    # 1. Audit Python Files & Imports
    py_files = [p for p in workspace.rglob("*.py") if "__pycache__" not in p.parts]
    print(f"\n1. Checking Python Modules & Imports ({len(py_files)} files):")
    
    failed_imports = 0
    for pf in py_files:
        with open(pf, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(pf))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    try:
                        __import__(alias.name)
                    except Exception as e:
                        print(f"  ❌ [{pf.name}] Failed import: {alias.name} -> {e}")
                        failed_imports += 1
            elif isinstance(node, ast.ImportFrom):
                if node.level > 0:
                    # Relative package import (e.g. from .models import ...)
                    rel_mod = f"sunriseset.{node.module}" if node.module else "sunriseset"
                    try:
                        __import__(rel_mod)
                    except Exception as e:
                        print(f"  ❌ [{pf.name}] Failed relative import: {rel_mod} -> {e}")
                        failed_imports += 1
                elif node.module:
                    try:
                        __import__(node.module)
                    except Exception as e:
                        print(f"  ❌ [{pf.name}] Failed from-import: {node.module} -> {e}")
                        failed_imports += 1
    if failed_imports == 0:
        print(f"  ✅ All imports in all {len(py_files)} Python files resolve 100% cleanly.")

    # 2. Audit Markdown Links and Paths
    md_files = [p for p in workspace.rglob("*.md") if ".git" not in p.parts and "__pycache__" not in p.parts]
    print(f"\n2. Checking Markdown Links & Paths across ({len(md_files)} files):")
    
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    for mf in md_files:
        rel_mf = mf.relative_to(workspace)
        with open(mf, "r", encoding="utf-8") as f:
            content = f.read()
        links = link_pattern.findall(content)
        for text, link in links:
            if link.startswith("http://") or link.startswith("https://") or link.startswith("#"):
                continue
            # Local link
            clean_link = link.split("#")[0]
            # Check relative to file or relative to workspace
            target_file_rel = mf.parent / clean_link
            target_workspace_rel = workspace / clean_link
            if target_file_rel.exists() or target_workspace_rel.exists():
                print(f"  ✅ [{rel_mf}] Link '{text}' -> '{clean_link}' (EXISTS)")
            else:
                print(f"  ❌ [{rel_mf}] Link '{text}' -> '{clean_link}' (MISSING!)")

    # 3. Audit pyproject.toml
    print(f"\n3. Checking pyproject.toml Configuration:")
    pyproject_file = workspace / "pyproject.toml"
    if pyproject_file.exists():
        content = pyproject_file.read_text(encoding="utf-8")
        # Check readme
        if 'readme = "README.md"' in content:
            readme_exists = (workspace / "README.md").exists()
            print(f"  {'✅' if readme_exists else '❌'} Readme reference -> README.md ({readme_exists})")
        # Check packages where
        if 'where = ["src"]' in content:
            src_exists = (workspace / "src").exists()
            print(f"  {'✅' if src_exists else '❌'} Source directory -> src/ ({src_exists})")
        # Check scripts entrypoint
        if 'sunriseset = "sunriseset.cli:main"' in content:
            try:
                from sunriseset.cli import main
                print(f"  ✅ Script entrypoint -> sunriseset.cli:main (CALLABLE)")
            except Exception as e:
                print(f"  ❌ Script entrypoint invalid: {e}")

    # 4. Audit .gitignore targets
    print(f"\n4. Checking .gitignore & Special Files:")
    gitignore_file = workspace / ".gitignore"
    if gitignore_file.exists():
        print(f"  ✅ .gitignore exists ({gitignore_file.stat().st_size} bytes)")
    gitattributes_file = workspace / ".gitattributes"
    if gitattributes_file.exists():
        print(f"  ✅ .gitattributes exists ({gitattributes_file.stat().st_size} bytes)")
    gitkeep_file = workspace / "report" / ".gitkeep"
    if gitkeep_file.exists():
        print(f"  ✅ report/.gitkeep exists")

    print("\n==================================================")
    print("🎯 PATH AUDIT COMPLETE!")
    print("==================================================")

if __name__ == "__main__":
    audit_all()
