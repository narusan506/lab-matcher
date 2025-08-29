# import pandas as pd

# #app_cacl.py
# session_state = {"線形計画法":"秀","情報システム・セキュリティ概論":"優"}
# #補遺
# #線形計画法：A
# #情報システム・セキュリティ概論：D,C

# #category.csv = 区分が記載されたcsvファイル
# cat = pd.read_csv("category.csv", encoding="cp932") #名前を付けて保存したら文字コードがShift-JISだったので、それを指定
# grades = {"A":0, "B":0, "C":0, "D":0, "E":0, "F":0} #得点部分の集計用
# gpa = {"不可":0, "可":1, "良":1.4, "優":1.8, "秀":2} #評価ごとのポイント
# total = {"A":0, "B":0, "C":0, "D":0, "E":0, "F":0} #どのカテゴリのものを何単位履修したのか集計する
# cacl_result = {"A":0, "B":0, "C":0, "D":0, "E":0, "F":0} #結果

# for key,value in session_state.items():
#     for number in range (len(cat)):
#         #print("!")
#         if cat["科目名"].iloc[number] == key:
#             #print(key)
#             #category = cat.loc[cat["科目名"] == key].values[0]
#             category_list = cat.loc[cat["科目名"] == key, "カテゴリ"].str.split(",").values[0]

#             #print(category_list[0])
#             subject_grade = gpa[value]
#             #print(subject_grade)
#             grades[category_list[0]] += subject_grade
#             total[category_list[0]] += 1
#             try:
#                 if category_list[1] != None:
#                     grades[category_list[1]] += subject_grade
#                     total[category_list[1]] += 1
#             except:
#                 pass
#             break

# #print(grades)
# #print(total)

# for key in cacl_result:
#     #print(grades[key], total[key])
#     try:
#         cacl_result[key] = grades[key] / total[key]
#     except:
#         pass
# print(cacl_result)


# # app_calc.py
import pandas as pd

def calculate_result(session_state):
    """
    session_state: { "科目名": "成績", ... } の辞書を受け取って
    カテゴリごとの計算結果を返す
    """

    # CSV読み込み
    cat = pd.read_csv("category.csv", encoding="cp932")

    grades = {"A":0, "B":0, "C":0, "D":0, "E":0, "F":0}
    gpa = {"不可":0, "可":1, "良":1.4, "優":1.8, "秀":2}
    total = {"A":0, "B":0, "C":0, "D":0, "E":0, "F":0}
    cacl_result = {"A":0, "B":0, "C":0, "D":0, "E":0, "F":0}

    # session_stateを走査
    for key, value in session_state.items():
        for number in range(len(cat)):
            if cat["科目名"].iloc[number] == key:
                category_list = cat.loc[cat["科目名"] == key, "カテゴリ"].str.split(",").values[0]
                subject_grade = gpa.get(value, 0)

                # カテゴリごとに集計
                grades[category_list[0]] += subject_grade
                total[category_list[0]] += 1
                try:
                    if category_list[1] != None:
                        grades[category_list[1]] += subject_grade
                        total[category_list[1]] += 1
                except:
                    pass
                break

    # 平均計算
    for key in cacl_result:
        try:
            cacl_result[key] = grades[key] / total[key]
        except:
            pass

    return cacl_result


# 単体テスト用
if __name__ == "__main__":
    # テストデータ
    session_state = {"線形計画法":"秀", "情報システム・セキュリティ概論":"優"}
    print(calculate_result(session_state))
