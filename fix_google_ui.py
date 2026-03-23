import os
import re

html_files = [
    r"c:\Users\sai pragnya\Downloads\AuthentiCheck\templates\login.html",
    r"c:\Users\sai pragnya\Downloads\AuthentiCheck\templates\register.html"
]

google_snippet = """      <hr style="margin: 20px 0;">
      <!-- Google Sign In -->
      <div id="g_id_onload" 
           data-client_id="674327002143-nhkch5dqp5g9cvbgu6rgtsmpattg83vp.apps.googleusercontent.com"
           data-context="use"
           data-ux_mode="popup"
           data-callback="handleCredentialResponse"
           data-auto_prompt="false">
      </div>
      <div class="g_id_signin" 
           data-type="standard" 
           data-shape="rectangular" 
           data-theme="outline" 
           data-text="continue_with"
           data-size="large" 
           data-logo_alignment="left"
           style="display: flex; justify-content: center; margin-top: 15px;">
      </div>

      <script>
        function handleCredentialResponse(response) {
          const form = document.createElement('form');
          form.method = 'POST';
          form.action = '/google-login';
          const input = document.createElement('input');
          input.type = 'hidden';
          input.name = 'credential';
          input.value = response.credential;
          form.appendChild(input);
          document.body.appendChild(form);
          form.submit();
        }
      </script>"""

for file_path in html_files:
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Remove the old GSI divs
        html = re.sub(r'<div id="g_id_onload".*?</div>', '', html, flags=re.DOTALL)
        html = re.sub(r'<div class="g_id_signin".*?</div>', '', html, flags=re.DOTALL)
        html = re.sub(r'<hr style="margin: 20px 0;">', '', html)
        
        # We need to inject the new code before the closing </form>
        html = html.replace('</form>', google_snippet + '\n</form>')
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

print("Google UI rewritten")
