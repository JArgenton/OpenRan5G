from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from .Executor import Executor
from typing import List
from fastapi.responses import JSONResponse # type: ignore
from fastapi.responses import FileResponse #type: ignore
import os
from fastapi import Path # type: ignore

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
    data = executor.load_results()
    #print(data)
    return data

@app.post("/api/plotting")
def plotGraphic(pltConfig: dict):
    if pltConfig.get("startDate", 0):
        filename = executor.plotGraphicByTime(pltConfig["server"].strip(), pltConfig["xParam"], pltConfig["yParam"], [pltConfig["startDate"], pltConfig["finalDate"]])
    if pltConfig.get("routineName", 0):
        filename = executor.plotGraphicByRoutine(pltConfig["server"], pltConfig["routineName"], pltConfig["yParam"])

    if not filename or not os.path.exists(filename):
        return {"error": "Gráfico não gerado"}

    return FileResponse(
        path=filename,
        media_type="image/png",
        filename=os.path.basename(filename)
    )

@app.post("/api/routine")
def insertRoutine(rtParams: dict):
    print(rtParams)
    executor.createRoutine(rtParams)

@app.get("/api/routine/saved")
def getSavedRoutines():
    return executor.getRoutines()

@app.post("/api/routine/activate")
def toggleActivate(params: dict):
    executor.activateRoutine(params["r_id"], params["active"], params["time"])  

@app.get("/api/routine/{routine_id}/tests")
def get_routine_tests(routine_id: str):
    return executor.getRoutineTests(int(routine_id))  

@app.get("/api/results/{testId}/{routineId}")
def get_routine_tests_results(
    testId: int = Path(..., description="ID do teste"),
    routineId: int = Path(..., description="ID da rotina")
):
    return executor.getRoutineTestResults(routineId, testId)