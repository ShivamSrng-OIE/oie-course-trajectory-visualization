import pymongo
from consts import MondoDBConsts


class DatabaseHandler:
  def __init__(self) -> None:
    mongo_db_consts = MondoDBConsts().get_constants()
    pymongo_client = pymongo.MongoClient(
      host=mongo_db_consts["host"],
    )
    self.courses_catalog_db = pymongo_client["courses_catalog"]
    self.courses_track_db = pymongo_client["courses_track_information"]
    self.__setup_meta_data()
  

  def __setup_meta_data(self) -> None:
    """
    Set up the meta data for the database.
    
    Args:
      - None
    
    Returns:
      - None
    """
    
    courses_catalog_collection = self.courses_catalog_db.list_collection_names()
    courses_track_information_collection = self.courses_track_db.list_collection_names()
    courses_catalog_collection.sort()
    courses_track_information_collection.sort()

    if courses_catalog_collection == courses_track_information_collection:
      self.dict_track_count_per_course = {}

      self.courses_catalog_cnt = len(courses_catalog_collection)
      self.courses_catalog_collection = courses_catalog_collection

      for course_name in courses_catalog_collection:
        self.dict_track_count_per_course[course_name] = self.courses_track_db[course_name].count_documents({})


  def get_tracks_count_per_course(self) -> dict:
    """
    Get the tracks count per course.
    
    Args:
      - None
    
    Returns:
      - dict: The dictionary of tracks count per course.
    """
    
    return self.dict_track_count_per_course
  

  def get_courses_catalog(self) -> list:
    """
    Get the courses catalog.
    
    Args:
      - None
    
    Returns:
      - list: The list of courses catalog.
    """
    
    return self.courses_catalog_collection
  

  def get_course_catalog_information(self,
                                     course_name: str) -> dict:
    """
    Get the course catalog information.
    
    Args:
      - course_name (str): The name of the course
    
    Returns:
      - dict: The course catalog information for the course
    """

    if course_name not in self.courses_catalog_collection:
      return {}
    
    course_catalog = {}
    for idx, course in enumerate(self.courses_catalog_db[course_name].find(), start=1):
      del course["_id"]
      course_catalog[f"track_{idx}"] = course

    return course_catalog
  

  def get_course_track_information(self,
                                   course_name: str) -> dict:
    """
    Get the course track information.

    Args:
      - course_name (str): The name of the course
    
    Returns:
      - dict: The course track information for the course
    """

    if course_name not in self.courses_catalog_collection:
      return {}
    
    all_tracks_in_course_information = {}
    for idx, track in enumerate(self.courses_track_db[course_name].find(), start=1):
      del track["_id"]
      all_tracks_in_course_information[f"track_{idx}"] = track
    
    return all_tracks_in_course_information