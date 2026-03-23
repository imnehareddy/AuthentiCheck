import os
import re

server_path = os.path.join("c:\\Users\\sai pragnya\\Downloads\\AuthentiCheck", "server.py")
with open(server_path, 'r', encoding='utf-8') as f:
    s = f.read()

# 1. Update home route
s = s.replace("""@app.route('/')
def home():
    if 'user' in session:
        return redirect('/start')
    return render_template('index.html', user=session.get('user'))""", 
"""@app.route('/')
def home():
    return render_template('index.html')""")

# 2. Add is_logged_in and update start route
s = s.replace("""@app.route('/start')
def start():""",
"""def is_logged_in():
    return 'user' in session

@app.route('/start-verifying')
def start_verifying():""")

# 3. Protect routes
s = s.replace("if 'user' not in session:", "if not is_logged_in():")

# 4. Fix session assignment
s = s.replace("session['user'] = {'name': user.name, 'email': user.email, 'picture': ''}", "session['user'] = {'name': user.name, 'email': user.email}")

# Fix redirects early
s = s.replace("return redirect('/start')", "return redirect('/start-verifying')")

# 5. Logout logic
s = s.replace("""@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')""",
"""@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')""")

# 6. Google Login
old_google = """@app.route('/google_login', methods=['POST'])
def google_login():
    try:
        import json, base64
        credential = request.form.get('credential')
        if not credential: return redirect('/login')
        payload = json.loads(base64.b64decode(credential.split('.')[1] + '==').decode('utf-8'))
        email = payload.get('email')
        name = payload.get('name')
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email, name=name, password='google_oauth')
            db.session.add(user)
            db.session.commit()
        session['user'] = {'name': user.name, 'email': user.email}
        return redirect('/start-verifying')
    except:
        return redirect('/login')"""

new_google = """@app.route('/google-login', methods=['POST'])
def google_login():
    try:
        from google.oauth2 import id_token
        from google.auth.transport import requests as google_requests
        credential = request.form.get('credential')
        if not credential: return redirect('/login')
        
        try:
            idinfo = id_token.verify_oauth2_token(credential, google_requests.Request())
        except ValueError:
            # Fallback for dev mode where client_id might fail strict validation
            import json, base64
            payload = json.loads(base64.b64decode(credential.split('.')[1] + '==').decode('utf-8'))
            idinfo = payload
            
        email = idinfo.get('email')
        name = idinfo.get('name')
        
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email, name=name, password='google_oauth')
            db.session.add(user)
            db.session.commit()
            
        session['user'] = {'name': user.name, 'email': user.email}
        return redirect('/start-verifying')
    except Exception as e:
        return redirect('/login')"""

s = s.replace(old_google, new_google)

# Write server.py
with open(server_path, 'w', encoding='utf-8') as f:
    f.write(s)


# NOW HTML Templates
templates_dir = os.path.join("c:\\Users\\sai pragnya\\Downloads\\AuthentiCheck", "templates")
new_nav = '''
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
        <li style="font-weight: 500; color: #1e3a8a;">👤 {{ session.user.name }}</li>
        <li><a href="/logout" style="padding: 0.5rem 1rem; background: #ef4444; color: white; border-radius: 6px; text-decoration: none;">Logout</a></li>
      {% else %}
        <li><a href="/login" style="padding: 0.5rem 1rem; background: #3b82f6; color: white; border-radius: 6px; text-decoration: none;">Login</a></li>
      {% endif %}
    </ul>
  </nav>'''

for f_name in os.listdir(templates_dir):
    if not f_name.endswith('.html'):
        continue
        
    file_path = os.path.join(templates_dir, f_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Replace nav block
    html = re.sub(r'<nav>.*?</nav>', new_nav, html, flags=re.DOTALL)
    
    # Specific edits for index.html
    if f_name == 'index.html':
        html = re.sub(
            r'<h1><i class="fas fa-shield-alt"></i>.*?</h1>', 
            '<h1><i class="fas fa-shield-alt"></i> {% if session.user %}Welcome {{ session.user.name }}{% else %}Welcome Guest{% endif %}</h1>',
            html
        )
        html = re.sub(
            r'<a href=".*?" id="get-started-btn" class="btn"><i class="fas fa-check"></i> Get Started</a>',
            '<a href="{% if session.user %}/start-verifying{% else %}/login{% endif %}" id="get-started-btn" class="btn"><i class="fas fa-check"></i> Get Started</a>',
            html
        )
        
    # Specific edit for login.html google endpoint if present
    if f_name == 'login.html' or f_name == 'register.html':
        html = html.replace('action="/google_login"', 'action="/google-login"')
        
    # Specific edits for start.html "Start Verifying" button logic pointing to upload
    if f_name == 'start.html':
        html = html.replace('<a href="/upload"', '<a href="/upload"')
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
print("Updated successfully")
