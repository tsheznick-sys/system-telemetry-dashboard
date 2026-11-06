#!/usr/bin/env python3
"""Standalone calculator-only web service."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field

from calculator import calculate, format_result

app = FastAPI(
    title="Ghost Calculator",
    description="A calculator-only service with no telemetry or host data routes.",
    docs_url=None,
    redoc_url=None,
)


class CalculatorExpression(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expression: Annotated[str, Field(min_length=1, max_length=256)]


def calculator_page() -> FileResponse:
    return FileResponse(Path(__file__).with_name("calculator.html"))


app.add_api_route("/", calculator_page, methods=["GET"], include_in_schema=False)
app.add_api_route(
    "/calculator",
    calculator_page,
    methods=["GET"],
    include_in_schema=False,
)


@app.get("/health", include_in_schema=False)
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/calculate")
def calculate_expression(
    request: CalculatorExpression,
) -> dict[str, int | float | str]:
    try:
        value = calculate(request.expression)
    except (
        SyntaxError,
        TypeError,
        ValueError,
        OverflowError,
        ZeroDivisionError,
    ) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"value": value, "result": format_result(value)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7862)
