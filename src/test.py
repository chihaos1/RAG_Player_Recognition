import pathlib
from datetime import datetime

log_filename = pathlib.Path.cwd().parent / f"logs/run_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.log"
print(log_filename)