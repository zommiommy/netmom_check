import os
import json
import logging
import argparse
from uuid import uuid4
from .main import NetmomCheck
from .utils import logger, setup_logger, get_path

def client():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--settings", help="Path to the settings json", type=str, default="settings.json")
    parser.add_argument("-v", "--verbose", help="The verbosity level, 0 = Summary, 1 = Detailed, 2 = Info, 3 = Debug", type=int, choices=(0, 1, 2, 3))

    snmpwalk_settings = parser.add_argument_group('snmpwalk settings')
    snmpwalk_settings.add_argument("-C", "--community", help="Password for the walk", type=str)
    snmpwalk_settings.add_argument("-H", "--host", help="The host on which the walk will be executed", type=str)
    query_settings = parser.add_argument_group('query settings')
    query_settings.add_argument("-D", "--database", help="The mysql database to use", type=str)
    query_settings.add_argument("-Q", "--query", help="The query to use to extract the mac addresses", type=str)
    tresholds_settings = parser.add_argument_group('tresholds settings')
    tresholds_settings.add_argument("-w", "--warning", help="The warning threshold", type=int)
    tresholds_settings.add_argument("-c", "--critical", help="The critical threshold", type=int)
    tresholds_settings.add_argument("-m", "--use-mac-addresses", help="Use the number of uniques mac addresses instead of the number of Ips", action="store_true", default=False)

    args = vars(parser.parse_args())
    args = {k:v for k, v in args.items() if v is not None}
    
    settings_path = os.path.join(
        get_path(),
        args["settings"]
    )
    with open(settings_path, "r") as f:
        settings = json.load(f)

    # Override the settings default with the arguments values 
    settings.update(args)

    setup_logger(
        get_path(),
        None,
        uuid4(),
        log_level={
            0:logging.WARNING,
            1:logging.WARNING,
            2:logging.INFO,
            3:logging.DEBUG
        }[settings["verbose"]]
    )
    NetmomCheck(settings).run()
