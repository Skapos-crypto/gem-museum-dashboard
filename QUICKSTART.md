# Quick Start Guide

## Installation & Setup

1. **Install dependencies:**
```powershell
pip install -r requirements.txt
```

2. **Initialize the system:**
```powershell
python setup.py
```

## Running the Applications

### Visitor Web App
```powershell
streamlit run webapp/visitor_app.py
```
Access at: http://localhost:8501

### Staff Dashboard
```powershell
streamlit run dashboard/staff_dashboard.py --server.port=8502
```
Access at: http://localhost:8502

## Quick Test

1. Open visitor app (port 8501)
2. Fill in your information
3. Complete one or more surveys
4. Open staff dashboard (port 8502)
5. View analytics and data

## Common Commands

```powershell
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Reset database
Remove-Item visitor_feedback.db
python setup.py

# Run both apps (use two terminals)
# Terminal 1:
streamlit run webapp/visitor_app.py

# Terminal 2:
streamlit run dashboard/staff_dashboard.py --server.port=8502
```

## Troubleshooting

- **Port in use**: Change port with `--server.port=XXXX`
- **Import errors**: Run `pip install -r requirements.txt`
- **Database errors**: Run `python setup.py` to reinitialize
