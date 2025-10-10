import streamlit as st
import pandas as pd

def render_grades_input(csv_path="subjects1.csv"):
    # タイトル
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

    # サブタイトル
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

    # ヘルプ表示
    if "show_help" not in st.session_state:
        st.session_state.show_help = False

    if st.button("ヘルプを表示/非表示"):
        st.session_state.show_help = not st.session_state.show_help

    if st.session_state.show_help:
        st.info("""- このサイトは情報コース(旧CSSS)の研究室マッチング診断サイトです  
- 成績を入力後、アンケートに答えると自分に合った研究室が表示されます  
- あくまでお遊びなので真に受けすぎないでください""")

    # CSV読み込み
    df = pd.read_csv(csv_path)

    # 成績データの保持
    if "grades" not in st.session_state:
        st.session_state["grades"] = {}

    # ===== 表示ロジック =====
    for main_category in ["共通", "専門"]:
        with st.expander(f"{main_category}科目", expanded=True):
            # 各カテゴリ（能力・コース専門科目）ごとにグループ化
            subcategories = sorted(df[df["科目区分"] == main_category]["カテゴリ"].unique())
            
            for subcat in subcategories:
                st.markdown(f"### 🔹 {subcat}")

                # 必修・選択で分ける
                required = df[(df["科目区分"] == main_category) & (df["カテゴリ"] == subcat) & (df["必修科目"] == 1)]
                elective = df[(df["科目区分"] == main_category) & (df["カテゴリ"] == subcat) & (df["必修科目"] == 0)]

                # ---- 必修科目 ----
                if not required.empty:
                    st.subheader("必修科目")
                    for course in required["科目名"]:
                        col1, col2 = st.columns([2, 1])
                        col1.write(course)
                        grade = col2.selectbox(
                            "",
                            ["未入力", "秀", "優", "良", "可", "不可"],
                            key=f"{main_category}_{subcat}_{course}"
                        )
                        if grade != "未入力":
                            st.session_state["grades"][course] = grade
                        elif course in st.session_state["grades"]:
                            del st.session_state["grades"][course]

                # ---- 選択科目 ----
                if not elective.empty:
                    st.subheader("選択科目")
                    elective_key = f"electives_{main_category}_{subcat}"
                    if elective_key not in st.session_state:
                        st.session_state[elective_key] = []

                    available_electives = [
                        c for c in elective["科目名"]
                        if c not in st.session_state[elective_key]
                    ]

                    add_course = st.selectbox(
                        f"{subcat} で追加する科目",
                        ["選択しない"] + available_electives,
                        key=f"add_{main_category}_{subcat}"
                    )

                    if add_course != "選択しない" and add_course not in st.session_state[elective_key]:
                        st.session_state[elective_key].append(add_course)
                        st.rerun()

                    remove_indices = []
                    for i, elective_name in enumerate(st.session_state[elective_key]):
                        col1, col2, col3 = st.columns([2, 1, 0.3])
                        col1.write(elective_name)
                        grade = col2.selectbox(
                            "",
                            ["未入力", "秀", "優", "良", "可", "不可"],
                            key=f"{main_category}_{subcat}_elective_{i}"
                        )
                        if grade != "未入力":
                            st.session_state["grades"][elective_name] = grade
                        elif elective_name in st.session_state["grades"]:
                            del st.session_state["grades"][elective_name]

                        if col3.button("×", key=f"remove_{main_category}_{subcat}_{i}"):
                            remove_indices.append(i)

                    for i in sorted(remove_indices, reverse=True):
                        removed_course = st.session_state[elective_key].pop(i)
                        if removed_course in st.session_state["grades"]:
                            del st.session_state["grades"][removed_course]
                        st.rerun()

    # 次のページボタン
    if st.button("アンケートへ進む"):
        st.session_state["page"] = "questionnaire"
