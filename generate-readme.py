#!/usr/bin/env python3
"""Generate multi-language README for GitHub repository"""

import json
from pathlib import Path

def generate_skill_table(skills_index):
    """Generate markdown table for skills"""
    table_rows = []
    for skill_id, data in list(skills_index.items())[:30]:
        info = data.get('en', {})
        title = info.get('title', skill_id)
        desc = info.get('description', 'No description')[:50]
        table_rows.append(f"| {skill_id} | {desc}... |")
    return "\n".join(table_rows)

def main():
    # Load skills index
    index_file = Path.home() / '.openclaw/workspace/skills-publisher/translations/skills-index.json'
    
    if index_file.exists():
        with open(index_file, 'r', encoding='utf-8') as f:
            skills = json.load(f)
    else:
        skills = {}
    
    readme_content = f"""# 🎓 OpenClaw Skills Library

A curated collection of **{len(skills)}** agent skills.

## 🌍 Multi-Language | 多语言 | बहुभाषी | Multilingüe | Multilingue | متعدد اللغات | বহুভাষিক | Многоязычный | Multilíngue | 多言語 | کثیر اللسانیت

## 📚 Available Skills | 可用技能 ({len(skills)} total)

| Skill ID | English Description |
|----------|---------------------|
{generate_skill_table(skills)}

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git

# Install a skill
cp -r skills/[skill-name] ~/.openclaw/workspace/skills/
```

## 🌐 Languages

| Language | Code | Status |
|----------|------|--------|
| English | en | ✅ |
| 简体中文 | zh-CN | ✅ |
| 繁體中文 | zh-TW | ✅ |
| हिंदी | hi | ✅ |
| Español | es | ✅ |
| Français | fr | ✅ |
| العربية | ar | ✅ |
| বাংলা | bn | ✅ |
| Русский | ru | ✅ |
| Português | pt | ✅ |
| 日本語 | ja | ✅ |
| اردو | ur | ✅ |

## ⏰ Auto-Sync

Skills are synchronized daily at **06:00 AM UTC** from OpenClaw workspace.

Last updated: Generated automatically
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"Generated README.md with {len(skills)} skills")

if __name__ == '__main__':
    main()
