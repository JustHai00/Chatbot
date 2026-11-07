from pathlib import Path

# ─── Read Any File ───
def read_file_content(file_path):
    """Read text from different file types"""
    try:
        ext = file_path.suffix.lower()
        
        if ext in ['.txt', '.md', '.py', '.json', '.csv', '.js', '.html', '.css']:
            return file_path.read_text(encoding='utf-8', errors='ignore')
        
        elif ext == '.pdf':
            try:
                import PyPDF2
                text = ""
                reader = PyPDF2.PdfReader(file_path)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
            except:
                return "[PDF — install PyPDF2 to read content]"
        
        elif ext == '.docx':
            try:
                from docx import Document
                doc = Document(file_path)
                return "\n".join([p.text for p in doc.paragraphs])
            except:
                return "[DOCX — install python-docx to read content]"
        
        elif ext in ['.xlsx', '.xls']:
            try:
                import pandas as pd
                df = pd.read_excel(file_path)
                return df.to_string()
            except:
                return "[Excel — install pandas & openpyxl to read content]"
        
        else:
            return f"[File type: {ext} — listed only]"
    
    except Exception as e:
        return f"[Could not read: {str(e)}]"

# ─── Get All Files ───
def get_all_files(folder_path, include_subfolders=True):
    """Get list of every file in folder"""
    path = Path(folder_path)
    pattern = "**/*" if include_subfolders else "*"
    
    all_files = []
    for f in path.glob(pattern):
        if f.is_file():
            all_files.append(str(f))
    
    return all_files

# ─── Search & Answer ───
def search_and_answer(folder_path, question):
    """Find relevant files and build answer"""
    path = Path(folder_path)
    
    if not path.exists():
        return f"❌ Folder not found: {folder_path}"
    
    # Get all files
    all_files = get_all_files(folder_path)
    if not all_files:
        return "📂 No files found in this folder."
    
    # Prepare search
    question_lower = question.lower()
    keywords = [k.strip() for k in question_lower.split() if len(k.strip()) > 2]
    
    # Search through files
    matches = []
    preview_length = 300
    
    for file_str in all_files:
        fpath = Path(file_str)
        content = read_file_content(fpath)
        content_lower = content.lower()
        
        # Check if any keyword matches
        found = False
        for kw in keywords:
            if kw in content_lower:
                found = True
                break
        
        if found or any(kw in content_lower for kw in keywords):
            # Find where match happens
            idx = content_lower.find(keywords[0]) if keywords else 0
            start = max(0, idx - 50)
            end = min(len(content), idx + preview_length)
            
            matches.append({
                "path": file_str,
                "name": fpath.name,
                "preview": content[start:end].strip()
            })
    
    # Build response
    if not matches:
        return f"🔍 Searched {len(all_files)} files — no matching content found.\n\nTry different keywords or check the folder path."
    
    response = f"✅ Found **{len(matches)}** matching file(s) from {len(all_files)} total scanned:\n\n"
    
    for idx, m in enumerate(matches, 1):
        response += f"**{idx}. {m['name']}**\n"
        response += f"📍 Path: {m['path']}\n"
        response += f"📝 Preview:\n{m['preview']}\n\n"
    
    return response
