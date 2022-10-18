import {
  applyPolyfills,
  // eslint-disable-next-line prettier/prettier
  defineCustomElements
} from "@aws-amplify/ui-components/loader";
import Amplify from "aws-amplify";
import { createApp } from "vue";
import App from "./App.vue";
import aws_exports from "./aws-exports";
import router from "./router";
import store from "./store";

Amplify.configure(aws_exports);
applyPolyfills().then(() => {
  defineCustomElements(window);
});

Amplify.configure({
  API: {
    endpoints: [
      {
        name: "LambdaAPIGateway",
        endpoint: "https://ect2qmyf4e.execute-api.ap-northeast-1.amazonaws.com",
      },
    ],
  },
});

createApp(App).use(store).use(router).mount("#app");
