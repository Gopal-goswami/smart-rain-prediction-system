from fastapi import FastAPI,Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from nearby import get_nearby_points
from weather import get_weather, get_weather_by_coords
import weather
from prediction import predict_rain

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
    lat = weather_data["lat"]
    lon = weather_data["lon"]
    nearby_points = get_nearby_points(lat, lon)
    nearby_weather = [get_weather_by_coords(lat, lon) for lat, lon in nearby_points]
    rain_probability = predict_rain(weather_data, nearby_weather)
    weather_data["rain_probability"] = rain_probability

    return templates.TemplateResponse(
      request=request,  
      name="index.html",
      context={"weather": weather_data,"nearby_weather": nearby_weather}
   )
