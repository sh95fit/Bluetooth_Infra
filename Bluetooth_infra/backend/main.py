from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def main():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bluetooth Infra</title>
    </head>
    <body>
        <h1>Welcome to Bluetooth Infra</h1>
        <p>This is bluetooth infra main page.</p>
    </body>
    </html>
    """
