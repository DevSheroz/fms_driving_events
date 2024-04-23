import os
import pymongo
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from mangum import Mangum


app = FastAPI()
handler = Mangum(app)


client = pymongo.MongoClient("mongodb://adcDb!0917:adcDb!0038@10.253.5.205:27017/adc")
db = client['adc']
dtg_data = db['fleet_data']


class DTGData(BaseModel):
    dtgTime: list
    lat: list[float]
    lon: list[float]
    AccelXr: list[float]
    AccelYr: list[float]
    Speed: list[float]
    gpsAngle: list[float]
    rpm: list[int]
        

@app.get("/fetch_dtg_data/{tripId}")
async def get_data(tripId: str):
    
    try:
        dtg_query = {"tripId": tripId}
        dtg_sorted = dtg_data.find(dtg_query).sort("dtgTime", 1) # sort by time ascending

        if not dtg_sorted.next():
            return {}
        
        # rearrange the objects into one dictionary
        dtg_data_dict = {key: [] for key in DTGData.model_fields.keys()}
        for data in dtg_sorted:

            for key in dtg_data_dict.keys():
                dtg_data_dict[key].append(data.get(key))
        
        dtgData=DTGData(**dtg_data_dict)

        return dtgData

    except:
        raise HTTPException(status_code=404, detail="Trip DTG data not found or invalid tripId")