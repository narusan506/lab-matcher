import pandas as pd
import streamlit as st

# =====================
# 成績計算
# =====================
def calculate_result(subject_grades):
    """
    subject_grades: { "科目名": "成績", ... } の辞書
    カテゴリごとの平均スコアを返す
    """
    cat = pd.read_csv("category.csv", encoding="cp932")
    grades = {"A":0, "B":0, "C":0, "D":0, "E":0, "F":0}
    gpa = {"不可":0, "可":1, "良":1.4, "優":1.8, "秀":2}
    total = {"A":0, "B":0, "C":0, "D":0, "E":0, "F":0}
    calc_result = {"A":0, "B":0, "C":0, "D":0, "E":0, "F":0}

    # 科目ごとの集計
    for key, value in subject_grades.items():
        matched = cat[cat["科目名"].str.strip() == key.strip()]
        if matched.empty:
            print(f"警告: {key} は CSV に見つかりませんでした。")
            continue

        category_list = matched["カテゴリ"].values[0].split(",")
        subject_score = gpa.get(value, 0)
        for cat_name in category_list:
            cat_name = cat_name.strip()
            grades[cat_name] += subject_score
            total[cat_name] += 1

        print(f"科目名: {key}, 成績: {value}({subject_score}), カテゴリ: {category_list}")

    # 平均計算
    for key in calc_result:
        if total[key] > 0:
            calc_result[key] = grades[key] / total[key]
        else:
            calc_result[key] = 0
    print(calc_result)
    return calc_result

# =====================
# アンケートベースの診断
# =====================
def calculate_survey_result(answers):
    scores = {
        "数学・アルゴリズム系": 0,
        "ソフトウェア開発系": 0,
        "セキュリティ系": 0,
        "UI/UXデザイン系": 0,
        "AI・データサイエンス系": 0,
        "ネットワーク・通信系": 0
    }

    if answers.get("math") == "はい": scores["数学・アルゴリズム系"] += 2
    if answers.get("software") == "はい": scores["ソフトウェア開発系"] += 2
    if answers.get("security") == "はい": scores["セキュリティ系"] += 2
    if answers.get("ui") == "はい": scores["UI/UXデザイン系"] += 2
    if answers.get("ai") == "はい": scores["AI・データサイエンス系"] += 2
    if answers.get("comm") == "はい": scores["ネットワーク・通信系"] += 2

    experiment = answers.get("experiment")
    if experiment == "AIや画像処理":
        scores["AI・データサイエンス系"] += 2
    elif experiment == "操作感重視":
        scores["UI/UXデザイン系"] += 2
    elif experiment == "独自の計算式":
        scores["数学・アルゴリズム系"] += 2
    elif experiment == "SNS/言語系":
        scores["ネットワーク・通信系"] += 2
    print(scores)
    return scores

# =====================
# 統合スコア
# =====================
def integrate_results(grade_results, survey_results):
    mapping = {
        "A": "数学・アルゴリズム系",
        "B": "ソフトウェア開発系",
        "C": "セキュリティ系",
        "D": "UI/UXデザイン系",
        "E": "AI・データサイエンス系",
        "F": "ネットワーク・通信系"
    }
    combined = {cat: grade_results.get(cat, 0) + survey_results.get(field, 0) 
                for cat, field in mapping.items()}
    print(combined)
    return combined

# =====================
# 教授診断
# =====================
def cal_professors(combined, answers):
    professors = {'安藤': 0, '小川': 0, '香川': 0, '亀井': 0, '喜田': 0, 
                  '米谷': 0, '高木': 0, '健二': 0, '正樹': 0, 
                  '福森': 0, '八重樫': 0, '山田': 0} 

    if answers.get("practical")=="すぐに世の中に役立つ研究をしたい":
        for p in ["安藤","亀井","喜田","高木","福森","八重樫","山田"]:
            professors[p] += 1
    else:
        for p in ["小川","香川","健二","正樹"]:
            professors[p] += 1

    if answers.get("practical")=="はい":
        for p in ["亀井","香川","喜田","健二","正樹","高木"]:
            professors[p] += 1
    else:
        for p in ["安藤","福森","八重樫","山田","米谷"]:
            professors[p] += 1

    professors["安藤"] += (combined["E"] + combined["B"])/2
    professors["小川"] += (combined["A"] + combined["B"])/2
    professors["香川"] += (combined["A"] + combined["B"])/2
    professors["亀井"] += combined["F"]
    professors["喜田"] += (combined["E"] + combined["C"])/2
    professors["米谷"] += combined["D"]
    professors["高木"] += combined["B"]
    professors["健二"] += (combined["A"] + combined["C"])/2
    professors["正樹"] += combined["C"]
    professors["福森"] += (combined["D"] + combined["B"])/2
    professors["八重樫"] += (combined["D"] + combined["B"])/2
    professors["山田"] += (combined["D"] + combined["B"])/2

    max_score = max(professors.values())
    your_laboratory = [name for name, score in professors.items() if score == max_score]
    return professors, your_laboratory

# =====================
# Streamlit 用まとめ
# =====================
def run_full_diagnosis(st_session_state, answers):
    # CSVから科目名リスト取得
    cat = pd.read_csv("category.csv", encoding="cp932")
    subject_names = cat["科目名"].str.strip().tolist()

    # 科目だけ抽出
    subject_grades = {k: v for k, v in st_session_state.items() if k.strip() in subject_names}

    # 計算
    grade_results = calculate_result(subject_grades)
    survey_results = calculate_survey_result(answers)
    combined = integrate_results(grade_results, survey_results)
    professors, your_laboratory = cal_professors(combined, answers)

    return grade_results, survey_results, combined, professors, your_laboratory

# =====================
# 単体テスト
# =====================
if __name__ == "__main__":
    # 成績テストデータ
    session_state = {"線形計画法":"秀", "情報システム・セキュリティ概論":"優"}
    # アンケートテストデータ
    answers = {"math":"はい", "software":"いいえ", "security":"はい", "ui":"いいえ", 
               "ai":"はい", "comm":"はい", "experiment":"AIや画像処理",
               "practical":"すぐに世の中に役立つ研究をしたい"}

    grade_results, survey_results, combined, professors, your_laboratory = run_full_diagnosis(session_state, answers)

    print("成績ベース:", grade_results)
    print("アンケートベース:", survey_results)
    print("統合スコア:", combined)
    print("教授スコア:", professors)
    print("オススメ研究室:", your_laboratory)
