import os
from os import listdir
import subprocess
from PIL import Image
from dotenv import load_dotenv
import random, json, gc, glob
import sqlite3
from sqlite3 import Error
from ipfs import uploadImage, uploadMetadata
from poll_transactions import pollTrx

# Load .env file
load_dotenv()

# Backgrounds
common_bg_path = "assets/background/Common"
rare_bg_path = "assets/background/Rare"
legendary_bg_path = "assets/background/Legendary"

# Body
common_body_path = "assets/body/Common"
rare_body_path = "assets/body/Rare"
legendary_body_path = "assets/body/Legendary"

# Eyes
common_eyes_path = "assets/eyes/Common"
rare_eyes_path = "assets/eyes/Rare"
legendary_eyes_path = "assets/eyes/Legendary"

# Mouth
common_mouth_path = "assets/mouth/Common"
rare_mouth_path = "assets/mouth/Rare"
legendary_mouth_path = "assets/mouth/Legendary"

# Accessories
rare_accessories_path = "assets/accessories/Rare"
legendary_accessories_path = "assets/accessories/Legendary"

# Head Accessories
common_head_path = "assets/head/Common"
rare_head_path = "assets/head/Rare"
legendary_head_path = "assets/head/Legendary"

# Probability variables
prob_common = 1
prob_rare = 0.5
prob_legendary = 0.2
prob_is_accessories = 0.3
prob_is_head = 0.3

# Lists
final_image = []
final_image_accessories = []
final_image_head = []
rarity_list = []

# Number of NFTs to generate
n_copies = 3
n_counter = 0

# Database path
database = "assets/output/store_list.db"

def setRarity():
    # Define Keywords to look for
    common = "common"
    rare = "rare"
    legendary = "legendary"

    # Define keyword counters
    leg = 0
    ra = 0
    co = 0

    # Count rarity attributes and return value
    for filename in rarity_list:

        # Rarity Names
        rc = "Common"
        ru = "Uncommon"
        rr = "Rare"
        re = "Epic"
        rl = "Legendary"
        rm = "Mythic"
        rg = "God"
        if legendary in filename or rare in filename or common in filename:
            co += filename.count(common)
            leg += filename.count(legendary)
            ra += filename.count(rare)
    media = (((leg * 5) + (ra * 3) + (co * 1)) / 6)
    rounded_media = round(media, 3)
    if 0 < rounded_media < 1:
        return rc
    elif 1 <= rounded_media < 2:
        return ru
    elif 2 <= rounded_media < 3:
        return rr
    elif 3 <= rounded_media <= 3.5:
        return re
    elif 3.5 < rounded_media < 4.333:
        return rl
    elif 4.333 <= rounded_media <= 4.833:
        return rm
    elif rounded_media == 5:
        return rg

# Create Db and tables and add data to the DB
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def add_data(conn, data_tile):
    sql = ''' INSERT INTO attributes(name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, data_tile)
    conn.commit()
    return cur.lastrowid

def get_data(current_data):
    global n_counter, database
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM attributes")
    rows = cur.fetchall()
    for row in rows:
        if current_data in row:
            print("Double found! Ignoring it.")
            n_counter -= 1
            return True

def execute_add_data(attributes):
    global database
    # create a database connection
    conn = create_connection(database)
    with conn:
        # add the data to the table
        data_tile = (attributes),
        add_data(conn, data_tile)

def only_create_table():
    global database
    sql_create_data_table = """ CREATE TABLE IF NOT EXISTS attributes (
                                        name text NOT NULL
                                    ); """
    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn, sql_create_data_table)
    else:
        print("Error! cannot create the database connection.")

def probability():
    prob = random.random()
    return prob

def mainLoop():
    global n_counter, n_copies, rarity_list

    # Delete all files in the metadata folder
    files = glob.glob('assets/output/metadata/*')
    for f in files:
        if f != 'assets/output/metadata/.gitkeep':
            os.remove(f)

    # Delete all files in the txs folder
    files = glob.glob('marmalade_token_creation/txs/*')
    for f in files:
        os.remove(f)

    # Prepare status.json
    with open("status.json", "w") as statusJsonFile:
        statusJsonFile.write('{\n}')
        statusJsonFile.close()

    # Prepare cids.txt
    with open("assets/output/cids.txt", "w") as cid_file:
        cid_file.write('')
        cid_file.close()

    while n_counter < n_copies:
        is_accessories = False
        is_head = False

        # Generate background
        while True:
            if prob_rare < probability() <= prob_common :
                image_list_background_common = []
                for image in listdir(common_bg_path):
                    image_list_background_common.append(image)
                result = random.choice(image_list_background_common)    
                final_image.append(common_bg_path + "/" + result)
                background_value_1 = result.replace(".png", "")
                background_value = background_value_1.replace("_", " ")
                rarity_list.append(background_value)
                break
            if prob_legendary < probability() <= prob_rare:
                image_list_background_rare = []
                for image in listdir(rare_bg_path):
                    image_list_background_rare.append(image)
                result = random.choice(image_list_background_rare)  
                final_image.append(rare_bg_path + "/" + result)  
                background_value_1 = result.replace(".png", "")
                background_value = background_value_1.replace("_", " ")
                rarity_list.append(background_value)
                break
            if probability() <= prob_legendary:
                image_list_background_legendary = []
                for image in listdir(legendary_bg_path):
                    image_list_background_legendary.append(image)
                result = random.choice(image_list_background_legendary)    
                final_image.append(legendary_bg_path + "/" + result)
                background_value_1 = result.replace(".png", "")
                background_value = background_value_1.replace("_", " ")
                rarity_list.append(background_value)
                break

        # Generate body
        while True:
            if prob_rare < probability() <= prob_common :
                image_list_body_common = []
                for image in listdir(common_body_path):
                    image_list_body_common.append(image)
                result = random.choice(image_list_body_common)    
                final_image.append(common_body_path + "/" + result)
                body_value_1 = result.replace(".png", "")
                body_value = body_value_1.replace("_", " ")
                rarity_list.append(body_value)
                break
            if prob_legendary < probability() <= prob_rare:
                image_list_body_rare = []
                for image in listdir(rare_body_path):
                    image_list_body_rare.append(image)
                result = random.choice(image_list_body_rare)  
                final_image.append(rare_body_path + "/" + result)  
                body_value_1 = result.replace(".png", "")
                body_value = body_value_1.replace("_", " ")
                rarity_list.append(body_value)
                break
            if probability() <= prob_legendary:
                image_list_body_legendary = []
                for image in listdir(legendary_body_path):
                    image_list_body_legendary.append(image)
                result = random.choice(image_list_body_legendary)   
                final_image.append(legendary_body_path + "/" + result) 
                body_value_1 = result.replace(".png", "")
                body_value = body_value_1.replace("_", " ")
                rarity_list.append(body_value)
                break   

        # Generate eyes
        while True:
            if prob_rare < probability() <= prob_common :
                image_list_eyes_common = []
                for image in listdir(common_eyes_path):
                    image_list_eyes_common.append(image)
                result = random.choice(image_list_eyes_common)    
                final_image.append(common_eyes_path + "/" + result)
                eyes_value_1 = result.replace(".png", "")
                eyes_value = eyes_value_1.replace("_", " ")
                rarity_list.append(eyes_value)
                break
            if prob_legendary < probability() <= prob_rare:
                image_list_eyes_rare = []
                for image in listdir(rare_eyes_path):
                    image_list_eyes_rare.append(image)
                result = random.choice(image_list_eyes_rare)  
                final_image.append(rare_eyes_path + "/" + result)  
                eyes_value_1 = result.replace(".png", "")
                eyes_value = eyes_value_1.replace("_", " ")
                rarity_list.append(eyes_value)
                break
            if probability() <= prob_legendary:
                image_list_eyes_legendary = []
                for image in listdir(legendary_eyes_path):
                    image_list_eyes_legendary.append(image)
                result = random.choice(image_list_eyes_legendary)   
                final_image.append(legendary_eyes_path + "/" + result) 
                eyes_value_1 = result.replace(".png", "")
                eyes_value = eyes_value_1.replace("_", " ")
                rarity_list.append(eyes_value)
                break 

        # Generate mouth
        while True:
            if prob_rare < probability() <= prob_common :
                image_list_mouth_common = []
                for image in listdir(common_mouth_path):
                    image_list_mouth_common.append(image)
                result = random.choice(image_list_mouth_common)    
                final_image.append(common_mouth_path + "/" + result)
                mouth_value_1 = result.replace(".png", "")
                mouth_value = mouth_value_1.replace("_", " ")
                rarity_list.append(mouth_value)
                break
            if prob_legendary < probability() <= prob_rare:
                image_list_mouth_rare = []
                for image in listdir(rare_mouth_path):
                    image_list_mouth_rare.append(image)
                result = random.choice(image_list_mouth_rare)  
                final_image.append(rare_mouth_path + "/" + result)  
                mouth_value_1 = result.replace(".png", "")
                mouth_value = mouth_value_1.replace("_", " ")
                rarity_list.append(mouth_value)
                break
            if probability() <= prob_legendary:
                image_list_mouth_legendary = []
                for image in listdir(legendary_mouth_path):
                    image_list_mouth_legendary.append(image)
                result = random.choice(image_list_mouth_legendary)   
                final_image.append(legendary_mouth_path + "/" + result) 
                mouth_value_1 = result.replace(".png", "")
                mouth_value = mouth_value_1.replace("_", " ")
                rarity_list.append(mouth_value)
                break 

        # Generate Accessories
        if probability() <= prob_is_accessories:
            while True:
                if prob_legendary < probability() <= prob_rare:
                    image_list_accessories_rare = []
                    for image in listdir(rare_accessories_path):
                        image_list_accessories_rare.append(image)
                    result = random.choice(image_list_accessories_rare)  
                    final_image_accessories.append(rare_accessories_path + "/" + result)  
                    body_accessories_value_1 = result.replace(".png", "")
                    body_accessories_value = body_accessories_value_1.replace("_", " ")
                    rarity_list.append(body_accessories_value)
                    break
                if probability() <= prob_legendary:
                    image_list_accessories_legendary = []
                    for image in listdir(legendary_accessories_path):
                        image_list_accessories_legendary.append(image)
                    result = random.choice(image_list_accessories_legendary)   
                    final_image_accessories.append(legendary_accessories_path + "/" + result) 
                    body_accessories_value_1 = result.replace(".png", "")
                    body_accessories_value = body_accessories_value_1.replace("_", " ")
                    rarity_list.append(body_accessories_value)
                    break 
        else:
            body_accessories_value = "None"

        # Generate head accessories
        if probability() <= prob_is_head:
            while True:
                if prob_rare < probability() <= prob_common :
                    image_list_head_common = []
                    for image in listdir(common_head_path):
                        image_list_head_common.append(image)
                    result = random.choice(image_list_head_common)    
                    final_image_head.append(common_head_path + "/" + result)
                    head_accessories_value_1 = result.replace(".png", "")
                    head_accessories_value = head_accessories_value_1.replace("_", " ")
                    rarity_list.append(head_accessories_value)
                    break
                if prob_legendary < probability() <= prob_rare:
                    image_list_head_rare = []
                    for image in listdir(rare_head_path):
                        image_list_head_rare.append(image)
                    result = random.choice(image_list_head_rare)  
                    final_image_head.append(rare_head_path + "/" + result)  
                    head_accessories_value_1 = result.replace(".png", "")
                    head_accessories_value = head_accessories_value_1.replace("_", " ")
                    rarity_list.append(head_accessories_value)
                    break
                if probability() <= prob_legendary:
                    image_list_head_legendary = []
                    for image in listdir(legendary_head_path):
                        image_list_head_legendary.append(image)
                    result = random.choice(image_list_head_legendary)   
                    final_image_head.append(legendary_head_path + "/" + result) 
                    head_accessories_value_1 = result.replace(".png", "")
                    head_accessories_value = head_accessories_value_1.replace("_", " ")
                    rarity_list.append(head_accessories_value)
                    break 
        else:
            head_accessories_value = "None"

        # Final image layer assembly
        n_counter += 1
        print(n_counter)
        store_list = final_image + final_image_accessories + final_image_head
        only_create_table()
        if get_data(str(store_list)):
            gc.collect()
            continue
        execute_add_data(str(store_list))
        store_list.clear()
        layer_background = Image.open(final_image[0]).convert("RGBA")
        layer_body = Image.open(final_image[1])
        layer_eyes = Image.open(final_image[2])
        layer_mouth = Image.open(final_image[3])
        if len(final_image_accessories) > 0:
            layer_accessories = Image.open(final_image_accessories[0])
            is_accessories = True
        if len(final_image_head) > 0:
            layer_head = Image.open(final_image_head[0])
            is_head = True
            
        first_assembly = Image.alpha_composite(layer_background, layer_body)
        second_assembly = Image.alpha_composite(first_assembly, layer_eyes)
        third_assembly = Image.alpha_composite(second_assembly, layer_mouth)

        if is_accessories:
            final_assembly = Image.alpha_composite(third_assembly, layer_accessories)
            final_assembly.save(f"assets/output/{n_counter}.png")
            if not is_head:
                final_image.clear()
                final_image_accessories.clear()
                final_image_head.clear()
        if is_head:
            if is_accessories:
                assembly = Image.alpha_composite(final_assembly, layer_head)
                assembly.save(f"assets/output/{n_counter}.png")
                final_image.clear()
                final_image_accessories.clear()
                final_image_head.clear()
            else:
                final_assembly = Image.alpha_composite(third_assembly, layer_head)
                final_assembly.save(f"assets/output/{n_counter}.png")
                final_image.clear()
                final_image_accessories.clear()
                final_image_head.clear()
        if not is_accessories and not is_head:
            third_assembly.save(f"assets/output/{n_counter}.png")
            final_image.clear()
            final_image_accessories.clear()
            final_image_head.clear()

        # Upload image to IPFS
        image_cid = uploadImage(f"assets/output/{n_counter}.png")

        # Save image CID locally
        with open("assets/output/cids.txt", "a") as cid_image_file:
            cid_image_file.write(image_cid + "\n")
            cid_image_file.close()
                    
        # Metadata generation
        data = {
            "name": f"Bloob #{n_counter}",
            "description": f"Bloob #{n_counter} is the #{n_counter} of 10000 unique slimy pets that are invading alursini's homes all around the Alursers Universe.",
            "image": f"ipfs://{image_cid}/{n_counter}.png",
            "properties": { 
                "background": background_value.title(), 
                "body": body_value.title(),
                "eyes": eyes_value.title(),
                "mouth": mouth_value.title(),
                "head_accessories": head_accessories_value.title(),
                "body_accessories": body_accessories_value.title(),
                "rarity": setRarity()
            },
            "external_url": "https://alursers.app/bloobs",
            "authors": [
                {
                    "name": "Alursers",
                }
            ],
            "collection": {
                "name": "Bloobs",
                "family": "Alursers Universe"
            }
        }
        rarity_list.clear()
        json_data = json.dumps(data)
        with open("assets/output/metadata/" + str(n_counter) + ".json", "w") as jsonFile:
            jsonFile.write(json_data)
            jsonFile.close()

        # Upload metadata to IPFS
        metadata_cid = uploadMetadata(f"assets/output/metadata/{n_counter}.json")

        # Save metadata CID locally
        with open("assets/output/cids.txt", "a") as cid_metadata_file:
            cid_metadata_file.write(metadata_cid + "\n")
            cid_metadata_file.close()

        # Set metadata CID to the blockchain transaction
        with open("marmalade_token_creation/env_data.json", "r") as file:
            data = json.load(file)
            data["metadata"] = 'ipfs://' + metadata_cid
        with open("marmalade_token_creation/env_data.json", "w") as file:
            json.dump(data, file)

        # Generate blockchain transaction
        generate_tx_command = [os.getenv('KDA_TOOL_PATH'), "gen", "-t", 'marmalade_token_creation/mint_token.yaml', '-d', 'marmalade_token_creation/data.yaml', '-o', f'marmalade_token_creation/txs/tx-{n_counter}.yaml']
        process = subprocess.run(generate_tx_command, capture_output=True, text=True, check=True)

        if process.returncode != 0:
            print("Tx generation failed: ", process.stderr)
        # else:
        #     print("Tx generated!")

        # Sign transaction
        sign_tx_command = [os.getenv('KDA_TOOL_PATH'), "sign", "-k", "marmalade_token_creation/keys.txt", f'marmalade_token_creation/txs/tx-{n_counter}.yaml']
        process = subprocess.run(sign_tx_command, capture_output=True, text=True, check=True)

        if process.returncode != 0:
            print("Tx signing failed: ", process.stderr)
        # else:
        #     print("Tx signed!")

        # Update status.json
        status_data = {
            "status": "pending",
            "message": f"Transaction {n_counter} pending",
            "requestKey": None,
        }

        with open("status.json", "r") as file:
            data = json.load(file)

        data['tx-' + str(n_counter)] = status_data

        with open("status.json", "w") as file:
            json.dump(data, file, indent=4)

    # Send transaction
    txs_files = glob.glob("marmalade_token_creation/txs/tx-*.json")
    send_txs_command = [os.getenv('KDA_TOOL_PATH'), "send"] + txs_files + ["-n", os.getenv('KADENA_NODE')]
    process = subprocess.run(send_txs_command, capture_output=True, text=True, check=True)

    if process.returncode != 0:
        print("Txs sending failed: ", process.stderr)
    else:
        print("Txs sent!")

    # Add the right requestKey to the status.json file
    txs_status = json.loads(process.stdout)
    requestKeys = []

    for url, data_list in txs_status.items():
        for item in data_list:
            requestKeys = item['body']['requestKeys']

    with open("status.json", "r") as file:
        data = json.load(file)

    for i in range(len(requestKeys)):
        data['tx-' + str(i + 1)]['requestKey'] = requestKeys[i]

    with open("status.json", "w") as file:
        json.dump(data, file, indent=4)
        jsonFile.close()

    # Start polling transactions
    pollTrx()

mainLoop()
