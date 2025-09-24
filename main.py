import streamlit as st
import app
import app_cacl as calc
import questionnaire as qu
import final_result as fin

# ===========================
# ページ初期化
# ===========================
if "page" not in st.session_state:
    st.session_state["page"] = "app"
    st.rerun()

# ===========================
# ページ分岐
# ===========================
page = st.session_state["page"]

if page == "app":
    # 科目入力ページ
    app.render_grades_input("subjects.csv")

elif page == "questionnaire":
    # アンケートページ
    qu.render_questionnaire()

elif page == "result":
    # ===========================
    # 結果ページ
    # ===========================
    # 安全に科目成績だけ抽出
    subject_grades = st.session_state.get("grades", {})  # {'デザイン概論': '優'}
    calc_result = calc.calculate_result(subject_grades)
    print(subject_grades)
    # answers は無ければ空辞書
    answers = st.session_state.get("answers", {})
    print(answers)

    # 診断実行
    grade_results, survey_results, combined, professors, your_laboratory = \
        calc.run_full_diagnosis(subject_grades, answers)
    # 結果表示
    fin.show_final_result(combined, your_laboratory, professors)

else:
    st.error("不正なページです")
