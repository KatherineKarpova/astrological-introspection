from kerykeion import AstrologicalSubjectFactory


def calculate_birth_chart(data, timezone_name):
    """Create a Kerykeion astrological subject from validated birth data."""

    birth_date = data["birth_date"]
    birth_time = data["birth_time"]

    if birth_time is None:
        raise ValueError("A known birth time is required to calculate the chart.")

    return AstrologicalSubjectFactory.from_birth_data(
        name=data.get("name") or "Your Chart",
        year=birth_date.year,
        month=birth_date.month,
        day=birth_date.day,
        hour=birth_time.hour,
        minute=birth_time.minute,
        seconds=birth_time.second,
        lat=data["latitude"],
        lng=data["longitude"],
        tz_str=timezone_name,
        online=False,
        zodiac_type="Tropical",
        houses_system_identifier="W",
    )