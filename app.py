from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'yocret'  # セッション用の秘密鍵

@app.route('/')
def profile():
    return render_template('profile.html') # プロフィール入力画面

@app.route('/save-profile', methods=['POST'])
def save_profile():
    # フォームから送られてきたデータを取得
    job = request.form.get('job')
    personality = request.form.get('personality')
    first_person = request.form.get('first_person')
    tone = request.form.get('tone')

    # セッション（あるいはデータベース）に保存
    session['user_profile'] = {
        'job': job,
        'personality': personality,
        'first_person': first_person,
        'tone': tone
    }

    # 取得したデータをターミナルで確認してみる
    print("保存されたプロフィール:", session['user_profile'])

    # career.html（次の画面）へリダイレクト
    return redirect(url_for('career'))

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
    return render_template('loading.html')

if __name__ == '__main__':
    app.run(debug=True)