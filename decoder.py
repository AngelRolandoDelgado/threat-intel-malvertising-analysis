# la biblioteca ipaddress permite convertir un número entero directamente a su representación en dirección IPv4 y viceversa
# The ipaddress library allows converting an integer directly into its IPv4 address representation
import ipaddress

# Decrypting/converting the integer-encoded IP to standard IPv4 format
# Decodificando/convirtiendo la IP codificada en entero al formato estándar IPv4
ip_integer = 392073681
malicious_ip = ipaddress.ip_address(ip_integer)
print(f"IP Maliciosa Decodificada: {malicious_ip}")  

# Resultado: 23.94.145.209
