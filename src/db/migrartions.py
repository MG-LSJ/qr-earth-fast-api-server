from alembic import command, config


def run_migrations(connection):
    print("Running migrations")
    alembic_config = config.Config("alembic.ini")
    alembic_config.attributes["connection"] = connection
    alembic_config.attributes["configure_logger"] = False
    command.upgrade(alembic_config, "head")
