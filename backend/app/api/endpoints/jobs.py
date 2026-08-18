# =================================================================
# FILE: backend/app/api/endpoints/jobs.py (WITH VOICE LIBRARY & UPLOAD)
# =================================================================
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from pydantic import BaseModel
import arq
from ...config import supabase_client, get_redis_queue
import shutil
import os

router = APIRouter()

# --- Mock User (Remains the same for now) ---
class MockUser:
    id: str = "9e263b63-17d5-41de-8d23-87b50a8b04a7"

def get_current_user():
    return MockUser()

# --- TEXT-TO-AUDIO ENDPOINT (NOW WITH VOICE SELECTION) ---
class JobCreate(BaseModel):
    text: str
    preset: str = "enhance_female" # A better default
    voice: str | None = None      # NEW: Optional field for voice selection

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_text_to_audio_job(
    job: JobCreate,
    current_user=Depends(get_current_user),
    redis: arq.ArqRedis = Depends(get_redis_queue)
):
    team_member_res = supabase_client.table('team_members').select('team_id').eq('user_id', current_user.id).limit(1).execute()
    if not team_member_res.data:
        raise HTTPException(status_code=403, detail="User does not belong to any team.")
    team_id = team_member_res.data[0]['team_id']
    
    # NEW: Include the selected_voice in the database record
    job_data = {
        "user_id": str(current_user.id),
        "team_id": str(team_id),
        "job_type": "text_to_audio",
        "input_text": job.text,
        "preset": job.preset,
        "selected_voice": job.voice, # <-- THE NEW DATA
        "status": "pending"
    }
    
    try:
        job_res = supabase_client.table('jobs').insert(job_data).execute()
        new_job = job_res.data[0]
        # We only need to send the job_id. The worker will fetch the details.
        await redis.enqueue_job("enhance_from_text", new_job['id'])
        print(f"Text-to-Audio Job #{new_job['id']} with voice '{job.voice}' enqueued.")
        return new_job
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- AUDIO-TO-AUDIO UPLOAD ENDPOINT (Remains the same) ---
# @router.post("/upload", status_code=status.HTTP_201_CREATED)
# async def create_audio_to_audio_job(
#     preset: str = Form("enhance_female"),
#     file: UploadFile = File(...),
#     current_user=Depends(get_current_user),
#     redis: arq.ArqRedis = Depends(get_redis_queue)
# ):
#     team_member_res = supabase_client.table('team_members').select('team_id').eq('user_id', current_user.id).limit(1).execute()
#     if not team_member_res.data: raise HTTPException(status_code=403, detail="User does not belong to any team.")
#     team_id = team_member_res.data[0]['team_id']

#     try:
#         job_data = { "user_id": str(current_user.id), "team_id": str(team_id), "job_type": "audio_to_audio", "preset": preset, "status": "pending" }
#         job_res = supabase_client.table('jobs').insert(job_data).execute()
#         new_job = job_res.data[0]
#         job_id = new_job['id']

#         temp_upload_path = f"{job_id}_upload{os.path.splitext(file.filename)[1]}"
#         with open(temp_upload_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)
        
#         supabase_client.table('jobs').update({'input_audio_url': temp_upload_path}).eq('id', job_id).execute()
#         await redis.enqueue_job("enhance_from_audio", job_id, temp_upload_path)
#         print(f"Audio-to-Audio Job #{job_id} successfully enqueued via ARQ.")
#         return new_job
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    

# --- NEW: AUDIO-TO-AUDIO UPLOAD ENDPOINT ---

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def create_audio_to_audio_job(
    preset: str = Form("enhance"),
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
    redis: arq.ArqRedis = Depends(get_redis_queue)
):
    team_member_res = supabase_client.table('team_members').select('team_id').eq('user_id', current_user.id).limit(1).execute()
    if not team_member_res.data:
        raise HTTPException(status_code=403, detail="User does not belong to any team.")
    team_id = team_member_res.data[0]['team_id']

    # --- TODO: File Validation Logic ---
    # We will need to add checks for file type, size, etc.

    try:
        # Create a new job record in the database
        job_data = {
            "user_id": str(current_user.id),
            "team_id": str(team_id),
            "job_type": "audio_to_audio", # CRITICAL: Set the correct job type
            "preset": preset,
            "status": "pending"
        }
        job_res = supabase_client.table('jobs').insert(job_data).execute()
        new_job = job_res.data[0]
        job_id = new_job['id']

        # Save the user's uploaded file to a temporary location
        temp_upload_path = f"{job_id}_upload{os.path.splitext(file.filename)[1]}"
        with open(temp_upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # --- TODO: Upload the temporary file to Supabase Storage ---
        # For now, we will assume the worker has access to this local file.
        # In production, the API will upload this to a bucket, and the worker will download it.
        
        # Update the job with the input file's location
        supabase_client.table('jobs').update({'input_audio_url': temp_upload_path}).eq('id', job_id).execute()

        # Enqueue the NEW job type for the worker
        await redis.enqueue_job("enhance_from_audio", job_id, temp_upload_path)
        print(f"Audio-to-Audio Job #{job_id} successfully enqueued via ARQ.")
        
        return new_job
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))