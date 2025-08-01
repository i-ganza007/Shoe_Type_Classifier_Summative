from fastapi import Request
from fastapi_utils.tasks import repeat_every
from datetime import datetime
from supabase import create_client, Client
import os
import time

# Globals
request_counter = 0
total_response_time = 0.0

# Supabase config
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Middleware
async def metrics_middleware(request: Request, call_next):
    global request_counter, total_response_time

    start = time.time()
    response = await call_next(request)
    end = time.time()

    duration = end - start
    request_counter += 1
    total_response_time += duration

    return response

# Background logging task
async def log_metrics():
    global request_counter, total_response_time

    if request_counter == 0:
        return

    avg_time = total_response_time / request_counter

    supabase.table("System_Metrics").insert({
        "timestamp": datetime.utcnow().isoformat(),
        "request_count": request_counter,
        "avg_response_time": avg_time,
        "model_uptime_status": "active"
    }).execute()

    request_counter = 0
    total_response_time = 0.0
