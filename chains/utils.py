import os

from pandasai.llm import GoogleGemini


def get_llm():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ""
    os.environ['GOOGLE_API_KEY'] = "AIzaSyAeIUyv8WWZlzq3FhEMhJ_VXoSq7nqukCE"
    return GoogleGemini(api_key= "AIzaSyAeIUyv8WWZlzq3FhEMhJ_VXoSq7nqukCE" ,model="gemini-1.5-flash",temperature=0, seed=32)