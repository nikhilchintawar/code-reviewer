import os

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain

from utils.db import db
from utils.load_env import load_env

# TODO: Should be user input
PR_NUMBER = 31

# Load the environment variables from the .env file
load_env()


def reviewer():
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", openai_api_key=os.environ.get("OPENAI_API_KEY"))

    retriever = db(PR_NUMBER).as_retriever(
        search_type="mmr",  # Also test "similarity"
        search_kwargs={"k": 8},
    )

    # qa = RetrievalQA.from_chain_type(
    #     llm=llm, chain_type="stuff", retriever=db.as_retriever(), return_source_documents=False
    # )

    memory = ConversationSummaryMemory(llm=llm, memory_key="chat_history", return_messages=True)
    qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)

    query = """
    Review the provided git diff code & give the answers to following questions:
    
    - Explain changes in the old code in detail
    - Explain changes in the new code in detail
    - General observations or insights
    """
    res = qa.run(query)

    print("re", res)


if __name__ == "__main__":
    reviewer()


# 1. **Overall Comments:**
#     - [ ] Code changes old & new
#     - [ ] Code structure and organization
#     - [ ] Logic and algorithm efficiency
#     - [ ] Code readability and clarity
#     - [ ] Error handling and edge cases

#     2. **Specific Feedback:**
#     - [ ] Variable names and naming conventions
#     - [ ] Function/method design and parameters
#     - [ ] Use of libraries or frameworks
#     - [ ] Potential performance improvements
#     - [ ] Security concerns, if any
#     - [ ] Code comments and documentation

#     3. **Testing:**
#     - [ ] Are there sufficient test cases?
#     - [ ] Do the tests cover edge cases?

#     4. **Suggestions for Improvement:**
#     - [ ] Refactoring recommendations
#     - [ ] Alternative approaches, if applicable
#     - [ ] Areas for code optimization

#     5. **Additional Comments:**
#     - [ ] General observations or insights
