from ncclient import manager
import xml.etree.ElementTree as ET

# Datos de conexión
router = {
    "host": "192.168.2.103",
    "port": 830,
    "username": "cisco",
    "password": "cisco123!",
    "hostkey_verify": False
}

# XML NETCONF para cambiar el hostname
hostname_config = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>ACOSTA-RAMIREZ</hostname>
  </native>
</config>
"""

def get_current_hostname(m):
    filter = """
    <filter>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname/>
      </native>
    </filter>
    """
    result = m.get_config(source='running', filter=filter)
    xml_data = result.data_xml
    root = ET.fromstring(xml_data)
    ns = {'xe': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native'}
    hostname_elem = root.find('.//xe:hostname', ns)
    return hostname_elem.text if hostname_elem is not None else None

def change_hostname():
    try:
        with manager.connect(**router) as m:
            print("🔄 Aplicando nuevo hostname...")
            m.edit_config(target='running', config=hostname_config)

            print("🔍 Verificando cambio de hostname...")
            current_hostname = get_current_hostname(m)

            if current_hostname == "ACOSTA-RAMIREZ":
                print("✅ Hostname cambiado y verificado: ACOSTA-RAMIREZ")
            else:
                print(f"❌ El hostname no coincide. Valor actual: {current_hostname}")

    except Exception as e:
        print("❌ Error durante la operación:", str(e))

if __name__ == "__main__":
    change_hostname()
