import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Agregar ruta al proyecto (muy importante)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar Base y modelos
from backend.db import Base
from backend.db.models import user
from backend.db.models import article  # Esto hace que Alembic vea el modelo User

# DO an check IN
print("Modelos detectados:", Base.metadata.tables.keys())

# Configuración de Alembic
config = context.config

# Configuración del logger de Alembic
fileConfig(config.config_file_name)

# Metadatos del modelo para autogenerar migraciones
target_metadata = Base.metadata

# Usamos la variable de entorno para conectar la base de datos
from dotenv import load_dotenv
load_dotenv()
config.set_main_option('sqlalchemy.url', os.getenv("DATABASE_URL"))

def run_migrations_offline():
    """Ejecuta migraciones en modo 'offline' (sin conexión)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Ejecuta migraciones en modo 'online' (con conexión activa)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Decide cuál método ejecutar según el contexto
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
