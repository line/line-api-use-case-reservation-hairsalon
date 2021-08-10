## 本番（AWS）フロントエンド環境構築
1. .env ファイルの設定

    front/.env ファイルの `LIFF_ID` に LIFF アプリの LIFF ID を、`BASE_URL` に AWS APIGateway の URL を、`APIGATEWAY_STAGE`に AWS APIGateway のステージ名を設定してください。

    ▼ .env ファイル
    ````
    # LIFF ID
    LIFF_ID=9999999999-xxxxxxxx

    # AXIOS BASE URL
    BASE_URL=https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com

    # API Gateway Stage
    APIGATEWAY_STAGE=dev

    # Ajax Module (axios or amplify)
    AJAX_MODULE=amplify
    ````

1. node_modules インストール

    front プロジェクトに Node.js の依存パッケージ(※ node_modules フォルダ)がインストールされていない場合、front フォルダー直下で以下のコマンドを実行して node_modules をインストールしてください。
    ```
    npm install
    ```
    もしくは
    ```
    yarn install
    ```

1. 静的ビルド

    フロント側をビルドして S3 に配置する静的モジュール生成します。 front フォルダ直下で以下のコマンドを実行してください。
    ```
    npm run build
    ```
    もしくは
    ```
    yarn run build
    ```
    ビルドが完了したら front/dist フォルダが生成されています。 dist フォルダ内のファイルが S3 配置対象になります。

1. S3 にフロントエンドのモジュールを配置

    上記、静的ビルドでビルドしたモジュール (※ dist フォルダの中身全部) を対象のS3に配置してください。


[次の頁へ](test-data-charge.md)

[目次へ戻る](../../README.md)
