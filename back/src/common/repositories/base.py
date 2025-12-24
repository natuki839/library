from typing import TypeVar, Generic
from pydantic import BaseModel

PK = TypeVar("PK", bound=BaseModel)
Body = TypeVar("Body", bound=BaseModel)
Row = TypeVar("Row", bound=BaseModel | None)


from src.common.utils.query_builder import columns, placeholders, where_clause


class BaseRepository(Generic[PK, Body, Row]):
    table_name: str
    pk_model: type[PK]
    body_model: type[Body] | None
    row_model: type[Row]

    def __init__(self, conn):
        self.conn = conn

    def insert(self, new_row: Row) -> None:
        data = new_row.model_dump(exclude_unset=True)

        if not data:
            raise ValueError("INSERTするカラムがありません")

        cols = list(data.keys())
        sql = f"""
        INSERT INTO {self.table_name}
        ({", ".join(cols)})
        VALUES ({placeholders(cols)})
        """

        self.conn.execute(sql, data)


    def find_by_pk(self, pk: PK) -> Row | None:
        cols = columns(pk.__class__)
        sql = f"""
        SELECT * FROM {self.table_name}
        WHERE {where_clause(cols)}
        """

        row = self.conn.execute(
            sql,
            pk.model_dump()
        ).fetchone()

        return self.row_model(**row) if row else None


    def update(self, pk: PK, body: Body) -> None:
        if body is None:
            return
        
        data = body.model_dump(exclude_unset=True)

        if not data:
            return

        set_clause = ", ".join(
            f"{c} = :{c}" for c in data.keys()
        )
        where = where_clause(columns(pk.__class__))

        sql = f"""
        UPDATE {self.table_name}
        SET {set_clause}
        WHERE {where}
        """

        params = {
            **pk.model_dump(),
            **data,
        }

        self.conn.execute(sql, params)


    def delete(self, pk: PK) -> None:
        where = where_clause(columns(pk.__class__))
        sql = f"""
        DELETE FROM {self.table_name}
        WHERE {where}
        """
        self.conn.execute(sql, pk.model_dump())

