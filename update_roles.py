import os

team_file = r"c:\Users\sai pragnya\Downloads\AuthentiCheck\templates\team.html"
with open(team_file, "r", encoding="utf-8") as f:
    text = f.read()

# Member 1
text = text.replace('<h3>Dr. Rajesh Kumar</h3>\n          <p class="role"><i class="fas fa-chess-king"></i> Project Lead</p>', '<h3>Project Lead</h3>')
text = text.replace("Dr. Rajesh Kumar leads", "Our Project Lead guides")
text = text.replace("He holds", "They hold")
text = text.replace("has", "have")

# Member 2
text = text.replace('<h3>Priya Sharma</h3>\n          <p class="role"><i class="fas fa-code"></i> Lead Developer</p>', '<h3>Lead Developer</h3>')
text = text.replace("Priya is a", "Our Lead Developer is a")
text = text.replace("She has", "They have")

# Member 3
text = text.replace('<h3>Aditya Patel</h3>\n          <p class="role"><i class="fas fa-robot"></i> ML Specialist</p>', '<h3>ML Specialist</h3>')
text = text.replace("Aditya brings", "Our ML Specialist brings")
text = text.replace("he developed", "they developed")

# Member 4
text = text.replace('<h3>Neha Gupta</h3>\n          <p class="role"><i class="fas fa-pencil-ruler"></i> UI/UX Designer</p>', '<h3>UI/UX Designer</h3>')
text = text.replace("Neha designed", "Our UI/UX Designer crafted")
text = text.replace("Her expertise", "Their expertise")

# Member 5
text = text.replace('<h3>Vikram Singh</h3>\n          <p class="role"><i class="fas fa-lock"></i> Security Officer</p>', '<h3>Security Officer</h3>')
text = text.replace("Vikram ensures", "Our Security Officer ensures")
text = text.replace("He manages", "They manage")

# Member 6
text = text.replace('<h3>Ananya Nair</h3>\n          <p class="role"><i class="fas fa-check-circle"></i> QA Lead</p>', '<h3>QA Lead</h3>')
text = text.replace("Ananya oversees", "Our QA Lead oversees")
text = text.replace("Her meticulous approach ensures", "Their meticulous approach ensures")

with open(team_file, "w", encoding="utf-8") as f:
    f.write(text)

readme_file = r"c:\Users\sai pragnya\Downloads\AuthentiCheck\README.md"
with open(readme_file, "r", encoding="utf-8") as f:
    readme_text = f.read()

readme_text = readme_text.replace("- **Dr. Rajesh Kumar** - Project Lead, Cryptography Expert", "- **Project Lead** - Cryptography Expert")
readme_text = readme_text.replace("- **Priya Sharma** - Lead Developer, Full Stack Engineer", "- **Lead Developer** - Full Stack Engineer")
readme_text = readme_text.replace("- **Aditya Patel** - Machine Learning Specialist", "- **Machine Learning Specialist**")
readme_text = readme_text.replace("- **Neha Gupta** - UI/UX Designer", "- **UI/UX Designer**")
readme_text = readme_text.replace("- **Vikram Singh** - Security & Compliance Officer", "- **Security & Compliance Officer**")
readme_text = readme_text.replace("- **Ananya Nair** - Quality Assurance Lead", "- **Quality Assurance Lead**")

with open(readme_file, "w", encoding="utf-8") as f:
    f.write(readme_text)

print("Done")
