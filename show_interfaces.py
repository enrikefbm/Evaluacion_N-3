from genie.testbed import load
import difflib
from colorama import Fore, Style, init

init(autoreset=True)  # Inicializa colorama para colores automáticos

def load_file(filename):
    with open(filename) as f:
        return f.readlines()

def main():
    # Cargar testbed y conectar
    testbed = load("testbed.yaml")
    device = testbed.devices["router1"]
    device.connect(log_stdout=False, learn_hostname=True, init_exec_commands=[], init_config_commands=[])

    # Cargar archivo previo
    before_lines = load_file("ipv6_interfaces_output.txt")

    # Obtener la salida actual del dispositivo
    output_after = device.execute("show ipv6 interface brief")
    after_lines = output_after.splitlines(keepends=True)

    device.disconnect()

    # Mostrar diferencias de forma amigable con colores
    diff = difflib.unified_diff(before_lines, after_lines, fromfile="Antes (archivo)", tofile="Después (en vivo)")

    print("\nDiferencias entre salida antes (archivo) y después (en vivo):\n")

    for line in diff:
        if line.startswith('---') or line.startswith('+++') or line.startswith('@@'):
            # Líneas de metadatos en diff, las ponemos en cyan
            print(Fore.CYAN + line.strip())
        elif line.startswith('-'):
            # Líneas eliminadas (antes pero no ahora)
            print(Fore.RED + "Eliminado: " + line[1:].strip())
        elif line.startswith('+'):
            # Líneas agregadas (ahora pero no antes)
            print(Fore.GREEN + "Agregado: " + line[1:].strip())
        else:
            # Líneas sin cambio
            print("       " + line.strip())

if __name__ == "__main__":
    main()
