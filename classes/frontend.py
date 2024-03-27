import pandas as pd
import plotly.express as px
from airport import Airport

class Frontend:
    airports: list[Airport]

    def __init__(self, airports: list[Airport]) -> None:
        self.airports = airports

    def plot(self) -> None:
        # Don't know pandas, don't mind this mess
        airpandas = pd.DataFrame(map(Airport.objectify, self.airports))
        print(airpandas)

        fig = px.scatter_mapbox(
            airpandas, lat="lat", lon="lon",
            hover_name="city"
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.show()

## Test
f = Frontend([Airport("YYZ")])
f.plot()