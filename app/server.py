from fastapi import FastAPI
from app.schema_guardian import (
    fetch_schema,
    analyze_schema,
    generate_descriptions,
    build_report,
)

app = FastAPI(title="NovaDynamics", version="0.1.0")


@app.get("/")
async def health():
    return {"status": "ok"}


@app.get("/schema_guardian")
async def schema_guardian():
    schema = await fetch_schema()
    collection = schema.get("collection", "unknown")
    fields = schema.get("fields", [])
    total_fields = len(fields)

    missing_fields = analyze_schema(schema)
    suggestions = await generate_descriptions(missing_fields)
    report = build_report(collection, total_fields, missing_fields, suggestions)

    return report
