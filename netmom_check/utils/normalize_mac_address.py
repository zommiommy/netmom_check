
def normalize_hex(hex_value):
    hex_value = hex_value.lower()
    if len(hex_value) == 0:
        hex_value = "00"
    if len(hex_value) == 1:
        hex_value = "0" + hex_value
    return hex_value

def normalize_mac_address(mac_address):
    return ":".join(
        normalize_hex(x)
        for x in mac_address.split(":")
    )