from pyflightdata import FlightData
from typing import Optional

class Airport:
    name: str      # "Toronto Pearson International Airport"
    code: str      # "YYZ"
    lat: float     # 43.6771
    lon: float     # 79.6334
    elev: int      # Elevation in meters
    country: str   # "Canada"
    city: str      # "Toronto"
    tz: str        # "Eastern Daylight Time (UTC-4)"
    temp: int      # Temperature in celsius
    humid: int     # Relative humidity
    desc: str      # A text description of weather, e.g. "Overcast"
    text: str      # Optional text to show upon hover in the map

    def __init__(self, code: str, text: Optional[str] = "") -> None:
        """
        Initialize an Airport with the given IATA airport code.
        Attributes will be filled in automatically using pyflightdata.
        To show text on hover in the map, pass it in as 'text'.

        Raises NameError if the given IATA airport code is invalid.

        >>> yyz = Airport("YYZ", "This is Toronto, the largest...")
        >>> yyz.country
        "Canada"
        """
        data = FlightData().get_airport_details(code)
        if not data:
            raise NameError("Invalid IATA airport code")

        self.text = text
        self.name = data["name"]
        self.code = data["code"]["iata"]
        self.lat = data["position"]["latitude"]
        self.lon = data["position"]["longitude"]
        self.elev = int(data["position"]["elevation"]["m"])
        self.country = data["position"]["country"]["name"]
        self.city = data["position"]["region"]["city"]
        self.tz = data["timezone"]["abbrName"]
        self.tz += f" (UTC{data["timezone"]["offset"]/3600:+.0f})"

        data = FlightData().get_airport_weather(code)
        self.temp = int(data["temp"]["celsius"])
        self.humid = int(data["humidity"])
        self.desc = data["sky"]["condition"]["text"]

    ## Maybe
    density: None # Population density
    traffic: None # How busy is the airport
    type:    None # International, domestic, or regional
