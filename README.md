
````markdown
# 🧠 Reddit Persona Analyzer

Automatically generate a detailed user persona from any public Reddit profile, complete with HTML output and citation links from posts/comments.

> 🔗 Paste a Reddit profile URL → 🛠️ Script scrapes activity → 🧾 Generates a user persona → 🌐 Outputs a beautiful HTML profile

---

## 📸 Sample Output

*(Insert screenshot here — e.g., a preview of the generated HTML page)*  
🧾 Example output: `output/persona_kojied.html`

---

## 🚀 Features

- ✅ Scrapes **posts and comments** from Reddit user profiles  
- ✅ Uses **NLP + LLMs** to build realistic psychological personas  
- ✅ Outputs a stylish, structured **HTML profile**  
- ✅ Every trait includes a **citation** from real posts/comments  
- ✅ Fully offline after setup  

---

## ⚙️ Built With

- **Python 3.10+**
- **Conda (recommended)**
- [PRAW](https://praw.readthedocs.io/) – Reddit API Wrapper  
- [spaCy](https://spacy.io/) – Natural Language Processing  
- [Jinja2](https://jinja.palletsprojects.com/) – HTML rendering  
- `dotenv` – Environment variable handling  

---

## 📥 Installation (Using Conda)

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/Santhosh-Ganesan2004/Reddit-Persona-Analyser.git
cd Reddit-Persona-Analyser
````

### 2️⃣ Create and Activate a Conda Environment

```bash
conda create -n reddit_env python=3.10
conda activate reddit_env
```

### 3️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

## 🔐 Reddit API Credentials

Reddit requires an API key to fetch data.

### Step-by-step:

1. Go to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. Click **"Create App"** → Choose **"script"**
3. Fill in:

   * Name: anything
   * Redirect URI: `http://localhost:8080`
4. Copy:

   * `client_id` (under app name)
   * `client_secret` (shown after creation)

### Then create a `.env` file in your project folder:

```
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
USER_AGENT=windows:reddit.persona:v1.0 (by u/your_username)
```

> ⚠️ **Don't share this file or upload it to GitHub!**

---

## ▶️ How to Use It

Run the script in your terminal:

```bash
python persona.py
```

Then when prompted, paste a Reddit profile URL:

```
https://www.reddit.com/user/kojied/
```

The tool will scrape data, process it, and generate:

```
📁 output/persona_kojied.html
```

Open that file in any browser to view the profile.

---

## 📁 Project Structure

```
📦 Reddit-Persona-Analyser
├── persona.py                 # Main script
├── .env                      # Reddit credentials (never push this!)
├── requirements.txt
├── output/                   # Folder for generated HTML personas
│   └── persona_<user>.html
└── README.md
```

---

## 🔐 .gitignore Reminder

Before committing:

```bash
echo .env > .gitignore
echo output/ >> .gitignore
git add .gitignore
git commit -m "🔒 Added .gitignore to exclude secrets and outputs"
```

---

## ✨ Future Upgrades (Ideas)

* ✅ Streamlit web interface
* ✅ PDF export of persona
* ✅ Tone & sentiment analysis graph
* ✅ GPT-powered summarization
* ✅ Keyword/tag heatmaps

---

## 📄 License

MIT License — open source, use it freely 🔓
Attribution appreciated but not required.

---



