import os
import requests

# Uploads image to IPFS and returns the CID
def uploadImage(image):
    formData = {
        'file': open(image, 'rb')
    }

    headers = {
        'Authorization': 'Bearer ' + os.getenv('PINATA_API_KEY')
    }

    try:
        response = requests.post(os.getenv('PINATA_URL'), files=formData, headers=headers)

        if response.status_code == 200:
            #print("Upload successful!")
            return response.json()['IpfsHash']
        else:
            print("Upload failed")
            print(response.text)

    except Exception as e:
        print("Error executing request:", e)

# Uploads metadata to IPFS and returns the CID
def uploadMetadata(metadata):
    formData = {
        'file': open(metadata, 'rb')
    }

    headers = {
        'Authorization': 'Bearer ' + os.getenv('PINATA_API_KEY')
    }

    try:
        response = requests.post(os.getenv('PINATA_URL'), files=formData, headers=headers)

        if response.status_code == 200:
            #print("Upload successful!")
            return response.json()['IpfsHash']
        else:
            print("Upload failed")
            print(response.text)

    except Exception as e:
        print("Error executing request:", e)
