import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()


@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="house-data-stream",
                               connection="EventHubConnection") 
def ReceiveHouseData(azeventhub: func.EventHubEvent):
    try:
        # Decode and parse the JSON payload
        payload = azeventhub.get_body().decode('utf-8')
        data = json.loads(payload)

        logging.info(f"✅ Received {len(data)} rows from Event Hub")
        logging.debug(data[:2])  # Preview first 2 rows

        # TODO: Add logic to process or store the data (e.g., insert into DB)

    except Exception as e:
        logging.error(f"❌ Failed to process event: {str(e)}")
