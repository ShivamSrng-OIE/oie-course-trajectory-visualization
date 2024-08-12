from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from components import sidebar, main_content


# Createing the Dash application with the name of the app, title, update title, external stylesheets, and suppress callback exceptions
app = Dash(
  name=__name__,
  title="OIE Course Catalog Visualization",
  update_title="OIE Processing...",
  suppress_callback_exceptions=True,
  external_stylesheets=[
    dbc.themes.BOOTSTRAP
  ],
)

# Setting the favicon for the app as the NJIT logo
app._favicon = (
  "icon/njit.ico"
)

server = app.server


app.layout = html.Div(
  [
    sidebar.layout,
    main_content.layout,
    dcc.Store(id="course-catalog-store", data="", storage_type="session"),
  ],
  className="indexpage-main-layout",
)

if __name__ == "__main__":
  # Running the app with debug mode off
  app.run(
    debug=False,
  )