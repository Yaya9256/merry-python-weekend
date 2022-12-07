from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
from datetime import date
from bson import json_util
import solution

app = FastAPI()


@app.get('/search')
def search(source: str, day: date, destination: str):
    results = solution.main(str(day), source, destination)
    hack = json.dumps(results, default=json_util.default, indent=4)
    return JSONResponse(json.loads(hack))
