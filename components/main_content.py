from dash import html
from components import track_tabs


layout = html.Div(
  children=[
      html.Div(
          children=[
              html.H1(
                children=[
                    "Interactive Coure Catalog Visualization",
                ],
                style={
                  "background-image": "linear-gradient(to right, #f12711, #a562f8)",
                  "font-size": "3.5rem",
                  "color": "transparent",
                  "background-clip": "text",
                }
              ),
          ],
            style={
                "height": "10vh",
            }
      ),
      track_tabs.card,
  ],
  style={
    "position": "relative",
    "width": "100%",
    "margin": "1.2rem",
    "margin-right": "2.4rem",
  }
)