import pandas as pd
import streamlit as st
import time

# CSVの読み込み
df = pd.read_csv("subjects.csv")  # ファイル名は適宜変更

# Qを前期/後期に変換
def convert_term(x):
    if "第1Q" in x or "第2Q" in x or "前期" in x:
        return "前期"
    elif "第3Q" in x or "第4Q" in x or "後期" in x:
        return "後期"
    return x

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
terms = [f"{y}年前期" for y in sorted(df["年次"].unique())] + \
        [f"{y}年後期" for y in sorted(df["年次"].unique())]

for term in terms:
    with st.expander(term, expanded=True):
        st.subheader("必修科目")
        for course in required_courses.get(term, []):
            col1, col2 = st.columns([2, 1])
            col1.write(course)
            col2.selectbox(
                "",
                ["未入力", "秀","優", "良", "可", "不可"],
                key=f"{term}_{course}"
            )

        st.subheader("選択科目")
        # 選択科目リストを初期化
        if f"electives_{term}" not in st.session_state:
            st.session_state[f"electives_{term}"] = []

        # まだ追加されていない科目だけを選択肢に表示
        available_electives = [
            course for course in elective_courses.get(term, [])
            if course not in st.session_state[f"electives_{term}"]
        ]

        # 科目追加用プルダウン
        add_course = st.selectbox(
            f"{term} に追加する科目",
            ["選択しない"] + available_electives,
            key=f"add_{term}",
            index=0
        )

        # 追加されたらリストに保存
        if add_course != "選択しない" and add_course not in st.session_state[f"electives_{term}"]:
            st.session_state[f"electives_{term}"].append(add_course)
            add_course="選択しない"
            st.rerun()

        # 追加済み科目を横並びで表示、削除ボタン付き
        remove_indices = []
        for i, elective in enumerate(st.session_state[f"electives_{term}"]):
            col1, col2, col3 = st.columns([2, 1, 0.3])
            col1.write(elective)
            col2.selectbox(
                "",
                ["未入力", "秀","優", "良", "可", "不可"],
                key=f"{term}_elective_{i}"
            )
            # 削除ボタン
            if col3.button("×", key=f"remove_{term}_{i}"):
                remove_indices.append(i)

        # 削除はループ後にまとめて行う（直接ループ内で削除すると描画が崩れることがある）
        for i in sorted(remove_indices, reverse=True):
            st.session_state[f"electives_{term}"].pop(i)
            
if st.button("マッチング実行"):
    with st.spinner("計算中…"):
        time.sleep(3)  # ここに処理を書く
    st.success("マッチング完了！")