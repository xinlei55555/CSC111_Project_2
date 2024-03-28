import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pyflightdata import FlightData
from airport import Airport
from flight import Flight

class Frontend:
    airports: list[Airport]
    flights: list[Flight]

    # def __init__(self, airports: list[Airport]) -> None:
    #     self.airports = airports

    def __init__(self, origin: str, dest: str) -> None:
        """
        Initialize a frontend UI rendered by plotly.
        Displays flights from 'origin' to 'dest' IATA codes.

        Raises an Exception if flight data can't be retrieved.
        """
        self.airports = [Airport(origin), Airport(dest)]
        self.flights = [self.airports[0].get_flight_to(self.airports[1])]

    def plot(self) -> None:
        """
        TODO WORK IN PROGRESS
        """
        # Don't know pandas, don't mind this mess
        airpandas = pd.DataFrame(map(Airport.objectify, self.airports))
        print(airpandas)

        fig = px.scatter_mapbox(
            airpandas, lat="lat", lon="lon",
            hover_name="city"
        )

        for i in self.flights:
            fig.add_trace(go.Scattermapbox(
                mode="markers+lines",
                lat=[i.o_lat, i.d_lat],
                lon=[i.o_lon, i.d_lon],
                marker={'size':10},
                hovertext=i.airline
            ))



        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.show()

if __name__ == "__main__":
    f = Frontend("YYZ", "JFK")
    print(f.airports, f.flights)
    f.plot()
