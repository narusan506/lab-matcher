import streamlit as st
import pandas as pd

cacl_result = {'A': 2.0, 'B': 0, 'C': 1.8, 'D': 1.8, 'E': 0, 'F': 0} #計算結果
your_laboratory = "高木"
st.markdown(
    f"<h1 style='text-align: center;'>最終結果</h1>",
    unsafe_allow_html=True
)
professors = {'安藤': 0, '小川': 0, '香川': 0, '亀井': 0, '喜田': 0, 
 '米谷': 0, '高木': 0, '健二': 0, '正樹': 0, 
 '福森': 0, '八重樫': 0, '山田': 0} #アンケート結果の可算部分
#B,Dなど2科目
st.subheader(f"貴方へのオススメ研究室は")
st.header(f"{your_laboratory}研究室です！")
category_results  = pd.DataFrame(list(cacl_result.items()), columns=["Category", "Value"])
st.bar_chart(category_results.set_index("Category"))


