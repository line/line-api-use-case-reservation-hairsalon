# Input test data

- Input test data to DynamoDB

  You need to input store information data for the operation of this app.
  Put the test data into the table with the table name set in HairSalonShopMasterDBName in template.yaml when deploying the hair salon app.
  The test data is a json format string of dynamodb_data / shop_master_id_1.json ~ shop_master_id_6.json in the backend > APP folder.
  Paste and submit the file in the DynamoDB console of the AWS management console. (*See image below)

  [Input test data]
  ![Data input image](../images/en/test-data-charge-en.png)

  Also, the part below @ in the lineAccountUrl of the json text needs to be changed to the basic ID of the bot of the MessagingAPI channel you created.

  [Check the basic ID of the bot]
  ![Bot Basic ID console](../images/en/bot-basic-id-en.png)

[Next page](validation.md)  

[Back to Table of Contents](README_en.md)
