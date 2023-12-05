import subprocess


def run_subfinder(domain):
    """Ejecuta subfinder y captura los subdominios en la variable subdomains."""
    subfinder_cmd = f"subfinder -silent -d {domain}"

    try:
        # Ejecutar el comando y capturar la salida estándar
        subdomains = subprocess.check_output(subfinder_cmd, shell=True, text=True)
        # Separar los subdominios en una lista
        subdomains = subdomains.strip().split('\n')
        return subdomains
    except subprocess.CalledProcessError as e:
        # Manejar errores si ocurren
        print(f"Error al ejecutar subfinder: {e}")
        return []


def run_assetfinder(domain):
    """Ejecuta assetfinder y captura los subdominios en la variable subdomains."""
    assetfinder_cmd = f"assetfinder {domain}"

    try:
        # Ejecutar el comando y capturar la salida estándar
        subdomains = subprocess.check_output(assetfinder_cmd, shell=True, text=True)
        # Separar los subdominios en una lista
        subdomains = subdomains.strip().split('\n')
        return subdomains
    except subprocess.CalledProcessError as e:
        # Manejar errores si ocurren
        print(f"Error al ejecutar assetfinder: {e}")
        return []


def run_sublist3r(domain):
    sublist3r_command = f"sublist3r -d {domain}"
    pass

def run_dnsrecon(domain):
    pass

def run_theharvester(domain):
    pass