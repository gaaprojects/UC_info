# 📄 Finance & Legal Digital Transformation — Project Intake Form

A modern **Streamlit application** that collects project intake data for Finance & Legal departments and automatically generates a professionally styled **PDF document** following a standardized template.

This tool replaces manual Word/PDF forms with an interactive, guided workflow and ensures all information is collected consistently.

---

## 🚀 Features

### ✅ Modern Form UI (Streamlit)
- Clean professional layout aligned with corporate green styling.
- Multi-step form with tabs for:
  1. **The Problem Space**
  2. **As-Is Workflow**
  3. **Solution & Compliance**
  4. **Attachments & Submission**
- Real-time conditional logic based on the selected use-case type.

### 🔍 Smart Use-Case–Based Questions
Depending on the selected solution type:
- **Power BI (Reporting / Dashboards)**
- **Power Automate (Automation / Workflow)**
- **AI / Machine Learning**
- **Power Apps (App / Front-end)**
- **Not sure yet**

Only the **relevant** follow-up questions are displayed.

### 🖨 Automatic PDF Generation
Generates a fully formatted intake PDF that includes:
- All major sections of the intake template  
- Guide boxes styled similar to the HTML version  
- Compliance information  
- Only the selected use-case–specific question block  
- A list of uploaded file names (files are not embedded)  

PDF is styled using fpdf2 to match your branding.

---

## 🛠 Technology Stack

| Component | Technology |
|----------|------------|
| User Interface | Streamlit |
| PDF Generator | fpdf2 |
| Language | Python 3.10+ |
| File Handling | Streamlit File Uploader |

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
