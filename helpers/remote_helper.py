import json
import os

from helpers.serial_hw_helper import get_hw_id


def process_remote_accessS(logger, client, msg):
    m_decode = str(msg.payload.decode("UTF-8", "ignore"))
    data = json.loads(m_decode)
    hardware_id = int(data.get("HardWareID", 0))
    access = int(data.get("object", {}).get("Access", 0))
    if hardware_id == get_hw_id(logger):
        logger.info(f"The From portal HW is: {access}")
        logger.info(f"The From Local HW is: {get_hw_id(logger)}")
        logger.info(f"Session: {access}")
        if access == 0:
            os.popen('/home/pi/rmoteStop.sh')
            logger.info(f"Remote Access (VPN) Stopped")
        elif access == 1:
            payload = json.dumps(
                {
                    "HardWareID": int(get_hw_id(logger)),
                    "object": {
                        "ParameterName": "Remote",
                        "Value": "1111",
                        "AlarmID": "8888"
                    }
                }
            )
            client.publish('iot-data3', payload=payload, qos=1, retain=True)
            os.popen('/home/pi/rmoteStart.sh')
            logger.info(f"Remote Access (VPN) Started")
    else:
        logger.info("Access value not found in the JSON.")

