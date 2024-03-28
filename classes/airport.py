from pyflightdata import FlightData
from typing import Optional, Any
from flight import Flight

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
        Raises an Exception if flight data can't be retrieved.

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
        try: self.elev = int(data["position"]["elevation"]["m"])
        except: assert "Sometimes elevation info is not available."
        self.country = data["position"]["country"]["name"]
        self.city = data["position"]["region"]["city"]
        self.tz = data["timezone"]["abbrName"]
        self.tz += f" (UTC{data["timezone"]["offset"]/3600:+.0f})"

        data = FlightData().get_airport_weather(code)
        if not data:
            raise Exception("Unable to get flight data.")
        self.temp = int(data["temp"]["celsius"])
        self.humid = int(data["humidity"])
        self.desc = data["sky"]["condition"]["text"]

    def objectify(self) -> dict[str, Any]:
        """
        Return a dictionary representation of Airport's attributes.

        >>> yyz = Airport("YYZ")
        >>> yyz.objectify()
        {
            "name": "Toronto Pearson International Airport",
            "code": "YYZ",
            "lat": 43.6771,
            "lon": 79.6334,
            ...
        }
        """
        return {
            i: getattr(self, i) for i in dir(self)
            if not i.startswith("__") and i != "objectify"
        }

    def get_flight_to(self, dest: "Airport") -> Flight:
        """
        Returns a single flight to the Airport 'dest'.

        Raises an Exception if flight data can't be retrieved.
        """
        data = FlightData().get_flights_from_to(self.code, dest.code)
        if not data:
            raise Exception("Unable to get flight data.")
        return Flight(
            data[-1]["identification"]["number"]["default"],
            data[-1]["airline"]["name"],
            self.code,
            dest.code,
            self.lat,
            self.lon,
            dest.lat,
            dest.lon
        )
