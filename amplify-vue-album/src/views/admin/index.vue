<template>
  <div>
    <h1>管理者サイト</h1>
  </div>
  <pre>res:{{ responces }}</pre>
</template>

<script>
// API機能読み込み
import { API } from "aws-amplify";

export default {
  name: "AdminIndex",
  components: {},
  data() {
    return {
      // API Gatewayの名称
      apiName: "liff-app-backend",
      // API Gatewayの設定パス
      path: "/cource_list_get",
      text: "",
      responces: null,
    };
  },
  mounted: function () {
    this.getData();
  },

  methods: {
    getData: function () {
      // 検索ID指定
      const path = this.path;
      // オプション
      // const myInit = {
      //   headers: {},
      //   response: true,
      // };
      // データ取得
      API.get(this.apiName, path)
        .then((response) => {
          // テーブル表示
          this.responces = response;
          console.log(this.responces);
        })
        .catch((error) => {
          console.log(error);

          // テーブルリセット
          this.responces = null;
        });
    },
    postData: function () {
      // オプション
      // const myInit = {
      //   headers: {},
      //   response: true,
      //   body: {
      //     id: Number(this.id),
      //     name: String(this.name),
      //   },
      // };
      // データ登録
      API.post(this.apiName, this.path)
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>
