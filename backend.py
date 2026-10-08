# backend.py
from data import (
    TAXI_RECORDS, TRIP_RECORDS, ANALYSIS_DATA,
    PARKING_ZONES, DRIVERS,
)
import storage

SUPABASE_ENABLED = False
_client = None

try:
    from config import SUPABASE_URL, SUPABASE_KEY
    if SUPABASE_URL and SUPABASE_KEY:
        from supabase import create_client
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
        SUPABASE_ENABLED = True
except Exception:
    SUPABASE_ENABLED = False


def _fetch(table_name, fallback):
    if not SUPABASE_ENABLED:
        return fallback
    try:
        resp = _client.table(table_name).select("*").execute()
        return resp.data if resp.data else fallback
    except Exception:
        return fallback


def get_taxi_records():
    base = _fetch("taxi_records", TAXI_RECORDS)
    if base and isinstance(base[0], dict):
        base = [(r.get("taxi_id",""), r.get("plate_number",""),
                 r.get("dzongkhag",""), r.get("vehicle_type",""),
                 r.get("registration_date",""), r.get("status",""))
                for r in base]
    added = storage.get_added("taxi_records")
    return list(base) + [tuple(r) for r in added]


def get_trip_records():
    base = _fetch("trip_records", TRIP_RECORDS)
    if base and isinstance(base[0], dict):
        base = [(r.get("origin",""), r.get("destination",""),
                 r.get("trip_date",""), str(r.get("num_trips","")))
                for r in base]
    added = storage.get_added("trip_records")
    return list(base) + [tuple(r) for r in added]


def add_taxi_record(record_tuple):
    storage.add_record("taxi_records", record_tuple)


def add_trip_record(record_tuple):
    storage.add_record("trip_records", record_tuple)


def get_analysis_data():
    rows = _fetch("analysis", ANALYSIS_DATA)
    if rows and isinstance(rows[0], dict):
        return [(r.get("dzongkhag",""), str(r.get("registered_taxis","")),
                 str(r.get("trips_out","")), str(r.get("trips_in","")),
                 r.get("activity_level","")) for r in rows]
    return rows


def get_parking_zones():
    rows = _fetch("parking_zones", PARKING_ZONES)
    if rows and isinstance(rows[0], dict):
        return [(r.get("name",""), r.get("dzongkhag",""),
                 str(r.get("stationed_taxis",""))) for r in rows]
    return rows


def get_drivers():
    return DRIVERS


def sign_in(email, password):
    if not SUPABASE_ENABLED:
        if email and password:
            return True, "Demo login (Supabase not configured)"
        return False, "Please enter username and password."
    try:
        _client.auth.sign_in_with_password({"email": email, "password": password})
        return True, "Signed in."
    except Exception as e:
        return False, f"Login failed: {e}"