import os

from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

from utils.diff import diff_url

os.environ["TOKENIZERS_PARALLELISM"] = "True"


def db(pr_number: int):
    # Load the diff
    loader = WebBaseLoader(diff_url(pr_number))
    docs = loader.load()

    # Split text into tokens
    docs_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    all_docs = docs_splitter.split_documents(docs)

    # Get embeddings
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": False}
    hf = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)

    # Store the embeddings into chromadb directory
    db = Chroma.from_documents(documents=all_docs, embedding=hf, persist_directory=f"./chromadb_{pr_number}")
    return db
