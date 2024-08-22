import os
import re
import json
import pandas as pd
from io import BytesIO
from PIL import Image
import google.generativeai as genai


class GeminiWorker:

    def __init__(self, genai):
        self.text_model = genai.GenerativeModel("gemini-1.5-pro")
        self.multimodal_model = genai.GenerativeModel("gemini-1.5-pro-001")
        self.multimodal_model_flash = genai.GenerativeModel("gemini-1.5-flash-001")

        gemini_prompts_df = pd.read_csv(
            os.path.join(os.path.dirname(__file__), 'config', 'gemini-prompts.csv'),
            encoding_errors='ignore')
        self.role_prompts = {r: p for r, p in zip(gemini_prompts_df['act'], gemini_prompts_df['prompt'])}

    def process(self, *args):
        raise NotImplementedError


class GeminiInvoiceWorker(GeminiWorker):

    def __init__(self, genai):
        super().__init__(genai=genai)

    def process(self, image):
        image = Image.open(BytesIO(image.read()))

        response = self.multimodal_model_flash.generate_content([self.role_prompts['invoice_classifier'], image])
        doc_classification = response.text.strip()
        print(doc_classification)

        response = self.multimodal_model_flash.generate_content([self.role_prompts['invoice_extractor'], image])
        doc_extraction = response.text.strip()
        print("\n-------Extracted Entities--------")
        doc_extraction = doc_extraction.replace('```json', '').replace('```', '').strip()
        doc_extraction = json.loads(doc_extraction)
        doc_extraction.update(doc_extraction['other_info'])
        del doc_extraction['other_info']
        doc_extraction['invoice_type'] = doc_classification
        print(doc_extraction)

        return doc_extraction


# class GeminiRAGPolicyQA(GeminiWorker):
#
#     def __init__(self, text_metadata_df, image_metadata_df):
#         super().__init__(genai=genai)
#         self.text_metadata_df = text_metadata_df
#         self.image_metadata_df = image_metadata_df
#
#     def get_docs_metadata(self, doc_folder):
#         # Extract text and image metadata from the PDF document
#         self.text_metadata_df, self.image_metadata_df = get_document_metadata(
#             self.multimodal_model,  # we are passing Gemini 1.5 Pro model
#             doc_folder,
#             image_save_dir="images",
#             image_description_prompt=self.role_prompts['image_description'],
#             embedding_size=1408,
#             # add_sleep_after_page = True, # Uncomment this if you are running into API quota issues
#             # sleep_time_after_page = 5,
#             # generation_config = # see next cell
#             # safety_settings =  # see next cell
#         )
#
#         print("\n\n --- Completed processing. ---")
#         print(self.text_metadata_df.head())
#         print(self.image_metadata_df.head())
#
#     def process(self, query):
#         matching_results_text = get_similar_text_from_query(
#             query,
#             self.text_metadata_df,
#             column_name="text_embedding_chunk",
#             top_n=3,
#             chunk_text=True,
#         )
#
#         # # Print the matched text citations
#         # print_text_to_text_citation(matching_results_text, print_top=False, chunk_text=True)
#         print("\n **** Result: ***** \n")
#
#         # All relevant text chunk found across documents based on user query
#         context = "\n".join(
#             [value["chunk_text"] for key, value in matching_results_text.items()]
#         )
#
#         instruction = f"""Answer the question with the given context.
#         If the information is not available in the context, just return "not available in the context".
#         Question: {query}
#         Context: {context}
#         Answer:
#         """
#
#         # Prepare the model input
#         model_input = instruction
#
#         # Generate Gemini response with streaming output
#         get_gemini_response(
#             self.text_model,  # we are passing Gemini 1.0 Pro
#             model_input=[model_input],
#             stream=True,
#             generation_config=genai.GenerationConfig(temperature=0.2),
#         )


if __name__ == "__main__":
    os.environ["GOOGLE_API_KEY"] = "AIzaSyBmh0EHQb3krLfUIZ7BC_Cgn2bu1URmqGM"

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"), transport='rest')

    llmer = GeminiInvoiceCLSNERWorker(genai=genai)
    llmer.process('data/japan_hotel.jpg')