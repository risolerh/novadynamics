import os
import httpx
from openai import AsyncOpenAI


SCHEMA_URL = (
    "https://designsuccess-media.s3.us-west-1.amazonaws.com/"
    "employee_records-dummy.json"
)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL = "mistralai/mistral-7b-instruct:free"


async def fetch_schema() -> dict:
    """Fetch the remote JSON schema."""
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(SCHEMA_URL)
        response.raise_for_status()
        return response.json()


def analyze_schema(schema: dict) -> list[dict]:
    """Return fields that are missing meta.description or meta.note."""
    missing: list[dict] = []
    for field in schema.get("fields", []):
        meta = field.get("meta", {})
        has_description = bool(meta.get("description"))
        has_note = bool(meta.get("note"))
        if not has_description or not has_note:
            missing.append(field)
    return missing


def _humanize_field_name(name: str) -> str:
    """Convert snake_case field name into a readable phrase."""
    return name.replace("_", " ").strip().capitalize()


async def _call_llm(field_name: str, field_type: str) -> str:
    """Call OpenRouter LLM to generate a field description."""
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key or api_key == "your_api_key_here":
        return f"{_humanize_field_name(field_name)} ({field_type})"

    client = AsyncOpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)
    prompt = (
        f"Generate a short, helpful metadata description (one sentence) "
        f"for a database field named '{field_name}' of type '{field_type}'. "
        f"Reply with ONLY the description text, nothing else."
    )
    try:
        response = await client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=80,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return f"{_humanize_field_name(field_name)} ({field_type})"


async def generate_descriptions(
    missing_fields: list[dict],
) -> list[dict[str, str]]:
    """Generate AI descriptions for each field missing metadata."""
    suggestions: list[dict[str, str]] = []
    for field in missing_fields:
        name = field.get("field", "unknown")
        ftype = field.get("type", "string")
        description = await _call_llm(name, ftype)
        suggestions.append({"field": name, "suggested_description": description})
    return suggestions


def build_report(
    collection: str,
    total_fields: int,
    missing_fields: list[dict],
    suggestions: list[dict[str, str]],
) -> dict:
    """Assemble the final JSON report."""
    table_rows = "\n".join(
        f"| {s['field']} | {s['suggested_description']} |" for s in suggestions
    )
    markdown_report = (
        "# Schema Guardian Report\n\n"
        f"**Collection:** {collection}\n\n"
        f"**Total fields:** {total_fields} · "
        f"**Missing metadata:** {len(missing_fields)}\n\n"
        "| Field | Suggested Description |\n"
        "|---|---|\n"
        f"{table_rows}"
    )

    return {
        "collection": collection,
        "total_fields": total_fields,
        "fields_missing_metadata": len(missing_fields),
        "report": markdown_report,
    }
