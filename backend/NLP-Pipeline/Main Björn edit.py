import json
import pandas as pd
import requests
import time
import fastapi
import socket
from fastapi import FastAPI, Request, UploadFile, File, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from joblib import dump, load
from pydantic import BaseModel

from predict_datapoint import read_aas
from edit_datapoint import start_correction

from typing import Any, Dict, AnyStr, List, Union

import uvicorn

app = FastAPI(title="NLP-Pipeline")

JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]

networkPort = 8003

isAppInUsageStatus = False   # Zusatz von Björn -------------------------------------------


# Für Tests lokal, mit aas als json, das andere darunter ist aas als string für björn

@app.post("/startNLPPipeline")
async def nlp_pipeline(aas: UploadFile = File(...)):
    print(type(aas))
    # Hier ists ja egal ob AAS oder SUbmodel
    data = json.load(aas.file)
    print(type(data))
    nlp_aas = read_aas(data)
    return nlp_aas



# 18.09.23, das ist so wie es bei Björn funktioniert mit aas als string, ich brauch aber json 
#-> wieder ändern

# AAS als string

"""
@app.post("/startNLPPipeline")
async def nlp_pipeline(
        aas: str = fastapi.Form(...)
    ):
    isAppInUsageStatus = True # Zusatz von Björn -------------------------------------------
    print(type(aas))
    # nlp pipeline braucht ein dictionary, deswegen umwandeln in dict
    print(aas)
    aas_dict = json.loads(aas)
    print(type(aas_dict))
    nlp_aas = read_aas(aas_dict)
    print(type(nlp_aas))
    isAppInUsageStatus = False # Zusatz von Björn -------------------------------------------
    return nlp_aas
"""
@app.post("/editDatapoint")
async def edit_datapoint(
        request: Request
        #datapointInformation: dict = fastapi.Form(...)
        #startPrediction: str = fastapi.Form(...),
        #correctedLabel: str = fastapi.Form(...),
        #datapoint: list = fastapi.Form(...)
    ):
    data = await request.json()
    print(data)
    result = start_correction(data)
    
    return result

@app.get("/isAppInUsageStatus") # Zusatz von Björn -------------------------------------------
async def nlp_AppStatus():      # Zusatz von Björn -------------------------------------------
    return isAppInUsageStatus   # Zusatz von Björn -------------------------------------------
	
def get_ip_address():
    hostname = socket.gethostname()         
    ip_address = socket.gethostbyname(hostname)
    return ip_address 

if __name__ == "__main__":
    #app = FastAPI()
    #APP.include_router(ExampleSemanticMatchingService().router)
    socket.getaddrinfo(get_ip_address(), networkPort)  
    uvicorn.run(app, host=get_ip_address(), port=networkPort)
    #uvicorn.run(app, host="127.0.0.1", port=8003)
