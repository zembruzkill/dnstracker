import sqlite3

conn = sqlite3.connect('dnstracker.db')  # You can create a new database by changing the name within the quotes
c = conn.cursor() # The database will be saved in the location where your 'py' file is saved

# Create table - DNS QUERY
c.execute('''CREATE TABLE dns_query
             ([id] INTEGER PRIMARY KEY AUTOINCREMENT,
              [version_id] INT,
              [domain] NVARCHAR(20), 
              [query_type] NVARCHAR(5), 
              [query_name] NVARCHAR(20), 
              [ipv4_address] NVARCHAR(20), 
              [ipv6_address] NVARCHAR(30), 
              [as_number] NVARCHAR(20),
              [as_name] NVARCHAR(20), 
              [bgp_prefix] NVARCHAR(20), 
              [worker_id] NVARCHAR(20), 
              [created_at] date, 
              [updated_at] date
             )''')

# Create table - RUN VERSION
c.execute('''CREATE TABLE run_version
             ([id] INTEGER PRIMARY KEY AUTOINCREMENT,
              [start_at] DATE,
              [end_at] DATE,
              [created_at] date, 
              [updated_at] date
             )''')

                 
conn.commit()
