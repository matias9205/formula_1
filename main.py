import os
import sys
import requests
import pandas as pd
import time
import fastf1

from scripts.extract import Extract

years = sys.argv[1:]

if __name__ == "__main__":
    extract = Extract(years)
    formula_1_data = {}
    "---------------sessions---------------"
    sessions = extract.extract_data("/sessions?year={}")
    print(sessions.info())
    print("")
    print("")
    print("")
    print("---------------meetings---------------")
    meetings = extract.extract_data("/meetings?year={}")
    print(meetings.info())
    print("")
    print("")
    print("")
    print("---------------drivers---------------")
    drivers = extract.extract_data("/drivers?session_key={}", sessions)
    formula_1_data["drivers"] = drivers
    print(drivers.info())
    print("")
    print("")
    print("")
    print("---------------cars data---------------")
    speed = 5
    cars_data = extract.extract_data("/car_data?driver_number={}&session_key={}&speed>=315", drivers)
    formula_1_data["cars_data"] = cars_data
    print(cars_data.info())
    print("")
    print("")
    print("")
    # df_unified_1 = sessions.merge(
    #         meetings,
    #         on="meeting_key",
    #         how="left",
    #         # suffixes=("_session", "_meeting")
    #     ).merge(
    #         drivers,
    #         on=["meeting_key", "session_key"],
    #         how="left"
    #     )
    # print({"DF UNIFIED 1 COLUMNS": df_unified_1.columns})
    # print(df_unified_1.info())
    # print("")
    # print("")
    print("---------------laps---------------")
    laps = extract.extract_data("/laps?session_key={}&driver_number={}", drivers)
    formula_1_data["laps"] = laps
    print(laps.info())
    print(laps.head())
    for year in years:
        formula_1_data[f"sessions_{year}"] = sessions[sessions["year"] == int(year)]
        formula_1_data[f"meetings_{year}"] = meetings[meetings["year"] == int(year)]
        formula_1_data[f"drivers_{year}"] = drivers[drivers["year"] == int(year)]
        formula_1_data[f"laps_{year}"] = laps[laps["year"] == int(year)]
        formula_1_data[f"cars_data_{year}"] = cars_data[cars_data["year"] == int(year)]
    print(formula_1_data)

    extract.save_raw_data(formula_1_data)