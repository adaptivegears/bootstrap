import os
import requests

for key, value in os.environ.items():
    print(f"{key}={value}")
