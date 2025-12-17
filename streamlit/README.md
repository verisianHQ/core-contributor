To view the dashboard, follow the steps below. Please note that if you've never run the setup script before, run that first.

1. In VSCode terminal, in the core-contributor directory, activate the virtual environment by running one of the following: \
    WINDOWS: `.\venv\Scripts\activate` \
    MAC: source `./venv/bin/activate`
2. If this is your first time trying to use the dashboard, run: \
    `pip install -r streamlit/requirements.txt` \
   - If you've run this command before, skip to 3
4. Run: \
  `streamlit run ./streamlit/app.py`

The dashboard should open automatically in your default browser! If it doesn't, paste the 'Local URL' link found in the terminal into your browser.
