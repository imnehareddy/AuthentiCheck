import re
import os

filepath = r"c:\Users\sai pragnya\Downloads\AuthentiCheck\templates\report.html"

with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the JS mapping script entirely
html = re.sub(r'<script>\s*function escapeHtml.*?</script>', '', html, flags=re.DOTALL)

# Let's replace the static doc information block
html = html.replace('<td class="value-cell" id="docName"></td>', '<td class="value-cell" id="docName">{{ report.filename }}</td>')
html = html.replace('<td class="value-cell" id="docType"></td>', '<td class="value-cell" id="docType">{{ report.mime_type }}</td>')
html = html.replace('<td class="value-cell" id="uploadTime"></td>', '<td class="value-cell" id="uploadTime">{{ report.upload_time }}</td>')
html = html.replace('<td class="value-cell" id="fileSize"></td>', '<td class="value-cell" id="fileSize">{{ report.file_size }}</td>')
html = html.replace('<td class="value-cell" id="docHash" style="font-family: monospace; font-size: 0.9rem;"></td>', '<td class="value-cell" id="docHash" style="font-family: monospace; font-size: 0.9rem;">{{ report.doc_hash }}</td>')

# Replacements for Modules
# Plagiarism Detection
html = re.sub(
    r'<div class="percentage-bar">\s*<div class="percentage-fill" style="width: 8%;">8%</div>\s*</div>\s*<span class="score-indicator score-low"><i class="fas fa-check"></i> Very Low</span>',
    r'''<div class="percentage-bar">
                <div class="percentage-fill" style="width: {{ report.modules['Plagiarism Detection'].score|int }}%;">{{ report.modules['Plagiarism Detection'].score|int }}%</div>
              </div>
              <span class="score-indicator {% if report.modules['Plagiarism Detection'].score >= 80 %}score-high{% elif report.modules['Plagiarism Detection'].score >= 50 %}score-medium{% else %}score-low{% endif %}"><i class="fas fa-check"></i> {{ report.modules['Plagiarism Detection'].status }}</span>''',
    html
)
html = html.replace('<td class="value-cell" id="plagiarismSources"></td>', '<td class="value-cell" id="plagiarismSources">{{ report.modules[\'Plagiarism Detection\'].status }}</td>')

# Paraphrasing Detection
html = re.sub(
    r'<div class="percentage-bar">\s*<div class="percentage-fill" style="width: 12%;">12%</div>\s*</div>\s*<span class="score-indicator score-low"><i class="fas fa-check"></i> Very Low</span>',
    r'''<div class="percentage-bar">
                <div class="percentage-fill" style="width: {{ report.modules['Paraphrasing Detection'].score|int }}%;">{{ report.modules['Paraphrasing Detection'].score|int }}%</div>
              </div>
              <span class="score-indicator {% if report.modules['Paraphrasing Detection'].score >= 80 %}score-high{% elif report.modules['Paraphrasing Detection'].score >= 50 %}score-medium{% else %}score-low{% endif %}"><i class="fas fa-check"></i> {{ report.modules['Paraphrasing Detection'].status }}</span>''',
    html
)
html = html.replace('<td class="value-cell" id="similarPhrases"></td>', '<td class="value-cell" id="similarPhrases">{{ report.modules[\'Paraphrasing Detection\'].status }}</td>')

# Metadata / Plagiarism matched content etc
html = re.sub(
    r'<tr>\s*<td class="label-cell"><i class="fas fa-align-left"></i> Matched Content Percentage</td>\s*<td class="value-cell">\s*<div class="percentage-bar">\s*<div class="percentage-fill" style="width: 8%;">8%</div>\s*</div>\s*</td>\s*</tr>',
    '',
    html
)
html = re.sub(
    r'<tr>\s*<td class="label-cell"><i class="fas fa-brain"></i> Semantic Similarity</td>\s*<td class="value-cell">\s*<div class="percentage-bar">\s*<div class="percentage-fill" style="width: 15%;">15%</div>\s*</div>\s*</td>\s*</tr>',
    '',
    html
)

html = html.replace(
    '<span class="classification-badge classification-original"><i class="fas fa-check-circle"></i> ORIGINAL</span>',
    '''<span class="classification-badge {% if report.final_score >= 80 %}classification-original{% else %}classification-suspicious{% endif %}">
                <i class="fas fa-check-circle"></i> {{ report.final_status|upper }}
              </span>'''
)

html = html.replace(
    '<span class="classification-badge classification-original"><i class="fas fa-check-circle"></i> INTACT</span>',
    '''<span class="classification-badge {% if report.modules['Metadata Verification'].score >= 80 %}classification-original{% else %}classification-suspicious{% endif %}">
                <i class="fas fa-check-circle"></i> {{ report.modules['Metadata Verification'].status|upper }}
              </span>'''
)

html = html.replace('<td class="value-cell" id="metadataConsistency"></td>', '<td class="value-cell" id="metadataConsistency">{{ report.modules[\'Metadata Verification\'].status }}</td>')
html = html.replace('<td class="value-cell" id="forgeryDetection"></td>', '<td class="value-cell" id="forgeryDetection">{{ report.modules[\'Metadata Verification\'].status }}</td>')
html = html.replace('<td class="value-cell" id="contentModification"></td>', '<td class="value-cell" id="contentModification">{{ report.modules[\'Metadata Verification\'].status }}</td>')
html = html.replace('<td class="value-cell" id="fingerprintMatch"></td>', '<td class="value-cell" id="fingerprintMatch">{{ report.modules[\'Similarity Detection\'].status }}</td>')

html = html.replace('<td class="value-cell" id="authorId"></td>', '<td class="value-cell" id="authorId">{{ report.modules[\'Authorship Analysis\'].status }}</td>')
html = html.replace('<td class="value-cell" id="writingConsistency"></td>', '<td class="value-cell" id="writingConsistency">{{ report.modules[\'Authorship Analysis\'].status }}</td>')
html = html.replace('<td class="value-cell" id="linguisticPattern"></td>', '<td class="value-cell" id="linguisticPattern">{{ report.modules[\'Authorship Analysis\'].status }}</td>')
html = html.replace('<td class="value-cell" id="vocabProfile"></td>', '<td class="value-cell" id="vocabProfile">{{ report.modules[\'Authorship Analysis\'].status }}</td>')
html = html.replace('<td class="value-cell" id="authorshipConfidence"></td>', '<td class="value-cell" id="authorshipConfidence">{{ report.modules[\'Authorship Analysis\'].score }}% Confidence</td>')

html = html.replace(
    '<span class="score-indicator score-high"><i class="fas fa-check"></i> Natural Writing</span>',
    '''<span class="score-indicator {% if report.modules['Paraphrasing Detection'].score >= 80 %}score-high{% else %}score-low{% endif %}"><i class="fas fa-check"></i> {{ report.modules['Paraphrasing Detection'].status }}</span>'''
)

# Final section overrides
html = re.sub(
    r'<div class="percentage-fill" style="width: 94%;">94%</div>',
    r'<div class="percentage-fill" style="width: {{ report.final_score|int }}%;">{{ report.final_score }}%</div>',
    html
)

html = html.replace('href="/upload"', 'href="/upload"') # Just checking
html = html.replace("const reportText = '{{ report | tojson | safe }}';", "")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)
print("Finished rewriting report.html")
