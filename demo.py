# import gradio as gr
# import os
# from typing import Dict, Any, Optional
#
# # --- 定义历史文档目录 (必须与 nodes.py 中的 DOCS_DIR 一致) ---
# DOCS_DIR = "generated_briefings"
# os.makedirs(DOCS_DIR, exist_ok=True)  # 确保文件夹存在
#
# # 导入编译后的图对象
# try:
#     from graph import graph
# except ImportError:
#     # 如果 graph 无法导入，提供一个假对象防止 Gradio 崩溃
#     class DummyGraph:
#         def invoke(self, *args, **kwargs):
#             return {"error": "Graph object not found. Please check graph.py"}
#
#
#     graph = DummyGraph()
#
# llm_chain = graph
# WorkflowState = Dict[str, Any]
#
#
# # --- 辅助函数：获取历史文件列表 ---
# def get_history_files():
#     """扫描历史目录并返回文件列表，用于 Gradio UI 更新。"""
#     files = [os.path.join(DOCS_DIR, f) for f in os.listdir(DOCS_DIR)]
#     # 仅返回文件，并按修改时间降序排列 (最新文件在前)
#     files = sorted([f for f in files if os.path.isfile(f)], key=os.path.getmtime, reverse=True)
#     return files
#
#
# # --- 核心运行函数：单次运行到底 (修改返回值以包含历史列表) ---
#
# def run_full_workflow(workflow_input: str, option_id_label: str, user_choice_label: str, user_outline: str) -> tuple:
#     """
#     运行整个工作流。
#
#     返回: (最终报告, 事实草稿, DOCX路径, 状态信息, 历史文件列表) 🚨 新增历史文件列表
#     """
#
#     # 键值解析
#     option_id_key = option_id_label.split(':')[0]
#     choice_id_key = user_choice_label.split(':')[0]
#
#     initial_inputs = {
#         "workflowInput": workflow_input,
#         "optionId": option_id_key,
#         "userChoiceId": choice_id_key,
#         "userOutline": user_outline if choice_id_key == "B" else "",
#     }
#
#     # 提前检查 OptionId 终止
#     if option_id_key == "Other":
#         return "", "", None, "⚠️ 流程已根据初始分类终止 (OptionId = Other)。", get_history_files()  # 返回历史文件
#
#     try:
#         new_state = llm_chain.invoke(initial_inputs, {"recursion_limit": 50})
#
#         final_briefing: Optional[str] = new_state.get('final_briefing')
#         export_path: Optional[str] = new_state.get('export_path')
#         briefing_draft: Optional[str] = new_state.get('briefing_draft')
#
#         # 🚨 统一在返回时调用 get_history_files()
#         history = get_history_files()
#
#         if new_state.get('error'):
#             return f"LangGraph 内部错误: {new_state['error']}", briefing_draft, None, "🚨 流程失败。", history
#         elif final_briefing:
#             # 成功生成最终报告 (A/B 模式)
#             return final_briefing, briefing_draft, export_path, "🎉 简报生成完毕！", history
#         elif briefing_draft and choice_id_key == "Other":
#             # 用户选择终止 (仅保留第一章)
#             return f"流程已终止。仅事实基础内容：\n\n{briefing_draft}", briefing_draft, None, "⚠️ 用户选择终止，仅生成事实基础。", history
#         else:
#             # 流程未能产生最终内容
#             return "流程失败，未产生最终简报内容。", briefing_draft, None, "🚨 流程失败，请检查 LangGraph 内部日志。", history
#
#     except Exception as e:
#         return f"工作流运行失败: {e}", "", None, f"🚨 运行失败: {e}", get_history_files()
#
#
# # --- Gradio UI 结构：Tabbed 结构 ---
#
# with gr.Blocks(title="LangGraph 简报生成器") as demo:
#     gr.Markdown("# 🤖 智能简报生成工作流")
#
#     with gr.Tabs() as tabs:
#         # --- Tab 1: 运行工作流 ---
#         with gr.Tab(label="1. 运行工作流"):
#             gr.Markdown("### 1. 工作流输入")
#
#             # --- 输入区 ---
#             with gr.Row():
#                 with gr.Column():
#                     st_workflow_input = gr.Textbox(
#                         label="📝 简报主题 (workflowInput):",
#                         value="AI芯片的最新政策和技术趋势",
#                         lines=2
#                     )
#
#                     st_option_id = gr.Radio(
#                         label="📊 1. 初始流程分类 (optionId):",
#                         choices=["A: 政策类", "B: 技术类", "C: 事件类", "Other: 其它流程 (直接结束)"],
#                         value="A: 政策类",
#                         interactive=True
#                     )
#                 with gr.Column():
#                     st_user_choice_id = gr.Radio(
#                         label="🎯 2. 第二章生成模式 (userChoiceId):",
#                         choices=["A: 自动生成建议和对策 (AUTO)",
#                                  "B: 提供大纲，按大纲生成建议和对策 (OUTLINE)",
#                                  "Other: 流程终止，仅保留事实基础"],
#                         value="A: 自动生成建议和对策 (AUTO)",
#                         interactive=True
#                     )
#
#                     st_user_outline = gr.Textbox(
#                         label="📋 3. 用户大纲 (userOutline - 仅选择 B 时有效):",
#                         placeholder="例如：第一节：政策影响分析；第二节：市场竞争态势。",
#                         lines=5
#                     )
#
#             run_button = gr.Button("🚀 运行完整工作流", variant="primary")
#
#             # --- 输出区 ---
#             gr.Markdown("---")
#             gr.Markdown("### 2. 运行结果")
#
#             error_output = gr.Textbox(label="状态/错误信息", interactive=False, lines=2)
#
#             with gr.Row():
#                 final_briefing_output = gr.Textbox(
#                     label="📄 最终报告摘要 / 最终结果:",
#                     lines=15,
#                     interactive=False
#                 )
#                 briefing_draft_output = gr.Textbox(
#                     label="📝 事实基础草稿 (第一章 - 仅供参考/调试):",
#                     lines=15,
#                     interactive=False
#                 )
#
#             download_file = gr.File(label="📥 下载 DOCX 简报文件", file_count="single", visible=True)
#
#             # 🚨 占位符：用于接收 run_full_workflow 返回的历史文件列表
#             temp_history_files_placeholder = gr.State(value=get_history_files())
#
#             # --- Tab 2: 历史文档查看 (新增) ---
#         with gr.Tab(label="2. 历史文档"):
#             gr.Markdown("## 历史简报文档")
#
#             # 🚨 关键组件：显示历史文件列表
#             history_files = gr.Files(
#                 label="已生成的简报文件 (点击下载)",
#                 file_count="multiple",
#                 value=get_history_files(),  # 初始加载时显示现有文件
#                 interactive=False
#             )
#
#             refresh_button = gr.Button("🔄 刷新文件列表")
#
#     # --- 事件绑定 ---
#
#     # 运行按钮绑定
#     run_button.click(
#         fn=run_full_workflow,
#         inputs=[st_workflow_input, st_option_id, st_user_choice_id, st_user_outline],
#         outputs=[final_briefing_output, briefing_draft_output, download_file, error_output, history_files]
#         # 🚨 修正：将 history_files 加入 outputs 列表
#     )
#
#     # 刷新按钮绑定
#     refresh_button.click(
#         fn=get_history_files,
#         inputs=[],
#         outputs=[history_files]
#     )
#
# if __name__ == "__main__":
#     demo.launch()