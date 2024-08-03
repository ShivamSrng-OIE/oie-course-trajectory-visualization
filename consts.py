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