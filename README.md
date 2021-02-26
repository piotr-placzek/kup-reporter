# First install
Based on Python 3.9.1.
```
python -m venv venv
activate.bat
pip install -r requirements.txt
deactivate.bat
```

# Generate report
## Preparations
Prepare configuration file `config/default.py` by filling all required fields, or just pass all parameters in a command line.

### Password
Password is an individual JIRA token.
Token can be generated on a user profile `https://id.atlassian.com/manage-profile/security/api-tokens`

## Generate
### With predefined configuration file
```
activate.bat
python main.py
deactivate.bat
```

### With parameters (or combined with configuration)
```
activate.bat
python main.py -s http://address -u username -p password ...
deactivate.bat
```
All parameters can be found under command `python main.py -h`, after entering vevn.
