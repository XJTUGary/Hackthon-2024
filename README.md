### README: Invoice Information Extraction and Compliance Verification System

---

# Invoice Information Extraction and Compliance Verification System

## Overview

This project is designed to extract key information from invoices and verify their compliance with company policies and relevant legal regulations. The system leverages state-of-the-art natural language processing (NLP) techniques and machine learning models to automate the entire process, ensuring accuracy and efficiency. Additionally, the system features an interactive chatbot interface, allowing users to inquire about invoice details and company reimbursement policies, with support for generating visual representations in responses.

## Key Features

- **Invoice Information Extraction**: Automatically extracts key details such as vendor, date, item descriptions, quantities, unit prices, and total amounts from invoice images or digital documents.
  
- **Compliance Verification**: Checks extracted invoice data against company policies and legal regulations to identify any potential discrepancies or non-compliance issues.

- **Interactive Chatbot Interface**: Users can interact with the system via a chatbot to query invoice details, seek clarification on company policies, or ask general questions about the reimbursement process. The chatbot is capable of generating and displaying images in the responses for better clarity.

- **Advanced NLP and AI Integration**: Utilizes LangChain for sequential task processing, Google Vertex AI for model training and inference, and Streamlit for building an intuitive user interface.

## Project Structure

```plaintext
|-- .streamlit/                  # Streamlit configuration directory
|   |-- config.toml              # Streamlit configuration file
|-- assets/                      # Directory for storing assets (e.g., images, icons)
|-- config/                      # Configuration files directory
|   |-- config.toml              # Main configuration file
|-- docs/                        # Documentation directory
|   |-- images/                  # Images for documentation
|   |-- inference/               # Inference-related documents or files
|   |-- json/                    # JSON files related to the project
|-- tools/                       # Utility scripts and styles
|   |-- style.css                # CSS for styling the Streamlit app
|   |-- utilities.py             # Utility functions
|-- views/                       # Directory for different views in the Streamlit app
|   |-- chat.py                  # Chatbot interface script
|   |-- dashboard.py             # Dashboard view script
|   |-- data_inference.py        # Script for data inference
|   |-- data_review.py           # Script for reviewing data
|-- .gitignore                   # Git ignore file
|-- config.py                    # Configuration script
|-- Dockerfile                   # Dockerfile for containerizing the application
|-- favicon.ico                  # Favicon for the application
|-- invoice_compliance.py        # Script for invoice compliance checking
|-- LICENSE                      # License file
|-- README.MD                    # Project documentation
|-- requirements.txt             # Python dependencies
|-- main.py                      # Main entry point for the application               
```

## Technologies Used

- **Python**: The primary programming language used for the project.
- **LangChain**: A framework for building customizable task pipelines for NLP applications.
- **Google Vertex AI**: A platform for training, deploying, and managing machine learning models.
- **Streamlit**: A framework for building and deploying interactive web applications.
- **Pandas**: For data manipulation and analysis.

## Installation

To set up the project on your local machine, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/XJTUGary/Hackthon-2024.git
   cd Hackthon-2024
   ```

2. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API keys**:

   Create a `.env` file in the root directory with your API keys:

   ```plaintext
   GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
   ```

## Usage

1. **Data Preparation**: Store your invoice images and policy documents in the `docs/` directory.

2. **Running Invoice Extraction**:

   To extract information from invoice images:

   ```bash
   python src/invoice_extraction.py --input data/invoices/ --output results/invoice_data.csv
   ```

3. **Compliance Verification**:

   To check the extracted invoice data for compliance:

   ```bash
   python src/compliance_check.py --input results/invoice_data.csv --output results/compliance_report.csv
   ```

4. **Interactive Chatbot**:

   To start the chatbot interface:

   ```bash
   streamlit run main.py
   ```

   The chatbot will be accessible in your browser, allowing you to interact with the system, ask questions, and get visual explanations.

## Example Use Cases

- **Automated Invoice Auditing**: Streamline the auditing process by automatically extracting and verifying invoice data.
- **Policy Compliance Monitoring**: Ensure all invoices comply with internal policies and external regulations.
- **Employee Support**: Provide employees with an easy-to-use interface to query reimbursement policies and get answers to invoice-related questions.


## Contributing

We welcome contributions from the community! Please read our [contributing guidelines](CONTRIBUTING.md) for more information on how to get involved.

## License

This project is licensed under the MIT License. See the [LICENSE](https://www.apache.org/licenses/) file for details.

## Acknowledgments

- Thanks to the developers of LangChain, Google Vertex AI, and Streamlit for providing the tools that power this project.
- Special recognition to the open-source community for their continuous contributions and innovations.

## Contact

For any questions or suggestions, please contact:


