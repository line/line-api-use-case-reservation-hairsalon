# 動作確認
## LIFFエンドポイントの設定
【LINEチャネルの作成 -> LIFFアプリの追加】にて作成したLIFFアプリのエンドポイントURLを設定します。  
※ローカル環境構築の場合は、[フロントエンドの開発環境](front-end-development-environment.md)の手順に従い、ローカルのURLを入れてください。

1. [LINE Developersコンソール](https://developers.line.biz/console/)にて、【LINEチャネルの作成 -> LIFFアプリの追加】にて作成したLIFFアプリのページに遷移する。
![LIFFのコンソール](../images/jp/liff-console.png)

1. エンドポイントURL項目の編集ボタンを押下する。
![エンドポイントURLの編集](../images/jp/end-point-url-editing.png)

1. 【バックエンドの構築 -> ヘアサロンアプリのデプロイ】の手順にてメモを取ったCloudFrontDomainNameを 先頭にhttps:// を付けて以下のように記載し、更新を押下する。
![エンドポイントURLの記載](../images/jp/end-point-url-description.png)

## リッチメニューの設定
リッチメニューを設定してアプリを起動する場合、以下リンクを参照し設定してください。  
https://developers.line.biz/ja/docs/messaging-api/using-rich-menus/#creating-a-rich-menu-with-the-line-manager

## 動作確認

すべての手順が完了後、【LINEチャネルの作成 -> LIFFアプリの追加】の手順にて作成したLIFFアプリのLIFF URLにアクセスし、動作を確認してください。

※Cloudfront作成に2時間ほどかかる可能性があります。Access Deniedの画面が表示される場合、一度時間を置いてから確認して下さい。

[目次へ戻る](../../README.md)
