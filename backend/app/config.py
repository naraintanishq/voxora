import os
import ssl
from dotenv import load_dotenv
from supabase import create_client, Client
import arq
from arq.connections import RedisSettings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '..', '.env'))

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
REDIS_URL = os.environ.get("REDIS_URL")

if not all([SUPABASE_URL, SUPABASE_KEY, REDIS_URL]):
    raise ValueError("Essential environment variables are missing from backend/.env")

try:
    supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Successfully connected to Supabase for Backend API.")
except Exception as e:
    print(f"FATAL: Could not connect to Supabase: {e}")
    raise

# Create SSL context (if needed) for custom settings
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Call from_dsn without extra args
ARQ_REDIS_SETTINGS = RedisSettings.from_dsn(REDIS_URL)

# If you need to adjust SSL settings beyond what from_dsn sets,
# mutate the object:
if REDIS_URL.startswith("rediss://"):
    ARQ_REDIS_SETTINGS.ssl = True
    ARQ_REDIS_SETTINGS.ssl_check_hostname = False
    ARQ_REDIS_SETTINGS.ssl_ca_certs = None  # or path to CA file
    # You might also need to set ssl_cert_reqs if relevant
    ARQ_REDIS_SETTINGS.ssl_cert_reqs = "none"

async def get_redis_queue():
    return await arq.create_pool(ARQ_REDIS_SETTINGS)
