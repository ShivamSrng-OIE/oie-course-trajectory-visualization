from time import sleep
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from consts import CourseTrajectoryConsts
from src.utils.gemini_interfacing import GeminiInterfacing 
from src.generate_3d_graph import Generate3DGraph
from dash import Input, Output, html, callback, State
from src.utils.database_handler import DatabaseHandler
from src.student_interaction import StudentInteraction


database_handler = DatabaseHandler()
gemini_interfacing = GeminiInterfacing()
student_interaction = StudentInteraction(
  gemini_interfacing=gemini_interfacing
)

card = html.Div(
  children=[
    dbc.Card(
      [
        dbc.CardHeader(
          dbc.Tabs(
            id="card-tabs",
            active_tab="track_1",
            persistence=True,
            persistence_type="session",
          ),
          id="card-header",
          style={
            "background": "#131314",
            "border-bottom": "1px solid white",
          }
        ),
        dbc.CardBody(
          id="card-content",
          style={
            "height": "100%",
          }
        ),
      ],
      style={
        "width": "100%",
        "height": "85vh",
        "background": "#1E1F20",
        "border": "1px solid #131314",
        "border-radius": "1.2rem",
        "transition": "0.5s linear",
      }
    ),
    html.Div(
      children=[
        html.P(
          children=[
            "© 2024 by ",
            html.Span(
              children=["New Jersey Institute of Technology"],
              style={
                "background-image": "linear-gradient(to right, #f12711, #a562f8)",
                "color": "transparent",
                "background-clip": "text",
              },
            ),
          ],
          style={
            "color": "white",
          }
        ),
        html.P(
          children=[
            "Developed by ",
            html.Span(
              children=["Office of Institutional Effectiveness"],
              style={
                "background-image": "linear-gradient(to right, #f12711, #a562f8)",
                "color": "transparent",
                "background-clip": "text",
              },
            ),
          ],
          style={
            "color": "white",
          }
        )
      ],
      style={
        "position": "relative",
        "display": "flex",
        "flexDirection": "row",
        "justifyContent": "space-between",
        "bottom": "0",
        "width": "100%",
        "textAlign": "center",
      }
    )
  ],
)
  
last_camera_position = None
last_click_data = None
original_fig = None
chat_history = []

@callback(
    Output("modal-fs", "is_open"),
    Input("open-fs", "n_clicks"),
    State("modal-fs", "is_open"),
)
def toggle_modal(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
  Output("card-tabs", "children"),
  Output("card-content", "children"),
  Input("card-tabs", "active_tab"),
  Input("course-catalog-store", "data"),
)
def update_tab_content(active_tab, course_catalog):
  if course_catalog is not None:
    dict_tabs_cnt = database_handler.get_tracks_count_per_course()
    global last_camera_position
    last_camera_position = None
    
    if int(active_tab.split("_")[-1]) > dict_tabs_cnt[course_catalog]:
      active_tab = "track_1"
      
    all_tracks_information = database_handler.get_course_track_information(
      course_name=course_catalog
    )
    
    course_catalog_info = database_handler.get_course_catalog_information(
      course_name=course_catalog
    )

    interactive_3d_graph_obj = Generate3DGraph(
      course_name=course_catalog,
      course_catalog=course_catalog_info,
      all_tracks_course_information=all_tracks_information
    )
    
    interactive_3d_graph = interactive_3d_graph_obj.run(
      track=active_tab,
    )
    
    return [
      [
        dbc.Tab(
          label=f"Track {i}",
          tab_id=f"track_{i}",
          label_style={
            "color": "gray",
            "transition": "0.5s linear",
            "opacity": "0.5",
          },
          active_label_style={
            "background-image": "linear-gradient(to right, #f12711, #a562f8)",
            "color": "transparent",
            "background-clip": "text",
            "opacity": "1",
          },
        )
        for i in range(1, dict_tabs_cnt[course_catalog] + 1)
      ],
        interactive_3d_graph,
    ]


course_trajectory_consts = CourseTrajectoryConsts().get_course_trajectory_consts()
color_for_corequisites = course_trajectory_consts["color_for_corequisites"]
color_for_prerequisites = course_trajectory_consts["color_for_prerequisites"]


@callback(
  Output("user-input", "value"),
  Output("send-chat-button", "n_clicks"),
  Output("conversation-area", "children"),
  Output('click-count', 'data'),
  Output('3d_course_graph', 'figure'),
  
  Input('3d_course_graph', 'clickData'),
  Input('3d_course_graph', 'figure'),
  Input('click-count', 'data'),
  State("camera", "data"),

  # Data about course catalog name, active tab
  State("course-catalog-store", "data"),
  Input("card-tabs", "active_tab"),
  
  # Chatbot data
  Input("user-input", "value"),
  Input("send-chat-button", "n_clicks"),
  State("conversation-area", "children"),
)
def update_figure(clickData, fig, click_count, camera_data, course_catalog, active_tab, chatbot_input, chatbot_send_clicks, chat_history):
  global last_click_data
  global original_fig

  if chatbot_send_clicks and chatbot_send_clicks > 0 and chatbot_input is not None and chatbot_input != "":
    all_tracks_information = database_handler.get_course_track_information(
      course_name=course_catalog
    )
    
    course_catalog_info = database_handler.get_course_catalog_information(
      course_name=course_catalog
    )

    chat_history.append(
      html.Div(
        children=[
          chatbot_input,
          html.Img(
            src="assets/images/student.png",
            style={
              "margin-left": "0.5rem",
              "width": "10%",
              "height": "10%",
              "border-radius": "50%",
            }
          ),
        ],
        style={
          "display": "flex",
          "flex-direction": "row",
          "justify-content": "flex-end",
          "text-align": "right",
          "color": "white",
          "margin": "0.5rem",
          "margin-top": "1.5rem",
        }
      ),
    )

    new_fig, complete_path_sorted, gemini_response = student_interaction.start_interaction(
      track=active_tab,
      initial_interaction=chatbot_input,
      course_catalog_name=course_catalog,
      course_catalog_info=course_catalog_info,
      last_camera_position=last_camera_position,
      all_tracks_information=all_tracks_information
    )
    if new_fig is not None:
      fig = go.Figure(new_fig)
      result = [gemini_response]
      result.extend(complete_path_sorted)
      gemini_response = html.Div(
        children=[
          html.P(
            children=result,
            style={
              "color": "white",
            }
          )
        ]
      )
    elif new_fig is None and len(complete_path_sorted) > 0:
      result = [gemini_response]
      result.extend(complete_path_sorted)
      gemini_response = html.Div(
        children=[
          html.P(
            children=result,
            style={
              "color": "white",
            }
          )
        ]
      )
    
    chat_history.append(
      html.Div(
        children=[
          html.Img(
            src="assets/images/njit.png",
            style={
              "width": "10%",
              "height": "10%",
              "border-radius": "50%",
              "margin-right": "0.5rem",
            }
          ),
          gemini_response 
        ],
        style={
          "display": "flex",
          "flexDirection": "row",
          "justifyContent": "flex-start",
          "color": "white",
          "margin": "0.5rem",
          "margin-top": "1.5rem",
        }
      )
    )
    
      
    return "", 0, [
      html.Div(
        children=chat_history,
      )
    ], click_count, fig
  
  if clickData is None:
    original_fig = fig
  
  last_click_data = clickData
  fig, click_count = highlight_course_node(clickData, fig, click_count, camera_data)
  return chatbot_input, chatbot_send_clicks, chat_history, click_count, fig


@callback(
  Output("camera", "data"),
  Input("3d_course_graph", "relayoutData"),
)
def store_camera_position(relayoutData):
  if relayoutData is not None:
    global last_camera_position
    if "scene.camera" in relayoutData:
      last_camera_position = relayoutData["scene.camera"]
      return relayoutData["scene.camera"]


def highlight_course_node(clickData, fig, click_count, camera_data):
    if clickData:
      sleep(0.5)
      custom_data = clickData['points'][0]['customdata']
      if custom_data not in click_count:
        click_count[custom_data] = 0
      
      click_count[custom_data] += 1

      for i in range(len(fig["data"])):
        if "customdata" in fig["data"][i]:
          if fig["data"][i]["customdata"][0] == custom_data and click_count[custom_data] % 2 == 1:
            fig["data"][i]["marker"]["color"] = "blue"
            for j in range(len(fig["data"])):
              if "customdata" in fig["data"][j] and "edge" in fig["data"][j]["customdata"][0]:
                node_edge_custom_data = fig["data"][j]["customdata"][0].split("_")[-1]
                pre_or_coreq = fig["data"][j]["customdata"][0].split("_")[1]
                if node_edge_custom_data == custom_data:
                  fig["data"][j]["visible"] = True
                  fig["data"][j]["line"]["width"] = 10
                  if pre_or_coreq == "pre":
                    fig["data"][j]["line"]["color"] = color_for_prerequisites
                  else:
                    fig["data"][j]["line"]["color"] = color_for_corequisites
            break

          elif fig["data"][i]["customdata"][0] == custom_data and click_count[custom_data] % 2 == 0:
            fig["data"][i]["marker"]["color"] = "gray"
            for j in range(len(fig["data"])):
              if "customdata" in fig["data"][j] and "edge" in fig["data"][j]["customdata"][0]:
                node_edge_custom_data = fig["data"][j]["customdata"][0].split("_")[-1]
                pre_or_coreq = fig["data"][j]["customdata"][0].split("_")[1]
                if node_edge_custom_data == custom_data:
                  fig["data"][j]["visible"] = False
                  fig["data"][j]["line"]["width"] = 0
                  fig["data"][j]["line"]["color"] = "gray"
            break
      
      fig["layout"]["scene"]["camera"] = last_camera_position
      return fig, click_count

    fig["layout"]["scene"]["camera"] = last_camera_position
    return fig, click_count