import os
import re

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # specifically fix index.html strings in js location assignments or direct strings
    content = content.replace("'index.html'", "'/'")
    content = content.replace('"index.html"', '"/"')
    # fix hrefs
    content = content.replace('href="index.html"', 'href="/"')
    
    # fix other .html files in hrefs
    content = re.sub(r'href="([a-zA-Z0-9_-]+)\.html"', r'href="/\1"', content)
    content = re.sub(r"href='([a-zA-Z0-9_-]+)\.html'", r"href='/\1'", content)
    
    # fix window.location / JS redirects
    content = re.sub(r"window\.location\.href\s*=\s*['\"]([a-zA-Z0-9_-]+)\.html['\"]", r"window.location.href = '/\1'", content)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

base = r"c:\Users\sai pragnya\Downloads\AuthentiCheck"
tpl = os.path.join(base, "templates")
js_file = os.path.join(base, "js", "script.js")

for fn in os.listdir(tpl):
    if fn.endswith(".html"):
        fix_file(os.path.join(tpl, fn))

if os.path.exists(js_file):
    fix_file(js_file)

print("Links fixed.")
