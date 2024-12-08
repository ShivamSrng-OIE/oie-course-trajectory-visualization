from consts import GeminiConstants
import google.generativeai as genai


class GeminiInterfacing:
  """
  This class is responsible for interfacing with the Google Gemini model.
  """
  
  def __init__(self) -> None:
    self.__initiliaze_gemini_model()


  def __initiliaze_gemini_model(self) -> None:
    """
    To initialize the Google Gemini model.

    Args:
      - None
    
    Returns:
      - None
    """

    gemini_consts = GeminiConstants().get_constants()

    genai.configure(
      api_key=gemini_consts["api_key"]
    )
    gemini_model = genai.GenerativeModel(
      model_name=gemini_consts["model_name"],
      generation_config={
        "temperature": gemini_consts["model_temperture"],
        "response_mime_type": "application/json"
      }
    )
    
    university_advisor_assistant_model = gemini_model.start_chat(
      history=[]
    )
    university_advisor_assistant_model.send_message(
      content=gemini_consts["prompt_for_advisor"]
    )
    track_extraction_model = gemini_model.start_chat(
      history=[]
    )
    track_extraction_model.send_message(
      content=gemini_consts["prompt_for_classifying_track"]
    )
    initial_course_recommendation_model = gemini_model.start_chat(
      history=[]
    )
    initial_course_recommendation_model.send_message(
      content=gemini_consts["prompt_for_initial_course_recommendation"]
    )

    self.gemini_models = {
      "university_advisor_assistant_model": university_advisor_assistant_model,
      "track_extraction_model": track_extraction_model,
      "initial_course_recommendation_model": initial_course_recommendation_model
    }


  def formulate_gemini_response(self, 
                                model: genai.GenerativeModel, 
                                data: str) -> dict:
    """
    To formulate the response from the Google Gemini model, into a structured JSON 
    format.

    Args:
      - model (google.generativeai.GenerativeModel): The Google Gemini model
      - data (str): The data to be sent to the Google Gemini model
    
    Returns:
      - dict: The structured JSON response from the Google Gemini model
    """

    try:
      gemini_model_response = str(
        object=self.gemini_models[model].send_message(
          content=data
        ).text
      ).replace("```", "").replace("json", "")
      
      response = eval(gemini_model_response)
      return response
    except Exception as e:
      return [-1]