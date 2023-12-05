import subprocess


def run_dig(domain):
    """Ejecuta el comando dig y guarda los resultados en una tabla de la base de datos."""
    dig_cmd = f"dig any {domain} +noall +answer"

    try:
        # Ejecutar el comando dig y capturar la salida estándar
        dig_results = subprocess.check_output(dig_cmd, shell=True, text=True)
        # Parsear los resultados de dig
        parsed_results = parse_dig_results(dig_results)
        return parsed_results
    except subprocess.CalledProcessError as e:
        # Manejar errores si ocurren
        print(f"Error al ejecutar dig: {e}")
        return []


def parse_dig_results(results):
    """Parsea los resultados del comando dig any +noall +answer y devuelve una lista de diccionarios con la
    información."""
    parsed_results = []
    for line in results.split('\n'):
        parts = line.split()
        if len(parts) >= 5:
            ttl = parts[1]
            record_type = parts[3]
            record_name = parts[0]
            record_value = ' '.join(parts[4:])
            parsed_results.append({
                'TTL': ttl,
                'RecordType': record_type,
                'RecordName': record_name,
                'RecordValue': record_value
            })
    return parsed_results
