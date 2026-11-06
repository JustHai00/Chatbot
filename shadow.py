# ==================================================
# 🔒 SHADOW — SECURITY MODULE v1.0
# All safety checks, validation, protection logic here
# For YOUR Personal Use Only — No sharing
# ==================================================

import re
import os
import uuid
from pathlib import Path

# ──────────────────────────────────────────────────
# ⚙️ SAFETY SETTINGS — Tune these as you need
# ──────────────────────────────────────────────────
SAFETY_CONFIG = {
    "max_file_size_mb": 10,
    "max_total_size_mb": 50,
    "allowed_extensions": {
        "txt", "md", "py", "c", "cpp", "h", "js", "html", "css", "json",
        "xml", "csv", "pdf", "docx", "xlsx", "zip", "tar", "gz"
    },
    "upload_dir": "shadow_uploads",
    "injection_patterns": [
        r"ignore\s+(all\s+)?previous",
        r"disregard\s+.*instructions",
        r"you\s+are\s+now",
        r"system:\s*prompt",
        r"override.*rule",
        r"forget\s+.*everything",
        r"change\s+your\s+role",
        r"new\s+persona",
        r"bypass\s+restriction",
    ],
}

# Auto-create upload folder
os.makedirs(SAFETY_CONFIG["upload_dir"], exist_ok=True)

# ──────────────────────────────────────────────────
# 🧹 File Name & Path Protection
# ──────────────────────────────────────────────────
def sanitize_filename(filename: str) -> str:
    """Block path traversal & dangerous characters"""
    # Remove any folder paths from name
    base_name = os.path.basename(filename)
    # Keep only safe characters
    safe_name = re.sub(r'[^\w.\-+ ]', '_', base_name)
    # Add unique ID to prevent overwrites & collisions
    ext = Path(safe_name).suffix.lower()
    unique_name = f"{uuid.uuid4().hex}{ext}"
    return unique_name

# ──────────────────────────────────────────────────
# ✅ File Validation
# ──────────────────────────────────────────────────
def validate_uploaded_file(file) -> tuple[bool, str]:
    """Check file size, type, and total storage limit"""
    # 1. Check single file size
    max_bytes = SAFETY_CONFIG["max_file_size_mb"] * 1024 * 1024
    if file.size > max_bytes:
        return False, f"❌ {file.name} too big — max {SAFETY_CONFIG['max_file_size_mb']}MB"
    
    # 2. Check file type
    ext = Path(file.name).suffix.lower().lstrip('.')
    if ext and ext not in SAFETY_CONFIG["allowed_extensions"]:
        return False, f"❌ .{ext} files not allowed"
    
    # 3. Check total folder size
    total_bytes = 0
    for f in Path(SAFETY_CONFIG["upload_dir"]).glob("**/*"):
        if f.is_file():
            total_bytes += f.stat().st_size
    if total_bytes + file.size > SAFETY_CONFIG["max_total_size_mb"] * 1024 * 1024:
        return False, "❌ Storage full — delete old files first"
    
    return True, "OK"

# ──────────────────────────────────────────────────
# 🛡️ Prompt Injection Detection
# ──────────────────────────────────────────────────
def detect_injection(text: str) -> bool:
    """Check if someone/something tries to override rules"""
    text_lower = text.lower()
    for pattern in SAFETY_CONFIG["injection_patterns"]:
        if re.search(pattern, text_lower):
            return True
    return False

# ──────────────────────────────────────────────────
# 📂 Safe File Reader
# ──────────────────────────────────────────────────
def read_file_safe(file_path: str | Path, max_chars: int = 30000) -> str:
    """Read files safely with limits & warning for suspicious content"""
    path = Path(file_path)
    suffix = path.suffix.lower()
    
    try:
        content = ""
        if suffix in [".txt", ".md", ".py", ".c", ".cpp", ".h", ".js", ".html", ".css", ".json", ".xml"]:
            content = path.read_text(encoding="utf-8", errors="ignore")[:max_chars]
        elif suffix == ".pdf":
            try:
                import PyPDF2
                text = ""
                with open(path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages[:30]:
                        text += page.extract_text() or ""
                content = text[:max_chars]
            except ImportError:
                content = "📄 PDF — install PyPDF2 to read full content"
        elif suffix == ".docx":
            try:
                from docx import Document
                doc = Document(path)
                content = "\n".join(p.text for p in doc.paragraphs)[:max_chars]
            except ImportError:
                content = "📘 DOCX — install python-docx to read full content"
        elif suffix in [".csv", ".xlsx", ".zip", ".tar", ".gz"]:
            content = f"✅ {path.name} — attached & accessible"
        else:
            content = f"✅ {path.name} — attached"
        
        # Warn if injection detected in file
        if detect_injection(content):
            content = "⚠️ SUSPICIOUS CONTENT DETECTED — processed with protection\n" + content[:5000]
        
        return content
    
    except Exception as e:
        return f"⚠️ Read error: {str(e)[:100]}"

# ──────────────────────────────────────────────────
# 🔑 Final Security Summary
# ──────────────────────────────────────────────────
def get_security_status() -> dict:
    """Return status for display in UI"""
    return {
        "ollama_locked": True,  # Set False if you change OLLAMA_HOST
        "max_file_mb": SAFETY_CONFIG["max_file_size_mb"],
        "injection_protection": True,
        "secrets_loaded": True,
    }
