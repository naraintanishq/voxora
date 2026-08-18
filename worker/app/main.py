# =================================================================
# FILE: worker/app/main.py (ENHANCED WITH QUALITY VALIDATION)
# Enhanced worker configuration that includes quality validation
# =================================================================
import os
import ssl
from dotenv import load_dotenv
from supabase import create_client
from arq.connections import RedisSettings
from .jobs.enhance_from_text import enhance_from_text
from .jobs.enhance_from_audio import enhance_from_audio
from .quality_validation import validate_output_quality, generate_quality_report

load_dotenv()

REDIS_URL = os.environ.get("REDIS_URL")
if not REDIS_URL:
    raise ValueError("REDIS_URL is not set in worker/.env file.")

# Prepare SSL context if needed
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Use from_dsn without extra args
WORKER_REDIS_SETTINGS = RedisSettings.from_dsn(REDIS_URL)

if REDIS_URL.startswith("rediss://"):
    WORKER_REDIS_SETTINGS.ssl = True
    WORKER_REDIS_SETTINGS.ssl_check_hostname = False
    WORKER_REDIS_SETTINGS.ssl_cert_reqs = "none"
    WORKER_REDIS_SETTINGS.ssl_ca_certs = None

async def startup(ctx):
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
    if not all([SUPABASE_URL, SUPABASE_KEY]):
        raise ValueError("Supabase creds missing in worker/.env")
    ctx['supabase'] = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("VOXORA ULTIMATE WORKER v3.0 - Professional audio processing system initialized")
    print("Mission: Deliver $200k/month quality through intelligent, adaptive processing")

async def shutdown(ctx):
    print("Voxora Ultimate Worker shutting down.")

# Enhanced job wrapper with quality validation
async def enhanced_audio_job(ctx, job_id: str, input_filename: str):
    """Enhanced audio job with quality validation."""
    
    # Process audio with ultimate engine
    success = await enhance_from_audio(ctx, job_id, input_filename)
    
    if success:
        # Validate output quality
        output_file = f"{job_id}.mp3"
        if os.path.exists(output_file):
            try:
                validation_results = validate_output_quality(output_file)
                quality_report = generate_quality_report(validation_results)
                
                # Update database with quality metrics
                ctx['supabase'].table('jobs').update({
                    'quality_score': validation_results.get('overall_quality_score', 0),
                    'quality_report': quality_report,
                    'professional_grade': validation_results.get('professional_grade', False),
                    'competitive_advantages': validation_results.get('competitive_advantages', [])
                }).eq('id', job_id).execute()
                
                print(f"Quality Validation Complete - Score: {validation_results.get('overall_quality_score', 0)}/100")
                
                # Fail job if quality is too low (below 75)
                if validation_results.get('overall_quality_score', 0) < 75:
                    print("WARNING: Quality below premium standards - consider process refinement")
                
            except Exception as e:
                print(f"Quality validation failed: {e}")
    
    return success

async def enhanced_text_job(ctx, job_id: str):
    """Enhanced text-to-audio job with quality validation."""
    
    success = await enhance_from_text(ctx, job_id)
    
    if success:
        # Validate TTS output quality
        output_file = f"{job_id}.mp3"
        if os.path.exists(output_file):
            try:
                validation_results = validate_output_quality(output_file)
                quality_report = generate_quality_report(validation_results)
                
                ctx['supabase'].table('jobs').update({
                    'quality_score': validation_results.get('overall_quality_score', 0),
                    'quality_report': quality_report,
                    'tts_quality_grade': validation_results.get('professional_grade', False)
                }).eq('id', job_id).execute()
                
            except Exception as e:
                print(f"TTS quality validation failed: {e}")
    
    return success

class WorkerSettings:
    redis_settings = WORKER_REDIS_SETTINGS
    functions = [
        enhanced_audio_job,  # Audio-to-Audio with quality validation
        enhanced_text_job,   # Text-to-Audio with quality validation
        # Backwards compatibility
        enhance_from_audio,  # Original function
        enhance_from_text    # Original function
    ]
    on_startup = startup
    on_shutdown = shutdown