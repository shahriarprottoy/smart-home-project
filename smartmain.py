import flet as ft
from datetime import datetime

# Use the uploaded image file path
IMAGE_PATH = "/mnt/data/4649ad6a-cfbe-403a-901e-11326dc3b6d2.png"


def format_time():
    return datetime.now().strftime("%H:%M:%S")


def main(page: ft.Page):
    page.title = "Smart Home Controller"
    page.padding = 16
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.bgcolor = "#F3E3D3"  # light brown background

    try:
        page.window_maximized = True
    except:
        pass

    # ===== DEVICE STATES =====
    light_on = {"value": False}
    door_locked = {"value": True}
    thermostat = {"value": 22.0}
    fan_speed = {"value": 0}

    # ===== DEVICE METADATA =====
    device_info = {
        "light": {"id": "light_1", "name": "Living Room Light", "type": "Light"},
        "door": {"id": "door_1", "name": "Front Door", "type": "Door Lock"},
        "thermostat": {"id": "thermo_1", "name": "Thermostat", "type": "Thermostat"},
        "fan": {"id": "fan_1", "name": "Ceiling Fan", "type": "Fan"},
    }

    # ===== LOG STORAGE =====
    action_log = []

    def add_log(device, action):
        action_log.insert(
            0,
            {
                "time": format_time(),
                "device": device,
                "action": action,
                "user": "User",
            },
        )
        if len(action_log) > 200:
            action_log.pop()
        update_action_log_view()
        update_statistics_log_table()

    # ===== UI REFERENCES =====
    light_status = ft.Text("Off")
    door_status = ft.Text("LOCKED")
    thermostat_label = ft.Text("22.0 °C")
    fan_label = ft.Text("Fan speed: 0")

    light_button = ft.ElevatedButton("Turn ON")
    door_button = ft.ElevatedButton("Unlock")

    thermostat_slider = ft.Slider(min=16, max=30, divisions=14)
    fan_slider = ft.Slider(min=0, max=3, divisions=3)

    action_log_column = ft.Column()
    chart_container = ft.Container()
    stats_log_container = ft.Container()

    body_placeholder = ft.Container()

    # ===== LOG UPDATES =====
    def update_action_log_view():
        rows = [
            ft.Row(
                [
                    ft.Container(ft.Text("Time", weight="bold"), width=80),
                    ft.Container(ft.Text("Device", weight="bold"), width=140),
                    ft.Container(ft.Text("Action", weight="bold"), width=140),
                    ft.Container(ft.Text("User", weight="bold"), width=80),
                ]
            ),
            ft.Divider(),
        ]
        for e in action_log[:8]:
            rows.append(
                ft.Row(
                    [
                        ft.Container(ft.Text(e["time"]), width=80),
                        ft.Container(ft.Text(e["device"]), width=140),
                        ft.Container(ft.Text(e["action"]), width=140),
                        ft.Container(ft.Text(e["user"]), width=80),
                    ]
                )
            )
            rows.append(ft.Container(height=4))
        action_log_column.controls = rows
        page.update()

    def update_statistics_log_table():
        rows = []
        header = ft.Row(
            [
                ft.Container(ft.Text("Time", weight="bold"), width=90),
                ft.Container(ft.Text("Device", weight="bold"), width=160),
                ft.Container(ft.Text("Action", weight="bold"), width=240),
                ft.Container(ft.Text("User", weight="bold"), width=100),
            ]
        )
        rows.append(header)
        rows.append(ft.Divider())
        for entry in action_log[:20]:
            rows.append(
                ft.Row(
                    [
                        ft.Container(ft.Text(entry["time"]), width=90),
                        ft.Container(ft.Text(entry["device"]), width=160),
                        ft.Container(ft.Text(entry["action"]), width=240),
                        ft.Container(ft.Text(entry["user"]), width=100),
                    ]
                )
            )
            rows.append(ft.Divider())
        stats_log_container.content = ft.Container(
            content=ft.Column(rows),
            padding=8,
            bgcolor="#FFFFFF",
            border_radius=6,
        )

    # ===== DEVICE HANDLERS =====
    def toggle_light(e):
        light_on["value"] = not light_on["value"]
        light_status.value = "On" if light_on["value"] else "Off"
        light_button.text = "Turn OFF" if light_on["value"] else "Turn ON"
        add_log(
            device_info["light"]["name"],
            "Turn ON" if light_on["value"] else "Turn OFF",
        )
        page.update()

    def toggle_door(e):
        door_locked["value"] = not door_locked["value"]
        door_status.value = "LOCKED" if door_locked["value"] else "UNLOCKED"
        door_button.text = "Unlock" if door_locked["value"] else "Lock"
        add_log(
            device_info["door"]["name"],
            "Lock" if door_locked["value"] else "Unlock",
        )
        page.update()

    def thermostat_changed(e):
        thermostat["value"] = float(e.control.value)
        thermostat_label.value = f"{thermostat['value']:.1f} °C"
        add_log(
            device_info["thermostat"]["name"],
            f"Set {thermostat['value']:.1f} °C",
        )
        page.update()

    def fan_changed(e):
        fan_speed["value"] = int(e.control.value)
        fan_label.value = f"Fan speed: {fan_speed['value']}"
        add_log(device_info["fan"]["name"], f"Speed {fan_speed['value']}")
        page.update()

    light_button.on_click = toggle_light
    door_button.on_click = toggle_door
    thermostat_slider.on_change = thermostat_changed
    fan_slider.on_change = fan_changed

    # ===== DEVICE DETAILS =====
    def show_device_details(key):
        info = device_info[key]
        if key == "light":
            state = "ON" if light_on["value"] else "OFF"
        elif key == "door":
            state = "LOCKED" if door_locked["value"] else "UNLOCKED"
        elif key == "thermostat":
            state = f"{thermostat['value']} °C"
        else:
            state = f"Speed {fan_speed['value']}"

        filtered = [
            f"{e['time']} - {e['action']} ({e['user']})"
            for e in action_log
            if e["device"] == info["name"]
        ]
        log_controls = [ft.Text(l) for l in filtered[:20]]

        details_view = ft.Container(
            padding=20,
            bgcolor="#eef0f2",
            border_radius=8,
            content=ft.Column(
                [
                    ft.Text(f"{info['name']} details", size=26, weight="bold"),
                    ft.Text(f"ID: {info['id']}"),
                    ft.Text(f"Type: {info['type']}"),
                    ft.Text(f"State: {state}"),
                    ft.Divider(),
                    ft.Text("Recent actions", size=20, weight="bold"),
                    ft.Column(log_controls),
                    ft.ElevatedButton(
                        "Back to overview", on_click=lambda e: show_overview()
                    ),
                ],
                spacing=10,
            ),
        )
        body_placeholder.content = details_view
        page.update()

    # ===== OVERVIEW PAGE =====
    def show_overview():
        overview = ft.Column(
            [
                ft.Divider(),
                ft.Text("On/Off devices", size=18, weight="bold"),
                ft.Row(
                    [
                        ft.Container(
                            padding=12,
                            width=360,
                            bgcolor="#FFFBEA",
                            border_radius=8,
                            content=ft.Column(
                                [
                                    ft.Text(
                                        "💡 Living Room Light",
                                        size=16,
                                        weight="bold",
                                    ),
                                    light_status,
                                    ft.Row(
                                        [
                                            light_button,
                                            ft.Container(width=8),
                                            ft.TextButton(
                                                "Details",
                                                on_click=lambda e: show_device_details(
                                                    "light"
                                                ),
                                            ),
                                        ]
                                    ),
                                ],
                                spacing=4,
                            ),
                        ),
                        ft.Container(
                            padding=12,
                            width=360,
                            bgcolor="#F3F1F0",
                            border_radius=8,
                            content=ft.Column(
                                [
                                    ft.Text(
                                        "🚪 Front Door", size=16, weight="bold"
                                    ),
                                    door_status,
                                    ft.Row(
                                        [
                                            door_button,
                                            ft.Container(width=8),
                                            ft.TextButton(
                                                "Details",
                                                on_click=lambda e: show_device_details(
                                                    "door"
                                                ),
                                            ),
                                        ]
                                    ),
                                ],
                                spacing=4,
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(),
                ft.Text("Slider controlled devices", size=18, weight="bold"),
                ft.Row(
                    [
                        ft.Container(
                            padding=12,
                            width=360,
                            bgcolor="#FFEFF0",
                            border_radius=8,
                            content=ft.Column(
                                [
                                    ft.Text(
                                        "🌡️ Thermostat",
                                        size=16,
                                        weight="bold",
                                    ),
                                    thermostat_label,
                                    thermostat_slider,
                                    ft.Row(
                                        [
                                            ft.TextButton(
                                                "Details",
                                                on_click=lambda e: show_device_details(
                                                    "thermostat"
                                                ),
                                            ),
                                        ]
                                    ),
                                ],
                                spacing=4,
                            ),
                        ),
                        ft.Container(
                            padding=12,
                            width=360,
                            bgcolor="#E7FBFF",
                            border_radius=8,
                            content=ft.Column(
                                [
                                    ft.Text(
                                        "🌀 Ceiling Fan",
                                        size=16,
                                        weight="bold",
                                    ),
                                    fan_label,
                                    fan_slider,
                                    ft.Row(
                                        [
                                            ft.TextButton(
                                                "Details",
                                                on_click=lambda e: show_device_details(
                                                    "fan"
                                                ),
                                            ),
                                        ]
                                    ),
                                ],
                                spacing=4,
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(),
                ft.Text("Action log (recent)", size=16, weight="bold"),
                ft.Container(
                    content=action_log_column,
                    padding=8,
                    bgcolor="#FFFFFF",
                    border_radius=6,
                    width=760,
                ),
            ],
            spacing=12,
        )
        body_placeholder.content = overview
        page.update()

    # ===== STATISTICS PAGE =====
    def build_fake_chart():
        grid_rows = []
        grid_rows.append(ft.Container(height=3, bgcolor="#1AA7C9"))
        for _ in range(14):
            grid_rows.append(
                ft.Container(height=28, content=ft.Divider(color="#EEEEEE"))
            )
        return ft.Container(
            content=ft.Column(grid_rows),
            padding=8,
            width=920,
            height=260,
            bgcolor="#FAFAFA",
            border=ft.border.all(1, "#DDDDDD"),
            border_radius=4,
        )

    chart_container.content = build_fake_chart()
    stats_content = ft.Column(
        [
            ft.Divider(),
            ft.Text("Power consumption (simulated)", size=18, weight="bold"),
            chart_container,
            ft.Divider(),
            ft.Text("Action log", size=18, weight="bold"),
            ft.Container(content=stats_log_container, padding=4),
        ],
        spacing=12,
    )

    def show_statistics():
        update_statistics_log_table()
        body_placeholder.content = stats_content
        page.update()

    # ===== HEADER =====
    header = ft.Row(
        [
            ft.Image(src=f"file://{IMAGE_PATH}", width=260, height=68),
            ft.Container(width=12),
            ft.Column(
                [
                    ft.Text("Smart Home Controller", size=26, weight="bold"),
                    ft.Row(
                        [
                            ft.TextButton(
                                "Overview", on_click=lambda e: show_overview()
                            ),
                            ft.TextButton(
                                "Statistics", on_click=lambda e: show_statistics()
                            ),
                        ]
                    ),
                ]
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # INITIALIZE
    update_action_log_view()
    show_overview()

    # Center everything in a main column of fixed width
    main_column = ft.Column(
        [header, ft.Divider(), body_placeholder],
        width=950,
        alignment=ft.MainAxisAlignment.START,
    )

    page.add(main_column)


if __name__ == "__main__":
    ft.app(target=main)
