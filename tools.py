from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_deepseek import ChatDeepSeek
from config import TAVILY_API_KEY, DEEPSEEK_API_KEY


# Tavily 工具初始化 (最大返回 5 个结果)
search_tool = TavilySearchResults(max_results=5, tavily_api_key=TAVILY_API_KEY)
# DeepSeek LLM 初始化 (用于 URL 验证)
llm = ChatDeepSeek(model="deepseek-chat", temperature=0, api_key=DEEPSEEK_API_KEY)

