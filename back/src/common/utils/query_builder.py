from pydantic import BaseModel
from typing import Type


def columns(model: Type[BaseModel]) -> list[str]:
    return list(model.model_fields.keys())


def placeholders(cols: list[str]) -> str:
    return ", ".join(f":{c}" for c in cols)


def where_clause(cols: list[str]) -> str:
    return " AND ".join(f"{c} = :{c}" for c in cols)


def diff_row(
    old: BaseModel,
    new: BaseModel,
    ignore: set[str] = set(),
) -> dict[str, object]:
    diffs = {}

    for field in old.model_fields:
        if field in ignore:
            continue

        old_val = getattr(old, field)
        new_val = getattr(new, field)

        if old_val != new_val:
            diffs[field] = new_val

    return diffs
