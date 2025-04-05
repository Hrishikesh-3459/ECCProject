# Azure Functions Event Hub Data Pipeline

Sender function - house-simulator

Receiver function - receiver-function

Need to type the following commands

`az login`

Create a resource group 

`az group create --name ECCResourceGroup --location eastus`

Create an Event Hubs namespace

`az eventhubs namespace create --name ECC-namespace --resource-group ECCResourceGroup --location eastus`

Create the Event Hub

`az eventhubs eventhub create --name house-data-stream --resource-group myResourceGroup --namespace-name my-eh-namespace`

Get the connection string from Azure Portal:

	•	Go to your Event Hub Namespace
	•	Under Shared Access Policies > RootManageSharedAccessKey
	•	Copy the Connection String–Primary Key

Add connection string to following places

house-simulator/function_app.py -> line 58

reciver-function/local.setting.json 
