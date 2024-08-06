import numpy as np
from dash import html
import plotly.graph_objects as go
from warnings import filterwarnings
from consts import CourseTrajectoryConsts


filterwarnings("ignore")


class DevelopPath:
  """
  The DevelopPath class is used to generate a 3d graph of the course catalogs of different departments.
  """
  

  def __init__(self,
               course_name: str,
               course_catalog: dict,
               all_tracks_course_information: dict) -> None:
    """
    Initialize the DevelopPath class.
    
    Args:
      - course_name (str): The name of the course.
      - course_catalog (dict): The course catalog.
      - all_tracks_course_information (dict): The course information.
    
    Returns:
      - None
    """
    
    self.course_name = course_name
    self.course_catalog = course_catalog
    self.all_tracks_course_information = all_tracks_course_information
    self.__initialize_constants()
  

  def __initialize_constants(self) -> None:
    """
    Initialize the constants.
    
    Args:
      - None
    
    Returns:
      - None
    """
    
    course_trajectory_consts = CourseTrajectoryConsts().get_course_trajectory_consts()
    self.z_level = course_trajectory_consts["z_level"]
    self.left_shift = course_trajectory_consts["left_shift"]
    self.z_increment = course_trajectory_consts["z_increment"]
    self.marker_size = course_trajectory_consts["marker_size"]
    self.radius_circle = course_trajectory_consts["radius_circle"]
    self.special_marker_size = course_trajectory_consts["special_marker_size"]
    self.complete_path_to_top = course_trajectory_consts["complete_path_to_top"]
    self.color_for_corequisites = course_trajectory_consts["color_for_corequisites"]
    self.color_for_prerequisites = course_trajectory_consts["color_for_prerequisites"]
    self.complete_path_from_start = course_trajectory_consts["complete_path_from_start"]
    self.critical_courses_threshold = course_trajectory_consts["critical_courses_threshold"]
    self.critical_courses_threshold_circle = course_trajectory_consts["critical_courses_threshold_circle"]


  def __dynamic_color_choice_for_semester(self,
                                          courses_in_year: dict) -> dict:
    """
    Assign colors to courses based on their semester.
    
    Args:
      - courses_in_year (dict): The courses in a year.
    
    Returns:
      - dict: The dictionary with the course colors.
    """

    semester_colors = {}
    cnt = 0
    for year in courses_in_year:
      for semester in courses_in_year[year]:
        semester_colors[
          (year, semester)
        ] = f"hsl({cnt * (360 // (len(courses_in_year) * len(courses_in_year[year])))}, 70%, 50%)"
        cnt += 1
    return semester_colors
           


  def __add_intermediate_br_tags(self,
                                 description: str,
                                 max_chars=50) -> str:
    """
    Insert <br> tags into the description string after every max_chars characters
    without breaking words.
    
    Args:
      - description (str): The original description string.
      - max_chars (int): Maximum number of characters before inserting a <br> tag (default is 64).
    
    Returns:
      - str: The modified description with <br> tags inserted.
    """
    
    words = description.split()
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line) + len(word) <= max_chars:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    
    if current_line:
        lines.append(current_line.strip())
    
    return "<br>".join(lines)
  

  def __create_circle(self,
                      tower: str,
                      n_points: int,
                      z_level: int) -> list[int]:
    """
    Create a circle of points in 3D space.
     
    Args:
      - n_points (int): The number of points in the circle.
      - z_level (int): The z-level of the circle.
       
    Returns:
      - list[int]: The list of points in the circle.
    """

    if tower == "pre-knowledge":
      radius = self.radius_circle / 2
    else:
      radius = self.radius_circle

    theta = np.linspace(
      start=0,
      stop=2*np.pi, 
      num=n_points,
      endpoint=False
    )
    x = radius * np.cos(theta)
    y = radius * np.sin(theta) 
    z = np.full_like(x, z_level)
    
    return x, y, z
  

  def __create_random_points_on_circle(self, z_level, num_points, angle_offset=0):
    theta = np.linspace(0, 2 * np.pi, num_points) + angle_offset
    x = self.radius_circle * np.cos(theta)
    y = self.radius_circle * np.sin(theta)
    z = np.full(num_points, z_level)
    return x.tolist(), y.tolist(), z.tolist()
  

  def __dynamic_color_choice_for_semester(self,
                                          courses_in_year: dict) -> dict:
    """
    Assign colors to courses based on their semester.
    
    Args:
      - courses_in_year (dict): The courses in a year.
    
    Returns:
      - dict: The dictionary with the course colors.
    """

    semester_colors = {}
    cnt = 0
    for year in courses_in_year:
      semester_colors[year] = {}
      for semester in courses_in_year[year]:
        semester_colors[year][semester] = "gray"
        cnt += 1
    return semester_colors
  

  def __develop_path_to_target(self,
                               track: str,
                               target_course: str,
                               path_to_target: list,
                               last_camera_position: dict) -> go.Figure:
    """
    Create a 3D graph of the course trajectory for a particular track.
    
    Args:
      - track (str): The track for which the course trajectory is to be generated.
      - target_course (str): The target course.
      - path_to_target (list): The path to the target course.

    Returns:
      - go.Figure: The 3D graph of the course trajectory.
    """

    courses = self.course_catalog[track]
    fig = go.Figure()
    semester_colors = self.__dynamic_color_choice_for_semester(courses)
    course_positions, course_colors = {}, {}
    
    taught_courses = set()
    for year in courses:
      if year != "extra_course_related_info":
        for semester in courses[year]:
          taught_courses.update(courses[year][semester].keys())

    z_level = self.z_level
    semester_elevation = {}
    for year in courses:
      if year == "extra_course_related_info":
        continue
      for semester in courses[year]:
        courses_in_semester = list(courses[year][semester].keys())
        n_courses = len(courses_in_semester)
        if year not in semester_elevation:
          semester_elevation[year] = {}

        semester_elevation[year][semester] = z_level
        course_colors.update({course: semester_colors[year][semester] for course in courses_in_semester})
            
        fig.add_trace(go.Scatter3d(
          x=[0],
          y=[0],
          z=[z_level],
          text=f"Year: {year}, Semester: {semester}",
          mode='text',
          showlegend=False,
          textposition='middle center',
          textfont=dict(size=12, color='black', family="Arial", weight="bold"),
          hoverinfo='skip'  
        ))

        course_cnt, critical_course_cnt = 0, 0
        angle_offset = np.random.uniform(0, 2 * np.pi)
        x, y, z = self.__create_random_points_on_circle(z_level, n_courses + 1, angle_offset)
        course_positions.update({course: (x[i], y[i], z[i]) for i, course in enumerate(courses_in_semester)})
    
        for i, course in enumerate(courses_in_semester):
          course_desc, course_name = "", ""
          course_cnt += 1
          if course in self.all_tracks_course_information[track]:
            if "course_description" in self.all_tracks_course_information[track][course]:
              course_desc = self.__add_intermediate_br_tags(self.all_tracks_course_information[track][course]["course_description"])
            if "course_name" in self.all_tracks_course_information[track][course]:
              course_name = self.all_tracks_course_information[track][course]["course_name"]

            self.all_tracks_course_information[track][course]["location"] = {"x": x[i], "y": y[i], "z": z[i]}

          if course in self.all_tracks_course_information[track] and self.all_tracks_course_information[track][course]["dependency_count"] >= self.critical_courses_threshold:
            critical_course_cnt += 1
            fig.add_trace(go.Scatter3d(
              x=[x[i]],
              y=[y[i]],
              z=[z[i]],
              text=course,  
              mode='markers+text',
              customdata=[course],
              hoverinfo='text',  
              marker=dict(size=self.special_marker_size, color=course_colors[course]),
              textfont=dict(size=12, color='black', family="Arial", weight="bold"),
              textposition='top center',
              hovertext=course_desc + f"<br><br>Dependencies: {self.all_tracks_course_information[track][course]['dependency_count']}",
              name=f"{course}-{course_name}" if course_name else course
            ))
          else:
            fig.add_trace(go.Scatter3d(
              x=[x[i]],
              y=[y[i]],
              z=[z[i]],
              text=course, 
              customdata=[course], 
              mode='markers+text',
              hoverinfo='text',  
              marker=dict(size=self.marker_size, color=course_colors[course]),
              textfont=dict(size=12, color='black', family="Arial", weight="bold"),
              textposition='top center',
              hovertext=course_desc,
              name=f"{course}-{course_name}" if course_name else course
            ))

        if critical_course_cnt >= self.critical_courses_threshold_circle:
          circle_x, circle_y, circle_z = self.__create_circle("", 100, z_level)
          fig.add_trace(go.Scatter3d(
            x=circle_x,
            y=circle_y,
            z=circle_z,
            mode='lines',
            line=dict(color='black', width=10),
            name=f"Year: {year}, Semester: {semester}",
            hoverinfo='skip'  
          ))
        else:
          circle_x, circle_y, circle_z = self.__create_circle("", 100, z_level)
          fig.add_trace(go.Scatter3d(
            x=circle_x,
            y=circle_y,
            z=circle_z,
            mode='lines',
            line=dict(color='black', width=2, dash='dash'),
            name=f"Year: {year}, Semester: {semester}",
            hoverinfo='skip'  
          ))

        z_level += self.z_increment

    external_radius = self.radius_circle
    external_positions = {}
    unique_prereqs = []
    unique_prereqs_complete_info = []

    for year in courses:
      if year == "extra_course_related_info":
        continue
      for semester in courses[year]:
        for course in courses[year][semester]:
          details = courses[year][semester][course]
          course_name = ""
          if "course_name" in details:
            course_name = details["course_name"]
          
          if 'prerequisites' in details:
            prerequisites_data = details['prerequisites']
            if isinstance(prerequisites_data, list):
              for item in prerequisites_data:
                if isinstance(item, list):
                  for prereq in item:
                    if isinstance(prereq, list):
                      for sub_prereq in prereq:
                        if sub_prereq not in taught_courses:
                          if sub_prereq not in unique_prereqs:
                            unique_prereqs.append(sub_prereq)
                            unique_prereqs_complete_info.append([sub_prereq, int(year), int(semester), semester_elevation[year][semester]])
                          elif sub_prereq in unique_prereqs:
                            index = unique_prereqs.index(sub_prereq)
                            already_present_prereq, already_present_year, already_present_semester, already_present_semester_elevation = unique_prereqs_complete_info[index]
                            if already_present_year > int(year):
                              unique_prereqs_complete_info[index] = [sub_prereq, int(year), int(semester), semester_elevation[year][semester]]
                            elif already_present_year == int(year) and already_present_semester > int(semester):
                              unique_prereqs_complete_info[index] = [sub_prereq, int(year), int(semester), semester_elevation[year][semester]]

                    elif prereq not in taught_courses:
                      if prereq not in unique_prereqs:
                        unique_prereqs.append(prereq)
                        unique_prereqs_complete_info.append([prereq, int(year), int(semester), semester_elevation[year][semester]])
                      elif prereq in unique_prereqs:
                        index = unique_prereqs.index(prereq)
                        already_present_prereq, already_present_year, already_present_semester, already_present_semester_elevation = unique_prereqs_complete_info[index]
                        if already_present_year > int(year):
                          unique_prereqs_complete_info[index] = [prereq, int(year), int(semester), semester_elevation[year][semester]]
                        elif already_present_year == int(year) and already_present_semester > int(semester):
                          unique_prereqs_complete_info[index] = [prereq, int(year), int(semester), semester_elevation[year][semester]]
                else:
                  if item not in taught_courses:
                    if item not in unique_prereqs:
                      unique_prereqs.append(item)
                      unique_prereqs_complete_info.append([item, int(year), int(semester), semester_elevation[year][semester]])
                    elif item in unique_prereqs:
                      index = unique_prereqs.index(item)
                      already_present_item, already_present_year, already_present_semester, already_present_semester_elevation = unique_prereqs_complete_info[index]
                      if already_present_year > int(year):
                        unique_prereqs_complete_info[index] = [item, int(year), int(semester), semester_elevation[year][semester]]
                      elif already_present_year == int(year) and already_present_semester > int(semester):
                        unique_prereqs_complete_info[index] = [item, int(year), int(semester), semester_elevation[year][semester]]
            else:
              if prerequisites_data not in taught_courses:
                if prerequisites_data not in unique_prereqs:
                  unique_prereqs.append(prerequisites_data)
                  unique_prereqs_complete_info.append([prerequisites_data, int(year), int(semester), semester_elevation[year][semester]])
                elif prerequisites_data in unique_prereqs:
                  index = unique_prereqs.index(prerequisites_data)
                  already_present_prerequisites_data, already_present_year, already_present_semester, already_present_semester_elevation = unique_prereqs_complete_info[index]
                  if already_present_year > int(year):
                    unique_prereqs_complete_info[index] = [prerequisites_data, int(year), int(semester), semester_elevation[year][semester]]
                  elif already_present_year == int(year) and already_present_semester > int(semester):
                    unique_prereqs_complete_info[index] = [prerequisites_data, int(year), int(semester), semester_elevation[year][semester]]

          if 'corequisites' in details:
            prerequisites_data = details['corequisites']
            if isinstance(prerequisites_data, list):
              for item in prerequisites_data:
                if isinstance(item, list):
                  for prereq in item:
                    if isinstance(prereq, list):
                      for sub_prereq in prereq:
                        if sub_prereq not in taught_courses:
                          if sub_prereq not in unique_prereqs:
                            unique_prereqs.append(sub_prereq)
                            unique_prereqs_complete_info.append([sub_prereq, int(year), int(semester), semester_elevation[year][semester]])
                          elif sub_prereq in unique_prereqs:
                            index = unique_prereqs.index(sub_prereq)
                            already_present_prereq, already_present_year, already_present_semester, already_present_semester_elevation = unique_prereqs_complete_info[index]
                            if already_present_year > int(year):
                              unique_prereqs_complete_info[index] = [sub_prereq, int(year), int(semester), semester_elevation[year][semester]]
                            elif already_present_year == int(year) and already_present_semester > int(semester):
                              unique_prereqs_complete_info[index] = [sub_prereq, int(year), int(semester), semester_elevation[year][semester]]

                    elif prereq not in taught_courses:
                      if prereq not in unique_prereqs:
                        unique_prereqs.append(prereq)
                        unique_prereqs_complete_info.append([prereq, int(year), int(semester), semester_elevation[year][semester]])
                      elif prereq in unique_prereqs:
                        index = unique_prereqs.index(prereq)
                        already_present_prereq, already_present_year, already_present_semester, already_present_semester_elevation = unique_prereqs_complete_info[index]
                        if already_present_year > int(year):
                          unique_prereqs_complete_info[index] = [prereq, int(year), int(semester), semester_elevation[year][semester]]
                        elif already_present_year == int(year) and already_present_semester > int(semester):
                          unique_prereqs_complete_info[index] = [prereq, int(year), int(semester), semester_elevation[year][semester]]

                else:
                  if item not in taught_courses:
                    if item not in unique_prereqs:
                      unique_prereqs.append(item)
                      unique_prereqs_complete_info.append([item, int(year), int(semester), semester_elevation[year][semester]])
                    elif item in unique_prereqs:
                      index = unique_prereqs.index(item)
                      already_present_item, already_present_year, already_present_semester, already_present_semester_elevation = unique_prereqs_complete_info[index]
                      if already_present_year > int(year):
                        unique_prereqs_complete_info[index] = [item, int(year), int(semester), semester_elevation[year][semester]]
                      elif already_present_year == int(year) and already_present_semester > int(semester):
                        unique_prereqs_complete_info[index] = [item, int(year), int(semester), semester_elevation[year][semester]]

            else:
              if prerequisites_data not in taught_courses:
                if prerequisites_data not in unique_prereqs:
                  unique_prereqs.append(prerequisites_data)
                  unique_prereqs_complete_info.append([prerequisites_data, int(year), int(semester), semester_elevation[year][semester]])
                elif prerequisites_data in unique_prereqs:
                  index = unique_prereqs.index(prerequisites_data)
                  already_present_prerequisites_data, already_present_year, already_present_semester, already_present_semester_elevation = unique_prereqs_complete_info[index]
                  if already_present_year > int(year):
                    unique_prereqs_complete_info[index] = [prerequisites_data, int(year), int(semester), semester_elevation[year][semester]]
                  elif already_present_year == int(year) and already_present_semester > int(semester):
                    unique_prereqs_complete_info[index] = [prerequisites_data, int(year), int(semester), semester_elevation[year][semester]]

    unique_prereqs.sort()
    unique_prereqs_complete_info.sort(key=lambda x: x[0])
    left_shift = self.left_shift
    already_present_semester_circle = []
    course_cnt, critical_course_cnt = 0, 0

    for i, prereq in enumerate(unique_prereqs):
      prerequisites_data, year, semester, semester_elevation = unique_prereqs_complete_info[i]
      
      x = (external_radius / 2) * np.cos(2 * np.pi * i / len(unique_prereqs)) + left_shift
      y = (external_radius / 2) * np.sin(2 * np.pi * i / len(unique_prereqs))
      z = semester_elevation
      course_cnt += 1

      if [year, semester] not in already_present_semester_circle:
          already_present_semester_circle.append([year, semester])
          circle_x, circle_y, circle_z = self.__create_circle("pre-knowledge", 100, semester_elevation)
          fig.add_trace(go.Scatter3d(
              x=circle_x + left_shift,
              y=circle_y,
              z=circle_z,
              mode='lines',
              line=dict(color='black', width=2, dash='dash'),
              name=f"Year: {year}, Semester: {semester}",
              showlegend=False,
              hoverinfo='skip'  
          ))
          fig.add_trace(go.Scatter3d(
          x=[0 + left_shift],
          y=[0],
          z=[semester_elevation],
          text="Pre-Knowledge Courses",
          mode='text',
          showlegend=False,
          textfont=dict(size=12, color='black', family="Arial", weight="bold"),
          textposition='middle center',
          hoverinfo='skip'  
      ))

      external_positions[prereq] = (x, y, z)
      course_positions[prereq] = (x, y, z)
      course_colors[prereq] = '#000000' 
      
      course_desc, course_name = "", ""
      if prereq in self.all_tracks_course_information:
          if "course_description" in self.all_tracks_course_information[prereq]:
              course_desc = self.__add_intermediate_br_tags(self.all_tracks_course_information[prereq]["course_description"])
          if "course_name" in self.all_tracks_course_information[prereq]:
              course_name = self.all_tracks_course_information[prereq]["course_name"]

          self.all_tracks_course_information[prereq]["location"] = {"x": x, "y": y, "z": z}
      if prereq in self.all_tracks_course_information and self.all_tracks_course_information[prereq]["dependency_count"] >= self.critical_courses_threshold:
          critical_course_cnt += 1
          fig.add_trace(go.Scatter3d(
              x=[x],
              y=[y],
              z=[z],
              customdata=[prereq],
              text=prereq,
              mode='markers+text',
              hoverinfo='text',  
              hovertext=course_desc + f"<br><br>Dependencies: {self.all_tracks_course_information[prereq]['dependency_count']}",
              marker=dict(size=self.special_marker_size, color='gray'),
              textfont=dict(size=12, color='black', family="Arial", weight="bold"),
              showlegend=False,
              name=f"{prereq}-{course_name}" if course_name else prereq
          ))
      else:
          fig.add_trace(go.Scatter3d(
              x=[x],
              y=[y],
              z=[z],
              customdata=[prereq],
              text=prereq,
              mode='markers+text',
              hoverinfo='text', 
              hovertext=course_desc,
              marker=dict(size=self.marker_size, color='gray'),
              showlegend=False,
              textfont=dict(size=12, color='black', family="Arial", weight="bold"),
              name=f"{prereq}-{course_name}" if course_name else prereq
          ))

    edge_traces = []
    for year in courses:
      if year == "extra_course_related_info":
        continue
      for semester in courses[year]:
        courses_in_semester = list(courses[year][semester].keys())
        for course in courses_in_semester:
          x1, y1, z1 = course_positions[course]
          course_year = self.all_tracks_course_information[track][course]["year"] if course in self.all_tracks_course_information[track] else 0
          course_semester = self.all_tracks_course_information[track][course]["semester"] if course in self.all_tracks_course_information[track] else 0
          if 'prerequisites' in courses[year][semester][course]:
            for prereq in courses[year][semester][course]['prerequisites']:
              if isinstance(prereq, list):
                for sub_prereq_list in prereq:
                  if isinstance(sub_prereq_list, list):
                    for sub_prereq in sub_prereq_list:
                      if sub_prereq in course_positions:
                        x0, y0, z0 = course_positions[sub_prereq]
                        sub_prereq_year = self.all_tracks_course_information[track][sub_prereq]["year"] if sub_prereq in self.all_tracks_course_information[track] else 0
                        sub_prereq_semester = self.all_tracks_course_information[track][sub_prereq]["semester"] if sub_prereq in self.all_tracks_course_information[track] else 0
                        uid = f"inbetween_edges_prerequisites_{course_year}_{course_semester}_{sub_prereq_year}_{sub_prereq_semester}_{year}_{semester}"
                        edge_traces.append(go.Scatter3d(
                          customdata=[f"edge_pre_{course}_{sub_prereq}"],
                          uid=uid,
                          x=[x0, x1],
                          y=[y0, y1],
                          z=[z0, z1],
                          mode='lines',
                          showlegend=False,
                          line=dict(color=self.color_for_prerequisites, width=2),  
                          hoverinfo='skip'  
                        ))
                  elif sub_prereq_list in course_positions:
                    x0, y0, z0 = course_positions[sub_prereq_list]
                    sub_prereq_year = self.all_tracks_course_information[track][sub_prereq_list]["year"] if sub_prereq_list in self.all_tracks_course_information[track] else 0
                    sub_prereq_semester = self.all_tracks_course_information[track][sub_prereq_list]["semester"] if sub_prereq_list in self.all_tracks_course_information[track] else 0
                    uid = f"inbetween_edges_prerequisites_{course_year}_{course_semester}_{sub_prereq_year}_{sub_prereq_semester}_{year}_{semester}"
                    edge_traces.append(go.Scatter3d(
                      customdata=[f"edge_pre_{course}_{sub_prereq_list}"],
                      uid=uid,
                      x=[x0, x1],
                      y=[y0, y1],
                      z=[z0, z1],
                      mode='lines',
                      showlegend=False,
                      line=dict(color=self.color_for_prerequisites, width=2), 
                      hoverinfo='skip' 
                    ))
              elif prereq in course_positions:
                x0, y0, z0 = course_positions[prereq]
                prereq_year = self.all_tracks_course_information[track][prereq]["year"] if prereq in self.all_tracks_course_information[track] else 0
                prereq_semester = self.all_tracks_course_information[track][prereq]["semester"] if prereq in self.all_tracks_course_information[track] else 0
                uid = f"inbetween_edges_prerequisites_{course_year}_{course_semester}_{prereq_year}_{prereq_semester}_{year}_{semester}"
                edge_traces.append(go.Scatter3d(
                  customdata=[f"edge_pre_{course}_{prereq}"],
                  uid=uid,
                  x=[x0, x1],
                  y=[y0, y1],
                  z=[z0, z1],
                  mode='lines',
                  showlegend=False,
                  line=dict(color=self.color_for_prerequisites, width=2),  
                  hoverinfo='skip'  
                ))

            
            if 'corequisites' in courses[year][semester][course]:
              for coreq in courses[year][semester][course]['corequisites']:
                if isinstance(coreq, list):
                  for sub_coreq in coreq:
                    if isinstance(sub_coreq, list):
                      for c in sub_coreq:
                        if c in course_positions:
                          x0, y0, z0 = course_positions[c]
                          coreq_year = self.all_tracks_course_information[track][c]["year"] if c in self.all_tracks_course_information[track] else 0
                          coreq_semester = self.all_tracks_course_information[track][c]["semester"] if c in self.all_tracks_course_information[track] else 0
                          uid = f"inbetween_edges_corequisites_{year}_{semester}_{coreq_year}_{coreq_semester}_{course_year}_{course_semester}"
                          edge_traces.append(go.Scatter3d(
                            customdata=[f"edge_coreq_{course}_{c}"],
                            uid=uid,
                            x=[x0, x1],
                            y=[y0, y1],
                            z=[z0, z1],
                            mode='lines',
                            showlegend=False,
                            line=dict(color=self.color_for_corequisites, width=2), 
                            hoverinfo='skip'  
                          ))
                    elif sub_coreq in course_positions:
                      x0, y0, z0 = course_positions[sub_coreq]
                      coreq_year = self.all_tracks_course_information[track][sub_coreq]["year"] if sub_coreq in self.all_tracks_course_information[track] else 0
                      coreq_semester = self.all_tracks_course_information[track][sub_coreq]["semester"] if sub_coreq in self.all_tracks_course_information[track] else 0
                      uid = f"inbetween_edges_corequisites_{year}_{semester}_{coreq_year}_{coreq_semester}_{course_year}_{course_semester}"
                      edge_traces.append(go.Scatter3d(
                        customdata=[f"edge_coreq_{course}_{sub_coreq}"],
                        uid=uid,
                        x=[x0, x1],
                        y=[y0, y1],
                        z=[z0, z1],
                        mode='lines',
                        showlegend=False,
                        line=dict(color=self.color_for_corequisites, width=2),
                        hoverinfo='skip' 
                      ))
                elif coreq in course_positions:
                  x0, y0, z0 = course_positions[coreq]
                  coreq_year = self.all_tracks_course_information[track][coreq]["year"] if coreq in self.all_tracks_course_information[track] else 0
                  coreq_semester = self.all_tracks_course_information[track][coreq]["semester"] if coreq in self.all_tracks_course_information[track] else 0
                  uid = f"inbetween_edges_corequisites_{year}_{semester}_{coreq_year}_{coreq_semester}_{course_year}_{course_semester}"
                  edge_traces.append(go.Scatter3d(
                    customdata=[f"edge_coreq_{course}_{coreq}"],
                    uid=uid,
                    x=[x0, x1],
                    y=[y0, y1],
                    z=[z0, z1],
                    mode='lines',
                    showlegend=False,
                    line=dict(color=self.color_for_corequisites, width=2),  
                    hoverinfo='skip'  
                  ))

    for edge_trace in edge_traces:
      fig.add_trace(edge_trace)

    for i in range(len(fig["data"])):
      if "customdata" in fig["data"][i]:
        if fig["data"][i]["customdata"] and "edge" in fig["data"][i]["customdata"][0]:
          fig["data"][i]["visible"] = False
          fig["data"][i]["line"]["color"] = "gray"
        elif "customdata" in fig["data"][i] and fig["data"][i]["customdata"] and fig["data"][i]["customdata"][0] not in self.all_tracks_course_information:
          fig["data"][i]["marker"]["color"] = "gray"

    if target_course == "None":
      fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        title=dict(
          text=f"Interactive Course Trajectory for {self.course_name.replace('_', ' ').title()}, {self.track.replace('_', ' ').title()}",
          font=dict(size=26, color="black", weight="bold"),
          y=0.98,
          x=0.5,
        ),
        legend=dict(
          title=dict(
            text=f"Legend: {self.track.replace('_', ' ').title()} Courses", 
            font=dict(size=16, weight="bold"),
          ),
          font=dict(size=11),
        ),
        scene=dict(
          aspectmode='cube',
          xaxis=dict(visible=False, range=[-3*self.radius_circle, 15*self.radius_circle], autorange=False),
          yaxis=dict(visible=False, range=[-3*self.radius_circle, 15*self.radius_circle], autorange=False),
          zaxis=dict(visible=False, range=[-3*self.radius_circle, 15*self.radius_circle], autorange=False),
          camera=last_camera_position
        ),
      )
      return fig
    
    already_in_legend = set()
    modified_path_to_target = {}
    for i in range(len(path_to_target)):
      source = path_to_target[i]["source"]
      destination = path_to_target[i]["destination"]
      relation = path_to_target[i]["relation"]
      if source in course_positions:
        x0, y0, z0 = course_positions[source]
      
      if destination in course_positions:
        x1, y1, z1 = course_positions[destination]

      source_course_desc, source_course_name = "", ""
      if source in self.all_tracks_course_information[track]:
        if "course_description" in self.all_tracks_course_information[track][source]:
          source_course_desc = self.__add_intermediate_br_tags(self.all_tracks_course_information[track][source]["course_description"])
        if "course_name" in self.all_tracks_course_information[track][source]:
          source_course_name = self.all_tracks_course_information[track][source]["course_name"]
      
      destination_course_desc, destination_course_name = "", ""
      if destination in self.all_tracks_course_information[track]:
        if "course_description" in self.all_tracks_course_information[track][destination]:
          destination_course_desc = self.__add_intermediate_br_tags(self.all_tracks_course_information[track][destination]["course_description"])
        if "course_name" in self.all_tracks_course_information[track][destination]:
          destination_course_name = self.all_tracks_course_information[track][destination]["course_name"]

      source_data = {
        "source": source,
        "source_course_name": source_course_name,
        "relation": relation,
        "year": int(self.all_tracks_course_information[track][source]["year"]) if source in self.all_tracks_course_information[track] else 0,
        "semester": int(self.all_tracks_course_information[track][source]["semester"]) if source in self.all_tracks_course_information[track] else 0,
      }
      if source_data["year"] not in modified_path_to_target:
        modified_path_to_target[source_data["year"]] = {}
      if source_data["semester"] not in modified_path_to_target[source_data["year"]]:
        modified_path_to_target[source_data["year"]][source_data["semester"]] = []
      if source_data not in modified_path_to_target[source_data["year"]][source_data["semester"]]:
        modified_path_to_target[source_data["year"]][source_data["semester"]].append(source_data)
      modified_path_to_target[source_data["year"]] = dict(sorted(modified_path_to_target[source_data["year"]].items()))

      destination_data = {
        "destination": destination,
        "destination_course_name": destination_course_name,
        "relation": relation,
        "year": int(self.all_tracks_course_information[track][destination]["year"]) if destination in self.all_tracks_course_information[track] else 0,
        "semester": int(self.all_tracks_course_information[track][destination]["semester"]) if destination in self.all_tracks_course_information[track] else 0,
      }
      if destination_data["year"] not in modified_path_to_target:
        modified_path_to_target[destination_data["year"]] = {}
      if destination_data["semester"] not in modified_path_to_target[destination_data["year"]]:
        modified_path_to_target[destination_data["year"]][destination_data["semester"]] = []
      if destination_data not in modified_path_to_target[destination_data["year"]][destination_data["semester"]]:
        modified_path_to_target[destination_data["year"]][destination_data["semester"]].append(destination_data)
      modified_path_to_target[destination_data["year"]] = dict(sorted(modified_path_to_target[destination_data["year"]].items()))

      if source not in already_in_legend:
        already_in_legend.add(source)
        fig.add_trace(go.Scatter3d(
          x=[x0],
          y=[y0],
          z=[z0],
          customdata=[source],
          mode='markers+text',
          hoverinfo='text', 
          showlegend=False,
          hovertext=source_course_desc,
          marker=dict(size=self.marker_size, color='red'),
          textfont=dict(size=12, color='black', weight="bold"),
          name=f"{source}-{source_course_name}" if source_course_name else source
        ))

      if destination not in already_in_legend:
        already_in_legend.add(destination)
        fig.add_trace(go.Scatter3d(
          x=[x1],
          y=[y1],
          z=[z1],
          customdata=[destination],
          mode='markers+text',
          hoverinfo='text', 
          hovertext=destination_course_desc,
          showlegend=False,
          marker=dict(size=self.marker_size, color='red'),
          textfont=dict(size=12, color='black', weight="bold"),
          name=f"{destination}-{destination_course_name}" if destination_course_name else destination
        ))
      
      if relation == "prerequisite":
        fig.add_trace(go.Scatter3d(
          x=[x0, x1],
          y=[y0, y1],
          z=[z0, z1],
          mode='lines',
          customdata=[f"edge_pre_{source}_{destination}"],
          showlegend=False,
          visible=True,
          line=dict(color=self.color_for_prerequisites, width=5),  
          hoverinfo='skip'  
        ))
      elif relation == "corequisite":
        fig.add_trace(go.Scatter3d(
          x=[x0, x1],
          y=[y0, y1],
          z=[z0, z1],
          mode='lines',
          customdata=[f"edge_coreq_{source}_{destination}"],
          showlegend=False,
          visible=True,
          line=dict(color=self.color_for_corequisites, width=5),  
          hoverinfo='skip'  
        ))

    modified_path_to_target = dict(sorted(modified_path_to_target.items()))
    complete_path_sorted = []
    for year in modified_path_to_target:
      if year == 0:
        year_name = "Pre-Knowledge Courses"
        if html.P(
            children=[year_name],
            style={"font-size": "0.8rem", "font-weight": "bold", "color": "black", "margin": "0rem"}
          ) not in complete_path_sorted:
          complete_path_sorted.append(
            html.P(
              children=[year_name],
              style={"font-size": "0.8rem", "font-weight": "bold", "color": "black", "margin": "0rem"}
            )
          )
        for course_data in modified_path_to_target[year][0]:
          if "source" in course_data:
            course_code = course_data["source"]
            course_name = course_data["source_course_name"]
            if html.P(
                children=[f"{course_code.upper()} {course_name.upper()}"],
                style={"font-size": "0.7rem", "color": "black", "margin": "0rem"}
              ) not in complete_path_sorted:
              complete_path_sorted.append(
                html.P(
                  children=[f"{course_code.upper()} {course_name.upper()}"],
                  style={"font-size": "0.7rem", "color": "black", "margin": "0rem"}
                )
              )
      else:
        year_name = f"Year {year}"
        if html.P(
            children=[year_name],
            style={"font-size": "0.8rem", "font-weight": "bold", "color": "black", "margin": "0rem"}
          ) not in complete_path_sorted:
          complete_path_sorted.append(
            html.P(
              children=[year_name],
              style={"font-size": "0.8rem", "font-weight": "bold", "color": "black", "margin": "0rem"}
            )
          )
        for semester in modified_path_to_target[year]:
          if semester != 0:
            semester_name = f"Semester {semester}"
          
          if html.P(
                children=[semester_name],
                style={"font-size": "0.8rem", "font-weight": "bold", "color": "black", "margin": "0rem"}
              ) not in complete_path_sorted:
            complete_path_sorted.append(
              html.P(
                children=[semester_name],
                style={"font-size": "0.8rem", "font-weight": "bold", "color": "black", "margin": "0rem"}
              )
            )

          for course_data in modified_path_to_target[year][semester]:
            if "source" in course_data:
              course_code = course_data["source"]
              course_name = course_data["source_course_name"]
              if html.P(
                  children=[f"{course_code.upper()}: {course_name.upper()}"],
                  style={"font-size": "0.7rem", "color": "black", "margin": "0rem"}
                ) not in complete_path_sorted:
                complete_path_sorted.append(
                  html.P(
                    children=[f"{course_code.upper()}: {course_name.upper()}"],
                    style={"font-size": "0.7rem", "color": "black", "margin": "0rem"}
                  )
                )

    complete_path_sorted.append(
      html.P(
        children=[f"{target_course.upper()} {self.all_tracks_course_information[track][target_course]['course_name'].upper()}"],
        style={"font-size": "0.7rem", "color": "black", "margin": "0rem"}
      )
    )
    fig.update_layout(
      margin=dict(l=0, r=0, t=0, b=0),
      title=dict(
        text=f"Interactive Course Trajectory for {self.course_name.replace('_', ' ').title()}, {self.track.replace('_', ' ').title()}<br />Target Course: {target_course}",
        font=dict(size=26, color="black", weight="bold"),
        y=0.96,
        x=0.5,
      ),
      legend=dict(
        title=dict(
          text=f"Legend: {self.track.replace('_', ' ').title()} Courses", 
          font=dict(size=16, weight="bold"),
        ),
        font=dict(size=11),
      ),
      scene=dict(
        aspectmode='cube',
        xaxis=dict(visible=False, range=[-3*self.radius_circle, 15*self.radius_circle], autorange=False),
        yaxis=dict(visible=False, range=[-3*self.radius_circle, 15*self.radius_circle], autorange=False),
        zaxis=dict(visible=False, range=[-3*self.radius_circle, 15*self.radius_circle], autorange=False),
        camera=last_camera_position
      ),
    )

    return fig, complete_path_sorted
  

  def run(self,
          track: str,
          target_course: str,
          last_camera_position: dict) -> go.Figure:
    """
    Generate a 3d graph of the course catalog.
    
    Args:
      - track (str): The track for which the course trajectory is to be generated.
      - target_course (str): The target course.
    
    Returns:
      - go.Figure: The 3D graph of the course trajectory to the target course.
    """

    if target_course not in self.all_tracks_course_information[track] and target_course != "None":
      return None, []
    
    else:

      self.track = track
      if target_course != "None":
        path_to_target = self.all_tracks_course_information[track][target_course]["complete_path"]
      else:
        path_to_target = []

      return self.__develop_path_to_target(
        track=track,
        target_course=target_course,
        path_to_target=path_to_target,
        last_camera_position=last_camera_position
      )