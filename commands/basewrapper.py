from datetime import datetime
import asyncio
import asyncpg
import json
import os


class Base:
    def info_logger(self, message):
        print(f'[{datetime.today()} - INFO] {message}')

    def error_logger(self, message):
        raise Exception(f'[{datetime.today()} - **ERROR**] {message}')

    def warning_logger(self, message):
        print(f'[{datetime.today()} - *WARNING*] {message}')

    def get_config_vars(self, var):
        token = os.environ.get(var)
        return token

    async def log_channel(self, client, guildid, embed):
        channelid = await Storage(str(guildid)).get("log_channel_id")
        channel = client.get_channel(int(channelid))
        await channel.send(embed=embed)



class Storage:

    def __init__(self, table_id: str):
        self.database_url = os.environ.get("DATABASE")
        self.table_id = "_" + table_id
        self.new_table = f'''
        CREATE TABLE IF NOT EXISTS {self.table_id} (
            join_channel_id BIGINT,
            log_channel_id BIGINT
            );
        '''

    async def initialize_db(self):
        # Improve this with with an sql if , no point in doing 2 queries
        database = await asyncpg.connect(self.database_url, ssl=True)
        try:
            await database.fetchrow(f'''
            SELECT EXISTS (
               SELECT * FROM {self.table_id}
               );
            ''')
            exists = True
        except asyncpg.exceptions.UndefinedTableError:
            exists = False

        if not exists:
            print("Created new database with id of " + self.table_id)
            await database.execute(f'''{self.new_table}''')
        else:
            print("Using existing table: " + self.table_id)
        await database.close()

    async def set(self, column, value):
        database = await asyncpg.connect(self.database_url, ssl=True)
        try:
            await database.execute(f'''                
                DO
                $do$
                BEGIN
                
                {self.new_table}

                IF EXISTS (SELECT {column} FROM {self.table_id}) THEN
                   UPDATE {self.table_id} SET {column} = {value};
                ELSE 
                    INSERT INTO {self.table_id}({column})
                    VALUES
                        ({value});
                END IF;
                END
                $do$
            ''')
            await database.close()
            return True
        except Exception as e:
            print("ERROR SET:")
            print(e)
            await database.close()
            return False

    async def get(self, column):
        database = await asyncpg.connect(self.database_url, ssl=True)
        try:
            await database.execute(f'''{self.new_table}''')
            value = await database.fetchrow(f'''SELECT {column} FROM {self.table_id};''')
            await database.close()
            if value is None:
                return None
            return value.get(column)
        except Exception as e:
            print("ERROR GET:")
            print(e)
            await database.close()
            return None

class Json:

    def __init__(self, filepath):
        self.jsonfilepath = filepath
        with open(self.jsonfilepath, 'r') as jsoncontents:
            self.jsondict = dict(json.load(jsoncontents))
            jsoncontents.close()

    def __setitem__(self, instance, value):
        self.jsondict[instance] = value

    def __getitem__(self, item):
        try:
            return self.jsondict[item]
        except KeyError:
            self.jsondict.setdefault(item, {})
            return self.jsondict[item]

    def __missing__(self, key):
        print(key + " is missing")

    def save(self):
        with open(self.jsonfilepath, 'w+') as jsoncontents:
            jsoncontents.write(json.dumps(self.jsondict, indent=4, sort_keys=True))
            jsoncontents.close()


    def _json_load(self, json_file, char):
        jsonfile = open(json_file, char)
        jl = json.load(jsonfile)
        jsonfile.close()
        return jl

    def _json_write(self, json_file, char, data_list):
        jsonfile = open(json_file, char)
        jsonfile.write(json.dumps(data_list, indent=4, sort_keys=True))
        jsonfile.close()
