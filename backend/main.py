from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from .Executor import Executor
from typing import List
from fastapi.responses import JSONResponse # type: ignore

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
    executor.clean_tests()
    try:
        for test in tests:
            executor.insert_tests(
                int(test["packetSize"]),
                int(test["duration"]),
                test["protocol"],
                1,
                int(test["pingPackets"])
            )
            
        resultado = executor.run_tests(tests[0]["ip"])
        return resultado
    except Exception as e:
        return JSONResponse(status_code=200, content={"error": str(e)})
    
@app.get("/api/log")
def get_data_log():
    return executor.load_data()

    
            
            
