import azure.functions as func
from azure.eventhub import EventHubProducerClient, EventData
import json
import datetime
import logging
import pandas as pd
import os

app = func.FunctionApp()

# Global variable to remember which time slot to send next
time_index = 0
df = None
unique_times = []

# Below is for 15 minutes
# @app.timer_trigger(schedule="0 */15 * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False) 
# Below is for 15 seconds
@app.timer_trigger(schedule="*/15 * * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False)
def SimulateHouseData(myTimer: func.TimerRequest) -> None:
    global time_index, df

    if myTimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Timer triggered: SimulateHouseData")

    # Load the CSV only once
    if df is None:
        file_path = os.path.join(os.path.dirname(__file__), "../simulated_1_day_3000_houses.csv")
        df = pd.read_csv(file_path)
        df = df.sort_values(by='local_15min').reset_index(drop=True)

    # Calculate total number of chunks
    total_chunks = len(df) // 3000

    # Safety check
    if time_index >= total_chunks:
        logging.info("All data chunks sent. Resetting to 0.")
        time_index = 0

    # Get the current chunk
    start_idx = time_index * 3000
    end_idx = start_idx + 3000
    chunk = df.iloc[start_idx:end_idx]

    # Clean the data (example: drop NaN and invalid values)
    chunk['grid'] = chunk['grid'].apply(lambda x: x if pd.notna(x) and x >= 0 else 0)

    # Simulate sending data
    logging.info(f"Sending chunk #{time_index + 1}/{total_chunks}, rows: {len(chunk)}")

    # Convert DataFrame chunk to JSON lines
    data_json_lines = chunk.to_dict(orient='records')
    json_payload = json.dumps(data_json_lines)

    # Send to Azure Event Hub
    connection_str = "ENTER HERE"
    eventhub_name = "house-data-stream"

    producer = EventHubProducerClient.from_connection_string(conn_str=connection_str, eventhub_name=eventhub_name)
    event_data_batch = producer.create_batch()
    event_data_batch.add(EventData(json_payload))
    producer.send_batch(event_data_batch)
    producer.close()

    logging.info(f"Sent chunk #{time_index + 1}/{total_chunks} to Event Hub")

    # Increment for next run
    time_index += 1