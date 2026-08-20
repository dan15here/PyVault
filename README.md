# 🔐 PyVault - Password Manager

A secure terminal-based (CLI) **Password Manager** application for storing and managing your account credentials. Built with Python and an interactive TUI (Text User Interface).

---

## ✨ Key Features

- 🔒 **Strong Encryption** — Uses Argon2 for password hashing and Cryptography for data encryption
- 🖥️ **Interactive Terminal Interface** — Easy-to-use curses-based interface
- 📋 **Copy to Clipboard** — Copy passwords directly to the clipboard with a single key press
- 🔍 **Search & Filter** — Quickly find credentials by label
- ✏️ **Complete CRUD Operations** — Add, view, edit, and delete password entries
- 📝 **Logging** — Records activity for security monitoring
- 🛡️ **Password Validation** — Ensures master passwords meet security requirements

---

## 📋 System Requirements

- **Python**: Version 3.8 or later
- **Operating System**: Windows, Linux, or macOS
- **Dependencies**: See `requirements.txt`

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/dan15here/PyVault.git
cd PyVault
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 💻 Usage

### Run the Application

```bash
python main.py
```

### First-Time Setup

1. The application will ask you to create a **Master Password**.
2. Your master password must meet the following requirements:
   - At least 8 characters long
   - Contains uppercase and lowercase letters
   - Contains numbers
   - Contains special symbols

### Main Menu

- **Dashboard** — View all saved credentials
- **Add New** — Add a new password entry
- **Search** — Search for credentials by label
- **Exit** — Close the application

### Navigation

- Use the **Arrow Keys** (↑/↓) to navigate the menu.
- Press **Enter** to select an option.
- Press **ESC** or **Q** to go back.

---

## 📁 Project Structure

```bash
tugas_pbl_kel2/
├── main.py              # Application entry point
├── requirements.txt     # List of dependencies
├── README.md            # Project documentation
└── src/
    ├── app_controller.py  # Main application logic
    ├── crypto_utils.py    # Encryption and decryption
    ├── db_manager.py      # Database management
    ├── tui.py             # Terminal UI components
    ├── utils.py           # Utility functions
    └── logger.py          # Logging system
```

---

## 🔧 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `argon2-cffi` | 23.1.0 | Password hashing with Argon2 |
| `cryptography` | 41.0.7 | Data encryption and decryption |
| `pyperclip` | 1.8.2 | Copy passwords to the clipboard |
| `windows-curses` | 2.3.3 | Curses support for Windows |

---

## 👥 Group 7 Members

| No. | Name | Student ID |
|-----|------|------------|
| 1 | Muhammad Danish | 4332511020 |
| 2 | Arya Deva Bahri | 4332511021 |
| 3 | M Maulana Alpidie Deputra | 4332511017 |

---

## 📚 Course Information

- **Course**: Algorithms and Programming
- **Department**: Informatics Engineering
- **Study Program**: Cyber Security Engineering
- **Institution**: Politeknik Negeri Batam
- **Semester**: 1 (Odd Semester)
- **Academic Year**: 2025/2026

---

## 📄 License

This project was created for academic purposes as part of a Project-Based Learning assignment at Politeknik Negeri Batam.

---

<p align="center">
  <b>🔐 PyVault - Secure Your Digital Life 🔐</b>
</p>
