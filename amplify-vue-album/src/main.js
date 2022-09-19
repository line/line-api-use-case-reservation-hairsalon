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

createApp(App).use(store).use(router).mount("#app");
