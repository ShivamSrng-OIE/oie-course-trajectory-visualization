import os
from dash import dcc, html, Input, Output, callback


layout = html.Div(
  [
    html.Div(
      html.Img(
        src="assets/images/njit_logo.png",
        style={
          "height": "60%",
        }
      ),
      style={
        "display": "flex",
        "margin-horizontal": "1.2rem",
        "align-items": "center",
        "justify-content": "center",
      }
    ),
    html.P(
      "Select a course catalog",
      style={
        "color": "white",
        "margin": "1.2rem",
        "margin-bottom": "1rem",
      }
    ),
    html.Div(
      children=[
        dcc.Dropdown(
          id="course-catalog-dropdown",
          options=[{"label": course_name.replace("_", " ").title(), "value": course_name} for course_name in os.listdir("data")],
          value="computer_engineering",
          persistence=True,
          clearable=False,
          searchable=False,
          style={
            "width": "100%",
          },
        ),
      ],
      style={
        "height": "100vh",
        "margin": "1.2rem",
        "margin-top": "0rem",
        "display": "flex", 
        "flexDirection": "column",
      }
    ),
  ],
  style={
    "width": "15%",
    "height": "100vh",
    "padding": "0rem",
    "margin": "0rem",
    "display": "flex",
    "flexDirection": "column",
    "marginRight": "1rem",
    "position": "relative",
    "background": "#1E1F20",
    "border-right": "1px solid #313131",
    "border-top-right-radius": "1.2rem",
    "border-bottom-right-radius": "1.2rem",
  },
)


@callback(
  Output('course-catalog-store', 'data'),
  Input('course-catalog-dropdown', 'value')
)
def update_course_catalog(value):
  return value