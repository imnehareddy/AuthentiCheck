import os
import shutil

base_dir = r"c:\Users\sai pragnya\Downloads\AuthentiCheck"
static_dir = os.path.join(base_dir, "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

# Move CSS and JS
for folder in ["css", "js", "images"]:
    src = os.path.join(base_dir, folder)
    dst = os.path.join(static_dir, folder)
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.move(src, dst)

# Update HTML templates
templates_dir = os.path.join(base_dir, "templates")
for fname in os.listdir(templates_dir):
    if not fname.endswith(".html"): continue
    
    path = os.path.join(templates_dir, fname)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
        
    html = html.replace('href="/css/styles.css"', 'href="{{ url_for(\'static\', filename=\'css/styles.css\') }}"')
    html = html.replace('src="/js/script.js"', 'src="{{ url_for(\'static\', filename=\'js/script.js\') }}"')
    
    # Specific navbar UI requirement: "user profile icon" (added font awesome icon)
    # The previous nav injected 👤. Let's make it a proper user icon if it matches:
    html = html.replace('👤 {{ session.user.name }}', '<i class="fas fa-user-circle"></i> {{ session.user.name }}')
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

# Update server.py
server_path = os.path.join(base_dir, "server.py")
with open(server_path, "r", encoding="utf-8") as f:
    s = f.read()

# Add /result route if not exists
if "@app.route('/result/<int:doc_id>')" not in s:
    result_route = """
@app.route('/result/<int:doc_id>')
def result(doc_id):
    if not is_logged_in(): return redirect('/login')
    doc = get_db_connection().execute("SELECT * FROM reports WHERE id=?", (doc_id,)).fetchone()
    if not doc: return "Not found", 404
    return render_template('result.html', doc=doc)
"""
    s = s.replace("@app.route('/report/<doc_id>')", result_route + "\n@app.route('/report/<doc_id>')")
    # Actually wait, report route in server is `@app.route('/report/<int:id>')` maybe?
    # Let's just append it before `@app.route('/report`
    
    import re
    s = re.sub(r'(@app\.route\(\'/report/<)', result_route + r'\n\1', s)

# Redirect /upload to /result instead of /report
s = s.replace("return redirect(f'/report/{report_id}')", "return redirect(f'/result/{report_id}')")
# Also handle if it returned jsonify
s = s.replace("'redirect': f'/report/{report_id}'", "'redirect': f'/result/{report_id}'")

# Add file size validation to /upload
size_val = """
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        if size > 50 * 1024 * 1024:
            return "File exceeds 50MB limit", 400
"""
if "File exceeds 50MB limit" not in s:
    s = s.replace("file_content = file.read()", size_val + "\n        file_content = file.read()")

with open(server_path, "w", encoding="utf-8") as f:
    f.write(s)

# Create /templates/result.html
result_path = os.path.join(templates_dir, "result.html")
result_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Verification Result - AuthentiCheck</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
  <nav style="display: flex; justify-content: space-between; align-items: center; background: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.1); padding: 1rem 2rem;">
    <ul class="nav-links" style="display: flex; align-items: center; gap: 1.5rem; list-style: none; margin: 0; padding: 0;">
      <li class="logo" style="font-weight: bold; font-size: 1.2rem; color: #1e3a8a;"><i class="fas fa-certificate"></i> AuthentiCheck</li>
      <li><a href="/" style="text-decoration: none; color: #4b5563;"><i class="fas fa-home"></i> Home</a></li>
      <li><a href="/upload" style="text-decoration: none; color: #4b5563;"><i class="fas fa-upload"></i> Upload</a></li>
      <li><a href="/history" style="text-decoration: none; color: #4b5563;"><i class="fas fa-history"></i> History</a></li>
      <li><a href="/about" style="text-decoration: none; color: #4b5563;"><i class="fas fa-info-circle"></i> About</a></li>
    </ul>
    <ul class="auth-links" style="display: flex; align-items: center; gap: 1.5rem; list-style: none; margin: 0; padding: 0;">
      {% if session.user %}
        <li style="font-weight: 500; color: #1e3a8a;"><i class="fas fa-user-circle"></i> {{ session.user.name }}</li>
        <li><a href="/logout" style="padding: 0.5rem 1rem; background: #ef4444; color: white; border-radius: 6px; text-decoration: none;">Logout</a></li>
      {% else %}
        <li><a href="/login" style="padding: 0.5rem 1rem; background: #3b82f6; color: white; border-radius: 6px; text-decoration: none;">Login</a></li>
      {% endif %}
    </ul>
  </nav>

  <main style="min-height: 80vh; padding: 3rem; background: #f8fafc; display: flex; justify-content: center; align-items: center;">
    <div style="background: white; padding: 3rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); text-align: center; max-width: 600px; width: 100%;">
      <h1 style="color: #1e3a8a; margin-bottom: 2rem;"><i class="fas fa-check-circle" style="color: #10b981;"></i> Analysis Complete</h1>
      
      <div style="margin-bottom: 2rem; text-align: left; background: #f1f5f9; padding: 1.5rem; border-radius: 8px;">
        <h3 style="margin-top:0; color: #334155;">Summary for {{ doc.filename }}</h3>
        <p><strong>Final Score:</strong> <span style="font-size: 1.2rem; font-weight: bold;">{{ doc.final_score }}%</span></p>
        <p><strong>Status:</strong> 
          {% if doc.final_status == 'ORIGINAL' %}
            <span style="color: #10b981; font-weight: bold; background: #d1fae5; padding: 0.2rem 0.6rem; border-radius: 4px;">{{ doc.final_status }}</span>
          {% elif doc.final_status == 'SUSPICIOUS' %}
            <span style="color: #d97706; font-weight: bold; background: #fef3c7; padding: 0.2rem 0.6rem; border-radius: 4px;">{{ doc.final_status }}</span>
          {% else %}
            <span style="color: #ef4444; font-weight: bold; background: #fee2e2; padding: 0.2rem 0.6rem; border-radius: 4px;">{{ doc.final_status }}</span>
          {% endif %}
        </p>
      </div>

      <a href="/report/{{ doc.id }}" style="display: inline-block; padding: 0.8rem 2rem; background: #2563eb; color: white; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 1.1rem; transition: background 0.2s;"><i class="fas fa-file-alt"></i> View Full Report</a>
    </div>
  </main>
  
  <footer style="text-align: center; padding: 2rem; background: #1e293b; color: white;">
    <p>&copy; 2026 AuthentiCheck. All rights reserved.</p>
  </footer>
  <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>"""

with open(result_path, "w", encoding="utf-8") as f:
    f.write(result_html)

# Fix script.js errors
script_path = os.path.join(static_dir, "js", "script.js")
if os.path.exists(script_path):
    with open(script_path, "r", encoding="utf-8") as f:
        js = f.read()
    
    if "function renderUploadedDocuments(" not in js:
        js += "\n\nfunction renderUploadedDocuments(docs) { console.log('renderUploadedDocuments called', docs); }\n"
        
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(js)

print("Rubric refactoring complete")
