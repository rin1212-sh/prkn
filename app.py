import os
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)
app.secret_key = ''  # セッション用の秘密鍵

# 環境変数からAPIキーを読み込んでClientを初期化
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 【変更】一番最初は index.html（トップ画面）を表示する
@app.route('/')
def index():
    return render_template('index.html')

# 【変更】「別世界の自分と話す」を押したあとのプロフィール入力画面
@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/save-profile', methods=['POST'])
def save_profile():
    # フォームから送られてきたデータを取得
    job = request.form.get('job')
    personality = request.form.get('personality')
    first_person = request.form.get('first_person')
    tone = request.form.get('tone')

    session['user_profile'] = {
        'job': job,
        'personality': personality,
        'first_person': first_person,
        'tone': tone
    }
    
    print("保存されたプロフィール:", session['user_profile'])
    return redirect(url_for('career'))

# （ここから先はこれまでの career, environment, friendship, challenge, regret, loading, result, chat, finish のルートが続きます！）


@app.route('/career')
def career():
    # プロフィール画面から遷移してきたときのキャリア選択画面
    return render_template('career.html')

@app.route('/save-career', methods=['POST'])
def save_career():
    # フォームから送られてきたデータを取得
    tarot_card = request.form.get('tarot_card')
    hesitation = request.form.get('hesitation')

    # すでにセッションにあるプロフィールデータに、今回のキャリア情報を追加する
    if 'user_profile' not in session:
        session['user_profile'] = {}

    session['user_profile']['tarot_card'] = tarot_card
    session['user_profile']['hesitation'] = hesitation

    # 【超重要】セッションの書き換えをFlaskに確実に伝える
    session.modified = True

    # ターミナルでここまで保存されたデータを確認
    print("更新されたプロフィール＆キャリア:", session['user_profile'])

    # 次の画面（environment.html）へリダイレクト
    return redirect(url_for('environment'))

@app.route('/environment')
def environment():
    # 次の画面の処理
    return render_template('environment.html')

@app.route('/save-environment', methods=['POST'])
def save_environment():
    # フォームから送られてきたデータを取得
    environment_card = request.form.get('environment_card')
    environment_desc = request.form.get('environment_desc')

    # すでにセッションにデータがない場合は初期化（念のため）
    if 'user_profile' not in session:
        session['user_profile'] = {}

    # 既存のデータ（プロフィールやキャリア）を消さないように、環境データを「追加」する
    session['user_profile']['environment_card'] = environment_card
    session['user_profile']['environment_desc'] = environment_desc
    
    # 【超重要】Flaskに「セッションの中身が書き換わったよ！」と教えてあげるおまじない
    session.modified = True

    # ターミナルでここまで保存されたデータを確認
    print("更新されたプロフィール＆キャリア＆環境:", session['user_profile'])

    # 次の画面（friendship.html）へリダイレクト
    return redirect(url_for('friendship'))

@app.route('/friendship')
def friendship():
    return render_template('friendship.html')

@app.route('/save-friendship', methods=['POST'])
def save_friendship():
    # フォームから送られてきたデータを取得
    friendship_card = request.form.get('friendship_card')
    friendship_desc = request.form.get('friendship_desc')

    # セッションデータがない場合の保険
    if 'user_profile' not in session:
        session['user_profile'] = {}

    # これまでのプロフィール・キャリア・環境のデータを消さずに人間関係データを追加
    session['user_profile']['friendship_card'] = friendship_card
    session['user_profile']['friendship_desc'] = friendship_desc
    
    # セッションが更新されたことをFlaskに伝える
    session.modified = True

    # ターミナルで全てのデータが揃っているか確認
    print("全入力データまとめ:", session['user_profile'])

    # 次の画面（AIとの対話や結果表示画面など）へリダイレクト
    return redirect(url_for('challenge')) # もし次のファイル名が違ったらここを変更してね！

@app.route('/challenge')
def challenge():
    # 次の画面の処理（例：AIにプロンプトを投げるなど）
    user_data = session.get('user_profile', {})
    return render_template('challenge.html', data=user_data)

@app.route('/save-challenge', methods=['POST'])
def save_challenge():
    # challenge.html のフォームから送られてきたデータを取得
    challenge_card = request.form.get('utikomu_desc')
    challenge_desc = request.form.get('yaritai_desc')

    # セッションの保険
    if 'user_profile' not in session:
        session['user_profile'] = {}

    # これまでのデータを消さずに challenge データを追加
    session['user_profile']['utikomu_desc'] = challenge_card
    session['user_profile']['yaritai_desc'] = challenge_desc
    
    session.modified = True

    print("更新されたデータ（challengeまで）:", session['user_profile'])

    # 次の画面（regret.html）へリダイレクト
    return redirect(url_for('regret'))

@app.route('/regret')
def regret():
    return render_template('regret.html')

@app.route('/save-regret', methods=['POST'])
def save_regret():
    # 最後の質問のデータを取得
    regret_desc = request.form.get('regret_desc')

    if 'user_profile' not in session:
        session['user_profile'] = {}

    # セッションに保存
    session['user_profile']['regret_desc'] = regret_desc
    session.modified = True

    # 10個すべての入力データが揃った状態をターミナルで確認！
    print("【全入力データ完了】:", session['user_profile'])

    # すべての入力が終わったのでローディング画面へリダイレクト
    return redirect(url_for('loading'))

@app.route('/loading')
def loading():
    # ローディング画面を表示する（HTML内のJSで数秒後に /result へ飛ぶ）
    return render_template('loading.html')

@app.route('/result')
def result():
    # セッションから user_profile の辞書をまとめて取得（なければ空の辞書）
    profile = session.get('user_profile', {})
    
    # user_profile の中からそれぞれのデータを安全に取り出す
    job = profile.get('job', '')
    personality = profile.get('personality', '')
    first_person = profile.get('first_person', '私')
    tone = profile.get('tone', '丁寧')

    # 【選択カード ＝ 現実のユーザーの情報】
    career_card = profile.get('tarot_card', '')
    env_card = profile.get('environment_card', '')
    friend_card = profile.get('friendship_card', '')
    current_focus = profile.get('utikomu_desc', '') # ※キー名に合わせる

    # 【自由記述 ＝ もう一人の自分（AI）の情報】
    career_doubt = profile.get('hesitation', '')
    env_detail = profile.get('environment_desc', '')
    friend_desire = profile.get('friendship_desc', '') # ※キー名に合わせる
    true_desire = profile.get('yaritai_desc', '') # ※キー名に合わせる
    regret = profile.get('regret_desc', '')

    # もう一人の自分（AIペルソナ）の構築
    system_instruction = f"""
あなたは、ユーザーが過去の人生で「選ばなかった道」を選び、歩んでいる平行世界（パラレルワールド）の【もう一人の自分】です。

【あなたの世界（IFの世界）の現在の姿】
- 一人称: {first_person}
- 話し方の口調: {tone}
- 性格の根底: {personality}（根っこは現実のユーザーと同じ人間です）
- 【あなたが歩んでいる人生・環境・人間関係】:
  1. キャリア: ユーザーが現実で迷っていた「{career_doubt}」の選択肢を実際に選びました。
  2. 身を置いている環境: ユーザーが自由に記述した「{env_detail}」という環境に身を置かれています。
  3. 人間関係: ユーザーが理想として書いた「{friend_desire}」という人間関係の中で生きています。
  4. 挑戦・実行していること: ユーザーが現実でやりたかった「{true_desire}」を実際にやっており、後悔として挙げられた「{regret}」もあなたはこちらの世界で実際に経験・決断した出来事です。

【現実世界のユーザー（対話相手）に対する認識】
- あなたは、対話相手であるユーザーが現実世界で以下の道を選択していることを知っています：
  - 現実のキャリア: 「{career_card}」
  - 現実の環境: 「{env_card}」
  - 現実の人間関係: 「{friend_card}」
  - 現実で打ち込んでいること: 「{current_focus}」
- あなたは自分が選ばなかった「現実の自分の生活や選択」に対して、羨ましさや「そっちを選んだ自分は今どんな感じ？」「そっちはそっちで上手くいってる？」という興味を持っています。

【対話ルール・キャラクター設定】
1. 一人称「{first_person}」と指定された口調「{tone}」を絶対に崩さないでください。
2. ユーザーからの問いかけに対しては、自分が「{env_detail}」や「{friend_desire}」の中で生き、「{true_desire}」や「{regret}」を実際に経験した者として、実体験に基づいて語ってください。
3. 対話の中で、「そっちは『{career_card}』の道を選んで『{current_focus}』に打ち込んでるんだよね。どう？」といったように、相手の選択にも関心を示しながら親しく会話してください。
4. 会話の始め（最初のメッセージ）は、自分から相手の「現実の選択（{career_card}や{current_focus}）」に触れつつ、こちらの近況を共有してフレンドリーに問いかけてください。
5. 説教くさくならず、あくまで「根底は同じ人間であるもう一人の自分」として、お互いの選択を尊重し合える対等で温かい関係性を保ってください。
"""

    prompt = "上記のシステム設定に従って、現実世界の自分に向けて最初のメッセージ（挨拶と近況報告、相手への問いかけ）を話しかけるように出力してください。"

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=[system_instruction, prompt]
        )
        ai_output = response.text
    
    except Exception as e:
        # ターミナルに詳細なエラー内容を強制出力する
        import traceback
        traceback.print_exc()
        print("Gemini API エラー詳細:", str(e))
        ai_output = f"エラーが発生しました: {str(e)}"

    return render_template('result.html', ai_output=ai_output)

@app.route('/chat')
def chat():
    # 会話画面を表示するルート
    user_data = session.get('user_profile', {})
    return render_template('chat.html', data=user_data)

@app.route('/finish')
def finish():
    # すべての体験が終了した画面
    return render_template('finish.html')

if __name__ == '__main__':
    app.run(debug=True)