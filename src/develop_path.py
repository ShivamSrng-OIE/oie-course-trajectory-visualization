import os
import numpy as np
import  plotly.io as pio
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
    self.z_increment = course_trajectory_consts["z_increment"]
    self.left_shift = course_trajectory_consts["left_shift"]
    self.radius_circle = course_trajectory_consts["radius_circle"]
    self.marker_size = course_trajectory_consts["marker_size"]
    self.special_marker_size = course_trajectory_consts["special_marker_size"]
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
  

  def __develop_path_to_target(self,
                               track: str,
                               target_course: str,
                               path_to_target: list) -> go.Figure:
    """
    Create a 3D graph of the course trajectory for a particular track.
    
    Args:
      - track (str): The track for which the course trajectory is to be generated.
      - target_course (str): The target course.
      - path_to_target (list): The path to the target course.

    Returns:
      - go.Figure: The 3D graph of the course trajectory.
    """

    if not os.path.exists(f"data/{self.course_name}/{track}/computed_path"):
      os.makedirs(f"data/{self.course_name}/{track}/computed_path")
    
    if not os.path.exists(f"data/{self.course_name}/{track}/computed_path/{target_course}"):
        os.makedirs(f"data/{self.course_name}/{track}/computed_path/{target_course}")
    else:
      if os.path.exists(f"data/{self.course_name}/{track}/computed_path/{target_course}/path_to_{target_course}.json"):
        with open(f"data/{self.course_name}/{track}/computed_path/{target_course}/path_to_{target_course}.json", "r") as file:
          fig = pio.from_json(file.read())
        return fig

    courses = self.course_catalog[track]
    fig = go.Figure()
    semester_colors = self.__dynamic_color_choice_for_semester(courses)
    course_positions, course_colors = {}, {}
    
    taught_courses = set()
    for year in courses:
      if year == "extra_course_related_info":
        continue
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
        x, y, z = self.__create_circle(n_courses, z_level)
        course_colors.update({course: semester_colors[(year, semester)] for course in courses_in_semester})
            
        fig.add_trace(go.Scatter3d(
          x=[0],
          y=[0],
          z=[z_level],
          text=f"Year: {year}, Semester: {semester}",
          mode='text',
          showlegend=False,
          textposition='middle center',
          textfont=dict(size=14, color='black', family="Arial", weight="bold"),
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
              hoverinfo='text',  
              marker=dict(size=self.special_marker_size, color="gray"),
              textfont=dict(size=14, color='black', family="Arial", weight="bold"),
              textposition='top center',
              hovertext=course_desc + f"<br><br>Dependencies: {self.all_tracks_course_information[track][course]['dependency_count']}",
              name=f"{course}- {course_name}" if course_name else course
            ))
          else:
            fig.add_trace(go.Scatter3d(
              x=[x[i]],
              y=[y[i]],
              z=[z[i]],
              text=course,  
              mode='markers+text',
              hoverinfo='text',  
              marker=dict(size=self.marker_size, color="gray"),
              textfont=dict(size=14, color='black', family="Arial", weight="bold"),
              textposition='top center',
              hovertext=course_desc,
              name=f"{course}- {course_name}" if course_name else course
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
              hoverinfo='skip'  
          ))
          fig.add_trace(go.Scatter3d(
          x=[0 + left_shift],
          y=[0],
          z=[semester_elevation],
          text="Pre-Knowledge Courses",
          mode='text',
          showlegend=False,
          textfont=dict(size=14, color='black', family="Arial", weight="bold"),
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
              text=prereq,
              mode='markers+text',
              hoverinfo='text',  
              hovertext=course_desc + f"<br><br>Dependencies: {self.all_tracks_course_information[prereq]['dependency_count']}",
              marker=dict(size=self.special_marker_size, color='#000000'),
              textfont=dict(size=14, color='black', family="Arial", weight="bold"),
              name=f"{prereq}- {course_name}" if course_name else prereq
          ))
      else:
          fig.add_trace(go.Scatter3d(
              x=[x],
              y=[y],
              z=[z],
              text=prereq,
              mode='markers+text',
              hoverinfo='text', 
              hovertext=course_desc,
              marker=dict(size=self.marker_size, color='#000000'),
              textfont=dict(size=14, color='black', family="Arial", weight="bold"),
              name=f"{prereq}- {course_name}" if course_name else prereq
          ))

    for year in courses:
      if year == "extra_course_related_info":
        continue
      for semester in courses[year]:
        courses_in_semester = list(courses[year][semester].keys())

        for course in courses_in_semester:
          x1, y1, z1 = course_positions[course]
          if 'prerequisites' in courses[year][semester][course]:
            for prereq in courses[year][semester][course]['prerequisites']:
              if isinstance(prereq, list):
                for sub_prereq_list in prereq:
                  if isinstance(sub_prereq_list, list):
                    for sub_prereq in sub_prereq_list:
                      if sub_prereq in course_positions:
                        x0, y0, z0 = course_positions[sub_prereq]
                        fig.add_trace(go.Scatter3d(
                          x=[x0, x1],
                          y=[y0, y1],
                          z=[z0, z1],
                          mode='lines',
                          showlegend=False,
                          line=dict(color='gray', width=2),  
                          hoverinfo='skip'  
                        ))
                  elif sub_prereq_list in course_positions:
                    x0, y0, z0 = course_positions[sub_prereq_list]
                    fig.add_trace(go.Scatter3d(
                      x=[x0, x1],
                      y=[y0, y1],
                      z=[z0, z1],
                      mode='lines',
                      showlegend=False,
                      line=dict(color='gray', width=2), 
                      hoverinfo='skip' 
                    ))
              elif prereq in course_positions:
                x0, y0, z0 = course_positions[prereq]
                fig.add_trace(go.Scatter3d(
                  x=[x0, x1],
                  y=[y0, y1],
                  z=[z0, z1],
                  mode='lines',
                  showlegend=False,
                  line=dict(color='gray', width=2),  
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
                          fig.add_trace(go.Scatter3d(
                            x=[x0, x1],
                            y=[y0, y1],
                            z=[z0, z1],
                            mode='lines',
                            showlegend=False,
                            line=dict(color='gray', width=2), 
                            hoverinfo='skip'  
                          ))
                    elif sub_coreq in course_positions:
                      x0, y0, z0 = course_positions[sub_coreq]
                      fig.add_trace(go.Scatter3d(
                        x=[x0, x1],
                        y=[y0, y1],
                        z=[z0, z1],
                        mode='lines',
                        showlegend=False,
                        line=dict(color='gray', width=2),
                        hoverinfo='skip' 
                      ))
                elif coreq in course_positions:
                  x0, y0, z0 = course_positions[coreq]
                  fig.add_trace(go.Scatter3d(
                    x=[x0, x1],
                    y=[y0, y1],
                    z=[z0, z1],
                    mode='lines',
                    showlegend=False,
                    line=dict(color='gray', width=2),  
                    hoverinfo='skip'  
                  ))

    already_in_legend = set()
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
      
      if source not in already_in_legend:
        already_in_legend.add(source)
        fig.add_trace(go.Scatter3d(
          x=[x0],
          y=[y0],
          z=[z0],
          mode='markers+text',
          hoverinfo='text', 
          hovertext=source_course_desc,
          marker=dict(size=self.marker_size, color='red'),
          textfont=dict(size=14, color='black', family="Arial", weight="bold"),
          name=f"{source}-{source_course_name}" if source_course_name else source
        ))

      if destination not in already_in_legend:
        already_in_legend.add(destination)
        fig.add_trace(go.Scatter3d(
          x=[x1],
          y=[y1],
          z=[z1],
          mode='markers+text',
          hoverinfo='text', 
          hovertext=destination_course_desc,
          marker=dict(size=self.marker_size, color='red'),
          textfont=dict(size=14, color='black', family="Arial", weight="bold"),
          name=f"{destination}-{destination_course_name}" if destination_course_name else destination
        ))
      
      if relation == "prerequisite":
        fig.add_trace(go.Scatter3d(
          x=[x0, x1],
          y=[y0, y1],
          z=[z0, z1],
          mode='lines',
          showlegend=False,
          line=dict(color='blue', width=5),  
          hoverinfo='skip'  
        ))
      elif relation == "corequisite":
        fig.add_trace(go.Scatter3d(
          x=[x0, x1],
          y=[y0, y1],
          z=[z0, z1],
          mode='lines',
          showlegend=False,
          line=dict(color='green', width=5),  
          hoverinfo='skip'  
        ))

    fig.update_layout(
      scene=dict(
        aspectmode='cube',
        xaxis=dict(visible=False, range=[-3*self.radius_circle, 8*self.radius_circle], autorange=False),
        yaxis=dict(visible=False, range=[-3*self.radius_circle, 8*self.radius_circle], autorange=False),
        zaxis=dict(visible=False, range=[-3*self.radius_circle, 8*self.radius_circle], autorange=False),
        camera=dict(
            eye=dict(x=1, y=1, z=1),  
            up=dict(x=0, y=0, z=1),  
            projection=dict(type='orthographic')
        ),
      ),
      title=f"3D Course Graph with Path to Target Course: {path_to_target[-1]['destination']}",
      title_font=dict(size=30, family="Arial", color="black", weight="bold"),
      width=2000,
      height=1050
    )

    fig.write_html(f"data/{self.course_name}/{track}/computed_path/{target_course}/path_to_{target_course}.html")
    fig.write_json(f"data/{self.course_name}/{track}/computed_path/{target_course}/path_to_{target_course}.json")
    return fig
  

  def run(self,
          track: str,
          target_course: str) -> go.Figure:
    """
    Generate a 3d graph of the course catalog.
    
    Args:
      - track (str): The track for which the course trajectory is to be generated.
      - target_course (str): The target course.
    
    Returns:
      - go.Figure: The 3D graph of the course trajectory to the target course.
    """

    if target_course not in self.all_tracks_course_information[track]:
      print(f"Target course {target_course} not found in the track {track}")
      return None
    else:
      path_to_target = self.all_tracks_course_information[track][target_course]["complete path"]
      return self.__develop_path_to_target(
        track=track,
        target_course=target_course,
        path_to_target=path_to_target
      )