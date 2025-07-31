# 🌐 Wikipedia Explorer

![GitHub Stars](https://img.shields.io/github/stars/kacabdev/wikipedia_explorer?style=social)
![Visitors](https://visitor-badge.laobi.icu/badge?page_id=kacabdev.wikipedia_explorer)

Wikipedia Explorer is a lightweight and user-friendly web application that allows users to explore Wikipedia articles with ease. It supports searching by keyword, discovering random articles, and switching between languages—all through a clean and responsive interface.

---

## 📌 Project Objective

The main goal of this project is to gain hands-on experience using external APIs—specifically the [Wikipedia API]—while building practical skills in **Flask** backend development and **responsive frontend design** using **Bootstrap**.

---

## ✨ Features

### ✅ Current Features
- **Random Article Display**: Loads a random Wikipedia article on page load or via button click.
- **Search**: Lets users search for Wikipedia articles by keyword or title.
- **Language Selection**: Switch the Wikipedia language version (e.g., English, French).
- **Responsive UI**: Built with Bootstrap 5 to ensure usability across all screen sizes.
- **Custom Favicon**: Unique icon for browser tab branding.

### 🚧 Planned Features
- **"Rabbit Hole" Navigation**: Jump to a random linked article from the current one.
- **Page Visit Counter**: Tracks number of random articles visited in the current session.
- **Visit History**: Display recently viewed articles.
- **Category Filter**: Suggest articles based on selected Wikipedia categories.

---

## 🛠️ Tech Stack

| Layer        | Technology                                 |
|--------------|--------------------------------------------|
| **Backend**  | Python (Flask)                             |
| **Frontend** | HTML5, CSS3 (SASS), JavaScript, Bootstrap5 |
| **API**      | Wikipedia RESTBase API & MediaWiki API     |
| **Tools**    | pip, Git, GitHub, requirements.txt         |

---

## 🚀 Getting Started

### 📋 Prerequisites
- Python 3.8+
- Git

### 🔧 Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/kacabdev/wikipedia_explorer.git
   cd wikipedia_explorer
   ```

2. **Create and Activate a Virtual Environment**
   - Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - macOS / Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment File (Optional)**
   ```bash
   echo "" > .env
   ```
   *Currently, no API keys are required. This file is reserved for future configuration.*

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Open in Browser**
   Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧪 Usage

| Feature            | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| Random Article      | Automatically shown on homepage load or via the **Get Random Page** button |
| Search              | Enter keywords to fetch matching articles                                  |
| Language Selection  | Switch between Wikipedia languages from the navbar                         |

---

## 🗂️ Project Structure

```
wikipedia_explorer/
├── api/
│   └──index.py
├── venv/                  # Python virtual environment
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── .env                   # Environment variables (git-ignored)
├── .gitignore             # Files and folders to exclude from Git
├── requirements.txt       # Python dependencies
├── static/                # Static files (CSS, JS, favicon)
│   ├── css/
│   │   └── style.css
│   └── favicon.png
└── templates/             # Jinja2 HTML templates
    ├── base.html
    └── index.html
```

---

## 🤝 Contributing

Pull requests, suggestions, and feature requests are welcome! If you'd like to contribute, feel free to fork the repository or contact the developer directly.

---

## 📝 License

This project is licensed under the **MIT License**. See [`LICENSE.md`](LICENSE.md) for more information (if available).

---

## 📬 Contact

**Developer**: [kacabdev](https://github.com/kacabdev)

For any questions, feedback, or collaboration opportunities, don’t hesitate to reach out!