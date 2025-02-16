import requests
import os


def get_task(task_id: int, org: str = "") -> dict:
    """
        Get a task by its ID.

        Parameters:
            task_id (int): The ID of the task you want to get.
            org (str): The organization parameter to send, default empty string.
        Returns:
            dict: The task object returned by the API.

        Sample Response:

        {
        "url": "http://192.168.1.51:8080/api/tasks/16",
        "id": 16,
        "name": "cwEsx5PC3CI_chunk_0012",
        "project_id": 1,
        "mode": "interpolation",
        "owner": {
            "url": "http://192.168.1.51:8080/api/users/1",
            "id": 1,
            "username": "cheelam",
            "first_name": "Chee Lam",
            "last_name": "Tan"
        },
        "assignee": null,
        "bug_tracker": "",
        "created_date": "2025-02-16T17:19:20.528907Z",
        "updated_date": "2025-02-16T17:19:28.430371Z",
        "overlap": 0,
        "segment_size": 804,
        "status": "annotation",
        "data_chunk_size": 804,
        "data_compressed_chunk_type": "audio",
        "guide_id": null,
        "data_original_chunk_type": "audio",
        "size": 806,
        "image_quality": 70,
        "data": 13,
        "dimension": "2d",
        "subset": "Train",
        "organization": null,
        "target_storage": null,
        "source_storage": null,
        "jobs": {
            "count": 2,
            "completed": 0,
            "validation": 0,
            "url": "http://192.168.1.51:8080/api/jobs?task_id=16"
        },
        "labels": {
            "url": "http://192.168.1.51:8080/api/labels?task_id=16"
        },
        "segment_duration": 28966,
        "flags": {
            "is_librivox": false,
            "is_vctx": false,
            "is_voxceleb": false,
            "is_librispeech": false,
            "is_voxpopuli": false,
            "is_tedlium": false,
            "is_commonvoice": true
        }
    }

    """
    url = os.getenv("HOST_URL") + f"/api/tasks/{task_id}?org={org}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {os.getenv('AUTH_TOKEN')}",
        "X-CSRFTOKEN": os.getenv("CSRF_TOKEN"),
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()

    return {"error": response.text}


def create_task(
    task_name: str,
    project_id: int,
    segment_duration: int,
    org="",
) -> dict:
    """Create the transcription task on audino

    Request Format:

    {
        "assignee_id": <id if assigned>,
        "name": "test",
        "project_id": "1",
        "subset": "Train",
        "assignee_id": null,
        "segment_duration": 1602,
        "overlap": "0",
        "flags": {
            "is_librivox": false,
            "is_vctx": false,
            "is_voxceleb": false,
            "is_librispeech": false,
            "is_voxpopuli": false,
            "is_tedlium": false,
            "is_commonvoice": true
        }
    }

    Response format (success):

    {
        "url": "http://192.168.1.51:8080/api/tasks/1",
        "id": 1,
        "name": "test",
        "project_id": 1,
        "mode": "",
        "owner": {
            "url": "http://192.168.1.51:8080/api/users/1",
            "id": 1,
            "username": "cheelam",
            "first_name": "Chee Lam",
            "last_name": "Tan"
        },
        "assignee": null,
        "bug_tracker": "",
        "created_date": "2025-02-16T08:04:49.366142Z",
        "updated_date": "2025-02-16T08:04:49.381887Z",
        "overlap": 0,
        "segment_size": 0,
        "status": "annotation",
        "guide_id": null,
        "dimension": "2d",
        "subset": "Train",
        "organization": null,
        "target_storage": null,
        "source_storage": null,
        "jobs": {
            "count": 0,
            "completed": 0,
            "validation": 0,
            "url": "http://192.168.1.51:8080/api/jobs?task_id=1"
        },
        "labels": {
            "url": "http://192.168.1.51:8080/api/labels?task_id=1"
        },
        "segment_duration": 1602,
        "flags": {
            "is_librivox": false,
            "is_vctx": false,
            "is_voxceleb": false,
            "is_librispeech": false,
            "is_voxpopuli": false,
            "is_tedlium": false,
            "is_commonvoice": true
        }
    }

    """

    url = os.getenv("HOST_URL") + f"/api/tasks?org={org}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {os.getenv('AUTH_TOKEN')}",
        "X-CSRFTOKEN": os.getenv("CSRF_TOKEN"),
    }
    data = {
        "name": task_name,
        "project_id": str(project_id),
        "subset": "Train",
        "assignee_id": None,
        "segment_duration": int(segment_duration),
        "overlap": "0",
        "flags": {
            "is_librivox": False,
            "is_vctx": False,
            "is_voxceleb": False,
            "is_librispeech": False,
            "is_voxpopuli": False,
            "is_tedlium": False,
            "is_commonvoice": True,
        },
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        return response.json()

    return {"error": response.text}
