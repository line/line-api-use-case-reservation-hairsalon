import Amplify from "aws-amplify";
import API from "@aws-amplify/api";

// Amplify設定
Amplify['API'] = API;
Amplify.configure({
    API: {
        endpoints: [
            {
                name: "LambdaAPIGateway",
                endpoint: process.env.BASE_URL,
            },
        ]        
    }
});

/**
 * Amplifyプラグイン
 *
 * @return {Object}
 */
const VueAmplify = () => {
    return Amplify;
}

export default ({}, inject) => {
    inject("amplify", VueAmplify());
}
