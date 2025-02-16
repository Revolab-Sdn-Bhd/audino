import os
import requests


def upload_task_data(
    task_id,
    file_path,
    image_quality=70,
    sorting_method="lexicographical",
    org="",
):
    """
    Uploads the audio file to audino task API.

    Parameters:
        task_id (int): The ID of the task you want to upload the file to.
        file_path (str): The local path to the file you want to upload.
        image_quality (int): The image quality parameter to send, default 70.
        sorting_method (str): The sorting method parameter to send, default lexicographical.
        org (str): The organization parameter to send, default empty string.

    Returns:
        dict: The JSON response from the API if successful, or an error message.
    """
    # Correct URL without the colon before task_id
    url = os.getenv("HOST_URL") + f"/api/tasks/{task_id}/data?org={org}"

    # Remove 'Content-Type' header so requests can set it automatically.
    headers = {
        "Authorization": f"Token {os.getenv('AUTH_TOKEN')}",
        "X-CSRFTOKEN": os.getenv("CSRF_TOKEN"),
    }

    # Open the file in binary mode
    with open(file_path, "rb") as file:
        # The file is sent under the key 'client_files[0]'
        files = {"client_files[0]": file}

        # Additional form data
        data = {"image_quality": image_quality, "sorting_method": sorting_method}

        # Make the POST request with files and data as multipart/form-data
        response = requests.post(url, headers=headers, files=files, data=data)

    if response.status_code == 202:
        return response.json()

    return {"error": response.text}
