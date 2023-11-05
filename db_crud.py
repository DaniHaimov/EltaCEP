import psycopg2


class EventsCRUD:
    def __init__(self, host, port, dbname, user, password):
        self.__conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        self.__cursor = self.__conn.cursor()
        self.__table_name = 'events'
        self.__create_table_if_not_exists()

    def __create_table_if_not_exists(self):
        # Check if the table exists, and if not, create it with columns based on dictionary keys
        self.__cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.__table_name} '
                              f'(event_id SERIAL PRIMARY KEY, '
                              f'device VARCHAR(255) NOT NULL, '
                              f'sensor_type VARCHAR(255) NOT NULL, '
                              f'sensor_value VARCHAR(255) NOT NULL, '
                              f'created_at TIMESTAMP DEFAULT current_timestamp);')
        self.__conn.commit()

    def create_event(self, event_data):
        sql = (f'INSERT INTO {self.__table_name} '
               f'(device, sensor_type, sensor_value) '
               f'VALUES (%s, %s, %s)'
               f'RETURNING event_id')

        device = event_data['device']
        sensor_type = event_data['sensor_type']
        sensor_value = event_data['sensor_value']

        self.__cursor.execute(sql, (device, sensor_type, sensor_value))
        event_id = self.__cursor.fetchone()[0]
        self.__conn.commit()

        return {'event_id': event_id}

    def read_events(self):
        sql = f'SELECT * FROM {self.__table_name}'
        self.__cursor.execute(sql)
        events = self.__cursor.fetchall()
        return [dict(zip([desc[0] for desc in self.__cursor.description], event)) for event in events]

    def read_last_sensor_event(self, event_data):
        # return the last value that recorded by specific sensor
        sql = (f'SELECT sensor_value, created_at '
               f'FROM {self.__table_name} '
               f'WHERE device = %s AND sensor_type = %s '
               f'ORDER BY created_at DESC '
               f'LIMIT 1')
        device = event_data['device']
        sensor_type = event_data['sensor_type']
        self.__cursor.execute(sql, (device, sensor_type))
        fetched = self.__cursor.fetchone()
        if fetched is None:
            return None
        sensor_value = fetched[0]
        created_at = fetched[1]
        self.__conn.commit()

        return {'sensor_value': sensor_value, 'created_at': created_at}


class RulesCRUD:
    def __init__(self, host, port, dbname, user, password):
        self.__conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        self.__cursor = self.__conn.cursor()
        self.__table_name = 'rules'
        self.__create_table_if_not_exists()

    def __create_table_if_not_exists(self):

        # Check if the table exists, and if not, create it with columns based on dictionary keys
        self.__cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.__table_name} '
                              f'(rule_id SERIAL PRIMARY KEY, '
                              f'device VARCHAR(255) NOT NULL, '
                              f'sensor_type VARCHAR(255) NOT NULL, '
                              f'operator VARCHAR(8) NOT NULL, '
                              f'unusual_value VARCHAR(255) NOT NULL, '
                              f'rule_description VARCHAR(255) NOT NULL, '
                              f'compare_to_last_event BOOLEAN NOT NULL, '
                              f'created_at TIMESTAMP DEFAULT current_timestamp);')
        self.__conn.commit()

    def create_rule(self, rule_data):
        sql = (f'INSERT INTO {self.__table_name} '
               f'(device, sensor_type, operator, unusual_value, rule_description, compare_to_last_event) '
               f'VALUES (%s, %s, %s, %s, %s, %s) '
               f'RETURNING rule_id')
        device = rule_data['device']
        sensor_type = rule_data['sensor_type']
        operator = rule_data['operator']
        unusual_value = rule_data['unusual_value']
        rule_description = rule_data['rule_description']
        compare_to_last_event = rule_data.get('compare_to_last_event', False)

        self.__cursor.execute(sql, (device, sensor_type, operator, unusual_value, rule_description, compare_to_last_event))
        rule_id = self.__cursor.fetchone()[0]
        self.__conn.commit()

        return {"rule_id": rule_id}

    def read_rules(self):
        sql = f'SELECT * FROM {self.__table_name}'
        self.__cursor.execute(sql)
        events = self.__cursor.fetchall()
        return [dict(zip([desc[0] for desc in self.__cursor.description], event)) for event in events]

    def get_rule_description(self, rule_id):
        sql = f'SELECT rule_description FROM {self.__table_name} WHERE rule_id = %s'
        self.__cursor.execute(sql, (rule_id,))
        rule_description = self.__cursor.fetchone()[0]
        return {"rule_description": rule_description}

    def read_specific_sensor_rules(self, rule_data):
        sql = f'SELECT * FROM {self.__table_name} WHERE device LIKE %s AND sensor_type LIKE %s'
        device = rule_data['device']
        sensor_type = rule_data['sensor_type']
        self.__cursor.execute(sql, (device, sensor_type))
        rules = self.__cursor.fetchall()
        return [dict(zip([desc[0] for desc in self.__cursor.description], rule)) for rule in rules]

