. .\venv\Scripts\activate.ps1

$env:FLASK_APP="app.py"
$env:FLASK_DEBUG=1
$env:FLASK_ENV="development"

flask run