import os
import pymongo
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel


app = FastAPI()
handler = Mangum(app)

client = pymongo.MongoClient(host=os.environ.get("FMS_URI"))
db = client['adc']
fleet_trip = db['fleet_trip']
dtg_data = db['fleet_data']
events_collection = db['driving_events']


@app.get("/last_trips/")
async def get_trips():
    try:
        last_event_time = events_collection.find_one(sort=[("endTime", pymongo.DESCENDING)])["endTime"]
        query_filter = {'endTime': {'$gt': last_event_time}}
        last_trip_cursor = fleet_trip.find(query_filter, sort=[("endTime", pymongo.DESCENDING)])
    
        trip_data_list = []
        
        for trip in last_trip_cursor:
            trip_data_list.append(trip)
            
        return trip_data_list

    except:
        raise HTTPException(status_code=404, detail="Trip not found")
