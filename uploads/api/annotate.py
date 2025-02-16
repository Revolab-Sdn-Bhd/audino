import requests
import os


def create_annotation(
    job_id: int,
    transcript: str,
    start_time: float,
    end_time: float,
    label_id=1,
    frame=0,  # Retrieve from https://192.168.1.51:8080/api/jobs/:job_id/data/meta?org=
    org="",
) -> dict:
    """Create annotation for labelling

    Request Format:
    {
        "shapes": [
            {
                "frame": 0,
                "label_id": 1,
                "points": [
                    0,
                    0,
                    0.43,
                    0.43
                ],
                "type": "rectangle",
                "transcript": "Abang ",
                "gender": "",
                "locale": "",
                "age": "",
                "accent": "",
                "emotion": ""
            }
        ]
    }

    Response format (success):
    {
        "version": 0,
        "tags": [],
        "shapes": [
            {
                "type": "rectangle",
                "occluded": false,
                "outside": false,
                "z_order": 0,
                "rotation": 0.0,
                "points": [
                    0.44,
                    0.44,
                    1.04,
                    1.04
                ],
                "id": 2,
                "frame": 0,
                "label_id": 1,
                "group": null,
                "source": "manual",
                "transcript": "Jom lepak mamak",
                "gender": "",
                "age": "",
                "locale": "",
                "accent": "",
                "emotion": "",
                "attributes": [
                    {
                        "spec_id": 1,
                        "value": "DEFAULT_ATTR_VALUE"
                    }
                ],
                "elements": []
            }
        ],
        "tracks": []
    }
    """

    url = (
        os.getenv("HOST_URL")
        + f"/api/jobs/{job_id}/annotations?org={org}&action=create"
    )
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {os.getenv('AUTH_TOKEN')}",
        "X-CSRFTOKEN": os.getenv("CSRF_TOKEN"),
    }
    data = {
        "shapes": [
            {
                "frame": frame,
                "label_id": label_id,
                "points": [start_time, start_time, end_time, end_time],
                "type": "rectangle",
                "transcript": transcript,
            }
        ]
    }
    response = requests.patch(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()

    return {"error": response.text}
