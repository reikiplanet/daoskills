#!/usr/bin/env python3
"""
Skills Translation Generator
Generates multi-language descriptions for each skill
"""

import os
import json
import sys
from pathlib import Path

# Language configurations
LANGUAGES = {
    'en': 'English',
    'zh-CN': 'Chinese (Simplified)',
    'zh-TW': 'Chinese (Traditional)', 
    'hi': 'Hindi',
    'es': 'Spanish',
    'fr': 'French',
    'ar': 'Arabic',
    'bn': 'Bengali',
    'ru': 'Russian',
    'pt': 'Portuguese',
    'ja': 'Japanese',
    'ur': 'Urdu'
}

def extract_skill_info(skill_path):
    """Extract skill name, description, and purpose from SKILL.md"""
    with open(skill_path / 'SKILL.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title (first # heading)
    title = ''
    for line in content.split('\n'):
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    # Extract first paragraph as description
    description = ''
    lines = content.split('\n')
    in_code = False
    for line in lines:
        if line.strip().startswith('```'):
            in_code = not in_code
            continue
        if not in_code and line.strip() and not line.startswith('#'):
            description = line.strip()
            break
    
    return {
        'name': skill_path.name,
        'title': title or skill_path.name,
        'description': description,
        'content': content[:2000]  # First 2000 chars for context
    }

def main():
    skills_dir = Path.home() / '.openclaw/workspace/skills'
    output_file = Path.home() / '.openclaw/workspace/skills-publisher/translations/skills-index.json'
    
    skills_index = {}
    
    print(f"Scanning {skills_dir}...")
    
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir() and (skill_dir / 'SKILL.md').exists():
            try:
                info = extract_skill_info(skill_dir)
                skills_index[info['name']] = {
                    'languages': {lang: {'name': name} for lang, name in LANGUAGES.items()},
                    'en': {
                        'title': info['title'],
                        'description': info['description'],
                        'full_content': info['content']
                    }
                }
                print(f"  ✓ Indexed: {info['name']}")
            except Exception as e:
                print(f"  ✗ Error with {skill_dir.name}: {e}")
    
    # Save index
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(skills_index, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Indexed {len(skills_index)} skills to {output_file}")

if __name__ == '__main__':
    main()
