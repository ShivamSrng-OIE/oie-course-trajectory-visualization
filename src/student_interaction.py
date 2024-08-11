from dash import html
import plotly.graph_objects as go
from src.develop_path import DevelopPath


class StudentInteraction:
  def __init__(self,
               gemini_interfacing) -> None:
    self.gemini_interfacing = gemini_interfacing


  def __perform_path_development_to_course(self,
                                           track: str,
                                           course_code: str,
                                           course_catalog_name: str,
                                           course_catalog_info: dict,
                                           last_camera_position: dict,
                                           all_tracks_information: dict) -> go.Figure:
    """
    To perform the path development to the course.
    
    Args:
      - course_code (str): The course code for which the path needs to be developed.
    
    Returns:
      - go.Figure: The figure for the path development.
    """

    fig, complete_path_sorted =  DevelopPath(
      course_name=course_catalog_name,
      course_catalog=course_catalog_info,
      all_tracks_course_information=all_tracks_information
    ).run(
      track=track,
      target_course=course_code,
      last_camera_position=last_camera_position
    )
    return fig, complete_path_sorted

  
  def __get_course_specific_information(self,
                                        track: str,
                                        course_code: str,
                                        all_tracks_information: dict) -> list:
    """
    To get the course specific information.

    Args:
      - track (str): The track for which the information needs to be fetched.
      - course_code (str): The course code for which the information needs to be fetched.
      - all_tracks_information (dict): The information about all the tracks.

    Returns:
      - list: The course specific information, if available indicated by 1, else 0 at 0th index of list.
    """

    if course_code not in all_tracks_information[track]:
      return 0, html.P(
        children=[f"The course code '{course_code}' is not available in the track '{track.replace('_', ' ').title()}'."],
        style={"color": "white", "margin": "0rem", "padding": "0rem", "margin-bottom": "0.5rem"}
      )
    
    course_specific_info = all_tracks_information[track][course_code]
    list_of_formatted_info = []
    for key, value in course_specific_info.items():
      if key not in ["track", "year", "semester", "complete_path", "on_dependant_courses_count", "dependency_count"]:
        if key == "course_link":
          list_of_formatted_info.append(
            html.P(
              children=[
                html.B(children=["Course Link:"]),
                html.Br(),
                html.A(children=value, href=value, target="_blank")
              ],
              style={"color": "white", "margin": "0rem", "padding": "0rem", "margin-bottom": "0.5rem"}
            )
          )
        elif key == "prerequisites" or key == "corequisites" and type(value) == list and len(value) > 0:
          value = self.__flatten_and_stringify(value)
          if value == "" or value is None:
            continue

          list_of_formatted_info.append(
            html.P(
              children=[
                html.B(children=[f"{key.title()}:"]),
                html.Br(),
                html.Span(value)
              ],
              style={"color": "white", "margin": "0rem", "padding": "0rem", "margin-bottom": "0.5rem"}
            )
          )
        elif key == "prerequisites_description" and type(value) == dict and len(value) > 0 and value is not None:
          value = self.__flatten_and_stringify([f"You need to have '{value[course]}' grade or better in {course} course." for course in value])
          if value == "" or value is None:
            continue

          list_of_formatted_info.append(
            html.P(
              children=[
                html.B(children=[f"{key.title()}:"]),
                html.Br(),
                html.Span(value),
              ],
              style={"color": "white", "margin": "0rem", "padding": "0rem", "margin-bottom": "0.5rem"}
            )
          )
        elif key != "course_link" and key != "prerequisites" and key != "corequisites" and key != "prerequisites_description":
          if type(value) == list:
            value = str(value)

          if value == "" or value is None:
            continue

          key = key.replace("_", " ").title()
          list_of_formatted_info.append(
            html.P(
              children=[
                html.B(children=[f"{key}:"]),
                html.Br(),
                html.Span(value)
              ],
              style={"color": "white", "margin": "0rem", "padding": "0rem", "margin-bottom": "0.5rem"}
            )
          )
    
    return 1, list_of_formatted_info
  

  def __root_down_in_pre_requisites_list(self,
                                         year: int,
                                         semester: int,
                                         course_code: str, 
                                         track_name: str,
                                         all_tracks_information: dict) -> list:
    """
    To root down in the pre-requisites list of a course to get all the pre-requisites
    of that course till the required year and semester.

    Args:
      - course_code (str): The course code of the course
      - track_name (str): The name of the track
    
    Returns:
      - list: The list of all the pre-requisites of the course till the required year and semester
    """

    courses_in_required_year_and_semester = []

    def dfs_traversal_of_course_prerequisistes(course_code: str|list, track_name: str):
      """
      To root down in the pre-requisites of a course to get all the pre-requisites
      of that course till the required year and semester.

      Args:
        - course_code (str): The course code of the course
        - track_name (str): The name of the track
      """

      if type(course_code) == list:
        for course in course_code:
          dfs_traversal_of_course_prerequisistes(course, track_name)

      elif type(course_code) == str:
        if course_code not in all_tracks_information[track_name]:
          return
        complete_course_information = all_tracks_information[track_name][course_code]
        prereq = []
        if "prerequisites" in complete_course_information:
          prereq = complete_course_information["prerequisites"]
        course_prerequisites = prereq
        course_year, course_semester = int(complete_course_information["year"]), int(complete_course_information["semester"])

        if course_year > year:
          for course in course_prerequisites:
            dfs_traversal_of_course_prerequisistes(course, track_name)

        elif course_year == year and course_semester > semester:
          for course in course_prerequisites:
            dfs_traversal_of_course_prerequisistes(course, track_name)

        elif course_year == year and course_semester == semester:
          courses_in_required_year_and_semester.append(course_code)

        else:
          return

    dfs_traversal_of_course_prerequisistes(course_code, track_name)
    return courses_in_required_year_and_semester


  def __flatten_and_stringify(self, 
                              nested_list: list) -> str:
    """
    To flatten the nested list and convert it into a string.
    
    Args:
      - nested_list (list): The nested list that needs to be flattened and converted into a string.
    
    Returns:
      - str: The stringified version of the flattened list.
    """
    
    flattened_list = []
    
    def flatten(lst):
        for item in lst:
            if isinstance(item, list):
                flatten(item)
            else:
                flattened_list.append(str(item))
    
    flatten(nested_list)
    return ", ".join(flattened_list)


  def __develop_recommendation(self,
                               year: int,
                               semester: int,
                               track_info: str,
                               all_tracks_information: dict,
                               career_goals_or_expectations: str) -> None:
    """
    To develop the recommendation for the student.

    Args:
      - year (int): The year for which the recommendation needs to be developed.
      - semester (int): The semester for which the recommendation needs to be developed.
      - track_info (str): The track information for which the recommendation needs to be developed.
      - all_tracks_information (dict): The information about all the tracks.
      - career_goals_or_expectations (str): The career goals or expectations of the student.
    """

    track_courses = {}
    only_course_description = {}
    only_course_pre_requisites_and_corequisites = {}

    for track_name in all_tracks_information:
      courses_name_list = []
      for course in all_tracks_information[track_name]:
        if "course_name" in all_tracks_information[track_name][course]:
          courses_name_list.append(all_tracks_information[track_name][course]["course_name"])

      track_focus = self.gemini_interfacing.formulate_gemini_response(
        model="track_extraction_model",
        data=courses_name_list
      )

      if track_focus["focus"] == track_info:
        track_courses[track_name] = []
        only_course_description[track_name] = []
        only_course_pre_requisites_and_corequisites[track_name] = []

        for course in all_tracks_information[track_name]:
          course_name = all_tracks_information[track_name][course]["course_link"]
          if "course_name" in all_tracks_information[track_name][course]:
            course_name = all_tracks_information[track_name][course]["course_name"]
          
          if int(all_tracks_information[track_name][course]["year"]) > year:
            track_courses[track_name].append(all_tracks_information[track_name][course])
            if "course_description" in all_tracks_information[track_name][course]:
              desc = all_tracks_information[track_name][course]["course_description"]
            else:
              desc = ""
            only_course_description[track_name].append({course_name: {
              "course_code": course,
              "description": desc,
              "year": all_tracks_information[track_name][course]["year"],
              "semester": all_tracks_information[track_name][course]["semester"]
            }})
            preq, coreq = "", ""
            if "prerequisites" in all_tracks_information[track_name][course]:
              preq = all_tracks_information[track_name][course]["prerequisites"]
            if "corequisites" in all_tracks_information[track_name][course]:
              coreq = all_tracks_information[track_name][course]["corequisites"]
            only_course_pre_requisites_and_corequisites[track_name].append([preq, coreq])

          elif int(all_tracks_information[track_name][course]["year"]) == year and int(all_tracks_information[track_name][course]["semester"]) >= semester:
            track_courses[track_name].append(all_tracks_information[track_name][course])
            if "course_description" in all_tracks_information[track_name][course]:
              only_course_description[track_name].append({course_name: {
                "course_code": course,
                "description": all_tracks_information[track_name][course]["course_description"],
                "year": all_tracks_information[track_name][course]["year"],
                "semester": all_tracks_information[track_name][course]["semester"]
              }})
            else:
              only_course_description[track_name].append({course_name: {
                "course_code": course,
                "description": "",
                "year": all_tracks_information[track_name][course]["year"],
                "semester": all_tracks_information[track_name][course]["semester"]
              }})
            if "prerequisites" not in all_tracks_information[track_name][course]:
              pre = []
            else:
              pre = all_tracks_information[track_name][course]["prerequisites"]
            if "corequisites" not in all_tracks_information[track_name][course]:
              coreq = []
            else:
              coreq = all_tracks_information[track_name][course]["corequisites"]

            only_course_pre_requisites_and_corequisites[track_name].append([pre, coreq])
    
    course_recommendation_model_response = {}
    for track_name in only_course_description:
      gemini_ranked_courses = self.gemini_interfacing.formulate_gemini_response(
        model="initial_course_recommendation_model",
        data=f"The career goals of the student are {career_goals_or_expectations}. The tracks information is {only_course_description[track_name]}."
      )

      course_recommendation_model_response[track_name] = []
      rank = 1
      for courses in gemini_ranked_courses["ranked_courses"]:
        course_code = courses["course_code"]
        complete_information = all_tracks_information[track_name][course_code]
        complete_information["rank"] = rank
        rank += 1
        complete_information["reason_for_recommendation"] = courses["reason_for_recommendation"]
        course_recommendation_model_response[track_name].append({
          key: value for key, value in complete_information.items()
        })
    
    phase_one_recommendation = {}
    requirements_dict = {}

    for track in course_recommendation_model_response:
      phase_one_recommendation[track] = []

      for course in course_recommendation_model_response[track]:
        course_year, course_semester = course["year"], course["semester"]
        course_prereq = []
        if "prerequisites" in course:
          course_prereq = course["prerequisites"]

        reason_for_recommendation = ""
        if "reason_for_recommendation" in course.keys():
          reason_for_recommendation = course["reason_for_recommendation"]
        if course_year == year and course_semester == semester:
          if course not in phase_one_recommendation[track]:
            phase_one_recommendation[track].append(course)
          
          if "complete_path" in course:
            for path in course["complete_path"]:
              if path["source"] not in requirements_dict.keys():
                requirements_dict[path["source"]] = {
                  "destination": {
                    course["course_code"]: {
                      "relation": [path["relation"]],
                      "grade_requirement": course["prerequisites_description"][path["source"]] if "prerequisites_description" in course and path["source"] in course["prerequisites_description"] else ""
                    }
                  },
                  "req_cnt": 1
                }
              else:
                if course["course_code"] not in requirements_dict[path["source"]]["destination"]:
                  requirements_dict[path["source"]]["destination"][course["course_code"]] = {
                    "relation": [path["relation"]]
                  }
                  requirements_dict
                  requirements_dict[path["source"]]["req_cnt"] += 1
        else:
          if "course_code" not in course:
            continue
          req_year_sem_courses = self.__root_down_in_pre_requisites_list(
            year=year,
            semester=semester,
            course_code=course["course_code"],
            track_name=track,
            all_tracks_information=all_tracks_information
          )
          for course_code in req_year_sem_courses:
            if all_tracks_information[track][course_code] not in phase_one_recommendation[track]:
              if "reason_for_recommendation" not in all_tracks_information[track][course_code]:
                all_tracks_information[track][course_code]["reason_for_recommendation"] = ""
              complete_reason = all_tracks_information[track][course_code]["reason_for_recommendation"].strip()
              if reason_for_recommendation != "":
                reason_for_recommendation = reason_for_recommendation[0].lower() + reason_for_recommendation[1:]
                complete_reason += f" This course is a pre-requisite for {course['course_code']} course. And the reason behind the recommendation of {course['course_code']} is that {reason_for_recommendation}."
              else:
                complete_reason = f" This course is a pre-requisite for {course['course_code']} course."
              all_tracks_information[track][course_code]["reason_for_recommendation"] = complete_reason.strip()
              phase_one_recommendation[track].append(all_tracks_information[track][course_code])

              if "complete_path" in all_tracks_information[track][course_code]:
                for path in all_tracks_information[track][course_code]["complete_path"]:
                  if path["source"] not in requirements_dict.keys():
                    requirements_dict[path["source"]] = {
                      "destination": {
                        course_code: {
                          "relation": [path["relation"]],
                          "grade_requirement": [course["grade_requirement"][path["source"]] if "grade_requirement" in course and path["source"] in course["grade_requirement"] else ""]
                        }
                      },
                      "req_cnt": 1
                    }
                  else:
                    if course_code not in requirements_dict[path["source"]]["destination"]:
                      requirements_dict[path["source"]]["destination"][course_code] = {
                        "relation": [path["relation"]]
                      }
                      requirements_dict[path["source"]]["req_cnt"] += 1

    requirements_dict = dict(sorted(
      requirements_dict.items(),
      key=lambda x: x[1]["req_cnt"],
      reverse=True
    ))
    phase_two_recommendation = dict(
      sorted(
        phase_one_recommendation.items(),
        key=lambda x: (-x[1][0]["rank"], x[1][0]["dependency_count"]),
        reverse=True
      )
    )
    
    formatted_recommendation = []
    for track in phase_two_recommendation:
      formatted_recommendation.append(
        html.Div(
          children=[
            html.P(
              children=[
                html.Span(track.replace("_", " ").title(), style={"color": "red"}),
              ],
              style={"padding": "0rem", "margin": "0rem", "margin-bottom": "0.3rem"}
            ),
            html.Hr(
              style={"color": "white", "margin": "0rem", "padding": "0rem", "line-height": "0.5rem", "margin-bottom": "0.3rem"}
            ),
          ],
          style={"padding": "0rem", "margin": "0rem", "margin-top": "0.5rem"}
        )
      )

      for idx, ranked_course in enumerate(phase_two_recommendation[track], start=1):
        course_code, course_name = ranked_course["course_code"] if "course_code" in ranked_course else "", ranked_course["course_name"] if "course_name" in ranked_course else ""
        prereq, coreq = self.__flatten_and_stringify(
          nested_list=ranked_course["prerequisites"]
          ) if "prerequisites" in ranked_course and len(ranked_course["prerequisites"]) else "None", self.__flatten_and_stringify(
            nested_list=ranked_course["corequisites"]
          ) if "corequisites" in ranked_course and len(ranked_course["corequisites"]) else "None"
        course_description = ranked_course["course_description"] if "course_description" in ranked_course else "None"
        reason_for_recommendation = ranked_course["reason_for_recommendation"]
        if "prerequisites_description" in ranked_course:
          list_of_prereq_desc = []
          for prereq_desc in ranked_course["prerequisites_description"].keys():
            list_of_prereq_desc.append(
              f"You need to have '{ranked_course['prerequisites_description'][prereq_desc]}' grade or better in {prereq_desc} course."
            )
          prereq_desc = self.__flatten_and_stringify(list_of_prereq_desc)

        formatted_recommendation.append(
          html.P(
            children=[
              html.B(
                children=[
                  html.Span(f"{idx}.", style={"color": "red", "margin-right": "0.3rem"}),
                  "Course Code:"
                ],
                style={"display": "flex", "flex-direction": "row", "margin": "0rem", "padding": "0rem"}
              ),
              html.P(children=[f"{course_code}"], style={"color": "white", "margin": "0rem", "padding": "0rem", "margin-bottom": "0.3rem"}),
              html.B(children=["Course Name:"]),
              html.P(children=[f"{course_name}"], style={"color": "white", "margin": "0rem", "padding": "0rem", "margin-bottom": "0.3rem"}),
              html.B(children=["Course Description:"]),
              html.P(children=[f"{course_description}"], style={"color": "white", "margin": "0rem", "padding": "0rem", "margin-bottom": "0.3rem"}),
              html.B(children=["Pre-requisites:"]),
              html.P(children=[f"{prereq}"], style={"color": "white", "margin": "0rem", "padding": "0rem", "margin-bottom": "0.3rem"}),
              html.B(children=["Pre-requisites Description:"]),
              html.P(children=[f"{prereq_desc}"], style={"color": "white", "margin": "0rem", "padding": "0rem", "margin-bottom": "0.3rem"}),
              html.B(children=["Co-requisites:"]),
              html.P(children=[f"{coreq}"], style={"color": "white", "margin": "0rem", "padding": "0rem", "margin-bottom": "0.3rem"}),
              html.B(children=["Reason for Recommendation:"]),
              html.P(children=[f"{reason_for_recommendation}"], style={"color": "white", "margin": "0rem", "padding": "0rem", "margin-bottom": "0.3rem"}),
            ],
            style={"color": "white", "margin": "0rem", "padding": "0rem", "margin": "0rem"}
          )
        )
      
      formatted_recommendation.append(
        html.Hr(
          style={"color": "white", "margin": "0rem", "padding": "0rem", "margin": "0rem", "line-height": "0.5rem", "margin-bottom": "1rem"}
        )
      )

    return formatted_recommendation


  def start_interaction(self,
                        track: str,
                        course_catalog_name: str,
                        initial_interaction: str,
                        course_catalog_info: dict,
                        last_camera_position: dict,
                        all_tracks_information: dict) -> list:
    """
    To start the student interaction.
    
    Args:
      - initial_interaction (str): The initial interaction with the student.
    
    Returns:
      - list: The response from the student interaction.
    """

    response_from_gemini = self.gemini_interfacing.formulate_gemini_response(
      model="university_advisor_assistant_model",
      data=initial_interaction
    )
    
    if response_from_gemini[0] == 1:
      follow_up_interaction = response_from_gemini[1]["follow_up_response"]
      completion_status = response_from_gemini[1]["completed"]
      if completion_status == 0:
        return None, [], follow_up_interaction
      elif completion_status == 1:
        course_code = response_from_gemini[1]["course_code"]
        fig, complete_path_sorted = self.__perform_path_development_to_course(
          track=track,
          course_code=course_code,
          course_catalog_name=course_catalog_name,
          course_catalog_info=course_catalog_info,
          last_camera_position=last_camera_position,
          all_tracks_information=all_tracks_information
        )
        if fig is None and len(complete_path_sorted) == 0:
          return None, [], f"The course code '{course_code}' is not available in the track '{track.replace('_', ' ').title()}'. Please, check the course code and try again."
        return fig, complete_path_sorted, follow_up_interaction
    

    elif response_from_gemini[0] == 2:
      follow_up_interaction = response_from_gemini[1]["follow_up_response"]
      completion_status = response_from_gemini[1]["completed"]
      if completion_status == 0:
        return None, [], follow_up_interaction
      elif completion_status == 1:
        course_code = response_from_gemini[1]["course_code"]
        success_status, course_specific_information = self.__get_course_specific_information(
          track=track,
          course_code=course_code,
          all_tracks_information=all_tracks_information
        )
        if success_status == 0:
          return None, [], course_specific_information
        else:
          return None, course_specific_information, follow_up_interaction
        
    
    elif response_from_gemini[0] == 3:
      follow_up_interaction = response_from_gemini[1]["follow_up_response"]
      completion_status = response_from_gemini[1]["completed"]
      if completion_status == 0:
        return None, [], follow_up_interaction
      elif completion_status == 1:
        year, semester, track, career_goal = response_from_gemini[1]["year"], response_from_gemini[1]["semester"], response_from_gemini[1]["track"], response_from_gemini[1]["career_goals"]
        return None, self.__develop_recommendation(
          year=year,
          semester=semester,
          track_info=track,
          career_goals_or_expectations=career_goal,
          all_tracks_information=all_tracks_information
        ), follow_up_interaction
      
    else:

      return None, [], "I am still in the learning phase, maybe in future I will be able to help you with this. As of now, I am not able to understand your query."