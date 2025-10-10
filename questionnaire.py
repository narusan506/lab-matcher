import streamlit as st

def render_questionnaire():
        # タイトル（大文字・水色・中央寄せ）
    st.markdown(
    """
    <div style='text-align:center;'>
        <h1 style='color:#2E8B57; font-size:48px; text-transform:uppercase;'>
            診断アンケート
        </h1>
    </div>
    """,
    unsafe_allow_html=True
    )
    # アンケート設問リストとキー
    questions = [
        ("昔から数学は好きなほうだ", "math"),
        ("世の中にない新しいソフトウェアを作りたいと思っている", "software"),
        ("セキュリティのニュースはよくチェックしている", "security"),
        ("日常生活で『このデザイン使いやすいな』と思ったことがある", "ui"),
        ("AIの中身の仕組みについて勉強したいと思っている", "ai"),
        ("データのやり取りについて興味がある", "comm"),
        ("研究内容について", "practical"),#↑ 安藤 亀井 喜田 米谷 高木 福森 八重樫 山田 ↓ 小川 香川 健二 正樹 
        ("夏休みの宿題は最後に追われてやる方ですか？", "plan"),#はい 亀井 香川 喜田 健二 正樹 高木 いいえ 安藤 福森 八重樫 山田 米谷
        ("二つのバイト先があります？どちらを選びますか？", "prof"),
        ("教師に社会人経験があった方がいいと思いますか？","co"),
        ("実験Iではどんなものを作りましたか？", "experiment")
    ]

    # セッションステート初期化
    if "q_index" not in st.session_state:
        st.session_state.q_index = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}

    q_index = st.session_state.q_index
    total_q = len(questions)

    # プログレスバーと進行テキスト
    progress = q_index / total_q
    st.progress(progress)
    st.write(f"質問 {min(q_index+1, total_q)}/{total_q}")

    # 質問表示
    if q_index < total_q:
        question_text, key = questions[q_index]

        # 質問を装飾して表示
        st.markdown(
    f"""
    <div style="background-color:#2E8B57; padding:10px; border-radius:5px; text-align:center;">
        <h5 style="margin:0; color:white;">{question_text}</h5>
    </div>
    """,
    unsafe_allow_html=True
        )

        # 選択肢分岐
        if key == "prof":
            options = ["新規開店のカフェ", "老舗の喫茶店"]
        elif key == "experiment":
            options = [
                "趣味に関するもの", "AIや画像処理", "SNS/言語系",
                "生活で使うもの", "操作感重視", "独自の計算式", "その他"
            ]
        elif key=="practical":
            options=["すぐに世の中に役立つ研究をしたい","理論について研究をしたい"]
        elif key=="co":
            options=["あったほうがいい","気にしない"]
        else:
            options = ["はい", "いいえ"]
        

        # 過去の回答をデフォルトに
        default_answer = st.session_state.answers.get(key, options[0])
        answer = st.radio("", options, index=options.index(default_answer))

        # ナビゲーションボタン
        col1, col2 = st.columns(2)
        with col1:
            if q_index > 0:
                if st.button("前の質問に戻る"):
                    st.session_state.q_index -= 1
                    st.rerun()
        with col2:
            if st.button("次の質問へ"):
                st.session_state.answers[key] = answer
                st.session_state.q_index += 1
                st.rerun()

    # 全問回答後
    else:
        st.write("アンケート終了！")
        col1, col2, col3 = st.columns([2,2,1])  # 真ん中を広めにする
        with col2:
            if st.button("結果を見る"):
                st.session_state["page"] = "result"
                st.rerun()

    # 回答履歴をサイドバーに表示
    key_to_question = {key: text for text, key in questions}
    st.sidebar.header("これまでの回答")
    for key, answer in st.session_state["answers"].items():
        question_text = key_to_question[key]
        st.sidebar.markdown(f"**{question_text}**  \n→  {answer}")
