import os

import sqlalchemy.orm as sa_orm

from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, create_engine

from skeleton import console


def add_record(
    db,
    record,
    debug=False,
):
    if debug:
        console.debug_msg(f"add_record: {record}")

    try:
        db.add(record)
        db.commit()
        db.refresh(record)
        console.ok_msg("record added")
    except IntegrityError as exc:
        db.rollback()
        console.warn_msg(f"rolled back - {exc}")
    return record


def build_engine(dsn, **kwargs):
    engine = create_engine(
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


def commit(db):
    try:
        db.commit()
        console.ok_msg("record deleted")
    except Exception as exc:
        db.rollback()
        console.warn_msg(f"rolled back - db exception: {exc}")
    return


def create_db(debug, dsn):
    db = next(get_db(debug, dsn))
    SQLModel.metadata.create_all(bind=db.bind)


def delete_record(
    db,
    record,
    debug=False,
):
    if debug:
        console.debug_msg(f"delete_record: {record}")

    try:
        db.delete(record)
        db.commit()
        console.ok_msg("record deleted")
    except Exception as exc:
        db.rollback()
        console.warn_msg(f"rolled back - db exception: {exc}")
    return


def get_db(debug, dsn):
    engine = build_engine(dsn, echo=debug, future=True)
    SessionLocal = build_session(engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_dsn(debug, db_name):
    db_dir = f"{os.getcwd()}/db"
    database = f"{db_dir}/{db_name}.db"
    dsn = f"sqlite:///{database}"
    if not os.path.exists(database):
        create_db(debug, dsn)
    return dsn


def update_record(
    db,
    record,
    debug=False,
):
    if debug:
        console.debug_msg(f"update_record: {record}")

    try:
        db.add(record)
        db.commit()
        db.refresh(record)
        console.ok_msg("record updated")
    except Exception as exc:
        db.rollback()
        console.warn_msg(f"rolled back - db exception: {exc}")
    return record
