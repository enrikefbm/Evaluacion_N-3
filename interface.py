from ncclient import manager

# Datos del router (igual que antes)
router = {
    "host": "192.168.2.103",
    "port": 830,
    "username": "cisco",
    "password": "cisco123!",
    "hostkey_verify": False
}

# Configuración XML para la interfaz Loopback2
loopback_config = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>2</name>
        <ip>
          <address>
            <primary>
              <address>2.2.2.2</address>
              <mask>255.255.255.255</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>
"""

def create_loopback():
    try:
        with manager.connect(**router) as m:
            print("🔧 Creando interfaz Loopback2 con IP 2.2.2.2/32...")
            response = m.edit_config(target='running', config=loopback_config)
            print("✅ Interfaz Loopback2 creada.")
            print(response)
    except Exception as e:
        print("❌ Error al crear la interfaz Loopback2:", str(e))

if __name__ == "__main__":
    create_loopback()
