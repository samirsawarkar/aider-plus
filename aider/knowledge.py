import os
from pathlib import Path

GLOBAL_KNOWLEDGE_DIR = "~/.aider-plus/global/"
PROJECT_KNOWLEDGE_DIR = ".ai-os/"

GLOBAL_WHITELIST = [
    "servers.md",
    "domains.md",
    "deployment.md",
    "docker.md",
    "security.md",
    "models.md",
]

PRIORITY_1 = [
    "PROJECT.md",
    "CONTEXT.md",
    "MEMORY.md",
    "STATE.md",
    "ARCHITECTURE.md",
    "RULES.md",
    "EXECUTION_RULES.md",
]

PRIORITY_2 = [
    "PROJECT_PLAN.md",
    "WORKFLOWS.md",
    "DECISIONS.md",
    "AGENTS.md",
    "COMMANDS.md",
    "DEPLOYMENT.md",
    "DATABASE.md",
]

MAX_CHARS = 50000


class KnowledgeData:
    def __init__(self):
        self.content = ""
        self.files_loaded = []


def _load_knowledge(directory, whitelist):
    data = KnowledgeData()
    directory_path = Path(directory).expanduser().resolve()

    if not directory_path.is_dir():
        return data

    for filename in whitelist:
        file_path = directory_path / filename
        if file_path.is_file():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
                
                if file_content.strip():
                    data.files_loaded.append(filename)
                    # Add section header
                    data.content += f"\n--- {filename} ---\n{file_content}\n"
            except Exception:
                pass # Silently ignore read errors

    # Check limits
    if len(data.content) > MAX_CHARS:
        data.content = data.content[:MAX_CHARS] + "\n\n[Knowledge truncated]"

    return data


def load_global():
    return _load_knowledge(GLOBAL_KNOWLEDGE_DIR, GLOBAL_WHITELIST)


def load_project(root_path):
    if not root_path:
        return KnowledgeData()
    
    data = KnowledgeData()
    root_dir = Path(root_path).resolve()
    ai_os_dir = root_dir / PROJECT_KNOWLEDGE_DIR

    def _try_load_file(filename):
        # Prefer .ai-os/ over root
        for base_dir in [ai_os_dir, root_dir]:
            file_path = base_dir / filename
            if file_path.is_file():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                    if file_content.strip():
                        return file_content
                except Exception:
                    pass
        return None

    for priority_list in [PRIORITY_1, PRIORITY_2]:
        for filename in priority_list:
            if len(data.content) >= MAX_CHARS:
                break
            
            content = _try_load_file(filename)
            if content:
                data.files_loaded.append(filename)
                data.content += f"\n--- {filename} ---\n{content}\n"
                
                if len(data.content) > MAX_CHARS:
                    data.content = data.content[:MAX_CHARS] + "\n\n[Knowledge truncated]"
                    return data

    return data
