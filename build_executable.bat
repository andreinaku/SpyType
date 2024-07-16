.venv\Scripts\pyinstaller --onefile --add-data ".\\.venv\\Lib\\site-packages\\maude\\*.maude;.\\maude\\" --add-data "new.maude;." simple_inference.py
