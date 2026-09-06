from kerykeion import AstrologicalSubjectFactory, ChartDataFactory
from kerykeion.charts.chart_drawer import ChartDrawer


def calculate_birth_chart(data, timezone_name):
    # create a Kerykeion astrological subject from validated birth data

    birth_date = data["birth_date"]
    birth_time = data["birth_time"]

    # use 12pm as birth time if unknown, but hide ascendents and houses from display
    if birth_time is None:
        hour = 12
        minute = 0
    else:
        hour = birth_time.hour
        minute = birth_time.minute

    return AstrologicalSubjectFactory.from_birth_data(
        name=data.get("name") or "Your Chart",
        year=birth_date.year,
        month=birth_date.month,
        day=birth_date.day,
        hour=hour,
        minute=minute,
        seconds=0,
        lat=data["latitude"],
        lng=data["longitude"],
        tz_str=timezone_name,
        online=False,
        zodiac_type="Tropical",
        houses_system_identifier="W",
    )

def generate_chart_svg(chart):
    chart_data = ChartDataFactory.create_natal_chart_data(chart)

    drawer = ChartDrawer(chart_data)

    return drawer.generate_wheel_only_svg_string()