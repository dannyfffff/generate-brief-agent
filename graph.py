from langgraph.graph import StateGraph, END
from typing import Literal
from nodes import create_fetch_all_data_node, MEDIA_CONFIG
from nodes import (
    WorkflowState, user_query_node, aggregate_and_draft_node, generate_chapter_2_node,
    generate_chapter_3_node, combine_briefing_node, export_to_docx_node, Agent_Agent_node,
    route_option_node
)



# 定义所有可能的选择ID作为分支判断依据
OptionID = Literal["A", "B", "C", "Other"]



# 路由函数：根据 optionId 决定下一个要执行的节点
def route_to_process(state: WorkflowState) -> str:
    process_id = state.get('optionId')
    if process_id in ["A", "B", "C"]:
        return "START_GRAB"
    return "END" # 或其他流程


workflow = StateGraph(WorkflowState)

workflow.add_node("Route_Option", route_option_node)
workflow.add_node("信息检索Agent", Agent_Agent_node)
workflow.add_node(
    "Fetch_All_Data_Node",
    create_fetch_all_data_node(MEDIA_CONFIG)
)


workflow.add_node("aggregate_and_draft", aggregate_and_draft_node)
workflow.add_node("user_query_node_1", user_query_node)

workflow.add_node("generate_chapter_2", generate_chapter_2_node)
workflow.add_node("generate_chapter_3", generate_chapter_3_node)
workflow.add_node("combine_briefing", combine_briefing_node)
workflow.add_node("export_to_docx", export_to_docx_node)



#设置入口点
workflow.set_entry_point("Route_Option")

workflow.add_conditional_edges(
    "Route_Option",
    lambda state: state.get("optionId"),
    {
        "A": "信息检索Agent",
        "B": "信息检索Agent",
        "C": "信息检索Agent",
        "Other": END
    }
)

workflow.add_edge("信息检索Agent", "Fetch_All_Data_Node")
workflow.add_edge("Fetch_All_Data_Node", "aggregate_and_draft")
workflow.add_edge("aggregate_and_draft", "user_query_node_1")


workflow.add_conditional_edges(
    "user_query_node_1",
    lambda state: state['userChoiceId'],
    {
        "A": "generate_chapter_2",  # 假设你需要处理选项 A 的新节点
        "B": "generate_chapter_2",
        "Other": END
    }
)

workflow.add_edge("generate_chapter_2", "generate_chapter_3")
workflow.add_edge("generate_chapter_3", "combine_briefing")
workflow.add_edge("combine_briefing", "export_to_docx")

workflow.add_edge("export_to_docx", END)


# 7. 编译图
graph = workflow.compile()
print("--- LangGraph 条件分支流程图已编译完成 ---")
#

print("\n" + "="*50)








