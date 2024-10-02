# PensionApp
This program simplifies pension planning by using a few key financial details from the user to estimate their pension income at a chosen retirement age. Its goal is to help users make informed decisions about their current pension contributions and ensure they are on track for a secure retirement.

## Directory Contents
- `README.md` Instructions
- `requirements.txt` Python dependencies
#### Application Files
- `main.py`
- `financial_calculations.py`
- `take_home_income_components.py`
- `visualisation_elements.py`
#### Testing
- `testing.py`

## Requirements
- Python 3.10

## Launch Instructions
1. Navigate your current working directory to directory of this readme
2. Install python requirements
`pip install -r requirements.txt`
3. Launch application using `python -m streamlit run main.py`. The application by default will listen by default on port `8501`, this can be changed if required by running with the additional argument `--server.port=X`. 
4. View application by navigating a web browser to http://localhost:8501/

### Virtual Environment Helper
Running this application in a virtual environment is not required, but is advisable to reduce the risk of clashing dependencies in the existing python install. Example setup using `virtualenv`:
1. Navigate you current working directory to the directory of this file
2. Create a new virtual environment `python -m virtualenv ./venv`
3. Activate environment `source venv/bin/activate`
4. Follow 'Launch Instructions' from the current terminal
