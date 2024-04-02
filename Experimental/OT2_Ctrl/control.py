import OT2_functions as OT
import cv2
import time
import detection_functions as DF

output_folder = "/home/pi/Desktop/object_detection/image"

TIP_RACK = "opentrons_96_tiprack_300ul"
RESERVOIR = "nest_96_wellplate_200ul_flat"
PIPETTE = "p300_multi"
FAKE_PLATE = "agilent_1_reservoir_290ml"

run_id, commands_url = OT.create_run
tiprack_id = OT.load_equipment(0,TIP_RACK,11)
reservoir_id = OT.load_equipment(1,RESERVOIR,4)
pipette_id = OT.load_equipment(1,PIPETTE,0)
fake_plate_id = OT.load_equipment(1,FAKE_PLATE,6)

OT.pick_up(tiprack_id)
OT.aspirate(reservoir_id)
OT.move(fake_plate_id, 50)
time.sleep(2)

DF.take_photo("test.jpg",output_folder)

time.sleep(2)

OT.dispense(reservoir_id)
OT.blowout(reservoir_id)

OT.drop_tips(tiprack_id)

OT.home()
