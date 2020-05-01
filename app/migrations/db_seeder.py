from app.core.migrations import Migrations
from app.migrations.seeder.seeder_provinces import SeederProvinces
from app.migrations.seeder.seeder_regencies import SeederRegencies
from app.migrations.seeder.seeder_districts import SeederDistricts
from app.migrations.seeder.seeder_villages import SeederVillages
import os

DB_NAME = os.environ.get('DB_NAME')

regencies_data = SeederRegencies().run()
districts_data = SeederDistricts().run()
villages_data = SeederVillages().run()

migrate = Migrations()
reconnect = False

# Create or Use database
migrate.create_database(DB_NAME)

# Seeder Data Provinces
migrate.create_begin_process('Seeder Data Provinces')
migrate.execute_command(
    SeederProvinces().run()
)
migrate.create_end_process('Seeder Data Provinces')

# Reconnect db because `cursor.execute` cannot run multiple queries
reconnect = True

# Close Connection
migrate.close_connection()

# Seeder Data Regencies
migrate.create_begin_process('Seeder Data Regencies')

for target_list in regencies_data:
    regencies_command = regencies_data.get(target_list)
    table_name = regencies_command.get('table_name')
    action = regencies_command.get('action')
    command = regencies_command.get('command')

    command_param = {}

    command_param[table_name] = {
        'action': action,
        'command': command
    }

    if reconnect == True:
        migrate = Migrations()
        
        # Create or Use database
        migrate.create_database(DB_NAME)
    
    print('[EXECUTE] {}'.format(target_list))

    migrate.execute_command(
        command_param
    )

    reconnect = True

    # Close Connection
    migrate.close_connection()

migrate.create_end_process('Seeder Data Regencies')

### Districts
# Reconnect db because `cursor.execute` cannot run multiple queries
reconnect = True

# Close Connection
migrate.close_connection()

# Seeder Data Districts
migrate.create_begin_process('Seeder Data Districts')

for target_list in districts_data:
    districts_command = districts_data.get(target_list)
    table_name = districts_command.get('table_name')
    action = districts_command.get('action')
    command = districts_command.get('command')

    command_param = {}

    command_param[table_name] = {
        'action': action,
        'command': command
    }

    if reconnect == True:
        migrate = Migrations()
        
        # Create or Use database
        migrate.create_database(DB_NAME)
    
    print('[EXECUTE] {}'.format(target_list))

    migrate.execute_command(
        command_param
    )

    reconnect = True

    # Close Connection
    migrate.close_connection()

migrate.create_end_process('Seeder Data Districts')

### Villages
# Reconnect db because `cursor.execute` cannot run multiple queries
reconnect = True

# Close Connection
migrate.close_connection()

# Seeder Data Villages
migrate.create_begin_process('Seeder Data Villages')

for target_list in villages_data:
    villages_command = villages_data.get(target_list)
    table_name = villages_command.get('table_name')
    action = villages_command.get('action')
    command = villages_command.get('command')

    command_param = {}

    command_param[table_name] = {
        'action': action,
        'command': command
    }

    if reconnect == True:
        migrate = Migrations()
        
        # Create or Use database
        migrate.create_database(DB_NAME)
    
    print('[EXECUTE] {}'.format(target_list))

    migrate.execute_command(
        command_param
    )

    reconnect = True

    # Close Connection
    migrate.close_connection()

migrate.create_end_process('Seeder Data Villages')

reconnect = False

# Close Connection
migrate.close_connection()