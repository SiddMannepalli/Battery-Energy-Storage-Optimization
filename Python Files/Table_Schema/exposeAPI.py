import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(r"C:\Sidd\Battery Optimization Project\Python Files\Table_Schema")

from processOutput import outputProcessor
from getBatteryHeader import batteryHeader, BatteryHeader
from sqlalchemy import select

app = FastAPI(title="Battery Optimization API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

processor = outputProcessor()
batteryHeaderClient = batteryHeader()


def format_result(row):
    output = row[0]
    detail = row[1]
    return {
        "output_id": output.output_id,
        "version": output.version,
        "battery_id": output.battery_id,
        "date": str(output.date),
        "optimization_type": output.optimization_type,
        "hour": detail.hour,
        "action": detail.action,
        "charge_kw": detail.charge_kw,
        "discharge_kw": detail.discharge_kw,
        "soc_kw": detail.soc_kw,
        "price_mwh": detail.price_mwh,
        "revenue": detail.revenue,
    }


@app.get("/batteries")
def get_all_batteries():
    rows = batteryHeaderClient.session.scalars(select(BatteryHeader)).all()
    return [{"battery_id": b.battery_id, "name": b.name, "location": b.location, "owner": b.owner, "iso": b.iso} for b in rows]


@app.get("/optimization")
def get_all_optimization_data():
    results = processor.getOptData()
    return [format_result(row) for row in results]


@app.get("/optimization/battery/{battery_id}/latest")
def get_latest_output_by_battery(battery_id: int):
    results = processor.getOptDataBatteryID(battery_id)
    if not results:
        raise HTTPException(status_code=404, detail="No optimization data found for this battery")
    max_version = max(row[0].version for row in results)
    return [format_result(row) for row in results if row[0].version == max_version]


@app.get("/optimization/battery/{battery_id}/all")
def get_all_output_by_battery(battery_id: int):
    results = processor.getOptDataBatteryID(battery_id)
    if not results:
        raise HTTPException(status_code=404, detail="No optimization data found for this battery")
    return [format_result(row) for row in results]


@app.get("/optimization/battery/{battery_id}")
def get_optimization_by_battery(battery_id: int):
    results = processor.getOptDataBatteryID(battery_id)
    return [format_result(row) for row in results]


@app.get("/optimization/date/{date}")
def get_optimization_by_date(date: str):
    results = processor.getOptDataDate(date)
    return [format_result(row) for row in results]
