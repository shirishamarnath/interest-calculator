from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from calculator import calculate_interest

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/calculate", response_class=HTMLResponse)
def calculate(
    request: Request,
    given_date: str = Form(...),
    release_date: str = Form(...),
    amount: float = Form(...),
    additional_interest: int = Form(0)
):
    result = calculate_interest(
        given_date,
        release_date,
        amount,
        additional_interest
    )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result,
            "given_date": given_date,
            "release_date": release_date,
            "amount": amount,
            "additional_interest": additional_interest
        }
    )
