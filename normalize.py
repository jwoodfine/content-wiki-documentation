import os
import re

root_dir = '/srv/foundry/clones/project-language/content-wiki-documentation'

def normalize_wikilink(match):
    name = match.group(1)
    display = match.group(2) if match.group(2) else ""
    return f'[[{name}{display}]]'

# Regexes
paired_re = re.compile(r'^paired_with:\s*topic-([^\s\n]+)', re.MULTILINE)
wikilink_re = re.compile(r'\[\[topic-([^|\]\n]+)(\|[^\]\n]+)?\]\]')
path_re = re.compile(r'path:\s*([^ \n]*?)topic-([^\s\n]+)')

# 1. First, update all contents (except slug which we'll do after rename)
all_files = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.md') or filename.endswith('.yaml'):
            all_files.append(os.path.join(dirpath, filename))

for file_path in all_files:
    with open(file_path, 'r') as f:
        content = f.read()
    
    new_content = content
    new_content = paired_re.sub(r'paired_with: \1', new_content)
    new_content = wikilink_re.sub(normalize_wikilink, new_content)
    new_content = path_re.sub(r'path: \1\2', new_content)
    
    if new_content != content:
        with open(file_path, 'w') as f:
            f.write(new_content)

# 2. Rename files starting with topic-
renamed_files = []
for file_path in all_files:
    dirpath, filename = os.path.split(file_path)
    if filename.startswith('topic-'):
        new_filename = filename[len('topic-'):]
        new_file_path = os.path.join(dirpath, new_filename)
        if not os.path.exists(new_file_path):
            os.rename(file_path, new_file_path)
            renamed_files.append(new_file_path)
        else:
            print(f"Warning: {new_file_path} already exists. Skipping rename.")
            renamed_files.append(file_path) # still process it for slug
    else:
        if file_path.endswith('.md'):
            renamed_files.append(file_path)

# 3. Update slugs in all .md files to match their filename stems
slug_re = re.compile(r'^slug:\s*([^\s\n]+)', re.MULTILINE)

for file_path in renamed_files:
    if not file_path.endswith('.md'):
        continue
        
    dirpath, filename = os.path.split(file_path)
    stem = filename[:-3] # remove .md
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # We only want to update the slug if it starts with topic- or if it's a renamed file
    # Actually, the instruction says "update the slug: field ... to match the new filename stem"
    # for EVERY renamed file.
    
    def slug_fix(m):
        current_slug = m.group(1)
        if current_slug.startswith('topic-') or current_slug != stem:
            return f'slug: {stem}'
        return f'slug: {current_slug}'

    new_content = slug_re.sub(slug_fix, content)
    
    if new_content != content:
        with open(file_path, 'w') as f:
            f.write(new_content)

print("Batch normalization complete.")
