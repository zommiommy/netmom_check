import sys
import mysql.connector
from .utils import logger, shell

class NetmomCheck:

    def __init__(self, settings):
        self.settings = settings

    def _extract_from_snmpwalk(self, table_key, regex_key):
        """Return a list of dictionaries with keys "ip" and "mac_address"."""
        output = shell(
            self.settings["snmpwalk_command"].format(table=self.settings[table_key], **self.settings), 
            capture_stdout=True
        )
        results = {}
        for line in output.split("\n"):
            m = re.match(self.settings[regex_key], line)
            if m is not None:
                values = m.groupdict()
                results[values["ip"]] = values
        logger.info("snmp results: %s"%results)
        return results

    def retreive_snmp_infos(self):
        mac_addresses = self._extract_from_snmpwalk("mac_address_table", "mac_address_regex")
        types = self._extract_from_snmpwalk("type_table", "type_regex")
        interface_indices = self._extract_from_snmpwalk("interface_index_table", "interface_index_regex")

        items = {}
        for ip in mac_address.keys():
            obj = mac_address[ip]
            obj.update(types[ip])
            obj.update(interface_indices[ip])
            items[ip] = obj
        
        for ip, obj in items.items():
            output = shell(
                self.settings["snmpwalk_command"].format(
                    table=self.settings["port_table"].format(
                        obj["interface_index"]
                    ), 
                    **self.settings
                ), 
                capture_stdout=True
            )
            match = re.match(self.settings["port_regex"], output)
            # UPDATE THE OBJ VALUE IN ITEMS
            obj.update(match.groupdict())
        return items

        
    def retreive_known_mac_addresses(self):
        mydb = mysql.connector.connect(
            host=self.settings["mysql_url"],
            user=self.settings["user"],
            password=self.settings["password"],
            database=self.settings["mydatabase"]
        )
        cursor = mydb.cursor()
        cursor.execute(self.settings["query"])
        result = cursor.fetchall()
        cursor.close()
        mydb.close()
        # the result it's a list of tuples, the mac address MUST be the first result
        flattened = [x[0] for x in my_result]
        return flattened

    def run(self):
        items = self.retreive_snmp_infos()
        known_mac_addresses = self.retreive_known_mac_addresses()
        unknown_items = [
            x for x in items
            if x["mac_address"] not in known_mac_addresses
        ]

        for group in unknown_items:
            print(self.settings["output_format"].format(**group))

        if len(unknown_items) >= self.settings["critical"]:
            sys.exit(2)
        elif len(unknown_items) >= self.settings["warning"]:
            sys.exit(1)
        else:
            sys.exit(0)