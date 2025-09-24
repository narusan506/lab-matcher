import streamlit as st
import pandas as pd

# Qを前期/後期に変換
def convert_term(x):
    if "第1Q" in x or "第2Q" in x or "前期" in x:
        return "前期"
    elif "第3Q" in x or "第4Q" in x or "後期" in x:
        return "後期"
    return x

def render_grades_input(csv_path="subjects.csv"):
    # タイトル（大文字・水色・中央寄せ）
    st.markdown(
    """
    <div style='text-align:center;'>
        <h1 style='color:deepskyblue; font-size:48px; text-transform:uppercase;'>
            ラボチェッカー
        </h1>
    </div>
    """,
    unsafe_allow_html=True
    )

    # サブタイトル（みずいろ背景に白文字・中央寄せ）
    st.markdown(
    """
    <div style='text-align:center; background-color:deepskyblue; color:white; 
                padding:10px; border-radius:8px; font-size:20px;'>
        あなたに合った研究室を診断！<br>
        成績を入力してください
    </div>
    """,
    unsafe_allow_html=True
    )

    if "show_help" not in st.session_state:
        st.session_state.show_help = False

    if st.button("ヘルプを表示/非表示"):
        st.session_state.show_help = not st.session_state.show_help

    if st.session_state.show_help:
        st.info("""    - このサイトは情報コース(旧CSSS)の研究室のマッチング診断が出来るお遊びサイトです  
    - 成績を入力後、アンケートに答えると自分に合った研究室が表示されます  
    - あくまでお遊びなので真に受けすぎないでください""")
    
    # CSVの読み込み
    df = pd.read_csv(csv_path)
    df["学期"] = df["時期"].apply(convert_term)

    # 学期ごとに必修・選択科目を整理
    required_courses = {}
    elective_courses = {}

    for year in sorted(df["年次"].unique()):
        for term in ["前期", "後期"]:
            key = f"{year}年{term}"
            required_courses[key] = df[
                (df["年次"] == year) & (df["学期"] == term) & (df["必修科目"] == 1)
            ]["科目名"].tolist()
            elective_courses[key] = df[
                (df["年次"] == year) & (df["学期"] == term) & (df["必修科目"] == 0)
            ]["科目名"].tolist()

    # UI部分
    if "grades" not in st.session_state:
        st.session_state["grades"] = {}
    terms = []
    for y in sorted(df["年次"].unique()):
        terms.append(f"{y}年前期")
        terms.append(f"{y}年後期")

    for term in terms:
        with st.expander(term, expanded=True):
            st.subheader("必修科目")
            for course in required_courses.get(term, []):
                col1, col2 = st.columns([2, 1])
                col1.write(course)
                grade = col2.selectbox(
                    "",
                    ["未入力", "秀", "優", "良", "可", "不可"],
                    key=f"{term}_{course}"
                )
                if grade != "未入力":
                    st.session_state["grades"][course] = grade
                elif course in st.session_state["grades"]:
                    del st.session_state["grades"][course]    

            st.subheader("選択科目")
            if f"electives_{term}" not in st.session_state:
                st.session_state[f"electives_{term}"] = []

            available_electives = [
                course for course in elective_courses.get(term, [])
                if course not in st.session_state[f"electives_{term}"]
            ]

            add_course = st.selectbox(
                f"{term} に追加する科目",
                ["選択しない"] + available_electives,
                key=f"add_{term}",
                index=0
            )

            if add_course != "選択しない" and add_course not in st.session_state[f"electives_{term}"]:
                st.session_state[f"electives_{term}"].append(add_course)
                st.rerun()

            remove_indices = []
            for i, elective in enumerate(st.session_state[f"electives_{term}"]):
                col1, col2, col3 = st.columns([2, 1, 0.3])
                col1.write(elective)
                grade = col2.selectbox(
                    "",
                    ["未入力", "秀", "優", "良", "可", "不可"],
                    key=f"{term}_elective_{i}"
                )
                if grade != "未入力":
                    st.session_state["grades"][elective] = grade
                elif elective in st.session_state["grades"]:
                    del st.session_state["grades"][elective]

                if col3.button("×", key=f"remove_{term}_{i}"):
                    remove_indices.append(i)

            for i in sorted(remove_indices, reverse=True):
                removed_course = st.session_state[f"electives_{term}"].pop(i)
                if removed_course in st.session_state["grades"]:
                    del st.session_state["grades"][removed_course]
                st.rerun()
    
    if st.button("アンケートへ進む"):
        st.session_state["page"] = "questionnaire"
