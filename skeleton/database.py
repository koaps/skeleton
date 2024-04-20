import os
import sys

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
from sqlalchemy.exc import IntegrityError

from skeleton import console


def add_record(
    db,
    record,
    debug=False,
):
    if debug:
        console.debug_msg(record)

    try:
        db.add(record)
        db.commit()
        db.refresh(record)
        console.ok_msg("record added")
    except IntegrityError as exc:
        db.rollback()
        console.warn_msg(f"rolled back - duplicate record")
    return record


def build_engine(dsn, **kwargs):
    engine = sa.create_engine(
        dsn,
        connect_args={"check_same_thread": False},
        **kwargs,
    )
    return engine


def build_session(engine):
    Session = sa_orm.sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )
    return Session


def get_db(debug, dsn):
    engine = build_engine(dsn, echo=debug, future=True)
    SessionLocal = build_session(engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_dsn(db_name, test):
    db_dir = f"{os.getcwd()}/db"
    makecmd = "db"
    if test:
        db_name = f"test_{db_name}"
        makecmd = "test_db"
    database = f"{db_name}.db"
    if not os.path.exists(f"{db_dir}/{database}"):
        sys.exit(f"Database file {db_dir}/{database} not found, run: make {makecmd}")

    return f"sqlite:///{db_dir}/{database}"


def update_record(
    db,
    record,
    debug=False,
):
    if debug:
        console.debug_msg(record)

    try:
        db.commit()
        db.refresh(record)
        console.ok_msg("record updated")
    except Exception as exc:
        db.rollback()
        console.warn_msg(f"rolled back - db exception: {exc}")
    return record


def delete_record(
    db,
    record,
    debug=False,
):
    if debug:
        console.debug_msg(record)

    try:
        db.delete(record)
        db.commit()
        console.ok_msg("record deleted")
    except Exception as exc:
        db.rollback()
        console.warn_msg(f"rolled back - db exception: {exc}")
    return
