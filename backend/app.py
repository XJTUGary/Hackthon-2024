import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from backend.gemini_worker import GeminiInvoiceWorker


app = Flask(__name__)
app.json.sort_keys = False


@app.route('/', methods=['GET'])
def index():
    return 'welcome to hackathon webpage!'


@app.route('/invoice_process', methods=['POST'])
def invoice_cls_ner_review():
    image = request.files['invoice']
    invoice_processor = GeminiInvoiceWorker(genai=genai)
    result = invoice_processor.process(image)
    return jsonify(result)


if __name__ == "__main__":
    print("config gemini")
    os.environ["GOOGLE_API_KEY"] = "AIzaSyBmh0EHQb3krLfUIZ7BC_Cgn2bu1URmqGM"
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"), transport='rest')

    print("Starting hackathon backend")
    app.run(port=8080, host="127.0.0.1", debug=True)
