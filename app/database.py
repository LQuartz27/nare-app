from sqlalchemy.engine import URL
from sqlalchemy import create_engine


# CONNECTION CREDENTIALS
DBServer = 'SQLSERVER'
DBName = 'EDM150'
User = 'edmadmin'
Password = r'EdmMansa#150'  # VpvBvuA/cWvqeuy3QVAvRxJQg5fdHB6oBC3beYYd2gg=
Server = '10.232.88.31' # 10.11.24.150
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
        #         "authentication": "ActiveDirectoryIntegrated",
    },
)
#engine = create_engine(connection_url)
print('Module database', connection_url)




