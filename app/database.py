from sqlalchemy.engine import URL
from sqlalchemy import create_engine, text
from app.api.queries import WELL_COMMON_NAMES_QUERY

# CONNECTION CREDENTIALS
DBServer = 'SQLSERVER'
DBName = 'EDM150'
User = 'edmadmin'
Password = r'EdmMansa#150'  #    EdmMansa23#   EdmMansa#150
Server = '10.232.88.31' #   10.11.24.149 10.232.88.31
Port = '1433'
tnsName = ''
ServiceName = ''
Sid = ''
Dsn = 'MANSA150'

# CREATING THE SQL SERVER CONNECTION URL
connection_url = URL.create(
    "mssql+pyodbc",
    username=User,
    password=Password,
    host=Server,
    port=Port,
    database=DBName,
    query={
        "driver": "ODBC Driver 17 for SQL Server",
    },
)
#engine = create_engine(connection_url)
# print('Module database', connection_url)

def get_well_common_names():
    engine = create_engine(connection_url)

    wellcommon_names = [(None, 'Well Common Name')]

    with engine.connect() as connection:
        # WELL_COMMON_NAMES_QUERY
        result_cursor = connection.execute(text(WELL_COMMON_NAMES_QUERY))
        ddbb_wellnames_result = result_cursor.fetchall()
        ddbb_wellnames_list = [tupla[0] for tupla in ddbb_wellnames_result if tupla[0]]
        # print(type(ddbb_wellnames_list))
        #print(ddbb_wellnames_list)

    wellcommon_names.extend(
        sorted([(wellname.strip(), wellname) for wellname in ddbb_wellnames_list], key=lambda variable: variable[0]))

    return wellcommon_names, ddbb_wellnames_list


