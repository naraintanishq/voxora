# =================================================================
# FILE: worker/run_test.py (V5 - FINAL & ACCURATE REPORTING)
# This version correctly checks the success/failure return value
# from the worker function for a 100% accurate test result.
# =================================================================
import asyncio
import os
import sys
from types import SimpleNamespace

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# We need to make sure we're importing the version that returns True/False
from app.jobs.enhance_from_audio import enhance_from_audio

class MockSupabaseClient:
    def __init__(self, test_data): self._test_data = test_data
    def table(self, table_name): return self
    def update(self, data): return self
    def select(self, *args, **kwargs): return self
    def eq(self, column, value): return self
    def single(self): return self
    def execute(self):
        print(f"(Test Runner: Bypassing database call, returning mock data: {self._test_data})")
        return SimpleNamespace(data=self._test_data)

async def main():
    print("--- VOXORA LOCAL TEST RUNNER (V5) ---")

    print("\nSTEP 1: Defining the Audio-to-Audio test case...")
    test_job_id = "local-audio-test-final"
    test_input_file = "test_input.m4a"
    test_preset = "podcast_pro_male"
    
    mock_job_data = {'preset': test_preset}
    ctx = {'supabase': MockSupabaseClient(mock_job_data)}
    
    print(f"  - Job ID: {test_job_id}")
    print(f"  - Input File: {test_input_file}")
    print(f"  - Preset to Inject: {test_preset}")

    if not os.path.exists(test_input_file):
        print(f"\n[FATAL ERROR] Input file '{test_input_file}' not found!")
        return

    print("\nSTEP 2: EXECUTING THE V17.1 PLATINUM ENGINE. STAND BY...")
    print("=========================================================")
    
    # We now capture the True/False return value from the worker function
    success = await enhance_from_audio(ctx, test_job_id, test_input_file)
        
    print("=========================================================")
    # And we check that value for our final report
    if success:
        print("\n[TEST SUCCEEDED] The audio engine completed its run without errors.")
        print("Check the 'worker' folder for your enhanced MP3 file!")
    else:
        print("\n[TEST FAILED] The audio engine encountered an error. Check the log above for details.")

    print("--- TEST RUN FINISHED ---")

if __name__ == "__main__":
    asyncio.run(main())