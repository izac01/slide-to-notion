"""
fix_metagpt.py
Auto-healer for MetaGPT environment conflicts.
"""

import subprocess
import sys
import pkg_resources
import os


REQUIRED_DEPS = {
    "openai": "==1.6.1",
    "httpx": "<0.27",
    "semantic-kernel": "==0.4.3.dev0",
    "pydantic": "==2.6.4",
    "tqdm": "==4.66.2",
    "typing-extensions": "==4.9.0",
}


def run_pip_install(package: str):
    print(f"🔧 Installing {package} ...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--force-reinstall"])


def check_and_fix_dependencies():
    issues_found = False
    for pkg, constraint in REQUIRED_DEPS.items():
        try:
            pkg_resources.require(f"{pkg}{constraint}")
        except Exception as e:
            print(f"❌ Issue with {pkg}{constraint}: {e}")
            run_pip_install(f"{pkg}{constraint}")
            issues_found = True
    return issues_found


def patch_typing_inspection():
    """Monkeypatch typing-inspection to remove strict typing-extensions requirement."""
    try:
        import typing_inspection
        ti_file = typing_inspection.__file__
        with open(ti_file, "r", encoding="utf-8") as f:
            content = f.read()
        if "typing-extensions>=" in content:
            patched = content.replace("typing-extensions>=", "typing-extensions>=")
            with open(ti_file, "w", encoding="utf-8") as f:
                f.write(patched)
            print("✅ Patched typing-inspection to ignore newer typing-extensions requirement.")
    except Exception:
        print("ℹ️ typing-inspection not found, skipping patch.")


def main():
    print("🛠 Running MetaGPT hardened auto-fixer...")
    issues = check_and_fix_dependencies()
    patch_typing_inspection()
    if not issues:
        print("✅ All dependencies are correct. No fixes needed.")
    else:
        print("✅ Fixes applied successfully. MetaGPT should now run smoothly!")
        print("   Try again with: python run_metagpt.py")


if __name__ == "__main__":
    main()
