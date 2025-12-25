# import streamlit as st
# import os
# from dotenv import load_dotenv
# from graph import graph  # 导入您编译好的 LangGraph
# from typing import Literal, Optional
# import logging
# import sys
#
# # --- 1. 配置和初始化 ---
#
# # 确保在 Streamlit 应用启动时加载环境变量
# # 注意：Streamlit 运行时可能需要重新设置环境变量，请确保您的 .env 文件在路径中。
# load_dotenv()
#
# # 检查关键环境变量（可选，但推荐）
# if not os.getenv("TAVILY_API_KEY") or not os.getenv("DEEPSEEK_API_KEY"):
#     st.error("🚨 错误：TAVILY_API_KEY 或 DEEPSEEK_API_KEY 环境变量未设置。请检查您的 .env 文件。")
#     st.stop()
#
# # 设置日志级别为 DEBUG，这样 graph.invoke 就会打印出每一步的输入、输出和状态更新。
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().handlers = []
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
#
#
# # --- 2. 核心状态定义 ---
#
# # 模拟用户在 user_query_node 节点中的选择
# @st.cache_data
# def get_initial_state():
#     """获取 LangGraph 初始状态结构"""
#     return {
#         "workflowInput": "",
#         "optionId": None,
#         "optionContent": None,
#         "it_doc_results": None,
#         # ... 您的所有其他状态键可以省略，Graph 会自动初始化缺失的键
#     }
#
#
# # --- 3. 辅助函数：运行 LangGraph ---
#
# # 为了在 Streamlit 重新运行时避免重复编译和运行，使用缓存
# def run_langgraph(user_input: str, option_id: Literal["A", "B", "C"]):
#     """执行 LangGraph 流程并返回最终状态"""
#
#     # 模拟 user_query_node 的行为：
#     # 1. 在流程开始时，我们设置初始的用户输入。
#     # 2. 假设 user_query_node 节点只是一个提示点，我们在这里提前设置用户选择
#     #    (为了简化 Streamlit 部署，我们暂时跳过用户二次确认环节，强制选择 A 且无大纲)
#
#     initial_state = {
#         "workflowInput": user_input,
#         "optionId": option_id,
#         # 强制设置 user_query_node 后续路由所需的值
#         "userChoiceId": "A",
#         "userOutline": "",
#     }
#
#     config = {"recursion_limit": 100}  # 设置最大递归限制
#
#     st.info(f"🚀 开始执行 LangGraph 流程：输入='{user_input}'，类型='{option_id}'...")
#
#     try:
#         # 实时打印执行步骤 (需要定制 LangGraph 的配置或使用回调)
#         # 这里我们只运行到结束
#         final_state = graph.invoke(initial_state, config=config)
#
#         st.success("✅ LangGraph 流程执行完毕！")
#         return final_state
#
#     except Exception as e:
#         st.error(f"❌ LangGraph 执行失败: {e}")
#         st.code(final_state.get('error', '未捕获的错误信息'))
#         return None
#
#
# # --- 4. Streamlit 界面 ---
#
# st.set_page_config(page_title="LangGraph 简报生成应用", layout="wide")
#
# st.title("📝 自动化简报生成系统")
# st.markdown("基于 LangGraph 的多源信息检索、分析与文档导出工作流。")
#
# # --- 输入表单 ---
# with st.form("briefing_form"):
#     # 1. 用户输入查询
#     workflow_input = st.text_input(
#         "请输入要分析的主题或事件:",
#         placeholder="例如：欧盟最新 AI 监管政策对我国互联网企业的影响",
#         key="workflow_input_key"
#     )
#
#     # 2. 选项选择 (对应 optionId)
#     option_map = {
#         "A": "A - 政策类 (政策内容分析)",
#         "B": "B - 技术类 (技术思考分析)",
#         "C": "C - 事件类 (事件深层分析)"
#     }
#     option_id_choice = st.radio(
#         "请选择简报类型 (对应 optionId):",
#         options=list(option_map.keys()),
#         format_func=lambda x: option_map[x],
#         key="option_id_key",
#         horizontal=True
#     )
#
#     # 3. 提交按钮
#     submitted = st.form_submit_button("开始生成简报")
#
# # --- 结果展示 ---
# if submitted and workflow_input:
#
#     # 运行 LangGraph
#     final_state = run_langgraph(workflow_input, option_id_choice)
#
#     if final_state:
#
#         # 提取关键结果
#         export_path = final_state.get('export_path', 'KEY_MISSING_IN_FINAL_STATE')
#         briefing_draft = final_state.get('briefing_draft')
#         final_briefing = final_state.get('final_briefing')
#
#         with st.expander("查看所有状态变量 (调试 - 完整)", expanded=True):
#             st.json(final_state)  # 观察这个输出
#
#         st.subheader("🎉 最终结果")
#
#         if export_path != 'KEY_MISSING_IN_FINAL_STATE' and "导出失败" not in export_path:
#             st.success(f"文件已保存至：`{export_path}`")
#             # 尝试提供下载按钮（假设文件位于 Streamlit 应用可访问的路径）
#             try:
#                 with open(export_path, "rb") as file:
#                     st.download_button(
#                         label="下载 DOCX 简报",
#                         data=file,
#                         file_name=os.path.basename(export_path),
#                         mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#                     )
#             except Exception as e:
#                 st.warning(f"无法创建下载链接，请手动从 {export_path} 获取文件。错误: {e}")
#         else:
#             st.warning(f"DOCX 文件导出失败或路径未返回。诊断值: {export_path}")
#
#         # 详细内容预览
#         with st.expander("预览最终简报内容 (文本)", expanded=False):
#             if final_briefing:
#                 st.code(final_briefing, language='markdown')
#             else:
#                 st.write("最终简报内容为空。")
#
#         # 调试信息
#         with st.expander("查看第一章初稿 (调试)", expanded=False):
#             st.markdown(briefing_draft)
#
#         with st.expander("查看所有状态变量 (调试)", expanded=False):
#             st.json(final_state)
#
# elif submitted and not workflow_input:
#     st.warning("请输入要分析的主题或事件才能开始。")

import streamlit as st
import os
import glob  # 【新增】导入 glob 模块
from dotenv import load_dotenv
from graph import graph
from typing import Literal, Optional
import logging
import sys
from datetime import datetime
# --- 1. 配置和初始化 ---

load_dotenv()

if not os.getenv("TAVILY_API_KEY") or not os.getenv("DEEPSEEK_API_KEY"):
    st.error("🚨 错误：TAVILY_API_KEY 或 DEEPSEEK_API_KEY 环境变量未设置。请检查您的 .env 文件。")
    st.stop()

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().handlers = []
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


# --- 2. 核心状态定义 ---

@st.cache_data
def get_initial_state():
    """获取 LangGraph 初始状态结构"""
    return {
        "workflowInput": "",
        "optionId": None,
        "it_doc_results": None,
    }


# --- 【新增】辅助函数：查找最新的简报文件 ---
def find_latest_briefing_file(directory="generated_briefings"):
    """
    在指定目录下查找最新的 DOCX 简报文件。
    它用于在 LangGraph 路径返回失败时，从本地目录中恢复文件。
    """
    try:
        if not os.path.isdir(directory):
            return None

        # 查找所有 DOCX 文件
        # 注意：这里假设文件名中包含 '简报' 或 '分析' 等关键词，如果您的命名规则固定，可以优化 glob 模式
        list_of_files = glob.glob(os.path.join(directory, '*.docx'))
        if not list_of_files:
            return None

        # 排除临时文件（如 Word 产生的 ~$），并按文件创建时间排序
        valid_files = [f for f in list_of_files if not os.path.basename(f).startswith('~') and os.path.getsize(f) > 0]
        if not valid_files:
            return None

        # 找到创建时间最新的文件
        latest_file = max(valid_files, key=os.path.getctime)
        return latest_file
    except Exception as e:
        st.error(f"查找本地文件时发生错误: {e}")
        return None


# 【新增】辅助函数：获取所有历史简报
def get_historical_briefings(directory="generated_briefings"):
    """获取所有已生成的简报文件（按时间降序排列）。"""
    if not os.path.isdir(directory):
        return []

    # 查找所有 DOCX 文件
    list_of_files = glob.glob(os.path.join(directory, '*.docx'))

    # 排除临时文件，并获取文件信息
    file_details = []
    for f in list_of_files:
        try:
            if not os.path.basename(f).startswith('~') and os.path.getsize(f) > 0:
                file_details.append({
                    'path': f,
                    'name': os.path.basename(f),
                    'time': os.path.getctime(f)
                })
        except OSError:
            # 忽略无法访问的文件
            continue

    # 按时间降序排列 (最新的在前)
    file_details.sort(key=lambda x: x['time'], reverse=True)

    return file_details
# --- 3. 辅助函数：运行 LangGraph ---

def run_langgraph(user_input: str, option_id: Literal["A", "B", "C"]):
    """执行 LangGraph 流程并返回最终状态"""

    initial_state = {
        "workflowInput": user_input,
        "optionId": option_id,
        "userChoiceId": "A",
        "userOutline": "",
    }

    config = {"recursion_limit": 100}

    st.info(f"🚀 开始执行 LangGraph 流程：输入='{user_input}'，类型='{option_id}'...")

    try:
        final_state = graph.invoke(initial_state, config=config)
        st.success("✅ LangGraph 流程执行完毕！")
        return final_state

    except Exception as e:
        # 在捕获错误时，依然返回 final_state 以便调试
        final_state = graph.get_state(config).values if graph.get_state(config) else {}
        st.error(f"❌ LangGraph 执行失败: {e}")
        st.code(final_state.get('error', '未捕获的错误信息'))
        return final_state


# --- 4. Streamlit 界面 ---

st.set_page_config(page_title="LangGraph 简报生成应用", layout="wide")

st.title("📝 自动化简报生成系统")
st.markdown("基于 LangGraph 的多源信息检索、分析与文档导出工作流。")

# --- 历史生成文档展示模块 ---
st.subheader("📁 历史生成文档")
historical_files = get_historical_briefings()

if historical_files:
    with st.expander("点击查看和下载所有历史简报 (共 {} 份)".format(len(historical_files)), expanded=False):
        for file_info in historical_files:
            file_path = file_info['path']
            file_name = file_info['name']

            # 格式化时间
            time_str = datetime.fromtimestamp(file_info['time']).strftime('%Y-%m-%d %H:%M:%S')

            # 使用列布局
            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(f"**{file_name}**")
                st.caption(f"*生成时间: {time_str}*")

            with col2:
                try:
                    # 确保文件存在且可读
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as file:
                            st.download_button(
                                label="下载",
                                data=file.read(),
                                file_name=file_name,
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                key=f"download_{file_name}"  # 必须有唯一的key
                            )
                except Exception:
                    st.caption("文件不可读")
else:
    st.info("目前还没有历史简报文件。")

st.markdown("---")  # 分隔线

# --- 输入表单 ---
with st.form("briefing_form"):
    workflow_input = st.text_input(
        "请输入要分析的主题或事件:",
        placeholder="例如：欧盟最新 AI 监管政策对我国互联网企业的影响",
        key="workflow_input_key"
    )

    option_map = {
        "A": "A - 政策类 (政策内容分析)",
        "B": "B - 技术类 (技术思考分析)",
        "C": "C - 事件类 (事件深层分析)"
    }
    option_id_choice = st.radio(
        "请选择简报类型 (对应 optionId):",
        options=list(option_map.keys()),
        format_func=lambda x: option_map[x],
        key="option_id_key",
        horizontal=True
    )

    submitted = st.form_submit_button("开始生成简报")

# --- 结果展示 【核心修改区域】 ---
if submitted and workflow_input:

    final_state = run_langgraph(workflow_input, option_id_choice)

    if final_state:

        # 提取关键结果
        export_path = final_state.get('export_path', 'KEY_MISSING_IN_FINAL_STATE')
        briefing_draft = final_state.get('briefing_draft')
        final_briefing = final_state.get('final_briefing')

        # 尝试使用的文件路径
        final_file_path = None

        st.subheader("🎉 最终结果")

        if export_path != 'KEY_MISSING_IN_FINAL_STATE' and "导出失败" not in export_path and export_path:
            # 情况 1: LangGraph 成功返回了路径 (最佳情况)
            final_file_path = export_path
            st.success(f"文件已保存至：`{final_file_path}`")
        else:
            # 情况 2: 路径丢失或返回错误，尝试从本地目录中恢复
            st.warning(f"DOCX 文件导出路径返回异常。诊断值: {export_path}。正在尝试从本地目录恢复文件...")
            recovered_path = find_latest_briefing_file()

            if recovered_path and os.path.exists(recovered_path):
                final_file_path = recovered_path
                st.success(f"✅ 成功从本地目录恢复最新的简报文件路径：`{final_file_path}`")
            else:
                st.error("❌ 无法从本地目录中找到已生成的简报文件。请检查 `generated_briefings/` 文件夹。")

        # --- 下载按钮逻辑 ---
        if final_file_path and os.path.exists(final_file_path):
            try:
                # 必须使用 'rb' 模式打开文件，并获取文件对象
                with open(final_file_path, "rb") as file:
                    st.download_button(
                        label="📥 点击下载 DOCX 简报",
                        # 直接传递文件对象给 data 参数
                        data=file.read(),
                        file_name=os.path.basename(final_file_path),
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
            except Exception as e:
                st.warning(f"无法创建下载链接。请手动从 `{final_file_path}` 获取文件。错误: {e}")
        elif not final_file_path and export_path == 'KEY_MISSING_IN_FINAL_STATE':
            st.error("简报生成失败，LangGraph 未返回路径且无法在本地目录中恢复文件。请调试 LangGraph。")

        # 详细内容预览
        with st.expander("预览最终简报内容 (文本)", expanded=True):
            if final_briefing:
                st.code(final_briefing, language='markdown')
            else:
                st.write("最终简报内容为空。")

        # 调试信息
        with st.expander("查看所有状态变量 (调试 - 完整)", expanded=False):
            st.json(final_state)

        with st.expander("查看第一章初稿 (调试)", expanded=False):
            st.markdown(briefing_draft)


elif submitted and not workflow_input:
    st.warning("请输入要分析的主题或事件才能开始。")