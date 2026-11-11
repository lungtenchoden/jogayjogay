# supabase_utils.py
from data import (
    TAXI_RECORDS, TRIP_RECORDS, DRIVERS, PARKING_ZONES,
    DZONGKHAGS, VEHICLE_TYPES,
)

SUPABASE_ENABLED = False
_client = None

try:
    from config import SUPABASE_URL, SUPABASE_KEY
    if SUPABASE_URL and SUPABASE_KEY:
        from supabase import create_client
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
        SUPABASE_ENABLED = True
except Exception as e:
    print(f"[supabase_utils] disabled: {e}")


def is_live():
    return SUPABASE_ENABLED


def get_dzongkhags():
    if SUPABASE_ENABLED:
        try:
            return [r["name"] for r in
                    _client.table("dzongkhags").select("name")
                    .order("name").execute().data]
        except Exception:
            pass
    return DZONGKHAGS


def get_vehicle_types():
    if SUPABASE_ENABLED:
        try:
            return [r["type_name"] for r in
                    _client.table("vehicle_types").select("type_name")
                    .order("type_name").execute().data]
        except Exception:
            pass
    return VEHICLE_TYPES


def get_taxis():
    if SUPABASE_ENABLED:
        try:
            dz = {r["dzongkhag_id"]: r["name"] for r in
                  _client.table("dzongkhags").select("dzongkhag_id, name").execute().data}
            vt = {r["vehicle_type_id"]: r["type_name"] for r in
                  _client.table("vehicle_types").select("vehicle_type_id, type_name").execute().data}

            rows = _client.table("taxis").select(
                "taxi_id, taxi_code, plate_number, dzongkhag_id, "
                "vehicle_type_id, registration_date, status"
            ).order("taxi_code").execute().data

            return [
                {
                    "id": r["taxi_id"],
                    "taxi_id": r["taxi_code"],
                    "plate": r["plate_number"],
                    "dzongkhag": dz.get(r["dzongkhag_id"], ""),
                    "vehicle": vt.get(r["vehicle_type_id"], ""),
                    "registered": r["registration_date"],
                    "status": r["status"],
                }
                for r in rows
            ]
        except Exception as e:
            print(f"[get_taxis] {e}")

    return [
        {"id": i, "taxi_id": r[0], "plate": r[1], "dzongkhag": r[2],
         "vehicle": r[3], "registered": r[4], "status": r[5]}
        for i, r in enumerate(TAXI_RECORDS)
    ]


def add_taxi(taxi_code, plate, dzongkhag_name, vehicle_name, reg_date, status):
    if SUPABASE_ENABLED:
        try:
            dz_id = _client.table("dzongkhags").select("dzongkhag_id")\
                .eq("name", dzongkhag_name).execute().data[0]["dzongkhag_id"]
            vt_id = _client.table("vehicle_types").select("vehicle_type_id")\
                .eq("type_name", vehicle_name).execute().data[0]["vehicle_type_id"]

            _client.table("taxis").insert({
                "taxi_code": taxi_code,
                "plate_number": plate,
                "dzongkhag_id": dz_id,
                "vehicle_type_id": vt_id,
                "registration_date": reg_date,
                "status": status,
            }).execute()
            return True, "Taxi added to Supabase."
        except Exception as e:
            return False, f"Supabase error: {e}"
    return False, "Supabase is not configured — using local mock data."


def get_trips():
    if SUPABASE_ENABLED:
        try:
            dz = {r["dzongkhag_id"]: r["name"] for r in
                  _client.table("dzongkhags").select("dzongkhag_id, name").execute().data}
            rows = _client.table("trips").select(
                "trip_id, origin_dzongkhag_id, destination_dzongkhag_id, "
                "trip_date, num_trips"
            ).order("trip_date", desc=True).execute().data

            return [
                {
                    "id": r["trip_id"],
                    "origin": dz.get(r["origin_dzongkhag_id"], ""),
                    "destination": dz.get(r["destination_dzongkhag_id"], ""),
                    "date": r["trip_date"],
                    "num_trips": r["num_trips"],
                }
                for r in rows
            ]
        except Exception as e:
            print(f"[get_trips] {e}")

    return [
        {"id": i, "origin": r[0], "destination": r[1],
         "date": r[2], "num_trips": int(r[3])}
        for i, r in enumerate(TRIP_RECORDS)
    ]


def add_trip(origin, destination, trip_date, num_trips):
    if SUPABASE_ENABLED:
        try:
            o_id = _client.table("dzongkhags").select("dzongkhag_id")\
                .eq("name", origin).execute().data[0]["dzongkhag_id"]
            d_id = _client.table("dzongkhags").select("dzongkhag_id")\
                .eq("name", destination).execute().data[0]["dzongkhag_id"]

            _client.table("trips").insert({
                "origin_dzongkhag_id": o_id,
                "destination_dzongkhag_id": d_id,
                "trip_date": trip_date,
                "num_trips": int(num_trips),
            }).execute()
            return True, "Trip added to Supabase."
        except Exception as e:
            return False, f"Supabase error: {e}"
    return False, "Supabase is not configured — using local mock data."


def get_drivers():
    if SUPABASE_ENABLED:
        try:
            dz = {r["dzongkhag_id"]: r["name"] for r in
                  _client.table("dzongkhags").select("dzongkhag_id, name").execute().data}
            vt = {r["vehicle_type_id"]: r["type_name"] for r in
                  _client.table("vehicle_types").select("vehicle_type_id, type_name").execute().data}

            rows = _client.table("drivers").select("*").order("full_name").execute().data

            return [
                {
                    "name": r["full_name"],
                    "license": r["license_no"],
                    "contact": r["phone"],
                    "dzongkhag": dz.get(r["dzongkhag_id"], ""),
                    "status": r["status"],
                    "vehicle": vt.get(r["vehicle_type_id"], ""),
                    "plate": r["license_plate"],
                    "trips": r["trips_completed"],
                    "rating": r["rating"],
                    "cancellations": r["cancellations"],
                }
                for r in rows
            ]
        except Exception as e:
            print(f"[get_drivers] {e}")

    return DRIVERS


def get_parking_zones():
    if SUPABASE_ENABLED:
        try:
            dz = {r["dzongkhag_id"]: r["name"] for r in
                  _client.table("dzongkhags").select("dzongkhag_id, name").execute().data}
            rows = _client.table("parking_zones").select(
                "zone_id, name, dzongkhag_id, stationed_taxis"
            ).order("name").execute().data

            return [
                {
                    "name": r["name"],
                    "dzongkhag": f"{dz.get(r['dzongkhag_id'], '')} dzongkhag",
                    "taxis": r["stationed_taxis"],
                }
                for r in rows
            ]
        except Exception as e:
            print(f"[get_parking_zones] {e}")

    return [
        {"name": r[0], "dzongkhag": r[1], "taxis": int(r[2])}
        for r in PARKING_ZONES
    ]