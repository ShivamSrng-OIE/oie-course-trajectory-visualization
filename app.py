from dash import Dash, html, dcc
from components import sidebar, main_content
import dash_bootstrap_components as dbc


DEFAULT_COURSE_CATALOG = "computer_engineering"


app = Dash(
  name=__name__,
  title="OIE Course Catalog Visualization",
  update_title="OIE Processing...",
  suppress_callback_exceptions=True,
  external_stylesheets=[
    dbc.themes.BOOTSTRAP
  ],
)
app._favicon = ("icon/njit.ico")

app.layout = html.Div(
  [
    sidebar.layout,
    main_content.layout,
    dcc.Store(id="course-catalog-store", data="", storage_type="session"),
  ],
  className="indexpage-main-layout",
)


if __name__ == "__main__":
  app.run(debug=True)