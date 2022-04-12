import time
from app.services.pipeline import start


start_time = time.time()

# Start pipeline
start()

print("--- %s seconds ---" % round(time.time() - start_time, 3))
