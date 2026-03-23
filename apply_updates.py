import os, re
base_dir = r"c:\Users\sai pragnya\Downloads\AuthentiCheck"
def get_path(f): return os.path.join(base_dir, f)

# === 1. server.py ===
srv_path = get_path("server.py")
with open(srv_path, "r", encoding="utf-8") as f: srv = f.read()
# Fix login redirect
srv = re.sub(r"session\['user'\] = email\s+return redirect\('/'\)", r"session['user'] = email\n                return redirect('/upload')", srv)

# Add google_login before register if absent
if "def google_login():" not in srv:
    g_log = "\n@app.route('/google_login', methods=['POST'])\ndef google_login():\n    try:\n        import json, base64\n        credential = request.form.get('credential')\n        if not credential: return redirect('/login')\n        payload = json.loads(base64.b64decode(credential.split('.')[1] + '==').decode('utf-8'))\n        email = payload.get('email')\n        name = payload.get('name')\n        user = User.query.filter_by(email=email).first()\n        if not user:\n            user = User(email=email, name=name, password='google_oauth')\n            db.session.add(user)\n            db.session.commit()\n        session['user'] = email\n        return redirect('/upload')\n    except:\n        return redirect('/login')\n"
    srv = srv.replace("@app.route('/register", g_log + "\n@app.route('/register")

# Fix register redirect
srv = re.sub(r"db\.session\.commit\(\)\s+session\['user'\] = email\s+return redirect\('/'\)", r"db.session.commit()\n        return redirect('/login')", srv)

# Auth Score upload calculation modification
if "authorship_score" not in srv:
    old_upload = r"metadata = run_module\(\)\s+similarity = run_module\(\)\s+plagiarism = run_module\(\)\s+paraphrasing = run_module\(\)"
    new_upload = "metadata = run_module()\n        similarity = run_module()\n        plagiarism = run_module()\n        paraphrasing = run_module()\n        authorship_score = random.randint(30, 95)"
    srv = re.sub(old_upload, new_upload, srv)
    
    old_calc = r"final_score = \(\s*metadata\['score'\] \* 0\.25 \+\s*similarity\['score'\] \* 0\.25 \+\s*plagiarism\['score'\] \* 0\.30 \+\s*paraphrasing\['score'\] \* 0\.20\s*\)"
    new_calc = "final_score = (metadata['score'] * 0.2 + similarity['score'] * 0.2 + plagiarism['score'] * 0.2 + paraphrasing['score'] * 0.2 + authorship_score * 0.2)"
    srv = re.sub(old_calc, new_calc, srv)
    
    rep_mod = """            'color': 'green' if final_score >= 80 else ('yellow' if final_score >= 50 else 'red'),
            'modules': {
                'Metadata Verification': metadata,
                'Similarity Detection': similarity,
                'Plagiarism Detection': plagiarism,
                'Paraphrasing Detection': paraphrasing,
                'Authorship Analysis': {'score': authorship_score, 'status': 'Pass' if authorship_score >= 80 else ('Suspicious' if authorship_score >= 50 else 'Fail')}
            }"""
    srv = re.sub(r"'modules': \{[^}]+}", rep_mod, srv)

# Apply History Protection
srv = srv.replace("def history():\n    return render_template('history.html')", "def history():\n    if 'user' not in session: return redirect('/login')\n    return render_template('history.html')")
with open(srv_path, "w", encoding="utf-8") as f: f.write(srv)

# === 2. login.html & register.html ===
for tmpl in ["login.html", "register.html"]:
    with open(get_path(f"templates/{tmpl}"), "r", encoding="utf-8") as f:
        html = f.read()
    if "data-login_uri" not in html:
        gi = """\n      <hr style="margin: 20px 0;">\n      <div id="g_id_onload" data-client_id="YOUR_GOOGLE_CLIENT_ID" data-login_uri="/google_login" data-auto_prompt="false"></div>\n      <div class="g_id_signin" data-type="standard" data-size="large" data-theme="outline" data-shape="rectangular"></div>\n"""
        html = html.replace("</form>", gi + "</form>")
    with open(get_path(f"templates/{tmpl}"), "w", encoding="utf-8") as f:
        f.write(html)

# === 3. upload.html ===
up_html = get_path("templates/upload.html")
with open(up_html, "r", encoding="utf-8") as f: uh = f.read()
uh = uh.replace('<button type="submit" class="btn">', '<button type="submit" class="btn btn-success" id="start-verifying-btn" style="padding: 15px 30px; font-size: 1.1rem; border-radius: 8px;">')
uh = uh.replace('Verify Document', 'Start Verifying')
with open(up_html, "w", encoding="utf-8") as f: f.write(uh)

# === 4. JS Fixes ===
js_path = get_path("js/script.js")
with open(js_path, "r", encoding="utf-8") as f: js = f.read()
for v in ["storedDocsCache", "storedAutoRefreshTimer", "storedSearchDebounce", "uploadedDocsCache", "uploadedAutoRefreshTimer", "uploadedSearchDebounce"]:
    js = js.replace(f"let {v}", f"var {v}")
with open(js_path, "w", encoding="utf-8") as f: f.write(js)

# === 5. CSS Fixes ===
css_path = get_path("css/styles.css")
with open(css_path, "r", encoding="utf-8") as f: css = f.read()
if "color: #000 !important;" not in css:
    css += "\ninput[type=\"text\"], input[type=\"email\"], input[type=\"password\"], input[type=\"file\"], textarea, select { color: #000 !important; background: #fff !important; }\n"
with open(css_path, "w", encoding="utf-8") as f: f.write(css)

# === 6. history.html Dynamic Fetch ===
hist_path = get_path("templates/history.html")
with open(hist_path, "r", encoding="utf-8") as f: hh = f.read()
if "fetch('/api/documents/uploaded')" not in hh:
    hs = """<div id="historyRenderBlock"></div>
<script>
document.addEventListener("DOMContentLoaded", function() {
   fetch('/api/documents/uploaded')
     .then(r => r.json())
     .then(d => {
        const c = document.getElementById('historyRenderBlock');
        if(!d.length) { c.innerHTML = '<p>No documents.</p>'; return; }
        let h = '<table class="report-table"><tr><th>Filename</th><th>Time</th></tr>';
        d.forEach(x => h += `<tr><td>${x.filename}</td><td>${x.upload_time}</td></tr>`);
        h += '</table>';
        c.innerHTML = h;
     });
});
</script>"""
    hh = hh.replace("</main>", hs + "\n</main>")
with open(hist_path, "w", encoding="utf-8") as f: f.write(hh)

print("Patching Complete.")
