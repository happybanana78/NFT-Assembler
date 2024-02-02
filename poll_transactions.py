import os
import subprocess
import json, time, glob

def pollTrx():

    txs_files = glob.glob("marmalade_token_creation/txs/tx-*.json")
    poll_txs_command = [os.getenv('KDA_TOOL_PATH'), "poll"] + txs_files + ["-n", os.getenv('KADENA_NODE')]
    process = subprocess.run(poll_txs_command, capture_output=True, text=True, check=True)

    # Isolate the body of the response
    body = []
    txs_status = json.loads(process.stdout)
    for url, data_list in txs_status.items():
        for item in data_list:
            body = item['body']

    # If there are no transactions to poll, wait 5 seconds and try again
    if not body:
        print("No transactions to poll")
        time.sleep(30)
        pollTrx()

    # For each transaction, update the status in the status.json file
    for request_key, request_value in body.items():

        # Set the status of the transaction to "confirmed"
        if request_value['result']['status'] == "success":

            with open("status.json", "r") as json_file:
                text_file = json.load(json_file)

            for tx_id, tx_info in text_file.items():
                if tx_info['requestKey'] == request_key:
                    tx_info['status'] = "confirmed"

            with open("status.json", "w") as json_file:
                json.dump(text_file, json_file, indent=4)

        # Set the status of the transaction to "failed"
        elif request_value['result']['status'] == "failure":
                
                with open("status.json", "r") as json_file:
                    text_file = json.load(json_file)
    
                for tx_id, tx_info in text_file.items():
                    if tx_info['requestKey'] == request_key:
                        tx_info['status'] = "failed"
    
                with open("status.json", "w") as json_file:
                    json.dump(text_file, json_file, indent=4)

    # Check if all transactions have been processed
    with open("status.json", "r") as json_file:
        text_file = json.load(json_file)

    for tx_id, tx_info in text_file.items():
        if tx_info['status'] == "pending":
            print("Waiting for all transactions to be processed")
            time.sleep(10)
            pollTrx()
        else:
            break
        
    print("All transactions have been processed")
    return
        