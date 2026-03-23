import os
import re

server_path = r"c:\Users\sai pragnya\Downloads\AuthentiCheck\server.py"
with open(server_path, 'r', encoding='utf-8') as f:
    server_content = f.read()

# Update final_score logic in server.py
server_content = re.sub(
    r'if final_score >= 80:\s*final_status = \'Authentic\'',
    r'if final_score >= 70:\n            final_status = \'Original\'',
    server_content
)
server_content = re.sub(
    r'color = \'#10b981\' if doc\[\'final_score\'\] >= 80 else',
    r'color = \'#10b981\' if doc[\'final_score\'] >= 70 else',
    server_content
)
server_content = re.sub(
    r'\'Pass\' if score >= 80 else \(\'Suspicious\' if score >= 50 else \'Fail\'\)',
    r'\'Pass\' if score >= 70 else (\'Suspicious\' if score >= 50 else \'Fail\')',
    server_content
)

with open(server_path, 'w', encoding='utf-8') as f:
    f.write(server_content)


report_path = r"c:\Users\sai pragnya\Downloads\AuthentiCheck\templates\report.html"
with open(report_path, 'r', encoding='utf-8') as f:
    report_content = f.read()

report_content = report_content.replace('>= 80', '>= 70')

# Fix the hardcoded ORIGINAL block
bad_block = '''              <span class="classification-badge classification-original">
                <i class="fas fa-check-circle"></i> ORIGINAL
              </span>'''
good_block = '''              <span class="classification-badge {% if report.final_score >= 70 %}classification-original{% else %}classification-suspicious{% endif %}">
                <i class="fas fa-check-circle"></i> {{ report.final_status|upper }}
              </span>'''
report_content = report_content.replace(bad_block, good_block)

with open(report_path, 'w', encoding='utf-8') as f:
    f.write(report_content)


preview_path = r"c:\Users\sai pragnya\Downloads\AuthentiCheck\templates\preview.html"
with open(preview_path, 'r', encoding='utf-8') as f:
    preview_content = f.read()

preview_content = preview_content.replace('>= 80', '>= 70')

with open(preview_path, 'w', encoding='utf-8') as f:
    f.write(preview_content)


history_path = r"c:\Users\sai pragnya\Downloads\AuthentiCheck\templates\history.html"
with open(history_path, 'r', encoding='utf-8') as f:
    history_content = f.read()

history_content = history_content.replace('>= 80', '>= 70')

with open(history_path, 'w', encoding='utf-8') as f:
    f.write(history_content)

print("Updated thresholds in all files.")
