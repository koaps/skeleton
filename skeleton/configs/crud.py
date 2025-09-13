from skeleton import database, models
from skeleton.configs import console


def add_config(db, debug, config_data):
    db_config = models.Config(
        name=config_data["name"],
        value=config_data["value"],
    )
    database.add_record(db, db_config, debug)
    return


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


def update_config(db, debug, config_id, config_data):
    config = get_config(db, config_id)
    if debug:
        console.debug_msg(f"update_config: {config}")
    if config:
        config.name = config_data["name"]
        config.value = config_data["value"]
        database.update_record(db, config, debug)
    else:
        console.exit_msg("Config not found")
    return


def delete_config(db, debug, config_id):
    config = get_config(db, config_id)
    if debug:
        console.debug_msg(f"delete config: {config}")
    if config:
        database.delete_record(db, config, debug)
    else:
        console.exit_msg("Config not found")
    return
