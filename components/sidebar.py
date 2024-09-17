import dash_bootstrap_components as dbc 
from dash import dcc, html, Input, Output, callback, callback_context, no_update, ALL

global selected_college 
global selected_college_department

colleges_departments = {
  "Hillier College Of Architecture And Design": {
    "New Jersey School of Architecture": {
      "Architecture - B.S.": "architecture_bs",
      "Architecture - B.Arch.": "architecture",
    },
    "School of Art and Design": {
      "Digital Design": "digital_design",
      "Industrial Design": "industrial_design",
      "Interior Design": "interior_design",
    },
  },
  "Ying Wu College Of Computing": {
    "Computer Science": {
      "Computer Science - B.S.": "computer_science",
      "Computer Science - B.A.": "computer_science_ba",
      "Double Majors in B.S. in Computer Science and B.S. in Applied Physics": "bs_in_computer_science_and_bs_in_applied_physics",
      "Double Majors in B.S. in Computer Science and B.S. in Mathematical Sciences, Applied Mathematics": "bs_in_computer_science_and_bs_in_mathematical_sciences_applied_mathematics",
      "Double Majors in BS in Computer Science and BS in Mathematical Sciences, Computational Mathematics": "bs_in_computer_science_and_bs_in_mathematical_sciences_computational_mathematics"
    },
    "Informatics": {
      "Business & Information Systems - B.S.": "business_and_information_systems",
      "Human-Computer Interaction - B.S.": "human_computer_interaction_bs",
      "Information Systems - B.A.": "information_systems_ba",
      "Information Technology - B.S.": "information_technology_bs",
      "Web & Information Systems - B.S.": "web_and_information_systems",
      "Double Majors in B.S. in Science, Technology & Society and B.S. in Business and Information Systems": "bs_in_science_technology_&_society_and_bs_in_business_and_information_systems"
    },
    "Data Science": {
      "Data Science (Computing Option) - B.S.": "data_science_bs_cosla",
    },
  },
  "College Of Science And Liberal Arts": {
    "Aerospace Studies": {},
    "Biological Sciences": {
      "Biology - B.A.": "biology_ba",
      "Biology - B.S.": "biology_bs",
      "Accelerated Biology - B.A./M.D.": "accelerated_ba_in_biology/md",
      "Accelerated Biology - B.A./D.M.D., O.D.": "accelerated_ba_in_biology/dmd_od",
      "Accelerated Biology - B. A. in Biology/Doctor in Physical Therapy (DPT) - Ph.D.": "accelerated_ba_in_biology/doctor_in_physical_therapy",
      "Accelerated Biology - B.A./Physician Assistant": "accelerated_ba_in_biology/physician_assistant",
      "Double Majors in Biology and Mathematical Sciences - B.S.": "double_major_in_biology_&_mathematical_sciences",
      "Double Majors in Biology & Law, Technology and Culture - B.A": "biology_&_law_technology_and_culture_ba",
    },
    "Chemistry and Environmental Science": {
      "Biochemistry - B.S.": "biochemistry_bs",
      "Chemistry - B.S.": "chemistry_bs",
      "Environmental Science - B.S.": "environmental_science_bs",
      "Forensic Science - B.S.": "forensic_science_bs",
      "Double Majors in Forensic Science & Law, Technology and Culture - B.S": "forensic_science_&_law_technology_and_culture_bs",
      "Double Majors in Chemistry & Law, Technology and Culture - B.S": "chemistry_&_law_technology_and_culture_bs",
    },
    "Mathematical Sciences": {
      "Data Science (Statistics Option) - B.S.": "data_science_bs",
      "Mathematical Sciences - B.S. with Applied Mathematics Concentration": "mathematical_sciences_with_applied_mathematics_concentration",
      "Mathematical Sciences - B.S. with Applied Statistics Concentration": "mathematical_sciences_with_applied_statistics_and_data_analysis_concentration",
      "Mathematical Sciences - B.S. with Computational Mathematics Concentration": "mathematical_sciences_with_computational_mathematics_concentration",
      "Mathematical Sciences - B.S. with Mathematical Biology Concentration": "mathematical_sciences_with_mathematical_biology_concentration",
      "Mathematical Sciences - B.S. with Mathematics of Finance and Acturial Science Concentration": "mathematical_sciences_with_mathematics_of_finance_and_actuarial_science_concentration",
      "Accelerated Mathematical Sciences - B.S./M.D., D.M.D., D.D.S., O.D.": "accelerated_bachelor_of_science_in_mathematical_sciences_for_md_dmd_dds_od",
      "Double Majors in Applied Physics & Mathematical Sciences with Applied Mathematics Concentration - B.S.": "bs_in_applied_physics_&_bs_in_mathematical_sciences_applied_mathematics",
      "Double Majors in Biology and Mathematical Sciences - B.S.": "biology_&_mathematical_sciences",
      "Double Majors in Computer Science & Mathematical Sciences with Computational Mathematics Concentration - B.S.": "bs_in_computer_science_and_bs_in_mathematical_sciences_computational_mathematics",
      "Double Majors in Computer Science and Applied Mathematics - B.S.": "bs_in_computer_science_and_bs_in_mathematical_sciences_applied_mathematics"
    },
    "History": {
      "History - B.A.": "history_ba",
      "Law, Technology and Culture - B.A.": "law_technology_and_culture_ba",
      "Law, Technology and Culture (Patent Law Concentration) - B.A.": "law_technology_and_culture_patent_law_concentration_ba",
      "Accelerated History - B.A. /D.P.T.": "accelerated_ba_in_history/dpt", 
      "Accelerated History - B.A./J.D.": "accelerated_ba_in_history/jd",
      "Accelerated History - B.A./M.D.": "accelerated_ba_in_history/md",
      "Accelerated History - B.A./ D.M.D., D.D.S., O.D.": "accelerated_ba_in_history/dmd_dds_od",
      "Accelerated Law, Technology and Culture - B.A./J.D.": "accelerated_law_technology_and_culture/jd",
      "Double Majors in Biology & Law, Technology and Culture - B.A.": "biology_&_law_technology_and_culture_ba",
      "Double Majors in Chemistry & Law, Technology and Culture - B.S.": "chemistry_&_law_technology_and_culture_bs",
      "Double Majors in Forensic Science & Law, Technology and Culture - B.S": "forensic_science_&_law_technology_and_culture_bs",
      "Double Majors in Physics & Law, Technology and Culture - Astronomy Option - B.S.": "physics_&_law_technology_and_culture_astronomy_option_bs",
      "Double Majors in Physics & Law, Technology and Culture - Optical Science & Engineering Option - B.S.": "physics_&_law_technology_and_culture_optical_science_&_engineering_option_bs",
    },
    "Humanities and Social Sciences": {
      "Communication and Media - B.A.": "communication_and_media_ba",
      "Communication and Media - B.S.": "communication_and_media_bs",
      "Law, Technology and Culture": "law_technology_and_culture_ba",
      "Science, Technology and Society": "science_technology_and_society_bs",
      "Environmental Science": "environmental_science_bs",
      "Theatre Arts and Technology": "theatre_arts_and_technology_ba",
      "B.S. in Science, Technology & Society and B.S. in Business and Information Systems": "science_technology_society_business_information_systems_bs"
    },
    "Physics": {
      "Applied Physics - B.S.": "applied_physics_bs",
      "Double Majors in Applied Physics & Mathematical Sciences with Applied Mathematics Concentration - B.S.": "bs_in_applied_physics_&_bs_in_mathematical_sciences_applied_mathematics",
      "Double Majors in Computer Science and Applied Physics - B.S.": "bs_in_computer_science_and_bs_in_applied_physics",
      "Double Majors in Physics & Law, Technology and Culture - Astronomy Option - B.S.": "physics_&_law_technology_and_culture_astronomy_option_bs",
      "Double Majors in Physics & Law, Technology and Culture - Optical Science & Engineering Option - B.S.": "physics_&_law_technology_and_culture_optical_science_&_engineering_option_bs"
    },
    "Interdisciplinary Programs": {
      "Communication and Media - B.A.": "communication_and_media_ba",
      "Communication and Media - B.S.": "communication_and_media_bs",
      "Law, Technology and Culture": "law_technology_and_culture_ba",
      "Science, Technology and Society": "science_technology_and_society_bs",
      "Environmental Science": "environmental_science_bs",
      "Theatre Arts and Technology": "theatre_arts_and_technology_ba",
    },
  },
  "Newark College Of Engineering": {
    "Biomedical Engineering": {
      "Biomedical Engineering - B.S.": "biomedical_engineering",
    },
    "Chemical and Materials Engineering": {
      "Chemical Engineering - B.S.": "chemical_engineering",
      "Materials Engineering - B.S.": "materials_engineering",
    },
    "Civil and Environmental Engineering": {
      "Civil Engineering - B.S.": "civil_engineering",
    },
    "Electrical and Computer Engineering": {
      "Computer Engineering - B.S.": "computer_engineering",
      "Electrical Engineering - B.S.": "electrical_engineering",
    },
    "Mechanical and Industrial Engineering": {
      "Industrial Engineering - B.S.": "industrial_engineering",
      "Mechanical Engineering - B.S.": "mechanical_engineering",
    },
    "SAET - Elec. & Mech. Division (SEMD)": {
      "Electrical and Computer Engineering Technology - B.S.": "electrical_and_computer_engineering_technology",
      "Industrial Engineering Technology - B.S.": "industrial_engineering_technology",
      "Mechanical Engineering Technology - B.S.": "mechanical_engineering_technology",
    },
    "SAET - Build Env. Division (SBCD)": {
      "Construction Engineering Technology - B.S.": "construction_engineering_technology",
      "Concrete Industry Management - B.S.": "concrete_industry_management_technology",
      "Surveying Engineering Technology - B.S.": "surveying_engineering_technology",
    },
    "SAET - Eng. Edu. Division (SEED)": {
      "Engineering Technology - B.S.": "engineering_technology",
      "General Engineering": "general_engineering",
    },
    "SAET - Biomedical & Life Sci Div (SBLSD)": {},
  },
  "Martin Tuchman School Of Management": {
    "Management": {
      "Business - B.S.": "business_bs",
      "Finanacial Technology - B.S.": "financial_technology_bs",
    },
  }
}

colleges_dropdown = dbc.DropdownMenu(
  label="colleges list",
  menu_variant="dark",
  children=[
    dbc.DropdownMenuItem(
      children=college,
      n_clicks=0,
      style={
        "font-size": "0.9rem",
        "padding-right": "1rem",
      },
      id=college.lower().replace(" ", "_"),
    ) for college in colleges_departments.keys()
  ],
  id="course-catalog-dropdown",
  toggle_style={
    "width": "100%",
    "word-wrap": "break-word",
    "white-space": "normal",
    "font-size": "0.9rem",
    "background": "#131314",
    "border": "1px solid #131314",
    "text-align": "left",
    "overflow": "hidden",
  },
)

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
    
    html.Div(
      children=[
        html.P(
          "Select a college",
          style={
            "color": "white",
            "margin": "1.2rem",
            "margin-bottom": "0.5rem",
            "margin-left": "0rem",
          }
        ),
        colleges_dropdown,
      ],
      style={
        "margin": "1rem",
        "margin-top": "0rem",
        "display": "flex", 
        "flexDirection": "column",
      }
    ),
    html.Div(
      id="dropdown-container",
      style={
        "margin": "1rem",
        "margin-top": "0rem",
        "display": "flex", 
        "flexDirection": "column",
      }
    ),
    html.Div(
      id="courses-selection-dropdown-container",
      style={
        "margin": "1rem",
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
  Output("dropdown-container", "children"),
  Output("course-catalog-dropdown", "label"),
  Input("hillier_college_of_architecture_and_design", "n_clicks"),
  Input("ying_wu_college_of_computing", "n_clicks"),
  Input("college_of_science_and_liberal_arts", "n_clicks"),
  Input("newark_college_of_engineering", "n_clicks"),
  Input("martin_tuchman_school_of_management", "n_clicks"),
)
def update_college_dropdown_label(*args):
  global selected_college

  ctx = callback_context
  if not ctx.triggered:
    return no_update
  college = ctx.triggered[0]["prop_id"].split(".")[0]
  college = college.replace("_", " ").title()

  selected_college = college
  return [
    [
      html.P(
        children=[
          "Select a department within ",
          html.Span(
            college, 
            style={
              "background-image": "linear-gradient(to right, #f12711, #a562f8)",
              "font-size": "0.9rem",
              "color": "transparent",
              "background-clip": "text",
            }
          ),
        ],
        style={
          "color": "white",
          "margin": "1.2rem",
          "margin-bottom": "0.5rem",
          "margin-left": "0rem",
        }
      ),
      dbc.DropdownMenu(
        label="departments list",
        menu_variant="dark",
        children=[
          dbc.DropdownMenuItem(
            children=department,
            n_clicks=0,
            style={
              "font-size": "0.9rem",
              "padding-right": "1rem",
            },
            id={"type": "department-dropdown-item", "index": department},
          ) for department in colleges_departments[selected_college].keys()
        ],
        id="department-dropdown",
        toggle_style={
          "width": "100%",
          "word-wrap": "break-word",
          "white-space": "normal",
          "font-size": "0.9rem",
          "background": "#131314",
          "border": "1px solid #131314",
          "text-align": "left",
          "overflow": "hidden",
        },
      ),
    ],
    college,
  ]


@callback(
  Output("courses-selection-dropdown-container", "children"),
  Output("department-dropdown", "label"),
  Input({"type": "department-dropdown-item", "index": ALL}, "n_clicks"),
)
def update_department_dropdown(n_clicks):
  global selected_college
  global selected_college_department

  ctx = callback_context
  if not ctx.triggered or not any(n_clicks):
    return no_update
  
  department_name = eval(ctx.triggered[0]["prop_id"].replace(".n_clicks", ""))["index"]
  selected_college_department = department_name

  return [
    [
      html.P(
        children = [
          "Select a course within ",
          html.Span(
            department_name, 
            style={
              "background-image": "linear-gradient(to right, #f12711, #a562f8)",
              "font-size": "0.9rem",
              "color": "transparent",
              "background-clip": "text",
            }
          ),
        ],
        style={
          "color": "white",
          "margin": "1.2rem",
          "margin-bottom": "0.5rem",
          "margin-left": "0rem",
        }
      ),
      dbc.DropdownMenu(
        label="courses list",
        menu_variant="dark",
        children=[
          dbc.DropdownMenuItem(
            children=course,
            n_clicks=0,
            style={
              "font-size": "0.9rem",
              "padding-right": "1rem",
            },
            id={"type": "course-dropdown-item", "index": course},
          ) for course in colleges_departments[selected_college][department_name]
        ],
        id="course-dropdown",
        toggle_style={
          "width": "100%",
          "word-wrap": "break-word",
          "white-space": "normal",
          "font-size": "0.9rem",
          "background": "#131314",
          "border": "1px solid #131314",
          "text-align": "left",
          "overflow": "hidden",
        },
      ),
    ],
    department_name,
  ]


@callback(
  Output('course-catalog-store', 'data'),
  Output("course-dropdown", "label"),
  Input({"type": "course-dropdown-item", "index": ALL}, "n_clicks"),
)
def update_course_dropdown(n_clicks):
  global selected_college
  global selected_college_department
  
  ctx = callback_context
  if not ctx.triggered or not any(n_clicks):
    return no_update
  
  course_name = eval(ctx.triggered[0]["prop_id"].replace(".n_clicks", ""))["index"]
  return [
    colleges_departments[selected_college][selected_college_department][course_name],
    course_name
  ]