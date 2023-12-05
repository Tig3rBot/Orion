import sys

from dns_records import *
from subdomains_enum import *
from dbms import *


def enum_dns_records(domain):
    return run_dig(domain)


def enum_subdomains(domain):
    # Obtener subdominios de subfinder y assetfinder
    print(f"Obteniendo subdominios de subfinder", end="... ")
    subdomains_subfinder = run_subfinder(domain)
    print(f"Listo")
    print(f"Obteniendo subdominios de assetfinder", end="...")
    subdomains_assetfinder = run_assetfinder(domain)
    print(f"Listo")

    # Unir las listas y eliminar duplicados
    print(f"Parseando resultados, eliminando duplicados y ordenando", end="...")
    all_subdomains = list(set(subdomains_subfinder + subdomains_assetfinder))

    # Ordenar alfabéticamente
    all_subdomains = sorted(all_subdomains)
    print("Listo")
    return all_subdomains


def main():
    # Verificar si se proporcionó el dominio como argumento
    if len(sys.argv) != 2:
        print("Por favor, proporcione el dominio como argumento. Ejemplo: python3 r3con.py example.com")
        sys.exit(1)

    # Obtener el dominio desde la línea de comandos
    domain = sys.argv[1]

    database_file = f"database.db"
    create_database_if_not_exists(database_file)

    dns_records = enum_dns_records(domain)
    save_dns_records_to_database(database_file, domain, dns_records)

    all_subdomains = enum_subdomains(domain)
    save_subdomains_to_database(database_file, domain, all_subdomains)


if __name__ == '__main__':
    main()
