import time
from app.services.pipeline import start


start_time = time.time()

# Start pipeline
start()

print("--- Looptijd: %s seconden ---" % round(time.time() - start_time, 3))
