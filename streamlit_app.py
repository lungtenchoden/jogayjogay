# streamlit_app.py
import streamlit as st
import pandas as pd
import supabase_utils as su

st.set_page_config(
    page_title="Jogay Jogay · Dashboard",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.markdown("# 🚕 Jogay Jogay")
    st.markdown("**Bhutan Transport Authority**")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["Dashboard", "Taxi Records", "Trip Records", "Drivers", "Parking Zones"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    if su.is_live():
        st.success("🟢 Connected to Supabase")
    else:
        st.warning("🟡 Demo mode (mock data)")
    st.markdown("---")
    st.caption("Built with Streamlit + Python")


if page == "Dashboard":
    st.title("Dashboard")
    st.caption("Overview of Bhutan's taxi transport activity")

    taxis = su.get_taxis()
    trips = su.get_trips()
    drivers = su.get_drivers()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Registered Taxis", len(taxis))
    with col2:
        st.metric("Total Trips", sum(t["num_trips"] for t in trips))
    with col3:
        st.metric("Drivers", len(drivers))
    with col4:
        dz_counts = {}
        for t in taxis:
            dz_counts[t["dzongkhag"]] = dz_counts.get(t["dzongkhag"], 0) + 1
        busiest = max(dz_counts, key=dz_counts.get) if dz_counts else "—"
        st.metric("Most Active Dzongkhag", busiest)

    st.markdown("---")
    st.subheader("Registered taxis by dzongkhag")
    df = pd.DataFrame(taxis)
    if not df.empty:
        counts = df.groupby("dzongkhag").size().sort_values(ascending=True)
        st.bar_chart(counts)
    else:
        st.info("No taxi data available.")


elif page == "Taxi Records":
    st.title("Taxi Records")
    st.caption("Manage all registered taxis with the authority")

    taxis = su.get_taxis()
    df = pd.DataFrame(taxis)

    if df.empty:
        st.info("No records yet.")
    else:
        c1, c2 = st.columns([2, 1])
        with c1:
            search = st.text_input("🔍 Search by plate, dzongkhag, or vehicle",
                                   placeholder="BP-1-A1234")
        with c2:
            dz_options = ["All"] + sorted(df["dzongkhag"].unique().tolist())
            dz_filter = st.selectbox("Dzongkhag", dz_options)

        filtered = df.copy()
        if search:
            q = search.lower()
            filtered = filtered[
                filtered["plate"].str.lower().str.contains(q) |
                filtered["dzongkhag"].str.lower().str.contains(q) |
                filtered["vehicle"].str.lower().str.contains(q)
            ]
        if dz_filter != "All":
            filtered = filtered[filtered["dzongkhag"] == dz_filter]

        st.dataframe(filtered[["taxi_id", "plate", "dzongkhag",
                               "vehicle", "registered", "status"]],
                     use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Add new taxi record")

    with st.form("add_taxi", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            taxi_code = st.text_input("Taxi ID", placeholder="TX010")
            plate = st.text_input("Plate Number", placeholder="BP-1-Z9999")
            reg_date = st.date_input("Registration Date")
        with c2:
            dz = st.selectbox("Dzongkhag", su.get_dzongkhags())
            vehicle = st.selectbox("Vehicle Type", su.get_vehicle_types())
            status = st.selectbox("Status", ["Active", "Review", "Inactive"])

        submit = st.form_submit_button("Save Record", type="primary")

        if submit:
            if not taxi_code or not plate:
                st.error("Taxi ID and Plate Number are required.")
            else:
                ok, msg = su.add_taxi(taxi_code, plate, dz, vehicle,
                                      str(reg_date), status)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)


elif page == "Trip Records":
    st.title("Trip Records")
    st.caption("Review travel activity between Bhutanese dzongkhags")

    trips = su.get_trips()
    df = pd.DataFrame(trips)

    if df.empty:
        st.info("No trips yet.")
    else:
        c1, c2 = st.columns([2, 1])
        with c1:
            search = st.text_input("🔍 Search by dzongkhag", placeholder="Thimphu")
        with c2:
            dz_all = sorted(set(df["origin"].tolist() + df["destination"].tolist()))
            dz_filter = st.selectbox("Filter", ["All"] + dz_all)

        filtered = df.copy()
        if search:
            q = search.lower()
            filtered = filtered[
                filtered["origin"].str.lower().str.contains(q) |
                filtered["destination"].str.lower().str.contains(q)
            ]
        if dz_filter != "All":
            filtered = filtered[
                (filtered["origin"] == dz_filter) |
                (filtered["destination"] == dz_filter)
            ]

        st.dataframe(filtered[["origin", "destination", "date", "num_trips"]],
                     use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Add trip record")

    with st.form("add_trip", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            origin = st.selectbox("Origin Dzongkhag", su.get_dzongkhags())
            trip_date = st.date_input("Trip Date")
        with c2:
            destination = st.selectbox("Destination Dzongkhag", su.get_dzongkhags())
            num_trips = st.number_input("Number of Trips", min_value=1, value=1)

        submit = st.form_submit_button("Save Trip", type="primary")

        if submit:
            if origin == destination:
                st.error("Origin and destination cannot be the same.")
            else:
                ok, msg = su.add_trip(origin, destination, str(trip_date), num_trips)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)


elif page == "Drivers":
    st.title("Driver Profiles")
    st.caption("Registered drivers across Bhutan")

    drivers = su.get_drivers()
    df = pd.DataFrame(drivers)

    if df.empty:
        st.info("No drivers yet.")
    else:
        c1, c2 = st.columns([2, 1])
        with c1:
            search = st.text_input("🔍 Search by name or license",
                                   placeholder="Sonam")
        with c2:
            status_filter = st.selectbox("Status",
                                          ["All", "Available", "On Trip", "Review"])

        filtered = df.copy()
        if search:
            q = search.lower()
            filtered = filtered[
                filtered["name"].str.lower().str.contains(q) |
                filtered["license"].str.lower().str.contains(q)
            ]
        if status_filter != "All":
            filtered = filtered[filtered["status"] == status_filter]

        st.dataframe(
            filtered[["name", "license", "contact", "dzongkhag",
                      "vehicle", "plate", "status", "trips", "rating"]],
            use_container_width=True,
            hide_index=True,
        )


elif page == "Parking Zones":
    st.title("Parking Zones")
    st.caption("Taxi stands across all 20 dzongkhags")

    zones = su.get_parking_zones()

    cols = st.columns(3)
    for i, z in enumerate(zones):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"### 🚕 {z['name']}")
                st.caption(z["dzongkhag"])
                st.metric("Stationed Taxis", z["taxis"])