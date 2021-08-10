## Building a local front-end environment

Front-end development is done in the Nuxt.js project's Single Page Application (SPA). Start the Nuxt development server and static build the production module in your local environment. After downloading the source code, perform these operations in the local environment.

- .env file settings

    Set the .env file to the value used by the front application.

    ▼ .env file
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

    - Set `LIFF_ID` to the LIFF ID of the LINE channel's LIFF app.
    - Set the URL of AWS APIGateway to `BASE_URL`
    - Set the stage name of the AWS APIGateway to `APIGATEWAY_STAGE`.
    - Set the module used for Ajax communication (Amplify API is "amplify" / Axios is "axios") in `AJAX_MODULE`

- node_modules installation

    If the Node.js dependency package (* node_modules folder) isn't installed in the front project, run this command directly under the front folder to install node_modules.
    ```
    npm install
    ```
    or
    ```
    yarn install
    ```
    After the installation is complete, the front/`node_modules` folder will be created.

- Fixing LIFF app endpoint URLs

    To develop on the web server of your local development environment, change the `endpoint URL` of the LINE channel LIFF app to the following URL (*Change it back to the CloudFront URL after development is complete)
    ```
    https://localhost:3000
    ```

- Start the Nuxt development server

    Development in the local environment is done by starting the Nuxt development server. Start the Nuxt development server by executing the following command directly under the front folder. You should now be able to access `https://localhost:3000`. If you have already set "Fixing LIFF app endpoint URLs" above, you can access your local environment with the LIFF URL of your LIFF app (e.g. `https://liff.line.me/9999999999-xxxxxxxx`) for development.
    ```
    npm run dev
    ```
    or
    ```
    yarn run dev
    ```

- Install an SSL certificate (self-signed certificate)

    When you access https://localhost:3000 with a browser, you will see a warning about the SSL certificate. If you don't want the warning to appear, you need to install an SSL certificate in your local development environment. Install `localhost.crt` in the front/cert folder to `Trusted Root Certificate Authority`.

    *You can install the SSL certificate (self-signed certificate) by executing the localhost.crt file.

[Next page](test-data-charge.md)  

[Back to Table of Contents](README_en.md)
