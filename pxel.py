#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
import platform

VERSION = "0.1"

# ---------------- UTIL ---------------- #

def run(cmd):
    try:
        return subprocess.run(
            cmd, shell=True, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
    except subprocess.CalledProcessError as e:
        return e

def exists(cmd):
    return shutil.which(cmd) is not None

def is_termux():
    return "com.termux" in os.environ.get("PREFIX", "")

def banner():
    print(f"pxel v{VERSION} — smart installer\n")

# ---------------- ENV DETECTION ---------------- #

def detect_env():
    env = {
        "os": platform.system().lower(),
        "arch": platform.machine(),
        "termux": is_termux(),
        "pip": exists("pip"),
        "pip3": exists("pip3"),
        "npm": exists("npm"),
        "pkg": exists("pkg"),
        "apt": exists("apt"),
        "pipx": exists("pipx"),
    }
    return env

# ---------------- INSTALL LOGIC ---------------- #

PYTHON_PACKAGES = {
    "numpy", "scipy", "pandas", "requests", "flask", "fastapi",
    "torch", "transformers", "tensorflow"
}

JS_HINTS = {"react", "express", "vue", "next", "svelte"}

def install_python(pkg, env):
    pip = "pip3" if env["pip3"] else "pip"
    attempts = [
        f"{pip} install {pkg}",
        f"{pip} install {pkg} --no-build-isolation",
    ]

    if env["termux"] and env["pkg"]:
        attempts.append(f"pkg install python-{pkg}")

    for cmd in attempts:
        print(f"→ Trying: {cmd}")
        r = run(cmd)
        if not isinstance(r, Exception):
            print("✔ Installed successfully\n")
            return True
        else:
            print("✖ Failed")

    explain_python_failure(pkg, env)
    return False

def install_js(pkg):
    print(f"→ Trying: npm install {pkg}")
    r = run(f"npm install {pkg}")
    if not isinstance(r, Exception):
        print("✔ Installed successfully\n")
        return True

    print("✖ npm failed")
    explain_js_failure(pkg)
    return False

# ---------------- EXPLANATIONS ---------------- #

def explain_python_failure(pkg, env):
    print("\n❌ Installation failed\n")
    if pkg == "torch" and env["termux"]:
        print("Why:")
        print("- PyTorch does NOT support Android / Termux\n")
        print("What you can do:")
        print("- Use llama.cpp + GGUF models")
        print("- Use cloud APIs (OpenAI, Gemini)")
        print("- Use a PC / VPS / Colab\n")
        print("This is NOT your fault.")
    else:
        print("Possible reasons:")
        print("- Unsupported architecture")
        print("- Missing build tools")
        print("- Python version mismatch")
        print("- Package not available for this OS\n")

def explain_js_failure(pkg):
    print("\nPossible reasons:")
    print("- npm not initialized (try `npm init`)")
    print("- Package name incorrect")
    print("- Network or registry issue\n")

# ---------------- COMMANDS ---------------- #

def cmd_install(pkg):
    env = detect_env()
    print("Detected environment:")
    for k, v in env.items():
        print(f"- {k}: {v}")
    print()

    if pkg in PYTHON_PACKAGES:
        install_python(pkg, env)
        return

    if pkg in JS_HINTS or env["npm"]:
        install_js(pkg)
        return

    print("❓ Unknown package type")
    print("pxel tried to guess, but couldn’t decide safely.")
    print("Try installing manually.")

# ---------------- MAIN ---------------- #

def main():
    banner()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python pxel.py install <package>")
        return

    cmd = sys.argv[1]

    if cmd == "install" and len(sys.argv) == 3:
        cmd_install(sys.argv[2])
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
