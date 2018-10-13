#Author(s): Matt Burridge
#Last modified: 02:14, 13/10/18
#Python 3.6.4
#Please keep the author(s) attached to the code segment for traceability, if changes are made please append the authour list and modify the timestamp #

#####################################################################################################################################
#The input from the code must be in list within a list, the sublist must contain the appropriate float type value and no whitespaces
#####################################################################################################################################

from opentrons import labware, instruments, robot, modules									# Import all opentrons API 
from sqlite3 import IntegrityError															# Import sqlite3 for custom container support 

#####################################################################################################################################
#####################################################################################################################################
# LOADED LABWARE

TempDeck = modules.load('tempdeck', '6')													# Loads TempDeck
tiprack200_1 = labware.load('opentrons-tiprack-300ul', '9')									
Compcells1 = labware.load('96-flat', '6', "compcells1", share=True)
trash = robot.fixed_trash																	# Specify trash 
Culture = labware.load('duran_100', '4')													# Chilledflask_100 and duran_250 are custom containers 
Buffers = labware.load('96-deep-well', '3')  

#####################################################################################################################################
#####################################################################################################################################
# LOADED PIPETTES 
# CAN CHANGE IF NEEDED

P300 = instruments.P300_Single(																# Import Pipette, set aspiration/dispense rates and equip with rack 
    mount='right',
    aspirate_flow_rate=200,
    dispense_flow_rate=200,
    tip_racks=[tiprack200_1],
    trash_container=trash
)


#####################################################################################################################################
#####################################################################################################################################
# BELOW ARE VALUES THAT CAN BE CHANGED 

target_temperature = 4																		# Specifies TempDeck temperature, 4 degrees is best for this protocol 

Even_wells= [
	'B2', 'B4', 'B6', 'B8', 'B10', 															# Specify the target wells that you want to have bacterial aliquots in 
	'C1', 'C3', 'C5', 'C7', 'C9',
	'D2', 'D4', 'D6', 'D8', 'D10', 
	'E1', 'E3', 'E5', 'E7', 'E9',
	'F2', 'F4', 'F6', 'F8', 'F10'
]

Buffers_positions = Buffers.wells('A1', length=25)											# Specify the buffer positions, change length=25 to whatever the number
																							# of buffers you have, eg if 15 buffers length=15
#####################################################################################################################################
#####################################################################################################################################
# PREAMBLE
# IF WORKING WITH E. COLI, BELOW IS A OPTIMAL PROTOCOL THAT ONLY REQUIRES 1 WASH STEP 
# IF INVESTINGATING DIFFERENT INCUBATION TIMES, ALTER P300 DELAYS 
# IF WANTING TO TURN TEMPDECK ON CONSTANTLY, REMOVE ALL tempdeck.disengage() AND PLACE BEFORE
# FINAL ROBOT COMMENT
# TURBLENT AIRFLOW WITHIN THE OT-2, TRY TO MINIMISE WITH FAN SHIELD

target_temperature1 = 4																		# Cold Incubation 

TempDeck.set_temperature(target_temperature1)												# Sets temperature to 4
TempDeck.wait_for_temp()



target1 = Compcells1(Even_wells)															# Where your cells are going 

robot.home()																				
robot.comment("Make sure that centrifuge has been chilled down to 4*C and all buffers are on ice.")
robot.comment("All plates should be chilled at the beginning and culture should be incubated on ice for 15 minutes before start.")
robot.comment("If all prepared, press resume")
robot.pause()
 
#####################################################################################################################################
#####################################################################################################################################
#bacterial culture																			# This is the first step of protocol, 200 uL bacterial culture at OD 0.4-0.6 

P300.transfer(
	200,
	Culture('A1'),
	target1(),																				# Specified in preamble, where the aliquots go
	new_tip='once',
	blow_out=True)	
robot.comment("Time to centrifuge your cultures")											# Pause to allow time for bacteria to be pelleted via centrifuge
robot.pause()
robot.comment("Resume when cultures have been centrifuged")

#####################################################################################################################################
#####################################################################################################################################
# Wash Aliquot

P300.transfer(
	200,
	target1(),
	Culture('A1').top(-27),																	# Culture is now used as microbial waste to reduce space
	new_tip='once',																			# Dispenses -27 mm below top to prevent contamination via
	blow_out=True)																			# tip touching culture

P300.transfer(																			
	100,
	Buffers_positions,																		# Follows the positions as specified in preamble, goes through columns
	target1(),																				# Can change buffer_positions to any position if only using 1 buffer
	mix_after=(5, 100),
	new_tip='always')

robot.comment("!!!REMOVE CELLS FROM TEMPDECK, TEMPDECK WILL DISENGAGE WHEN RESUMED AND HEAT!!!")
robot.pause()
robot.comment("!!!REMOVE CELLS FROM TEMPDECK, TEMPDECK WILL DISENGAGE WHEN RESUMED AND HEAT!!!")

TempDeck.deactivate()																							
robot.comment("Protocol Finished")
