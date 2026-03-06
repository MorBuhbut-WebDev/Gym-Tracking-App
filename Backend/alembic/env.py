# Configures Python's logging system using the settings defined in alembic.ini
from logging.config import fileConfig

# engine_from_config builds a SQLAlchemy engine from alembic.ini settings
# pool and Table are used to configure connection pooling and reflect external tables
from sqlalchemy import engine_from_config
from sqlalchemy import pool, Table

# context is Alembic's runtime object — it holds the connection, metadata,
# and controls how migrations are discovered and executed
from alembic import context

# Base.metadata contains all SQLAlchemy model definitions (tables, constraints, indexes)
# Alembic uses this to compare against the live DB and generate migrations
from app.db.session import Base

# Importing models registers them into Base.metadata so Alembic can detect them
# Without these imports, autogenerate would produce empty migrations
from app.models import (
    Exercise,
    Routine,
    RoutineExercise,
    Workout,
    WorkoutExercise,
    WorkoutSet,
)

# App settings provide the database URL so we don't hardcode credentials in alembic.ini
from app.config import settings

# Alembic's config object — provides access to alembic.ini values at runtime
config = context.config

# Set up logging as defined in alembic.ini so migration output is properly formatted
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Override the database URL from alembic.ini with the one from our app settings
# This ensures migrations always use the correct environment's DB (dev, staging, prod)
# We use the sync URL here because Alembic does not support async connections
config.set_main_option("sqlalchemy.url", settings.database_url_sync)


def run_migrations_offline() -> None:
    # Offline mode generates SQL scripts without connecting to the DB
    # Useful for reviewing migration SQL before applying it, or for DBAs who apply migrations manually
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=Base.metadata,
        # literal_binds renders parameter values directly in the SQL output instead of placeholders
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # Online mode connects to the live DB and applies migrations directly

    # Build a synchronous engine from alembic.ini config
    # NullPool disables connection pooling — each migration gets a fresh connection
    # This is important for Alembic since migrations are one-off operations, not sustained workloads
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # First connection: reflect the public.users table into Base.metadata
    # users is managed by Supabase auth and has no SQLAlchemy model in our codebase
    # Reflecting it allows SQLAlchemy to resolve FK references to users.user_id
    # at metadata build time without us needing to define a User model
    # We use a separate connection here to keep reflection outside the migration transaction
    with connectable.connect() as connection:
        Table(
            "users",
            Base.metadata,
            autoload_with=connection,
            schema="public",
            # extend_existing prevents errors if this reflection runs more than once
            extend_existing=True,
        )

    # Second connection: run the actual migrations in their own clean transaction
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata,
            # include_schemas tells Alembic to be aware of schema namespaces
            # required because our DB has multiple schemas (public, auth, etc.)
            include_schemas=True,
            # include_object filters which DB objects Alembic should manage
            # - exclude the users table entirely since it's Supabase-managed
            # - only include tables in the public schema or with no explicit schema (also public)
            # - non-table objects (indexes, constraints) are always included
            include_object=lambda obj, name, type_, reflected, compare_to: (
                # not (type_ == "table" and name == "users")
                # and (type_ != "table" or obj.schema in ("public", None))
                type_ != "table"
                or (name != "users" and obj.schema in ("public", None))
            ),
        )

        with context.begin_transaction():
            context.run_migrations()


# Entry point: Alembic calls this file and we route to the appropriate mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
