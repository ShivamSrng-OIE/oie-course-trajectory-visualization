import numpy as np
import plotly.graph_objects as go
from warnings import filterwarnings
from consts import CourseTrajectoryConsts


filterwarnings("ignore")


class PreCoRequisiteHighlight:
  """
  The PreCoRequisiteHighlight class is used to highlight the prerequisites and corequisites of a course.
  """
  

  def __init__(self,
               course_name: str,
               course_catalog: dict,
               all_tracks_course_information: dict) -> None:
    """
    Initialize the PreCoRequisiteHighlight class.
    
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
      if year == "extra_course_related_info":
        continue
      semester_colors[int(year)] = {}
      for semester in courses_in_year[year]:
        semester_colors[int(year)][int(semester)] = f"hsl({cnt * (360 // (len(courses_in_year) * len(courses_in_year[year])))}, 70%, 50%)"
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

    theta = np.linspace(
      start=0,
      stop=2*np.pi, 
      num=n_points,
      endpoint=False
    )
    x = self.radius_circle * np.cos(theta)
    y = self.radius_circle * np.sin(theta) 
    z = np.full_like(x, z_level)
    
    return x, y, z
  

  def __create_random_points_on_circle(self, z_level, num_points, angle_offset=0):
    theta = np.linspace(0, 2 * np.pi, num_points) + angle_offset
    x = self.radius_circle * np.cos(theta)
    y = self.radius_circle * np.sin(theta)
    z = np.full(num_points, z_level)
    return x.tolist(), y.tolist(), z.tolist()
  

  def __grayed_out_graph(self,
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
  

  def __perform_highlight_to_target(self,
                                    track: str,
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
    semester_colors = self.__grayed_out_graph(
      courses_in_year=courses
    )
    colored_semester = self.__dynamic_color_choice_for_semester(
      courses_in_year=courses
    )
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
              uid=f"course_{year}_{semester}_{course}",
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
              uid=f"course_{year}_{semester}_{course}",
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
          circle_x, circle_y, circle_z = self.__create_circle(100, z_level)
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
          circle_x, circle_y, circle_z = self.__create_circle(100, z_level)
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
                        if sub_prereq not in taught_courses and sub_prereq not in unique_prereqs:
                          unique_prereqs.append(sub_prereq)
                          unique_prereqs_complete_info.append([sub_prereq, int(year), int(semester), semester_elevation[year][semester]])
                    elif prereq not in taught_courses and prereq not in unique_prereqs:
                        unique_prereqs.append(prereq)
                        unique_prereqs_complete_info.append([prereq, int(year), int(semester), semester_elevation[year][semester]])
                else:
                  if item not in taught_courses and item not in unique_prereqs:
                    unique_prereqs.append(item)
                    unique_prereqs_complete_info.append([item, int(year), int(semester), semester_elevation[year][semester]])
            else:
              if prerequisites_data not in taught_courses and prerequisites_data not in unique_prereqs:
                unique_prereqs.append(prerequisites_data)
                unique_prereqs_complete_info.append([prerequisites_data, int(year), int(semester), semester_elevation[year][semester]])

    unique_prereqs.sort()
    unique_prereqs_complete_info.sort(key=lambda x: x[0])
    left_shift = self.left_shift
    already_present_semester_circle = []
    course_cnt, critical_course_cnt = 0, 0

    for i, prereq in enumerate(unique_prereqs):
      prerequisites_data, year, semester, semester_elevation = unique_prereqs_complete_info[i]
      if unique_prereqs_complete_info[i][1] == 1 and unique_prereqs_complete_info[i][2] == 1:
          semester_elevation = -self.z_increment
          left_shift = 0
      else:
          semester_elevation = semester_elevation - 2* self.z_increment
          left_shift = self.left_shift
      
      x = external_radius * np.cos(2 * np.pi * i / len(unique_prereqs)) + left_shift
      y = external_radius * np.sin(2 * np.pi * i / len(unique_prereqs))
      z = semester_elevation
      course_cnt += 1

      if [year, semester] not in already_present_semester_circle:
          already_present_semester_circle.append([year, semester])
          circle_x, circle_y, circle_z = self.__create_circle(100, semester_elevation)
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
              uid=f"course_{year}_{semester}_{prereq}",
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
              uid=f"course_{year}_{semester}_{prereq}",
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

    fig.add_traces(edge_traces)

    for data in fig.data:
      if str(data.uid).startswith("course"):
        fig_year, fig_semester = str(data.uid).split("_")[1], str(data.uid).split("_")[2]
        if int(fig_year) == int(self.year) and int(fig_semester) == int(self.semester):
          data.marker.color = colored_semester[int(fig_year)][int(fig_semester)]

      if str(data.uid).startswith("inbetween_edges"):
        fig_year, fig_semester = str(data.uid).split("_")[-2], str(data.uid).split("_")[-1]

        if self.direction == "bottom":
          bool_comparision = int(fig_year) < int(self.year)
          nested_bool_comparision = int(fig_year) == int(self.year) and int(fig_semester) <= int(self.semester)
        elif self.direction == "top":
          bool_comparision = int(fig_year) > int(self.year)
          nested_bool_comparision = int(fig_year) == int(self.year) and int(fig_semester) >= int(self.semester)

        if str(data.uid).endswith(f"{self.year}_{self.semester}") or bool_comparision:
          data.visible = True
          data.line.width = 5
        elif nested_bool_comparision:
          data.visible = True
          data.line.width = 5
        else:
          data.visible = False
          data.line.width = 0


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
        bordercolor="black",
        borderwidth=1,
        yanchor="top",
        xanchor="right",
        y=0.80,
        x=0.99,
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

  def run(self,
          track: str,
          year: int,
          semester: int,
          direction: str,
          last_camera_position: dict) -> go.Figure:
    """
    Perform the highlighting of the prerequisites and corequisites.
    
    Args:
      - track (str): The track for which the course trajectory is to be generated.
      - year (int): The year.
      - semester (int): The semester.
      - direction (str): The direction.
      - last_camera_position (dict): The last camera position.
    
    Returns:
      - go.Figure: The 3D graph of the course trajectory.
    """

    self.track = track
    self.year, self.semester, self.direction = year, semester, direction
    fig = self.__perform_highlight_to_target(
      track=track,
      last_camera_position=last_camera_position
    )
    return fig