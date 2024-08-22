import os
from langchain_google_vertexai import VertexAI, VertexAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Weaviate
import weaviate
from weaviate.embedded import EmbeddedOptions
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.chains import RetrievalQA
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field


class InvoiceComplianceChecker:
    """
    A class to handle the process of checking invoice compliance with given policies.
    """

    def __init__(self, model_name: str, credentials_path: str, document_path: str):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        self.model = VertexAI(model_name=model_name, api_transport='rest')
        self.documents = self._load_documents(document_path)
        self.embeddings = self._get_embeddings()
        self.vectorstore = self._get_vectorstore()
        self.retriever = self.vectorstore.as_retriever()
        self.parser = self._get_compliance_parser()

    def _load_documents(self, path: str):
        loader = TextLoader(path, encoding='utf-8')
        return loader.load()

    def _get_embeddings(self):
        return VertexAIEmbeddings(model_name='text-embedding-004', pi_transport='rest')

    def _get_vectorstore(self):
        client = weaviate.Client(embedded_options=EmbeddedOptions())
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50, separators=[" ", ",", "\n"])
        chunks = text_splitter.split_documents(self.documents)
        return Weaviate.from_documents(client=client, documents=chunks, embedding=self.embeddings, by_text=False)

    def _get_compliance_parser(self):
        class ComplianceCheck(BaseModel):
            is_compliant: str = Field(
                description="Whether the invoice is compliant with the policies. 'Y' for Yes, 'N' for No.")
            reason: str = Field(description="Explanation for why the invoice is or isn't compliant.")

        return JsonOutputParser(pydantic_object=ComplianceCheck)

    def _create_rag_chain(self):
        rag_template = """
        Given the following invoice details:

        Invoice Information:
        {question}

        Retrieve the most relevant policy information from the following pieces of context that specifically address any spending limits that apply to this invoice:
        {context}.

        If a clear spending limit is found that applies to the invoice, return that specific limit. If no relevant spending limit is found, return a response indicating that no specific limit information was identified.

        Note:
        1. Focus on retrieving spending limit information that is directly relevant to the invoice details provided.
        2. Avoid retrieving unrelated or overly general policy information.
        3. Don't try to make up an answer.
        """
        rag_prompt = PromptTemplate(template=rag_template, input_variables=["context", "question"])
        chain_type_kwargs = {"prompt": rag_prompt}
        return RetrievalQA.from_chain_type(
            chain_type="stuff",
            llm=self.model,
            retriever=self.retriever,
            chain_type_kwargs=chain_type_kwargs
        )

    def _create_compliance_chain(self):
        compliance_template = """
        Given the following policy context:

        {policy_context}

        And the following invoice information:

        {invoice}

        Check the following:
        1. Analyze the policy context to identify any applicable spending limits. Compare the invoice amount to these limits. If the invoice amount exceeds any identified limit without the necessary approvals, classify it as non-compliant.
        2. Unless you have a strong reason based on the policy to determine that the invoice is non-compliant, do not hastily judge it as non-compliant. However, if spending limits are exceeded, this should be flagged as non-compliant.

        For each issue found, provide a detailed explanation.
        If there are multiple compliance issues, list each reason with a number (e.g., 1, 2, 3).
        Return the result in the following JSON format:
        {format_instructions}
        """
        compliance_prompt = PromptTemplate(
            template=compliance_template,
            input_variables=["policy_context", "invoice"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        return compliance_prompt | self.model | StrOutputParser()

    def check_compliance(self, invoice_info: dict) -> dict:
        """
        Check the compliance of the given invoice information with the retrieved policy context.

        Args:
            invoice_info (dict): The invoice details.

        Returns:
            dict: The original invoice info merged with the compliance check result.
        """
        rag_chain = self._create_rag_chain()
        compliance_chain = self._create_compliance_chain()

        query = """
        "expense_type": "{expense_type}",
        "invoice_id": "{invoice_id}",
        "invoice_date": "{invoice_date}",
        "vendor": "{vendor}",
        "customer": "{customer}",
        "city": "{city}",
        "currency": "{currency}",
        "amount": {amount}
        """.format(**invoice_info)

        policy_context = rag_chain.invoke(query)
        compliance_result = compliance_chain.invoke({"policy_context": policy_context, "invoice": invoice_info})

        compliance_data = self.parser.parse(compliance_result)
        return self.merge_compliance_result(invoice_info, compliance_data)

    def merge_compliance_result(self, invoice_info: dict, compliance_data: dict) -> dict:
        """
        Merge the compliance check result into the original invoice dictionary.

        Args:
            invoice_info (dict): The original invoice details.
            compliance_data (dict): The compliance check result.

        Returns:
            dict: The combined dictionary with compliance information.
        """
        invoice_info.update(compliance_data)
        return invoice_info


if __name__ == "__main__":
    checker = InvoiceComplianceChecker(
        model_name="gemini-pro",
        credentials_path="/Users/wangmingliang/Downloads/gen-lang-client-0233197284-eaa2bc08aade.json",
        document_path="/Users/wangmingliang/policy.rtf"
    )

    invoice_info = {
        "expense_type": "Transportation",
        "invoice_id": "987654",
        "invoice_date": "07/06/2024",
        "vendor": "Beijing Transportation",
        "customer": "John Doe",
        "city": "Beijing",
        "currency": "USD",
        "amount": "80"
    }

    result = checker.check_compliance(invoice_info)
    print("Compliance check result:", result)