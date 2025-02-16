import os
import requests


def get_job(task_id: int, org: str = "") -> dict:
    """
    Get a job by its ID.

    Parameters:
        task_id (int): The ID of the task you want to get the job for.
        org (str): The organization parameter to send, default empty string.
    Returns:
        dict: The job object returned by the API.

    Sample Response:

    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "url": "http://192.168.1.51:8080/api/jobs/2",
                "id": 2,
                "task_id": 3,
                "project_id": 1,
                "assignee": null,
                "guide_id": null,
                "dimension": "2d",
                "bug_tracker": "",
                "status": "annotation",
                "stage": "annotation",
                "state": "new",
                "mode": "interpolation",
                "frame_count": 31,
                "start_frame": 0,
                "stop_frame": 30,
                "data_chunk_size": 31,
                "data_compressed_chunk_type": "audio",
                "created_date": "2025-02-16T11:02:43.274864Z",
                "updated_date": "2025-02-16T11:02:43.274884Z",
                "issues": {
                    "url": "http://192.168.1.51:8080/api/issues?job_id=2",
                    "count": 0
                },
                "labels": {
                    "url": "http://192.168.1.51:8080/api/labels?job_id=2"
                },
                "type": "annotation",
                "organization": null,
                "target_storage": null,
                "source_storage": null,
                "ai_audio_annotation_status": "not started",
                "ai_audio_annotation_task_id": "",
                "ai_audio_annotation_error_msg": "",
                "task_flags": {
                    "is_librivox": false,
                    "is_vctx": false,
                    "is_voxceleb": false,
                    "is_librispeech": false,
                    "is_voxpopuli": false,
                    "is_tedlium": false,
                    "is_commonvoice": true
                }
            }
        ]
    }
    """
    url = os.getenv("HOST_URL") + f"/api/jobs?task_id={task_id}&org={org}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {os.getenv('AUTH_TOKEN')}",
        "X-CSRFTOKEN": os.getenv("CSRF_TOKEN"),
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()

    return {"error": response.text}
