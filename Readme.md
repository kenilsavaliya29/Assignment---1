# Insurance Claim Management System

This is a simple web application built with Flask for managing insurance policyholders and claims. It includes features for adding/viewing policyholders and claims, updating claim statuses, performing basic risk analysis, and generating reports.

## Setup Instructions

Follow these steps to set up and run the project on your local machine.

### Prerequisites

*   Python 3.6+ installed

### 1. Clone the repository (if applicable)

If you have the project in a repository, clone it to your local machine.

```bash
# Example: git clone <repository_url>
```

If you already have the project files, navigate to the project directory in your terminal.

### 2. Set up a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

#### For macOS/Linux Users

```bash
python3 -m venv venv
source venv/bin/activate
```

#### For Windows Users

```bash
python -m venv venv
venv\Scripts\activate
```

(The terminal prompt should now show `(venv)` at the beginning, indicating the virtual environment is active.)

### 3. Install Dependencies

With the virtual environment activated, install the required libraries using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Run the Application

Execute the main application file to start the Flask development server.

```bash
python app.py
```

The application will typically run on `http://127.0.0.1:5000/` or `http://localhost:5000/`. Open your web browser and navigate to this address.

## Project Structure

*   `app.py`: The main Flask application file, handling routes and views.
*   `insurance_system.py`: Contains the core logic for managing policyholders, claims, risk analysis, and reports.
*   `data/`: Directory where application data (policyholders and claims) is stored in JSON files.
*   `templates/`: Contains HTML templates for rendering web pages.
*   `requirements.txt`: Lists the project dependencies (Flask).
*   `Readme.md`: This file, providing setup and running instructions.

## Features

*   Add, view, and list policyholders.
*   Add, view, and list claims.
*   Update claim statuses (with validation against sum insured).
*   Basic risk analysis (high-risk policyholders, claims by policy type).
*   Generate reports (monthly claims, average claim amount, highest claim, policyholders with pending claims).
*   Basic API endpoints for policyholders and claims.