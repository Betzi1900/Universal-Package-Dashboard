# 📦 Universal Package Dashboard

A clean, local Python dashboard to track all your packages in one place. Built with a focus on simplicity, local privacy, and easy extensibility.

## ✨ Features
* **Local Privacy:** No cloud tracking! All your data is stored locally in a SQLite database.
* **DHL API Integration:** Reliable tracking using the official DHL API, utilizing a smart XML-bypass to handle firewall restrictions.
* **Extensible:** Designed to easily add more carriers like Hermes, DPD, or GLS in the future.
* **Desktop GUI:** Built with Python (Tkinter) for a native look and feel.

## 🚀 Getting Started

### Prerequisites
* Python 3.x installed on your machine.
* `pip` (Python package manager).

### Installation & Running

**For Linux (Debian/Ubuntu/Mint) users:**
Make sure Tkinter and python-venv are installed on your system:
```bash
sudo apt update
sudo apt install python3-tk python3-venv
```
1. Clone the repository:
```bash
git clone https://github.com/Betzi1900/Universal-Package-Dashboard.git
cd Universal-Package-Dashboard
```
2. Create and activate a virtual environment (Recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Configuration:

Create a config.json file in the root directory (you can use config_template.json as a reference):
```json
{
    "dhl_api_key": "YOUR_KEY",
    "dhl_api_secret": "YOUR_SECRET"
}
```
Note: Never share your config.json publicly!

5. Start the dashboard:
```bash
python main.py
```
## ⚙️ How it works

The dashboard communicates directly with the DHL API. All tracking information is fetched in real-time and stored in a local SQLite database file (dashboard.db) to ensure your privacy and offline access to your package history.
## 🛠️ Built With

* **Python** - The core programming language.
* **Tkinter** - The GUI framework.
* **SQLite** - Lightweight, serverless local database.
* **Requests** - For handling API calls.

## 📄 License

This project is licensed under the GNU General Public License v3.0.
See the LICENSE file for details.
## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

Stay organized, stay private!