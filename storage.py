# storage.py
import json
import os

_FILE = os.path.join(os.path.dirname(__file__), "records.json")
_memory = {"taxi_records": [], "trip_records": []}


def _load_all():
    if not os.path.exists(_FILE):
        return {"taxi_records": [], "trip_records": []}
    try:
        with open(_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return {"taxi_records": [], "trip_records": []}
            data.setdefault("taxi_records", [])
            data.setdefault("trip_records", [])
            return data
    except Exception:
        return {"taxi_records": [], "trip_records": []}


def _save_all(data):
    try:
        with open(_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False


def get_added(table_name):
    data = _load_all()
    return data.get(table_name, [])


def add_record(table_name, record_tuple):
    data = _load_all()
    data.setdefault(table_name, []).append(list(record_tuple))
    if not _save_all(data):
        _memory.setdefault(table_name, []).append(list(record_tuple))
        return _memory[table_name]
    return data[table_name]


def clear(table_name):
    data = _load_all()
    data[table_name] = []
    _save_all(data)
