# Run this to test if everything is installed and working.
import importlib

print("=" * 40)
print("SHADOW setup check")
print("=" * 40)

for mod, pip in [("streamlit", "streamlit"), ("customtkinter", "customtkinter"),
                 ("requests", "requests"), ("PyPDF2", "PyPDF2"), ("docx", "python-docx")]:
    try:
        importlib.import_module(mod)
        print(f"✅ {mod}")
    except ImportError:
        print(f"❌ {mod} missing  ->  pip install {pip}")

try:
    from shadow_core import ollama_online, get_installed_models, AI_TEAM, resolve_model, call_ai
    if ollama_online():
        print("✅ Ollama is online")
        print("   Installed models:", ", ".join(get_installed_models(True)) or "NONE (run: ollama pull qwen3.5:9b)")
        for k, ai in AI_TEAM.items():
            print(f"   {ai['name']} will use -> {resolve_model(ai['want'])}")
        print("\nTest question: say hello in 5 words")
        print("Reply:", call_ai("general", [{"role": "user", "content": "Say hello in 5 words"}]))
    else:
        print("❌ Ollama is OFFLINE  ->  open Ollama or run: ollama serve")
except Exception as e:
    print("❌ Core error:", e)

print("=" * 40)
input("Press Enter to close...")
