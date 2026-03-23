with open('server.py', 'r', encoding='utf-8') as f:
    s = f.read()

s = s.replace("\\'", "'")

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(s)
