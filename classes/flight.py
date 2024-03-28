from dataclasses import dataclass

@dataclass
class Flight:
    id: str        # Flight ID, e.g. "MU7208"
    airline: str   # "China Eastern Airlines"
    origin: str    # "YYZ"
    dest: str      # "PVG"
    o_lat: float   # Origin latitude
    o_lon: float   # Origin longitude
    d_lat: float   # Destination latitude
    d_lon: float   # Destination longitude
