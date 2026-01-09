ProgressManagement（Django）提出物 README

■ 1. アプリ概要
ProgressManagement は、卒業制作のチーム（6人）で進捗を管理するためのWebアプリです。
メンバーは自分のタスクの進捗（0〜100）とメモを更新できます。
リーダーは全員の進捗を一覧で確認し、タスクの追加・編集・削除やユーザー管理ができます。

■ 2. 主要機能
【メンバー（一般ユーザー）】
- 自分のタスク一覧の表示
- タスクの進捗（progress 0〜100）の更新
- 今日のメモ / 次回のメモの更新

【リーダー（is_staff=True）】
- メンバー別の進捗確認（ダッシュボード）
- 全タスク一覧の確認
- タスクの追加 / 編集 / 削除
- ユーザー一覧、ユーザー追加 / 編集 / 削除（※自分自身とsuperuserは削除不可）

■ 3. ログイン後の画面分岐
ログイン後は /after-login/ で権限により自動的に画面が切り替わります。
- is_staff=True（リーダー）→ /leader/
- それ以外（メンバー）→ /me/

■ 4. 状態（未着手/作業中/完了）の判定ルール
本アプリでは status の入力は行わず、progress の値で状態を判定します。
- progress = 0   → 未着手
- progress = 100 → 完了
- それ以外       → 作業中

■ 5. 起動手順（Windows / PowerShell）
※ このREADMEがあるフォルダ（manage.py がある場所）で PowerShell を開いてください。

1) 仮想環境の作成
py -m venv venv

2) 仮想環境の有効化
.\venv\Scripts\Activate.ps1
（もしブロックされた場合：venv\Scripts\activate.bat）

3) 依存関係のインストール
pip install -r requirements.txt

4) DBの反映（db.sqlite3が含まれている場合でも実行して問題ありません）
py manage.py migrate

5) 管理者ユーザー作成（必要な場合のみ）
py manage.py createsuperuser

6) サーバ起動
py manage.py runserver

7) ブラウザでアクセス
http://127.0.0.1:8000/

■ 6. 使い方（簡単）
- ログイン画面からユーザーでログインします。
- メンバーは /me/ で自分のタスク進捗とメモを更新します。
- リーダーは /leader/ で全員の進捗確認やタスク管理、ユーザー管理を行います。

■ 7. 提出用設定について
本提出物は、環境変数が未設定でもローカル起動できるように settings.py を調整しています。
（本番公開を行う場合は SECRET_KEY/DEBUG/ALLOWED_HOSTS を環境変数で管理する想定です。）

■ 8. ユーザについて
リーダーユーザー ユーザ名:otagiri pass:takachan 
その他 ユーザ名:
sutou
kasai
takamizawa
ogawa
siraki
※passはすべてtakachan

以上
