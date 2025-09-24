import streamlit as st
import pandas as pd

def show_final_result(cacl_result, your_laboratory, professors=None):
    """
    最終結果を表示する関数
    
    Parameters
    ----------
    cacl_result : dict
        {"A": 2.0, "B": 0, ...} のようなカテゴリごとの結果
    your_laboratory : str
        オススメの研究室名
    professors : dict, optional
        教員名とスコアの辞書（使う場合だけ渡す）
    """
    
    # タイトル
    st.markdown(
        "<h1 style='text-align: center;'>最終結果</h1>",
        unsafe_allow_html=True
    )
    
    # 研究室のおすすめ表示
    st.subheader("貴方へのオススメ研究室は")
    st.header(f"{your_laboratory}研究室です！")
    
    # 成績ベースのカテゴリ結果をグラフ化
    category_results = pd.DataFrame(list(cacl_result.items()), columns=["Category", "Value"])
    st.bar_chart(category_results.set_index("Category"))
    
    # 教員スコアを表示したい場合（任意）
    if professors:
        st.write("教授ごとのスコア")
        professors_df = pd.DataFrame(list(professors.items()), columns=["Professor", "Score"])
        st.bar_chart(professors_df.set_index("Professor"))
