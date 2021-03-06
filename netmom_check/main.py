import re
import sys
from .utils import logger, shell, normalize_mac_address

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
        logger.debug("snmp results: %s"%results)
        return results

    def retreive_snmp_infos(self):
        mac_addresses = self._extract_from_snmpwalk("mac_address_table", "mac_address_regex")
        types = self._extract_from_snmpwalk("type_table", "type_regex")
        interface_indices = self._extract_from_snmpwalk("interface_index_table", "interface_index_regex")

        items = {}
        for ip in mac_addresses.keys():
            obj = mac_addresses[ip]
            obj.update(types[ip])
            obj.update(interface_indices[ip])
            items[ip] = obj

        for ip, obj in items.items():
            output = shell(
                self.settings["snmpwalk_command"].format(
                    table=self.settings["port_table"].format(
                        **obj
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
        mac_addresses = shell(self.settings["query_command"].format(**self.settings), capture_stdout=True)
        return [
            normalize_mac_address(x)
            for x in mac_addresses.split("\n")[1:]
        ]

    def run(self):
        items = self.retreive_snmp_infos()
        for k, v in items.items():
            items[k]["mac_address"] = normalize_mac_address(v["mac_address"])

        logger.info("Values extracted from snmpwalks %s"%items)
        known_mac_addresses = self.retreive_known_mac_addresses()
        logger.info("Mac addresses found in the mysqldb %s"%known_mac_addresses)
        unknown_items = [
            x for x in items.values()
            if x["mac_address"] not in known_mac_addresses
        ]
        known_items = [
            x for x in items.values()
            if x["mac_address"] in known_mac_addresses
        ]

        logger.info("Mac addresses known:\n%s"%known_items)

        if self.settings["use_mac_addresses"]:
            metric = len(set(x["mac_address"] for x in unknown_items))
        else:
            metric = len(unknown_items)

        if metric >= self.settings["critical"]:
            status = "critical"
            exit_code = 2
        elif metric >= self.settings["warning"]:
            status = "warning"
            exit_code = 1
        else:
            status = "ok"
            exit_code = 0
    
        # print the summary
        print(self.settings["summary_format"].format(
            status=status.upper(),
            exit_code=exit_code,
            unknown_ip_count=len(unknown_items),
            known_ip_count=len(known_items),
            unknown_mac_count=len(set(x["mac_address"] for x in unknown_items)),
            known_mac_count=len(set(x["mac_address"] for x in known_items)),
        ))
        # Print the info for each ip
        if self.settings["verbose"] >= 1:
            for group in unknown_items:
                print(self.settings["output_format"].format(**group))

        sys.exit(exit_code)