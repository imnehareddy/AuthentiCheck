import os, re
base = r"c:\Users\sai pragnya\Downloads\AuthentiCheck"

f = os.path.join(base, "server.py")
with open(f, "r", encoding="utf-8") as file:
    srv = file.read()

# Fix login redirect -> /start
srv = srv.replace("return redirect('/upload')", "return redirect('/start')")

# Fix start route
old_start = """@app.route('/start')
def start():
    if 'user' in session: return redirect('/upload')
    return redirect('/login')"""
new_start = """@app.route('/start')
def start():
    if 'user' not in session: return redirect('/login')
    return render_template('start.html')"""
srv = srv.replace(old_start, new_start)

# Save
with open(f, "w", encoding="utf-8") as file:
    file.write(srv)

# Fix upload.html button (reverting Start Verifying to Upload)
u = os.path.join(base, "templates", "upload.html")
with open(u, "r", encoding="utf-8") as file:
    uh = file.read()
uh = uh.replace('<i class="fas fa-check"></i> Start Verifying', '<i class="fas fa-upload"></i> Upload')
uh = uh.replace('id="start-verifying-btn"', '')
with open(u, "w", encoding="utf-8") as file:
    file.write(uh)
