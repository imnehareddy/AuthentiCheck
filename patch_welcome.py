import os, re
base_dir = r"c:\Users\sai pragnya\Downloads\AuthentiCheck"

sp = os.path.join(base_dir, "server.py")
with open(sp, "r", encoding="utf-8") as file:
    srv = file.read()

# Update route
srv = srv.replace("def home():\n    return render_template('index.html')", "def home():\n    return render_template('index.html', user=session.get('user'))")

# Update session['user'] assignments
old_sess = "session['user'] = email"
new_sess = "session['user'] = {'name': user.name, 'email': user.email, 'picture': ''}"
srv = srv.replace(old_sess, new_sess)

# Only write if it actually modified something
with open(sp, "w", encoding="utf-8") as file:
    file.write(srv)

ip = os.path.join(base_dir, "templates", "index.html")
with open(ip, "r", encoding="utf-8") as file:
    idx = file.read()

old_h1 = "<h1>Welcome to AuthentiCheck</h1>"
new_b = "{% if user %}\n      <h1>Welcome, {{ user.name }}</h1>\n    {% else %}\n      <h1>Welcome to AuthentiCheck</h1>\n    {% endif %}"
if old_h1 in idx:
    idx = idx.replace(old_h1, new_b)
    
if '<div id="welcome-user"></div>' in idx:
    idx = idx.replace('<div id="welcome-user"></div>', '')

with open(ip, "w", encoding="utf-8") as file:
    file.write(idx)

print("patched")
