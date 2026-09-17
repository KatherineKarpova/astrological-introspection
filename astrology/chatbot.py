import json
from django.conf import settings
from openai import OpenAI


# load these server-controlled files.
# the user can ask questions, but cannot replace the application's
# instructions or its approved source collection.
SYSTEM_PROMPT = (
    settings.BASE_DIR / "shared" / "chat-policy.txt"
).read_text(encoding="utf-8")

SOURCES = json.loads(
    (
        settings.BASE_DIR / "shared" / "sources.json"
    ).read_text(encoding="utf-8")
)


def ask_chart_guide(
    chart_context,
    question,
    history,
    level="auto",
    tone="auto",
):
    """generate an explanation using calculated facts and recent chat."""

    if not settings.OPENAI_API_KEY:
        raise ValueError("The chatbot needs an API key.")

    # explicit preferences override the model's estimate.
    # automatic mode leaves the level and tone to the instructions.
    if level not in {"auto", "beginner", "technical"}:
        raise ValueError("Invalid explanation level.")

    if tone not in {"auto", "gentle", "direct"}:
        raise ValueError("Invalid conversation tone.")

    client = OpenAI(
        api_key=settings.OPENAI_API_KEY,
        timeout=35,
        max_retries=0,
    )

    # the chart and sources are supplied separately from the question.
    # this makes the distinction between application context and
    # the user's conversational input clearer.
    supplied_context = {
        "chart": chart_context,
        "sources": SOURCES,
        "preferences": {
            "level": level,
            "tone": tone,
        },
    }

    # retain a bounded amount of recent conversation.
    # without history, a follow-up such as "explain that more simply"
    # would arrive without the explanation it refers to.
    recent_history = history[-8:]

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "system",
            "content": json.dumps(supplied_context),
        },
        *recent_history,
        {
            "role": "user",
            "content": question,
        },
    ]

    completion = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=messages,

        # request a machine-readable response so django can separate
        # the answer, reflection question, and source references.
        response_format={"type": "json_object"},

        # bound response length and the cost of an individual answer.
        max_completion_tokens=850,

        # request that this completion not be stored by this feature.
        # this does not mean the provider never processes request data.
        store=False,
    )

    raw_content = completion.choices[0].message.content

    if not raw_content:
        raise ValueError("The model did not return an answer.")

    reply = json.loads(raw_content)

    # json mode guarantees neither your expected fields nor their types.
    # validate the response before passing it to your interface.
    if not isinstance(reply, dict):
        raise ValueError("Unexpected response format.")

    if not isinstance(reply.get("answer"), str):
        raise ValueError("The response is missing an answer.")

    if not isinstance(reply.get("reflection"), str):
        raise ValueError("The reflection has an invalid format.")

    source_ids = reply.get("source_ids")

    if not isinstance(source_ids, list):
        raise ValueError("The source references have an invalid format.")

    approved_sources = {
        source["id"]: source
        for source in SOURCES
    }

    # accept only ids from your own collection.
    # the browser will receive your verified URLs, rather than
    # URLs that the model generated.
    if any(
        not isinstance(source_id, str)
        or source_id not in approved_sources
        for source_id in source_ids
    ):
        raise ValueError("The response cited an unknown source.")

    reply["sources"] = [
        approved_sources[source_id]
        for source_id in dict.fromkeys(source_ids)
    ]

    return reply

# provide json dicts for llm to have context for responses
def build_chart_context(chart, has_birth_time):
    """convert a kerykeion subject into json-compatible chart facts."""

    sign_names = [
        "Aries", "Taurus", "Gemini", "Cancer",
        "Leo", "Virgo", "Libra", "Scorpio",
        "Sagittarius", "Capricorn", "Aquarius", "Pisces",
    ]

    # the list follows zodiac order, matching kerykeion's sign_num
    # these are traditional rulers: mars rules scorpio,
    # jupiter rules pisces, and saturn rules aquarius
    sign_rulers = [
        "Mars", "Venus", "Mercury", "Moon",
        "Sun", "Mercury", "Venus", "Mars",
        "Jupiter", "Saturn", "Saturn", "Jupiter",
    ]

    planet_names = [
        "Sun", "Moon", "Mercury", "Venus",
        "Mars", "Jupiter", "Saturn",
    ]

    context = {
        "zodiac": "tropical",
        "house_system": "whole_sign",
        "birth_time_known": has_birth_time,
        "ascendant": None,
        "chart_ruler": None,
        "planets": [],
    }

    # current calculation uses noon when the time is unknown
    # that does not establish a real rising sign or house placement
    # explicitly recording the uncertainty helps the model avoid
    # interpreting those temporary calculations as birth facts
    if has_birth_time:
        rising_sign_index = chart.ascendant.sign_num

        context["ascendant"] = {
            "sign": sign_names[rising_sign_index],
            "degree": round(chart.ascendant.position, 2),
        }

        context["chart_ruler"] = sign_rulers[rising_sign_index]

    for name in planet_names:
        # getattr(chart, "sun") is equivalent to chart.sun
        # using getattr lets the same code handle all seven planets
        planet = getattr(chart, name.lower())

        house = None

        if has_birth_time:
            # whole-sign houses count signs from the rising sign
            # modulo wraps the count around the end of the zodiac
            # adding one changes a zero-based index into houses 1–12
            house = (
                planet.sign_num - rising_sign_index
            ) % 12 + 1

        context["planets"].append({
            "name": name,
            "sign": sign_names[planet.sign_num],
            "degree": round(planet.position, 2),
            "house": house,
            "sign_ruler": sign_rulers[planet.sign_num],
            "retrograde": planet.retrograde,
        })

    # the model needs the calculated placements
    # it does not need the person's name or raw birth location
    return context