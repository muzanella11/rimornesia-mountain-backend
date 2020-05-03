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
migrate.create_begin_process('Create Table')
migrate.create_table()
migrate.create_end_process('Create Table')

# Re run Create Table for prevent `Cannot add foreign key constraint`
migrate.create_begin_process('Re Run Create Table')
migrate.create_table()
migrate.create_end_process('Re RunCreate Table')

# Execute Command
# migrate.execute_command(
#     DatabaseStructure().rename_fields_salaries()
# )

# migrate.execute_command(
#     DatabaseStructure().add_relation()
# )

# Drop Database
# migrate.drop_database()

# Rename Table
# migrate.rename_table("salariesss", "gaji")

# Close Connection
migrate.close_connection()