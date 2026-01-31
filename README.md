# Watson

Watsonは、Dr.ワトソン（シャーロック・ホームズの助手）として振る舞うAIチャットボットです。FastAPIバックエンドとシンプルなWebフロントエンドで構成されています。

## 特徴
- FastAPIによるAPIサーバー
- Llama3等のローカルLLM（Ollama API）と連携
- シンプルなHTML/JavaScriptフロントエンド
- セッションごとに会話履歴を管理

## セットアップ
1. [Ollama](https://ollama.com/) をインストールし、`llama3`モデルをダウンロードして起動してください。
   ```sh
   ollama run llama3
   ```
2. 必要なPythonパッケージをインストールします。
   ```sh
   pip install fastapi uvicorn pydantic requests
   ```

## サーバーの起動
以下のコマンドでFastAPIサーバーを起動します。
```sh
uvicorn main:app --reload
```
デフォルトで http://localhost:8000 でAPIが立ち上がります。

## フロントエンドの利用
`index.html` をブラウザで開いてください。
 - メッセージを入力し「Send」ボタンで送信できます。
 - Watsonが1～3文で簡潔に返答します。

## ファイル構成
- main.py ... FastAPIバックエンド
- index.html ... チャット用フロントエンド
- style.css ... スタイルシート
- README.md ... このファイル

## 注意
- Ollamaサーバー（デフォルト: http://localhost:11434）が必要です。
- APIやフロントエンドのポート番号は必要に応じて変更してください。