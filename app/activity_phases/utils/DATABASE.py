from sqlalchemy.engine import URL
from sqlalchemy import create_engine, text


# CONNECTION CREDENTIALS
DBServer = 'SQLSERVER'
DBName_EDM = 'EDM150'  # EVIDENCIAS EDM150
DBName_EDM_Iniciales = 'EDM3'  # EVIDENCIAS EDM150

DBName_EVIDENCIAS = 'EVIDENCIAS'  # EVIDENCIAS EDM150

User = 'edmadmin'
Password_EVIDENCIAS = r'EdmMansa_22#'
Password_EDM = r'EdmMansa#150'

server_EDM = '10.232.88.31'
server_EVIDENCIAS = '10.11.24.149'

Port = '1433'
tnsName = ''
ServiceName = ''
Sid = ''
Dsn = 'MANSA150'

# CREATING THE SQL SERVER CONNECTION URL
edm_connection_url = URL.create(
    "mssql+pyodbc",
    username=User,
    password=Password_EDM,
    host=server_EDM,
    port=Port,
    database=DBName_EDM,
    query={
        "driver": "ODBC Driver 17 for SQL Server",
    },
)


edm_iniciales_connection_url = URL.create(
    "mssql+pyodbc",
    username=User,
    password=Password_EDM,
    host=server_EDM,
    port=Port,
    database=DBName_EDM_Iniciales,
    query={
        "driver": "ODBC Driver 17 for SQL Server",
    },
)


evidencias_connection_url = URL.create(
    "mssql+pyodbc",
    username=User,
    password=Password_EVIDENCIAS,
    host=server_EVIDENCIAS,
    port=Port,
    database=DBName_EVIDENCIAS,
    query={
        "driver": "ODBC Driver 17 for SQL Server",
    },
)