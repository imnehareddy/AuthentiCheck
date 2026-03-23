import os
import re

team_file = r"c:\Users\sai pragnya\Downloads\AuthentiCheck\templates\team.html"
with open(team_file, "r", encoding="utf-8") as f:
    text = f.read()

text = re.sub(r'<!-- Contact Section -->.*?</div>', '', text, flags=re.DOTALL)

with open(team_file, "w", encoding="utf-8") as f:
    f.write(text)

readme_file = r"c:\Users\sai pragnya\Downloads\AuthentiCheck\README.md"
with open(readme_file, "r", encoding="utf-8") as f:
    readme_text = f.read()

readme_text = re.sub(r'## 📞 Contact & Support.*?(?=---|$)', '', readme_text, flags=re.DOTALL)

# Ensure no double dashes left behind
readme_text = readme_text.replace("\n---\n\n---", "\n---")

with open(readme_file, "w", encoding="utf-8") as f:
    f.write(readme_text)

print("Contact section removed successfully")
