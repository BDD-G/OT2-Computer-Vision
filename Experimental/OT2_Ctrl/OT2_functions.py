import requests
import json

HEADERS = {"opentrons-version": "3"}
ROBOT_IP = "10.199.253.141"
commands_url = ""  
pipette_id = "" 

def create_run():
    global commands_url
        runs_url = f"http://{ROBOT_IP}:31950/runs"
    print(f"Command:\n{runs_url}")

    r = requests.post(
	    url=runs_url,
	    headers=HEADERS
	)

    r_dict = json.loads(r.text)
    run_id = r_dict["data"]["id"]
    commands_url = f"{runs_url}/{run_id}/commands"
    print(f"Run ID:\n{run_id}")
    return run_id, commands_url


def load_equipment(equipment_type, equipment_name, *location):
    id_value = None 

     if equipment_type == 1:
        command_dict = {
            "data": {
                "commandType": "loadLabware",
                "params": {
                    "location": {"slotName": location}, 
                    "loadName": equipment_name,
                    "namespace": "opentrons",
                    "version": 1
                },
                "intent": "setup"
            }
        }
        command_payload = json.dumps(command_dict)
        print(f"Command:\n{command_payload}")

        r = requests.post(
	        url=commands_url,
	        headers=HEADERS,
	        params={"waitUntilComplete": True},
	        data=command_payload
	        )

        r_dict = json.loads(r.text)
    
        labware_id = r_dict["data"]["result"]["labwareId"]
        print(f"{labware_id} ID:\n{labware_id}\n")
        id_value = labware_id
        
        
    elif equipment_type == 0:
        global pipette_id
        command_dict = {
	        "data": {
		        "commandType": "loadPipette",
		        "params": {
			        "pipetteName": equipment_name,
			        "mount": "right"
		        },
		        "intent": "setup"
	        }
        }
        command_payload = json.dumps(command_dict)
        print(f"Command:\n{command_payload}")

        r = requests.post(
	        url=commands_url,
	        headers=HEADERS,
	        params={"waitUntilComplete": True},
	        data=command_payload
	        )

        r_dict = json.loads(r.text)

        pipette_id = r_dict["data"]["result"]["pipetteId"] 
        print(f"Pipette ID:\n{pipette_id}\n")
        id_value = pipette_id
    
    return id_value


def pick_up(tiprack_id, wellname = None, offset = None):
    default_wellname = "A1"
    wellname_value = wellname if wellname is not None else default_wellname
    
    default_offset = {"x": 0, "y": 0, "z": 0}
    offset_value = {"x": offset[0], "y": offset[1], "z": offset[2]} if offset is not None else default_offset
    
    # Pick up tip
    command_dict = {
        "data": {
            "commandType": "pickUpTip",
            "params": {
                "labwareId": tiprack_id,
                "wellName": wellname_value, 
                "wellLocation": {
                    "origin": "top", "offset": offset_value
                },
                "pipetteId": pipette_id
            },
            "intent": "setup"
        }
    }

    command_payload = json.dumps(command_dict)
    print(f"Command:\n{command_payload}\n")

    r = requests.post(
        url=commands_url,
        headers=HEADERS,
        data=command_payload
        )

    print(f"Response:\n{r}\n{r.text}\n")


def aspirate(reservoir_id, wellname = None, offset = None):
    default_wellname = "A1"
    wellname_value = wellname if wellname is not None else default_wellname
    
    default_offset = {"x": 0, "y": 0, "z": 0}
    offset_value = {"x": offset[0], "y": offset[1], "z": offset[2]} if offset is not None else default_offset
    # Aspirate
    command_dict = {
        "data": {
            "commandType": "aspirate",
            "params": {
                "labwareId": reservoir_id,
                "wellName": wellname_value,
                "wellLocation": {
                    "origin": "top", "offset": offset_value
                },
                "flowRate": 0.75,
                "volume": 50,
                "pipetteId": pipette_id
            },
            "intent": "setup"
        }
    }

    command_payload = json.dumps(command_dict)
    print(f"Command:\n{command_payload}\n")

    r = requests.post(
        url=commands_url,
        headers=HEADERS,
        data=command_payload
        )

    print(f"Response:\n{r}\n{r.text}\n")


def move(fake_plate_id, wellname = None, offset = None):
    default_wellname = "A1"
    wellname_value = wellname if wellname is not None else default_wellname
    
    default_offset = {"x": 0, "y": 0, "z": 0}
    offset_value = {"x": offset[0], "y": offset[1], "z": offset[2]} if offset is not None else default_offset
    
    # Move to well fake plate
    command_dict = {
        "data": {
            "commandType": "moveToWell",
            "params": {
                "labwareId": fake_plate_id,
                "wellName": wellname_value,
                "wellLocation": {
                    "origin": "top", "offset": offset_value
                },
                "pipetteId": pipette_id
            },
            "intent": "setup"
        }
    }

    command_payload = json.dumps(command_dict)
    print(f"Command:\n{command_payload}\n")

    r = requests.post(
        url=commands_url,
        headers=HEADERS,
        data=command_payload
        )

    print(f"Response:\n{r}\n{r.text}\n")        
    

def dispense(reservoir_id, wellname  = None, offset = None):
    default_wellname = "A1"
    wellname_value = wellname if wellname is not None else default_wellname
    
    default_offset = {"x": 0, "y": 0, "z": 0}
    offset_value = {"x": offset[0], "y": offset[1], "z": offset[2]} if offset is not None else default_offset
    
    # Dispense
    command_dict = {
        "data": {
            "commandType": "dispense",
            "params": {
                "labwareId": reservoir_id,
                "wellName": wellname_value,
                "wellLocation": {
                    "origin": "top", "offset": offset_value
                },
                "flowRate": 0.75,
                "volume": 50,
                "pipetteId": pipette_id
            },
            "intent": "setup"
        }
    }

    command_payload = json.dumps(command_dict)
    print(f"Command:\n{command_payload}\n")

    r = requests.post(
        url=commands_url,
        headers=HEADERS,
        data=command_payload
        )

    print(f"Response:\n{r}\n{r.text}\n")
    
    
def blowout(reservoir_id, wellname = None, offset = None, flowrate = None):
    default_wellname = "A1"
    wellname_value = wellname if wellname is not None else default_wellname
    
    default_offset = {"x": 0, "y": 0, "z": 0}
    offset_value = {"x": offset[0], "y": offset[1], "z": offset[2]} if offset is not None else default_offset
    
    default_flowrate = 1.23
    flowrate_value = flowrate if flowrate is not None else default_flowrate
    # Blowout
    command_dict = {
        "data": {
            "commandType": "blowout",
            "params": {
                "labwareId": reservoir_id,
                "wellName": wellname_value,
                "wellLocation": {
                    "origin": "top", "offset": offset_value
                },
                "flowRate": flowrate_value,
                "pipetteId": pipette_id
            },
            "intent": "setup"
        }
    }

    command_payload = json.dumps(command_dict)
    print(f"Command:\n{command_payload}\n")

    r = requests.post(
        url=commands_url,
        headers=HEADERS,
        data=command_payload
        )

    print(f"Response:\n{r}\n{r.text}\n")


def drop_tips(tiprack_id = None, wellname = None, offset = None):
    default_wellname = "A1"
    wellname_value = wellname if wellname is not None else default_wellname
    
    default_offset = {"x": 0, "y": 0, "z": 0}
    offset_value = {"x": offset[0], "y": offset[1], "z": offset[2]} if offset is not None else default_offset
    
    default_tiprack_id = "fixedTrash"
    tiprack_id_value = tiprack_id if tiprack_id is not None else default_tiprack_id
    
# Drop tip
    command_dict = {
        "data": {
            "commandType": "dropTip",
            "params": {
                "labwareId": tiprack_id_value,
                "wellName": wellname_value,
                "wellLocation": {
                    "origin": "top", "offset": offset_value
                },
                "pipetteId": pipette_id
            },
            "intent": "setup"
        }
    }
    command_payload = json.dumps(command_dict)
    print(f"Command:\n{command_payload}\n")

    r = requests.post(
        url=commands_url,
        headers=HEADERS,
        data=command_payload
        )

    print(f"Response:\n{r}\n{r.text}\n")
    

def home():
    home_url = f"http://{ROBOT_IP}:31950/robot/home"
    command_dict = {"target": "robot"}
    command_payload = json.dumps(command_dict)
    print(f"Command:\n{command_payload}")

    r = requests.post(
        url=home_url,
        headers=HEADERS,
        data=command_payload
        )

    print(f"Response:\n{r}\n{r.text}\n")
    

def light(state):
    lights_url = f"http://{ROBOT_IP}:31950/robot/lights"
    if state:
        lights_status = json.dumos({"on": True})
    else:
        lights_status = json.dumos({"on": False})
    
    #change light status
    r = requests.post(url=lights_url, headers=HEADERS, data=lights_status)
    print(f"Request status:\n{r}\n{r.text}")
    
    #get lights status
    r = requests.get(url=lights_url, headers=HEADERS)
    print(f"Request status:\n{r}\n{r.text}")