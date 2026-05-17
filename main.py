from fastapi import FastAPI,Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from weather import get_weather
import weather

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home(request: Request):

     return templates.TemplateResponse(
      request=request,  
      name="index.html",
      context={"weather": None}
   )


@app.post("/")
def get_weather_info(request: Request, city: str = Form(...)):

    weather_data = get_weather(city)

    return templates.TemplateResponse(
      request=request,  
      name="index.html",
      context={"weather": weather_data}
   )
