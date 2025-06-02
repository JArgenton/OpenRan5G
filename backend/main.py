from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Executor import Executor
from typing import List

app = FastAPI()

# Libera acesso do React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

executor = Executor()

@app.post("/api/tests")
def run_tests(tests: List[dict]):
    for test in tests:
        executor.insert_tests(
            int(test["packetSize"]),
            int(test["duration"]),
            test["protocol"],
            1,
            int(test["pingPackets"])
        )
    return executor.run_tests(tests[0]["ip"])
    
            
            
