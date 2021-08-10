## Production (AWS) front-end environment construction

1. .env file settings

    Set the LIFF ID of the LIFF app in `LIFF_ID` of the front/.env file, the URL of AWS APIGateway in `BASE_URL`, and the stage name of AWS APIGateway in `APIGATEWAY_STAGE`.

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

1. node_modules installation

    If the Node.js dependent package (* node_modules folder) isn't installed in the front project, execute one of these commands directly under the front folder to install node_modules:
    ```
    npm install
    ```
    or
    ```
    yarn install
    ```

1. Static build

    Generate a static module that builds the front side and place it in S3. Run one of these commands directly under the front folder:
    ```
    npm run build
    ```
    or
    ```
    yarn run build
    ```
    When the build is complete, the front/dist folder will be created. The files in the dist folder are placed in S3.

1. Place front-end modules in S3

    Place the module built by Static build (*all dist folder content) in the target S3.


[Next page](test-data-charge.md)  

[Back to Table of Contents](README_en.md)
