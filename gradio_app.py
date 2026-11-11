# gradio_app.py
import gradio as gr
import supabase_utils as su


def lookup_taxi(query):
    if not query.strip():
        return "Enter a plate number, dzongkhag, or vehicle type."

    taxis = su.get_taxis()
    q = query.lower()
    matches = [t for t in taxis
               if q in t["plate"].lower()
               or q in t["dzongkhag"].lower()
               or q in t["vehicle"].lower()]

    if not matches:
        return f"No taxis found for **'{query}'**."

    lines = [f"### Found {len(matches)} result(s)\n"]
    for t in matches:
        lines.append(
            f"**{t['taxi_id']}** · {t['plate']}\n"
            f"- Dzongkhag: {t['dzongkhag']}\n"
            f"- Vehicle: {t['vehicle']}\n"
            f"- Registered: {t['registered']}\n"
            f"- Status: **{t['status']}**\n"
        )
    return "\n".join(lines)


def lookup_driver(query):
    if not query.strip():
        return "Enter a driver name or license number."

    drivers = su.get_drivers()
    q = query.lower()
    matches = [d for d in drivers
               if q in d["name"].lower()
               or q in d["license"].lower()]

    if not matches:
        return f"No drivers found for **'{query}'**."

    lines = [f"### Found {len(matches)} result(s)\n"]
    for d in matches:
        lines.append(
            f"**{d['name']}** · {d['license']}\n"
            f"- Contact: {d['contact']}\n"
            f"- Dzongkhag: {d['dzongkhag']}\n"
            f"- Vehicle: {d['vehicle']} ({d['plate']})\n"
            f"- Rating: {d['rating']}\n"
            f"- Trips: {d['trips']} · Cancellations: {d['cancellations']}\n"
            f"- Status: **{d['status']}**\n"
        )
    return "\n".join(lines)


def lookup_zone(query):
    if not query.strip():
        return "Enter a zone name or dzongkhag."

    zones = su.get_parking_zones()
    q = query.lower()
    matches = [z for z in zones
               if q in z["name"].lower()
               or q in z["dzongkhag"].lower()]

    if not matches:
        return f"No parking zones found for **'{query}'**."

    lines = [f"### Found {len(matches)} result(s)\n"]
    for z in matches:
        lines.append(
            f"**{z['name']}**\n"
            f"- Dzongkhag: {z['dzongkhag']}\n"
            f"- Stationed Taxis: **{z['taxis']}**\n"
        )
    return "\n".join(lines)


def zone_drivers(zone_name):
    zones = su.get_parking_zones()
    match = next((z for z in zones if z["name"] == zone_name), None)
    if not match:
        return "Zone not found."

    dzong = match["dzongkhag"].replace("dzongkhag", "").strip()
    drivers = [d for d in su.get_drivers()
               if d["dzongkhag"].lower() == dzong.lower()]

    if not drivers:
        return f"No drivers currently stationed at **{zone_name}**."

    lines = [f"### Drivers in {dzong} ({len(drivers)})\n"]
    for d in drivers:
        lines.append(
            f"**{d['name']}** · {d['vehicle']} ({d['plate']})\n"
            f"- Contact: {d['contact']} · Status: {d['status']}\n"
        )
    return "\n".join(lines)


with gr.Blocks(title="Jogay Jogay · Public Lookup", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🚕 Jogay Jogay · Public Lookup
    ### Bhutan Transport Authority
    Search for taxis, drivers, and parking zones across all 20 dzongkhags.
    """)

    with gr.Tabs():
        with gr.Tab("🔍 Find a Taxi"):
            with gr.Row():
                taxi_query = gr.Textbox(
                    label="Search",
                    placeholder="e.g. BP-1-A1234, Thimphu, Maruti Alto",
                    scale=3,
                )
                taxi_btn = gr.Button("Search", variant="primary", scale=1)
            taxi_out = gr.Markdown("Results will appear here.")
            taxi_btn.click(lookup_taxi, inputs=taxi_query, outputs=taxi_out)
            taxi_query.submit(lookup_taxi, inputs=taxi_query, outputs=taxi_out)

        with gr.Tab("👤 Find a Driver"):
            with gr.Row():
                driver_query = gr.Textbox(
                    label="Search",
                    placeholder="e.g. Sonam Dorji, DL-2024-0456",
                    scale=3,
                )
                driver_btn = gr.Button("Search", variant="primary", scale=1)
            driver_out = gr.Markdown("Results will appear here.")
            driver_btn.click(lookup_driver, inputs=driver_query, outputs=driver_out)
            driver_query.submit(lookup_driver, inputs=driver_query, outputs=driver_out)

        with gr.Tab("🅿 Parking Zones"):
            with gr.Row():
                zone_query = gr.Textbox(
                    label="Search",
                    placeholder="e.g. Thimphu, Paro Taxi Stand",
                    scale=3,
                )
                zone_btn = gr.Button("Search", variant="primary", scale=1)
            zone_out = gr.Markdown("Results will appear here.")
            zone_btn.click(lookup_zone, inputs=zone_query, outputs=zone_out)
            zone_query.submit(lookup_zone, inputs=zone_query, outputs=zone_out)

            gr.Markdown("---")
            gr.Markdown("### See who's stationed in a zone")
            zone_options = [z["name"] for z in su.get_parking_zones()]
            zone_picker = gr.Dropdown(choices=zone_options, label="Choose a zone")
            zone_drivers_out = gr.Markdown()
            zone_picker.change(zone_drivers, inputs=zone_picker, outputs=zone_drivers_out)

    gr.Markdown("---")
    gr.Markdown(
        "*Built with Python, Gradio, and Supabase. "
        f"Data source: {'🟢 Live' if su.is_live() else '🟡 Demo mode'}*"
    )


if __name__ == "__main__":
    demo.launch()
    