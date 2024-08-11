from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')


class CourseTrajectoryConsts:
  def __init__(self) -> None:
    pass


  def __perform_prechecks(self) -> dict:
    """
    Perform prechecks before generating the 3d graph.
    
    Args:
      - None
    
    Returns:
      - dict: The dictionary of constants after performing the prechecks.
    """
    
    course_trajectory_consts = config["3D_COURSE_TRAJECTORY_CONSTS"]
    return {
      "z_level": course_trajectory_consts.getint("z_level"),
      "z_increment": course_trajectory_consts.getint("z_increment"),
      "marker_size": course_trajectory_consts.getint("marker_size"),
      "radius_circle": course_trajectory_consts.getint("radius_circle"),
      "special_marker_size": course_trajectory_consts.getint("special_marker_size"),
      "color_for_corequisites": course_trajectory_consts.get("color_for_corequisites"),
      "color_for_prerequisites": course_trajectory_consts.get("color_for_prerequisites"),
      "complete_path_to_top": course_trajectory_consts.getboolean("complete_path_to_top"),
      "complete_path_from_start": course_trajectory_consts.getboolean("complete_path_from_start"),
      "critical_courses_threshold": course_trajectory_consts.getint("critical_courses_threshold"),
      "critical_courses_threshold_circle" : course_trajectory_consts.getint("critical_courses_threshold_circle"),
      "left_shift": course_trajectory_consts.getfloat("left_shift_multiplier") * course_trajectory_consts.getint("radius_circle"),
    }
  

  def get_course_trajectory_consts(self) -> dict:
    """
    Get the course trajectory constants.
    
    Args:
      - None
    
    Returns:
      - dict: The dictionary of constants.
    """
    
    return self.__perform_prechecks()


class MondoDBConsts:
  """
  A class to store the constants for the MongoDB database
  """
  
  def __init__(self) -> None:
    self.config = config["MONGODB_CONSTS"]


  def get_constants(self) -> dict:
    """
    Returns the constants for the MongoDB database
    
    Args:
      - None
    
    Returns:
      - dict: The constants for the MongoDB database
    """
    
    username = self.config.get("username")
    password = self.config.get("password")
    cluster = self.config.get("cluster")
    host = f"mongodb+srv://{username}:{password}@{cluster}.e00xjor.mongodb.net/"

    return {
      "host": host,
    }


class GeminiConstants:
  """
  A class to store the constants for the Gemini API
  """

  def __init__(self) -> None:
    self.config = config["GEMINI_CONSTS"]


  def get_constants(self) -> dict:
    """
    Returns the constants for the Gemini API
    
    Args:
      - None
    
    Returns:
      - dict: The constants for the Gemini API
    """
    
    api_key = self.config.get("api_key")
    model_name = self.config.get("model_name")
    model_temperture = self.config.getint("model_temperture")
    prompt_for_advisor = self.config.get("prompt_for_advisor")
    prompt_for_classifying_track = self.config.get("prompt_for_classifying_track")
    prompt_for_extracting_track_info = self.config.get("prompt_for_extracting_track_info")
    prompt_extracting_year_semester_information = self.config.get("prompt_extracting_year_semester_information")
    prompt_for_initial_course_recommendation = self.config.get("prompt_for_initial_course_recommendation")

    return {
      "api_key": api_key,
      "model_name": model_name,
      "model_temperture": model_temperture,
      "prompt_for_advisor": prompt_for_advisor,
      "prompt_for_classifying_track": prompt_for_classifying_track,
      "prompt_for_extracting_track_info": prompt_for_extracting_track_info,
      "prompt_extracting_year_semester_information": prompt_extracting_year_semester_information,
      "prompt_for_initial_course_recommendation": prompt_for_initial_course_recommendation,
    }
  