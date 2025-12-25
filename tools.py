from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_deepseek import ChatDeepSeek
# from config import DEEPSEEK_API_KEY, TAVILY_API_KEY
#
#
# search_tool = TavilySearchResults(max_results=5)
from config import TAVILY_API_KEY

api_wrapper = TavilySearchAPIWrapper(tavily_api_key=TAVILY_API_KEY)

search_tool = TavilySearchResults(
    name="tavily_search",
    api_wrapper=api_wrapper,
    max_results=5
)
# DeepSeek LLM 初始化 (用于 URL 验证)
llm = ChatDeepSeek(model="deepseek-chat", temperature=0)
