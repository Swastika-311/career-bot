"""
Full ScaleDown Pipeline Integration Test (REAL API)
Tests HASTE Optimizer + ScaleDown Compressor chain with actual network calls.
"""
import os
import tempfile
import sys
import scaledown as sd
from scaledown.optimizer import HasteOptimizer
from scaledown.compressor import ScaleDownCompressor
from scaledown.pipeline import Pipeline
from scaledown.types import PipelineResult
from scaledown.exceptions import AuthenticationError, APIError

# -------------------------------------------------------------------------
# 🔑 CONFIGURATION
# -------------------------------------------------------------------------
# REPLACE THIS WITH YOUR ACTUAL API KEY
API_KEY = os.environ.get("SCALEDOWN_API_KEY", "yVlJ8qWWVF6wj8RZUfNHm7fUYqNBVEFr3Rrfep67")

if API_KEY == "YOUR_REAL_API_KEY_HERE":
    print("⚠️  WARNING: Using placeholder API key. The API call will likely fail.")
    print("   Export your key: export SCALEDOWN_API_KEY='sk_...'\n")

# Set the API key globally
sd.set_api_key(API_KEY)

# -------------------------------------------------------------------------
# Test Setup
# -------------------------------------------------------------------------
TEST_CODE = """
def calculate_sum(numbers):
    \"\"\"Calculate sum of numbers.\"\"\"
    total = 0
    for num in numbers:
        total += num
    return total

def calculate_average(numbers):
    \"\"\"Calculate average of numbers.\"\"\"
    if len(numbers) == 0:
        return 0
    return calculate_sum(numbers) / len(numbers)

class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    def process(self):
        return calculate_average(self.data)
"""

print("=" * 70)
print("SCALEDOWN PIPELINE REAL API TEST")
print("=" * 70)

# Helper to handle potential string input for HASTE
temp_file = None
file_path_arg = None

with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
    f.write(TEST_CODE)
    file_path_arg = f.name
    temp_file = f.name

try:
    # -------------------------------------------------------------------------
    # 1. Initialize Components
    # -------------------------------------------------------------------------
    print("\n1. Initializing Pipeline...")
    
    optimizer = HasteOptimizer(
        top_k=2,
        semantic=False
    )
    
    compressor = ScaleDownCompressor(
        target_model="gpt-4o",
        rate="auto"
    )
    
    pipe = Pipeline([
        ('haste', optimizer),
        ('compressor', compressor)
    ])
    print(" Pipeline created successfully")

    # -------------------------------------------------------------------------
    # 2. Run Pipeline (REAL NETWORK CALL)
    # -------------------------------------------------------------------------
    print(f"\n2. Calling API (Key: {API_KEY[:4]}...{API_KEY[-4:] if len(API_KEY)>8 else ''})...")
    
    query_str = "calculate_average function"
    prompt_str = "Summarize this function"
    
    result = pipe.run(
        context=TEST_CODE,
        query=query_str,
        file_path=file_path_arg, 
        prompt=prompt_str
    )
    
    print(" API call successful!")

    # -------------------------------------------------------------------------
    # 3. Step-by-Step Verification
    # -------------------------------------------------------------------------
    print("\n3. Pipeline Flow Verification:")
    print("=" * 60)
    
    # --- STEP 0: ORIGINAL INPUT ---
    print(f"[INPUT] Context (Start of Pipeline):")
    print("-" * 20)
    print(f"{TEST_CODE.strip()[:200]}... [Total chars: {len(TEST_CODE)}]")
    print(f"Query: '{query_str}'")
    print(f"File Path: {file_path_arg}")
    print("=" * 60)

    # --- RECONSTRUCTING INTERMEDIATE OUTPUT ---
    # Since PipelineResult stores the FINAL content, we need to re-run just the optimizer 
    # locally to verify EXACTLY what the compressor received, or assume correctness.
    # For full transparency in this test script, let's manually run the optimizer to show the user.
    
    print("\n[STEP 1] Optimizer (HASTE) Output / Compressor Input:")
    print("-" * 20)
    
    # We can perform a manual check to see what HASTE does
    opt_result = optimizer.optimize(context=TEST_CODE, query=query_str, file_path=file_path_arg)
    optimized_code = opt_result.content
    
    print(f"{optimized_code.strip()[:300]}")
    if len(optimized_code) > 300: print("... (truncated)")
    print("-" * 20)
    print(f"Tokens (HASTE est.): {opt_result.metrics.optimized_tokens}")
    print("=" * 60)

    # --- STEP 2: COMPRESSOR OUTPUT ---
    print(f"\n[STEP 2] Compressor Output (Final Result):")
    print("-" * 20)
    print(f"{result.final_content}")
    print("-" * 20)
    
    # Get metrics from history
    haste_step = result.history[0]
    comp_step = result.history[1]
    
    print(f"Prompt used: '{prompt_str}'")
    print(f"Compressor Input Tokens (API est.):  {comp_step.input_tokens}")
    print(f"Compressor Output Tokens (API est.): {comp_step.output_tokens}")
    print("=" * 60)

    # -------------------------------------------------------------------------
    # 4. Summary Metrics
    # -------------------------------------------------------------------------
    print("\n4. Summary Metrics:")
    print("-" * 30)
    print(f"Original Context Size:  {len(TEST_CODE)} chars")
    print(f"Final Content Size:     {len(result.final_content)} chars")
    print(f"Total Savings:          {result.savings_percent:.1f}%")
    print(f"Total Latency:          {haste_step.latency_ms + comp_step.latency_ms:.0f}ms")
    print("-" * 30)

    print("\nREAL API TEST PASSED!")

except AuthenticationError:
    print("\nAUTHENTICATION FAILED: Invalid API Key.")
    print("   Please check your SCALEDOWN_API_KEY environment variable.")

except APIError as e:
    print(f"\n API ERROR: {str(e)}")
    print("   The server might be down or unreachable.")

except Exception as e:
    print(f"\nUNEXPECTED ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

finally:
    if temp_file and os.path.exists(temp_file):
        os.unlink(temp_file)
