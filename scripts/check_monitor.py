"""Check logging. Run: python -m scripts.check_monitor"""
from app.monitor import fetch_requests, log_request

log_request(source="test", prompt_version="v2", success=1, latency_s=1.5)
rows = fetch_requests()
print("Rows in database:", len(rows))
print("Last row:", rows[-1])