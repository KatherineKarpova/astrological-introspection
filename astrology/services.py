from kerykeion import AstrologicalSubject, KerykeionChartSVG

# make global array so the 4 angels I want in the chart are included on top of the 7 planets and true nodes in active_points
TRADITIONAL_CHART_POINTS = [ 
    'Sun',
    'Moon',
    'Mercury',
    'Venus',
    'Mars',
    'Jupiter',
    'Saturn',
    'True_Node',
    'Ascendant',
    'Descendant',
    'Medium_Coeli',
    'Imum_Coeli',
]

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

    # this function creates the chart Kerykeion object from the validated form data 
    return AstrologicalSubject(
        name=data.get("name") or "Your Chart",
        year=birth_date.year,
        month=birth_date.month,
        day=birth_date.day,
        hour=hour,
        minute=minute,
        lat=data["latitude"],
        lng=data["longitude"],
        tz_str=timezone_name,
        online=False,
        zodiac_type="Tropic",
        houses_system_identifier="W",
    )

# this function manipulates the svg string created form 
def generate_chart_svg(chart, show_houses=True):
    # traditional active points excludes uranus, neptune, pluto, chiron, and lilith
    # takes the astrological subject object and creates a chart data object specifically to render
    drawer = KerykeionChartSVG(chart, active_points=TRADITIONAL_CHART_POINTS)
    svg = drawer.makeWheelOnlyTemplate()
    # remove houses from made svg if show houses is False, as determined by no birth time given
    if not show_houses:
        svg = remove_houses_from_svg(svg)

    return svg


# this function removes the houses visibility from the wheel for when birth time is unknown
def remove_houses_from_svg(svg):
    houses_start = svg.find('<!-- Houses -->')
    planets_start = svg.find('<!-- Planets -->')

    if houses_start != -1 and planets_start != -1:
        svg = svg[:houses_start] + svg[planets_start:]

    return svg