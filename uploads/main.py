import os
import pandas as pd
import time
from dotenv import load_dotenv

from utils import *
from api import *

env_path = os.path.join(os.path.dirname(__file__), ".env")
data_dir = os.path.join(os.path.dirname(__file__), "data")

if os.path.exists(env_path):
    success = load_dotenv(dotenv_path=env_path)
    print(f"Loaded {env_path} file: {success}")


# Load all environment variables
HOST_URL = os.getenv("HOST_URL")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
CSRF_TOKEN = os.getenv("CSRF_TOKEN")
PROJECT_ID = os.getenv("PROJECT_ID")
DEFAULT_LABEL_ID = os.getenv("DEFAULT_LABEL_ID")
ORG = os.getenv("ORG") or ""


if __name__ == "__main__":
    # Load the data
    dataset = pd.read_csv(os.path.join(data_dir, "upload.csv"))

    for row in dataset.values:
        audio_file = str(row[0])
        file_path = os.path.join(data_dir, f"chunks/{audio_file}")
        transcription = preprocess_transcription(row[1])

        # Get the audio length
        audio_length = get_audio_length_ms(file_path)

        # Create a task
        new_task: dict = create_task(
            task_name=audio_file.split(".")[0],
            project_id=PROJECT_ID,
            segment_duration=audio_length,
            org=ORG,
        )
        print(f"Task created: {new_task}")

        new_task_id = new_task.get("id")

        # Upload the audio file
        upload_response = upload_task_data(
            task_id=new_task_id,
            file_path=file_path,
            org=ORG,
        )
        print(f"Audio file uploaded: {upload_response}")

        # Wait for 3 seconds
        time.sleep(3)
        print(get_task(new_task_id, ORG))

        # Get the job ID
        new_jobs = get_job(new_task_id, ORG)
        job_id = new_jobs.get("results")[-1].get("id")

        # Upload the transcription
        for i, transcript in enumerate(transcription):
            text = transcript.get("text")
            start, end = transcript.get("timestamp")
            upload_response = create_annotation(
                job_id=job_id,
                transcript=text,
                start_time=start,
                end_time=end,
                label_id=DEFAULT_LABEL_ID,
                org=ORG,
            )
            print(f"Transcription {i+1} uploaded: {upload_response}")
