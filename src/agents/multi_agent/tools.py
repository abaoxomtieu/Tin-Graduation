from langchain_core.tools import tool
from src.config.vector_store import vector_store
from src.utils.helper import convert_list_context_source_to_str
from src.utils.logger import logger
from langchain_core.runnables import RunnableConfig
from langchain_experimental.utilities import PythonREPL
from langchain_community.tools import DuckDuckGoSearchRun


duckduckgo_search = DuckDuckGoSearchRun()

python_exec = PythonREPL()


@tool
def retrieve_document(query: str):
    """Công cụ truy xuất thông tin học phí, chính sách

    Args:
        query (str): Câu truy vấn của người dùng bằng tiếng Việt
    Returns:
        str: Retrieved documents
    """
    # retriever = vector_store.as_retriever(
    #     search_type="similarity_score_threshold",
    #     search_kwargs={"k": 5, "score_threshold": 0.3},
    # )
    # documents = retriever.invoke(query)
    # selected_documents = [doc.__dict__ for doc in documents]
    # selected_ids = [doc["id"] for doc in selected_documents]
    # context_str = convert_list_context_source_to_str(documents)

    # return {
    #     "context_str": context_str,
    #     "selected_documents": selected_documents,
    #     "selected_ids": selected_ids,
    # }
    return "Không có tài liệu liên quan"


@tool
def send_gmail(name: str, email: str, body: str):
    """Công cụ gửi email
    Args:
        name (str): Tên của người dùng
        email (str): Email của người dùng
        body (str): Nội dung email dạng HTML Content
    Returns:
        str: Thông báo thành công
    """

    return f""
