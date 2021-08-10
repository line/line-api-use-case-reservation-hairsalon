# Operation check

## LIFF endpoint configuration

Set the endpoint URL of the LIFF app created in [Create LINE channel > Add LIFF app].
*To build a local environment, follow the steps in [Front-end development environment](front-end-development-environment.md) and enter the local URL.

1. In the [LINE Developers Console](https://developers.line.biz/console/), go to the LIFF app page created in [Create LINE channel > Add LIFF app].
![LIFF console](../images/en/liff-console-en.png)

1. Click the Edit button of the Endpoint URL.
![Edit the endpoint URL](../images/en/end-point-url-editing-en.png)

1. Enter the CloudFrontDomainName that you took a note of in the [Building the Backend > Deploying the Hair Salon Application] procedure with https:// at the beginning as shown below, and then click Update.
![Description of the endpoint URL](../images/en/end-point-url-description-en.png)

## Rich menu settings

If you want to set the rich menu and start the app, see this link to set it up.  
https://developers.line.biz/en/docs/messaging-api/using-rich-menus/#creating-a-rich-menu-with-the-line-manager

# Operation check

After completing all the steps, please access the LIFF URL of the LIFF app that you created in [Create LINE Channel > Add LIFF App] and check if it works.

*It may take up to two hours to create the Cloudfront, so if you see the Access Denied screen, please wait a while before checking again.

[Back to Table of Contents](README_en.md)
