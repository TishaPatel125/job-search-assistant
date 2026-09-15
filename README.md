# 💼 AI-Powered Job Search Assistant

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

An end-to-end, AI-powered application that acts as your personal job application strategist. This tool ingests job posting PDFs, performs automated market analysis, flags fraudulent job postings using a custom Legitimacy Agent, and calculates a customized candidate fit score using Large Language Models (LLMs).

## ✨ Key Features

* **🖥️ Interactive Web Dashboard:** A sleek UI built with Streamlit that allows users to upload PDF job postings via drag-and-drop.
* **🧠 Structured AI Extraction:** Utilizes Pydantic and LLMs (OpenRouter/Gemini) to extract highly structured JSON metadata (skills, salary, experience) from unstructured PDFs.
* **🕵️ Legitimacy Agent:** Automatically protects applicants from scams by running WHOIS domain lookups and web scraping (Tavily API) to verify company legitimacy.
* **🗄️ Relational Database:** Automatically catalogs all processed jobs and metadata into a local SQLite database for historical tracking.
* **🤖 Automated Application Strategy:** Generates a comprehensive HTML report featuring a tailored cover letter guide, resume adaptation tips, and predicted interview questions.

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TishaPatel125/job-search-assistant.git
   cd job-search-assistant
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables:**
   Rename `.env.example` to `.env` and add your API keys:
   ```text
   OPENROUTER_API_KEY=your_openrouter_key
   TAVILY_API_KEY=your_tavily_key
   ```

4. **Initialize the Database & Run the App:**
   ```bash
   python src/db.py
   streamlit run app.py
   ```

## 🧪 Testing (CI/CD)

This project features a fully automated CI/CD pipeline using **GitHub Actions**. To run the `pytest` unit tests locally:

```bash
python -m pytest tests/
```

## 🛠️ Technology Stack

* **Language:** Python
* **Frontend:** Streamlit
* **Database:** SQLite3
* **AI / APIs:** OpenRouter (LLMs), Tavily Search API, Instructor (Structured Outputs)
* **Testing:** Pytest, GitHub Actions (CI/CD)
