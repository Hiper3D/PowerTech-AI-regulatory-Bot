## AI-Regulatory-Bot
Power Tech AI - Developer Setup Guide
This package contains the Regulatory AI Backend. It is a self-contained Python application that uses OpenAI GPT-4o and Vector Search (FAISS) to answer domain-specific questions.
🚀 Step 1: Install & Setup (Do this once)
 1,Extract Files: Unzip this folder on your laptop.
 2,Open Terminal: Open Command Prompt (Windows) or Terminal (Mac) inside this folder.
 3,Install Libraries: Run the following command:
pip install -r requirements.txt

4,Add API Key:
Create a new file named .env (no name, just dot env).
Open it and paste your company OpenAI Key:
<!-- end list -->
OPENAI_API_KEY=sk-proj-YOUR-REAL-KEY-HERE

🏃 Step 2: Run the Server
Run this command in your terminal:
uvicorn main:app --reload 

You should see: Uvicorn running on http://0.0.0.0:8000.
Keep this terminal open! This is the brain of the AI.

📚 Step 3: Train the AI (Upload PDFs)
Open your browser and go to: http://127.0.0.1:8000/admin
Click Select PDF and choose a Tariff Order or Regulation file.
Click Upload & Train.
Wait for the success message.

The AI has now "learned" that document. You don't need to re-upload it even if you restart the server.
 
🌐 Step 4: Integrate with Website
Open the file widget.html included in this package.
Copy the entire code block.
Open your website's main template file (e.g., base.html in Django/Flask).
Paste the code just before the closing </body> tag.
Refresh your website. You will see the Blue Chat Bubble in the corner.

🔗 API Documentation (For Backend Integration)
If you prefer to connect via Python code instead of the widget:
Endpoint: POST http://127.0.0.1

Server-to-Server API (Backend Integration) (Professional / Enterprise)
Advantages
More secure
Full control over logic & responses
Can integrate with internal systems (CRM, ERP, Billing)
No UI dependency
Disadvantages
Requires backend development
Slightly more setup time
