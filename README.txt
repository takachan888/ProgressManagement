ProgressManagement（Django）提出物 README
1. アプリ概要

ProgressManagement は、卒業制作のチーム（6人）で進捗を管理するためのWebアプリです。
メンバーは自分のタスクの進捗（0〜100）とメモを更新できます。
リーダーは全員の進捗を一覧で確認し、タスクの追加・編集・削除やユーザー管理ができます。

2. 主要機能
メンバー（一般ユーザー）

自分のタスク一覧の表示

タスクの進捗（progress 0〜100）の更新

今日のメモ / 次回のメモの更新

リーダー（is_staff=True）

メンバー別の進捗確認（ダッシュボード）

全タスク一覧の確認

タスクの追加 / 編集 / 削除

ユーザー一覧、ユーザー追加 / 編集 / 削除
※自分自身と superuser は削除不可

3. ログイン後の画面分岐

ログイン後は /after-login/ で権限により自動的に画面が切り替わります。

is_staff=True（リーダー）→ /leader/

それ以外（メンバー）→ /me/

4. 状態（未着手/作業中/完了）の判定ルール

本アプリでは status の入力は行わず、progress の値で状態を判定します。

progress = 0 → 未着手

progress = 100 → 完了

それ以外 → 作業中

5. 起動手順（Windows / PowerShell）

※ このREADMEがあるフォルダ（manage.py がある場所）で PowerShell を開いてください。

5-1) ローカル起動（SQLite）

仮想環境の作成

py -m venv venv


仮想環境の有効化

.\venv\Scripts\Activate.ps1


（もしブロックされた場合：venv\Scripts\activate.bat）

依存関係のインストール

pip install -r requirements.txt


DBの反映

py manage.py migrate


管理者ユーザー作成（必要な場合のみ）

py manage.py createsuperuser


サーバ起動

py manage.py runserver


ブラウザでアクセス
http://127.0.0.1:8000/

6. 使い方（簡単）

ログイン画面からユーザーでログインします。

メンバーは /me/ で自分のタスク進捗とメモを更新します。

リーダーは /leader/ で全員の進捗確認やタスク管理、ユーザー管理を行います。

7. 提出用設定について（環境変数 / .env）

本プロジェクトは、以下を想定しています。

ローカル：.env（manage.py と同じ階層）から読み込み可能
※ .env は .gitignore により GitHub には含めません

本番（Vercel）：Vercel の Environment Variables に設定します

使用ライブラリ（requirements.txt）：

Django==5.2.9

psycopg[binary]==3.2.3（Postgres接続）

python-dotenv==1.0.1（ローカルで .env 読み込み）

8. 公開（Vercel + Supabase）手順（再現手順）

本番公開は Vercel（アプリ） + Supabase（Postgres） で行っています。

8-1) Supabase（無料Postgres）を作成して接続情報を控える

Supabaseでプロジェクトを作成し、Connect から Session Pooler の接続情報を控えます。

今回の構成例：

host: aws-1-ap-southeast-1.pooler.supabase.com

port: 5432

database: postgres

user: postgres.<project-ref>（例：postgres.upyonvgurehygzrgepzy）

password: Supabaseプロジェクト作成時のDBパスワード

※ Vercel側の接続で IPv6 関連の問題が出ることがあるため、db.<ref>.supabase.co（Direct）ではなく Pooler を使用しています。

8-2) ローカルからSupabaseに migrate（テーブル作成）

ローカルの .env に Supabaseの接続情報（Pooler）を設定してから：

py manage.py migrate
py manage.py createsuperuser

8-3) Vercelに環境変数を登録

Vercel → Project → Settings → Environment Variables に以下を設定します
（Production / Preview の両方に入れると安全です）

Postgres（Supabase / Pooler）

POSTGRES_HOST = aws-1-ap-southeast-1.pooler.supabase.com

POSTGRES_PORT = 5432

POSTGRES_DB = postgres

POSTGRES_USER = postgres.<project-ref>

POSTGRES_PASSWORD = （SupabaseのDBパスワード）

Django

DJANGO_SECRET_KEY = （長いランダム文字列）

DJANGO_DEBUG = 0

DJANGO_ALLOWED_HOSTS = .vercel.app

DJANGO_CSRF_TRUSTED_ORIGINS = https://*.vercel.app

設定後、Vercelで Redeploy（再デプロイ） します。

9. ユーザーについて

リーダーユーザー

ユーザー名：otagiri

パスワード：takachan

その他（メンバー）

sutou / kasai / takamizawa / ogawa / siraki

パスワード：すべて takachan

以上