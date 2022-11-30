from sqlalchemy import Column, Integer, MetaData, Numeric, Sequence, String, \
    Table, TEXT, UniqueConstraint, select, alias, and_
from sqlalchemy.dialects.postgresql import ENUM, TIMESTAMP

from typing import Optional, List
from sqlalchemy.engine import Connection, Row
from sqlalchemy.dialects.postgresql import insert
from database import get_connection

VEHICLE = "bus"

metadata = MetaData()
Journeys = Table(
    "journeys",
    metadata,
    Column("id", Integer, Sequence("journeys_seq"), primary_key=True),
    Column("source", TEXT, index=True, nullable=False),
    Column("destination", TEXT, index=True, nullable=False),
    Column("departure_datetime", TIMESTAMP, nullable=False),
    Column("arrival_datetime", TIMESTAMP, nullable=False),
    Column("carrier", TEXT, index=True, nullable=False),
    Column("vehicle_type",
           ENUM("airplane", "bus", "train", name="vehicle_type")),
    Column("price", Numeric(20, 6), nullable=False),
    Column("currency", String(3), nullable=False),
    UniqueConstraint("source", "destination", "departure_datetime",
                     "arrival_datetime", "carrier", name="unique_journey"),
)


def create_journey(connection: Connection, journey) -> Optional[Row]:
    query = insert(Journeys).values(**journey).returning("*") \
        .on_conflict_do_nothing()
    executed_query = connection.execute(query)
    return executed_query.one_or_none()


def insert_data(src, dst, am, curr, dep_date, arr_date):
    with get_connection.database_connection() as conn:
        data = {
            "source": src,
            "destination": dst,
            "departure_datetime": dep_date,
            "arrival_datetime": arr_date,
            "carrier": "LH",
            "vehicle_type": VEHICLE,
            "price": am,
            "currency": curr
        }
        create_journey(conn, data)


def get_journeys(destination: str,
                 source: str,
                 stop_over: bool = None) -> List[Row]:
    with get_connection.database_connection() as conn:

        if stop_over:
            print("&&&stopover")
            aliasJourneys = alias(Journeys)
            query = select([Journeys, aliasJourneys]).join(aliasJourneys,
                            Journeys.c.destination == aliasJourneys.c.source)
            results = conn.execute(query).fetchall()
            for combination in results:
                yield {"source": combination["source"],
                       "stopover": combination["destination"],
                       "destination": combination["destination_1"],
                       "departure_datetime": combination["departure_datetime"],
                       "arrival_datetime": combination["arrival_datetime_1"]}

        else:
            print("&&&no")
            query = select(Journeys).where(
                and_(Journeys.c.source == source,
                     Journeys.c.destination == destination
                     # Journeys.c.departure_datetime.between()
                     )
            )
        rows = conn.execute(query).all()
        yield from rows

