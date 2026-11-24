import streamlit as st
from processor import process_excel

st.set_page_config(page_title="收料通知单作数工具", page_icon="📊")

st.title("📊 收料通知单作数工具")

# ==========================
# 下载Excel模板
# ==========================
col1, col2 = st.columns([1, 2])

with col1:

    try:
        with open("templates/收料通知单作数.xlsx", "rb") as template_file:

            st.download_button(
                label="📥 下载Excel模板",
                data=template_file,
                file_name="收料通知单模板.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except FileNotFoundError:
        st.error("模板文件不存在")

with col2:
    st.info("""
    使用步骤：
            
    ① 下载模板
            
    ② 填写【来货数量】Sheet
            
    ③ 填写【PO数量】Sheet
            
    ④ 上传Excel
            
    ⑤ 下载处理结果
    """)

st.divider()

uploaded_file = st.file_uploader("上传Excel文件", type=["xlsx"])

if uploaded_file:
    try:
        result = process_excel(uploaded_file)

        st.success("处理完成！")

        st.download_button(
            label="下载处理结果",
            data=result,
            file_name="收料通知单作数-Done.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"处理失败：{str(e)}")
        st.info("请确认Excel包含工作表：来货数量、PO数量，以及对应字段名称正确。")
