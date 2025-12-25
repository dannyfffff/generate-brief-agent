from typing_extensions import TypedDict
from typing import Optional, Literal, List

class DocumentResult(TypedDict):
    """精简的搜索文档结构"""
    title: str
    url: str
    content: str

# 你的所有节点函数都依赖这个类型
class WorkflowState(TypedDict):
    """图的全局状态 - 复制到 nodes.py 以解决导入问题"""
    workflowInput: str
    optionId: Optional[Literal["A", "B", "C", "Other"]]
    optionContent: Optional[str]
    it_doc_results: Optional[List[DocumentResult]]  # IT之家
    lz_doc_results: Optional[List[DocumentResult]]  # 量子位
    xz_doc_results: Optional[List[DocumentResult]]  # 新智元 (xz)
    jq_doc_results: Optional[List[DocumentResult]]  # 机器之心Pro (jq)
    error: Optional[str]
    it_url_out_1: Optional[str]
    it_url_out_2: Optional[str]
    it_url_out_3: Optional[str]
    lz_url_out_1: Optional[str]
    lz_url_out_2: Optional[str]
    lz_url_out_3: Optional[str]
    xz_url_out_1: Optional[str]
    xz_url_out_2: Optional[str]
    xz_url_out_3: Optional[str]
    jq_url_out_1: Optional[str]
    jq_url_out_2: Optional[str]
    jq_url_out_3: Optional[str]
# 3. 内容和标题抓取键 (24 个)
    it_content_1: Optional[str]
    it_title_1: Optional[str]
    it_content_2: Optional[str]
    it_title_2: Optional[str]
    it_content_3: Optional[str]
    it_title_3: Optional[str]

    lz_content_1: Optional[str]
    lz_title_1: Optional[str]
    lz_content_2: Optional[str]
    lz_title_2: Optional[str]
    lz_content_3: Optional[str]
    lz_title_3: Optional[str]

    xz_content_1: Optional[str]
    xz_title_1: Optional[str]
    xz_content_2: Optional[str]
    xz_title_2: Optional[str]
    xz_content_3: Optional[str]
    xz_title_3: Optional[str]

    jq_content_1: Optional[str]
    jq_title_1: Optional[str]
    jq_content_2: Optional[str]
    jq_title_2: Optional[str]
    jq_content_3: Optional[str]
    jq_title_3: Optional[str]

    briefing_draft: Optional[str]
    chapter_2_content: Optional[str]
    lz_url_1_content: Optional[str]
    chapter_3_content: Optional[str]
    final_briefing: Optional[str]

    userChoiceId: Optional[Literal["A", "B", "Other"]]
    userOutline: Optional[str]