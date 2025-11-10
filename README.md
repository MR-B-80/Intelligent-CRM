# 🏢 Intelligent CRM

![GitHub stars](https://img.shields.io/github/stars/MR-B-80/Intelligent-CRM.svg?style=social)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build Status](https://img.shields.io/badge/Build-Development-brightgreen)

A lightweight yet powerful **Customer Relationship Management (CRM)** system built with **Django**. This project helps sales teams and businesses efficiently manage customer information, track call records, and gain **AI-powered insights** for better decision-decision making.

---

## 📝 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Contributing](#-contributing)
- [Roadmap](#-roadmap)
- [License](#-license)
- [Contact](#-contact)

---

## ✨ Features

- **User Authentication & Authorization**

  - Secure login & signup
  - Django Admin panel for user & record management

- **Customer Management**

  - Add, edit, and delete customer records
  - View detailed customer profiles
  - Track customer interaction history

- **Call Records**

  - Log and store customer calls
  - Summarize key conversation points

- **AI-Powered Suggestions**

  - Integration with **Google Gemini API**
  - Automatically generates conversation summaries
  - Provides strategic recommendations for next sales steps

- **Responsive UI**
  - Sidebar navigation
  - Bootstrap 5 modals & DataTables for smooth UX

---

## ⚙️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** Bootstrap 5
- **Database:** MySQL (configurable)
- **AI Integration:** Google Gemini API

---

## 🚀 Installation

Follow these steps to set up the project locally.

### Prerequisites

Make sure you have the following installed:

- Python 3.8+
- pip (Python package installer)
- Git

### Steps

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/Intelligent-CRM.git
    cd Intelligent-CRM
    ```

2.  **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    _Note: A `requirements.txt` file should be created in the project root containing all Python dependencies._

4.  **Database Setup:**
    This project uses MySQL by default. Ensure you have a MySQL server running and create a database.

    Update your database settings in `dcrm/settings.py`:

    ```python
    # dcrm/settings.py
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'your_database_name',
            'USER': 'your_database_user',
            'PASSWORD': 'your_database_password',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
    ```

5.  **Apply migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Create a superuser (for Django Admin access):**

    ```bash
    python manage.py createsuperuser
    ```

    Follow the prompts to create your admin user.

7.  **Set up Google Gemini API (for AI-powered suggestions):**
    Obtain an API key from Google Cloud Console. Then, add it to your project's settings or environment variables.

    ```python
    # dcrm/settings.py or a local_settings.py file
    GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
    ```

---

## 💡 Usage

1.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

2.  **Access the application:**

    Open your web browser and navigate to `http://127.0.0.1:8000/`.

3.  **Access the Django Admin panel:**

    Navigate to `http://127.0.0.1:8000/admin/` and log in with the superuser credentials you created.

### Example Interaction (Conceptual)

Imagine adding a new customer:

1.  Log in to the CRM.
2.  Navigate to the "Customers" section.
3.  Click "Add New Customer".
4.  Fill in customer details (name, email, phone, etc.) and save.

Upon saving, the system might leverage the Gemini API to suggest initial engagement strategies based on the customer's profile, if such integration is enabled and configured.

---

## 🤝 Contributing

We welcome contributions to the Intelligent CRM project! To contribute:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Make your changes and commit them (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/YourFeature`).
5.  Open a Pull Request.

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

---

## 📊 Roadmap

Our future plans for the Intelligent CRM include:

- Email & SMS integration
- User profile & settings management
- Messages & Alerts system
- Advanced analytics dashboard
- Enhanced team collaboration features
- Integration with more AI services

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ✉️ Contact

For any questions or suggestions, please reach out to:

- **GitHub:** [https://github.com/MR-B-80]
