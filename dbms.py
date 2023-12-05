import sqlite3


def create_database_if_not_exists(database_file):
    """Crea la base de datos si no existe."""
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Crear la tabla domains si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS domains (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def create_subdomains_table_if_not_exists(database_file, domain):
    database_file = "database.db"
    """Crea la tabla subdomains si no existe."""
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Crear la tabla subdomains si no existe
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS subdomains (
            id INTEGER PRIMARY KEY,
            subdomain TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def create_dns_records_table_if_not_exists(database_file):
    """Crea la tabla dns_records si no existe."""
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Crear la tabla dns_records si no existe
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS dns_records (
            id INTEGER PRIMARY KEY,
            domain_id INTEGER,
            ttl INTEGER NOT NULL,
            record_type TEXT NOT NULL,
            record_name TEXT NOT NULL,
            record_value TEXT NOT NULL,
            FOREIGN KEY (domain_id) REFERENCES domains (id)
        )
    ''')

    conn.commit()
    conn.close()


def save_subdomains_to_database(database_file, domain, subdomains):
    """Almacena los subdominios en la tabla subdomains de la base de datos SQLite."""
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Verificar si la tabla subdomains existe, si no, crearla
    create_subdomains_table_if_not_exists(database_file, domain)

    # Obtener el ID del dominio
    cursor.execute('SELECT id FROM domains WHERE name = ?', (domain,))
    domain_id = cursor.fetchone()

    if domain_id is None:
        # Si el dominio no existe en la tabla domains, ingresarlo
        cursor.execute('INSERT INTO domains (name) VALUES (?)', (domain,))
        domain_id = cursor.lastrowid
    else:
        domain_id = domain_id[0]

    # Insertar los subdominios en la tabla subdomains
    for subdomain in subdomains:
        cursor.execute(f'INSERT INTO subdomains (subdomain) VALUES (?)', (subdomain,))

    conn.commit()
    conn.close()


def save_dns_records_to_database(database_file, domain, records):
    """Almacena los registros DNS en la tabla dns_records de la base de datos SQLite."""
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Verificar si la tabla dns_records existe, si no, crearla
    create_dns_records_table_if_not_exists(database_file)

    # Obtener el ID del dominio
    cursor.execute('SELECT id FROM domains WHERE name = ?', (domain,))
    domain_id = cursor.fetchone()

    if domain_id is None:
        # Si el dominio no existe en la tabla domains, ingresarlo
        cursor.execute('INSERT INTO domains (name) VALUES (?)', (domain,))
        domain_id = cursor.lastrowid
    else:
        domain_id = domain_id[0]

    # Insertar los registros DNS en la tabla dns_records
    for record in records:
        cursor.execute(f'''
            INSERT INTO dns_records (domain_id, ttl, record_type, record_name, record_value)
            VALUES (?, ?, ?, ?, ?)
        ''', (domain_id, record['TTL'], record['RecordType'], record['RecordName'], record['RecordValue']))

    conn.commit()
    conn.close()
