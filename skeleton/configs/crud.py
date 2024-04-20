import os

from sqlalchemy.exc import IntegrityError

from skeleton import database
from skeleton.configs import console, models, schemas


def add_config(db, debug, config_info: schemas.ConfigAdd):
    db_config = models.Config(
        name=config_info.name,
        value=config_info.value,
        ts=config_info.ts,
    )
    database.add_record(db, db_config, debug)
    return

def create_db(debug, dsn):
    db = next(database.get_db(debug, dsn))
    models.mapper_registry.metadata.create_all(bind=db.bind)

def get_dsn(debug, name, test):
    db_dir = f"{os.getcwd()}/db"
    database = f"{name}.db"
    if test:
        database = f"test_{database}"

    dsn = f"sqlite:///{db_dir}/{database}"
    if not os.path.exists(f"{db_dir}/{database}"):
        create_db(debug, dsn)

    return dsn

def get_config(db, config_id: int):
    return db.query(models.Config).filter(models.Config.id == config_id).first()


def get_config_by_match(db, name: str):
    return db.query(models.Config).filter(models.Config.name.contains(name)).first()


def get_config_by_name(db, name: str):
    return db.query(models.Config).filter(models.Config.name == name).first()

def get_configs(db, skip: int = 0, limit: int = 100):
    return db.query(models.Config).offset(skip).limit(limit).all()

def get_configs_by_match(db, name: str):
    return db.query(models.Config).filter(models.Config.name.contains(name)).all()


def update_config(db, debug, config_id, config_info: schemas.ConfigUpdate):
    db_config = db.query(models.Config).get(config_id)
    if db_config:
        db_config.id = int(config_id)
        db_config.name = config_info.name
        db_config.value = config_info.value
        db_config.ts = config_info.ts
        database.update_record(db, db_config, debug)
    else:
        console.exit_msg("Config not found")
    return


def delete_config(db, debug, config_id):
    db_config = db.query(models.Config).get(config_id)
    database.delete_record(db, db_config, debug)
    return
