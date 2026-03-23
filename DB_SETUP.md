# MySQL Database Setup Instructions for AuthentiCheck

1. Install MySQL Server (if not already installed):
   - Download from https://dev.mysql.com/downloads/installer/
   - Follow the installation steps and set a root password.

2. Create a new database and user for AuthentiCheck:

   ```sql
   CREATE DATABASE authenticheck_db;
   CREATE USER 'authuser'@'localhost' IDENTIFIED BY 'authpass123';
   GRANT ALL PRIVILEGES ON authenticheck_db.* TO 'authuser'@'localhost';
   FLUSH PRIVILEGES;
   ```

3. Install MySQL client for Python:
   - In your virtual environment, run:
     ```
     pip install mysql-connector-python
     ```

4. Update your server.py to connect to the MySQL database.

5. Migrate reference files and add educational data as needed.

---

See README_backend.md for more details after setup.
