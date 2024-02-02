import os
import subprocess

akord_cmd = r"C:\Users\leona\AppData\Local\Yarn\bin\akord.cmd"

# Login to Akord
def login():
    login_command = [akord_cmd, "login", os.getenv('AKORD_EMAIL')]

    try:

        process = subprocess.Popen(login_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        output, error = process.communicate(input=os.getenv('AKORD_PASSWORD'))

        if process.returncode != 0:
            print("Login failed:", error)
        else:
            print("Login successful!")

    except Exception as e:
        print("Error executing command:", e)

# Upload file to Akord
def upload(image):
    upload_command = [akord_cmd, "stack:create", os.getenv('AKORD_VAULT_ID'), "--file-path", image, "--parent-id", os.getenv('AKORD_PARENT_ID')]

    try:
        process = subprocess.run(upload_command, capture_output=True, text=True, shell=True, check=True, encoding='utf-8')

        if process.returncode != 0:
            print("Upload failed: ", process.stderr)
        else:
            print("Upload successful!")
            
            output_lines = process.stderr.splitlines()
            for line in output_lines:
                if "Stack successfully created with id:" in line:
                    image_id = line.split("Stack successfully created with id:")[1].strip()
                    return image_id

    except Exception as e:
        print("Error executing command:", e)
