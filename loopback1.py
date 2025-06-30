import requests
from requests.auth import HTTPBasicAuth
import urllib3
import json

# Desactiva advertencias de certificados autofirmados
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Datos del router
router = {
    "host": "192.168.2.103",
    "user": "cisco",
    "password": "cisco123!"
}

# Encabezados RESTCONF
headers = {
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json"
}

# Payload JSON para crear Loopback1 con IP 1.1.1.1/32 y dejarla apagada
payload = {
    "ietf-interfaces:interface": {
        "name": "Loopback1",
        "type": "iana-if-type:softwareLoopback",
        "enabled": False,  # Apagada
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "1.1.1.1",
                    "netmask": "255.255.255.255"
                }
            ]
        }
    }
}

# URL RESTCONF para la interfaz Loopback1
url = f"https://{router['host']}/restconf/data/ietf-interfaces:interfaces/interface=Loopback1"

def create_loopback():
    response = requests.put(
        url,
        auth=HTTPBasicAuth(router["user"], router["password"]),
        headers=headers,
        data=json.dumps(payload),
        verify=False  # Solo en pruebas; ignora SSL
    )

    if response.status_code in [200, 201, 204]:
        print("✅ Interfaz Loopback1 creada y apagada.")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    create_loopback()
