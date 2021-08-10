## ローカルフロントエンド環境構築
フロントエンドの開発は Nuxt.js プロジェクトの SPA (Single Page Application) で開発を行います。ローカル環境で Nuxt 開発用サーバーの起動や本番モジュールの静的ビルドを行います。ソースコードダウンロード後、ローカル環境で以下の作業を行ってください。

- .env ファイルの設定

    .env ファイルにフロントのアプリケーションで使用する値を設定してください。

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

    - `LIFF_ID` には LINE チャンネルの LIFF アプリの LIFF ID を設定
    - `BASE_URL` には AWS APIGateway の URL を設定
    - `APIGATEWAY_STAGE` には AWS APIGateway のステージ名を設定
    - `AJAX_MODULE` には Ajax 通信の時に使用するモジュール（ Amplify API は "amplify" ／ Axios は "axios" ）を設定

- node_modules インストール

    front プロジェクトに Node.js の依存パッケージ(※ node_modules フォルダ)がインストールされていない場合、 front フォルダー直下で以下のコマンドを実行して node_modules をインストールしてください。
    ```
    npm install
    ```
    もしくは
    ```
    yarn install
    ```
    インストールが完了したら front/`node_modules` フォルダが生成されています。

- LIFF アプリのエンドポイントURLの修正

    ローカル開発環境の Web サーバーで開発する為、 LINE チャンネルの LIFF アプリの`エンドポイントURL`を以下の URL に変更してください（※開発完了後 CloudFront の URL に戻してください）。
    ```
    https://localhost:3000
    ```

- Nuxt 開発サーバーの起動

    ローカル環境での開発は Nuxt 開発サーバーを起動して行います。 front フォルダ直下で以下のコマンドを実行して Nuxt 開発サーバーを起動してください。 `https://localhost:3000` にアクセスできるようになります。上記 「 LIFF アプリのエンドポイントURLの修正 」を設定済みの場合、 LIFF アプリの LIFF URL (例：`https://liff.line.me/9999999999-xxxxxxxx`) でローカル環境にアクセスして開発を行えます。
    ```
    npm run dev
    ```
    もしくは
    ```
    yarn run dev
    ```

- SSL 証明書（自己署名証明書）のインストール

    ブラウザ等で https://localhost:3000 にアクセスする場合、 SSL 証明書の警告が表示されます。警告を表示されないようにしたい場合はローカル開発環境に SSL 証明書をインストールする必要があります。 front/cert フォルダ内の `localhost.crt` を「`信頼されたルート証明機関`」にインストールしてください。

    ※ SSL 証明書（自己署名証明書）のインストールは localhost.crt ファイルを実行することで行うことができます。

[次の頁へ](test-data-charge.md)

[目次へ戻る](../../README.md)
