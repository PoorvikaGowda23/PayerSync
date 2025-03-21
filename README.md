
# 🦷 Dental Insurance Payer Processing System 🚀

This project is a Flask-based web application designed to process and manage dental insurance payer data from Excel files. It includes features for uploading data, mapping payers, setting display names, and managing payer hierarchies.

---

## 📂 Project Structure
```
├── app.py                        # Main Flask application
├── mapping.py                    # Data processing and mapping logic
├── models.py                     # Database models
├── requirements.txt              # Python dependencies
├── templates/                    # HTML templates
│ ├── base.html                   # Base template
│ ├── index.html                  # Home page with file upload
│ ├── admin_mapping.html          # Manual mapping interface
│ ├── admin_pretty_names.html     # Pretty names interface
│ ├── admin_hierarchy.html        # Hierarchy management interface
│ ├── payer_groups.html           # Payer groups display
│ └── payer_details.html          # Payer details display
└── static/ # Static files (CSS, JS)
```

---

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Steps to Set Up the Project

1. **Clone the repository:**
   
2. **Create a virtual environment:**
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. **Install dependencies:**
```sh
pip install -r requirements.txt
```

4. **Set up the database:**

5. **Run the application:**
```sh
python app.py
```
Visit **`http://127.0.0.1:5000/`** in your browser.

## 🐛 Routes
| Route                 | Description |
|-----------------------|-------------|
| `/`                   | Upload and process files |
| `/payer-groups`       | View payer groups |
| `/payer/<id>`         | View payer details |
| `/admin/mapping`      | Map raw names to payers |
| `/admin/pretty_names` | Assign display names |
| `/admin/hierarchy`    | Manage payer groups |

## 🌟 Features

- **📤 Upload Excel Files**
  - Upload Excel files containing payer data from multiple sources.
  - The system processes the data and populates the database automatically.
- **🗺️ Manual Mapping**
  - Manually map payer details to payers using the "Manual Mapping" interface.
- **🖋️ Set Pretty Names**
  - Set custom display names for payers in the "Pretty Names" section.
- **🌳 Manage Hierarchy**
  - Assign payers to payer groups in the "Manage Hierarchy" section.
- **📊 View Payer Groups**
  - Explore payer groups and their details in the "Payer Groups" section.
 
## 🛠 Tech Stack

- **Backend:** Flask, Flask-WTF (Forms), Flask-SQLAlchemy
- **Database:** SQLite
- **Frontend:** HTML, CSS, Jinja2 templates
- **Libraries:** Pandas (for Excel processing), difflib (for string similarity matching)


## 📝 Usage
### 1. Upload Data
- Navigate to the home page and upload an Excel file containing payer data.
- The system will process the data and populate the database.
### 2. Manual Mapping
- Go to the "Manual Mapping" section to map payer details to payers manually.
### 3. Set Pretty Names
- Use the "Pretty Names" section to set display names for payers.
### 4. Manage Hierarchy
- Assign payers to groups in the "Manage Hierarchy" section.
### 5. View Payer Groups
- Explore payer groups and their details in the "Payer Groups" section.

## 🧩 Code Overview
### app.py
- The main Flask application file.
- Contains routes for handling file uploads, payer mapping, pretty names, and hierarchy management.
### models.py
- Defines the database models using SQLAlchemy.
- Includes PayerGroup, Payer, and PayerDetail models.
### mapping.py
- Handles the processing of Excel data.
- Uses semantic matching to map payer details to payers.
### templates/
- Contains HTML templates for rendering the web pages.
### requirements.txt
- Lists all Python dependencies required for the project.

## 🛠️ Development
### Running in Debug Mode
- To run the application in debug mode, use:
```
bash
python app.py
```
- Debug mode allows for automatic reloading of the application when changes are made.
### Database Management
- The application uses SQLite for the database.
- The database is initialized automatically when the application is first run.
### Adding New Features
- To add new features, create new routes in app.py and corresponding templates in the templates/ folder.
- Update the database models in models.py if necessary.
