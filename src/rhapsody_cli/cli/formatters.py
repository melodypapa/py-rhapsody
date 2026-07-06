"""Output formatting for different display formats."""

from __future__ import annotations

import csv
import io
import json
from typing import Any

from tabulate import tabulate  # type: ignore[import-untyped]


class OutputFormatter:
    """Handles formatting output in table, JSON, CSV, or tree formats."""

    @staticmethod
    def table(headers: list[str], rows: list[list[Any]]) -> str:
        """Format as ASCII table."""
        if not rows:
            return "(no data)"
        return str(tabulate(rows, headers=headers, tablefmt="grid"))

    @staticmethod
    def json_format(data: Any) -> str:
        """Format as JSON."""
        return json.dumps(data, indent=2, default=str)

    @staticmethod
    def csv_format(headers: list[str], rows: list[list[Any]]) -> str:
        """Format as CSV."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(rows)
        return output.getvalue()

    @staticmethod
    def format(data: Any, format_type: str, headers: list[str] | None = None) -> str:
        """Route data to appropriate formatter."""
        if format_type == "json":
            return OutputFormatter.json_format(data)
        elif format_type == "csv":
            headers = headers or []
            rows = data if isinstance(data, list) else [data]
            return OutputFormatter.csv_format(headers, rows)
        else:  # table (default)
            headers = headers or []
            rows = data if isinstance(data, list) else [data]
            return OutputFormatter.table(headers, rows)
