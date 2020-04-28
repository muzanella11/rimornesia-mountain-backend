from app.core.migrations import Migrations
from app.migrations.db_structure import DatabaseStructure
import os

DB_NAME = os.environ.get('DB_NAME')

migrate = Migrations()

# Prepare Tables
migrate.prepare_tables(
    DatabaseStructure().init_structure()
)

# Create or Use database
migrate.create_database(DB_NAME)

# Create Tables
migrate.create_table()

# Execute Command
migrate.execute_command(
    DatabaseStructure().rename_fields_salaries()
)

# Drop Database
# migrate.drop_database()

# Rename Table
# migrate.rename_table("salariesss", "gaji")

# Close Connection
migrate.close_connection()