#Author(s): Matt Burridge
#Last modified: 22:50, 01/08/18
#Python 3.6.4
#Please keep the author(s) attached to the code segment for traceability, if changes are made please append the authour list and modify the timestamp

#####################################################################################################################################
#The input from the code must be in list within a list, the sublist must contain the appropriate float type value and no whitespaces


from opentrons import labware, instruments, robot											# Import all opentrons API 
from sqlite3 import IntegrityError															# Import sqlite3 for custom container support 
from opentrons.drivers.temp_deck import TempDeck											# Import TempDeck driver for usable temp deck 

tiprack200_1 = labware.load('tiprack-200ul', slot='1')										# Import labware
Compcells1 = labware.load('96-flat', slot='3')
tiprack200_2 = labware.load('tiprack-200ul', slot='2')
trash = robot.fixed_trash																	# Specify trash 
Culture = labware.load('chilledflask_100', slot='6')										# Chilledflask_100 and duran_250 are custom containers 
Buffers = labware.load('96-deep-well', slot ='5')  
Microbial_waste = labware.load('duran_250', slot='11')


P300 = instruments.P300_Single(																# Import Pipette, set aspiration/dispense rates and equip with rack 
    mount='right',
    aspirate_flow_rate=200,
    dispense_flow_rate=200,
    tip_racks=[tiprack200_1, tiprack200_2],
    trash_container=trash
)


# BELOW ARE VALUES THAT CAN BE CHANGED 
#########################################################################################
#########################################################################################

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
#########################################################################################	
#########################################################################################
# BELOW IS CODE FOR THE PROTOCOL 
# IF WORKING WITH E. COLI, BELOW IS A OPTIMAL PROTOCOL THAT ONLY REQUIRES 1 WASH STEP 
# IF INVESTINGATING DIFFERENT INCUBATION TIMES, ALTER P300 DELAYS 
# IF WANTING TO CHANGE TEMPDECK ON CONSTANTLY, REMOVE ALL tempdeck.disengage() AND PLACE BEFORE
# FINAL ROBOT COMMENT




tempdeck = TempDeck()																		# Connects the Tempdeck module to OT-2 
tempdeck.connect('/dev/ttyACM0')

if not robot.is_simulating():																# Cannot use while simulating,
	tempdeck.connect('/dev/ttyACM0')
	tempdeck.set_temperature(target_temperature)											# Sets the temperature to whats specified above



target1 = Compcells1(Even_wells)															# Where your cells are going 

robot.home()
P300.delay(minutes =5)																		# Cools tempdeck but switches off before liquid handling to prevent
tempdeck.disengage()																		# turbulent airflow within the OT-2
robot.pause()
robot.comment("Make sure that centrifuge has been chilled down to 4*C and all buffers are on ice.")
robot.comment("All plates should be chilled at the beginning and culture should be incubated on ice for 15 minutes before start.")
robot.comment("Once at set temperature, insert culture into slot 6 and plate onto TempDeck, then resume")

#bacterial culture																			# This is the first step of protocol, 200 uL bacterial culture at OD 0.4-0.6 
for i in range(1):																			# added to 96 well plate in specified wells 
	P300.pick_up_tip()
	P300.transfer(
		200,
		Culture('A1'),
		target1(),
		blow_out=True)	
	robot.comment("Time to centrifuge your cultures")										# Pause to allow time for bacteria to be pelleted via centrifuge
	tempdeck.set_temperature(target_temperature)											# Switches tempdeck back on to cool for next liquid handling before
	robot.home()																			# being turned off again 
	P300.delay(minutes =5)
	tempdeck.disengage()
	robot.pause()
	
# First Wash
for i in range(1):																			# Wash step
	P300.pick_up_tip()																		# Supernatant is removed from each well to leave the pellet
	P300.transfer(
		200,
		target1(),
		Microbial_waste('A1').top(-37))
	P300.drop_tip()
	
	P300.pick_up_tip()																		# Wash buffer is added to each individual well and mixing occurs
	P300.transfer(																			# to resuspend the pellet
		200,
		Buffers_positions,
		target1(),
		mix_after=(3, 100),
		new_tip='always')
	robot.comment("Time to incubate your cultures")
	P300.delay(minutes =35)
	tempdeck.set_temperature(target_temperature)											# Delay for ice incubation 
	robot.home()																			# Tempdeck recools and switches off while allowing time for centrifugation
	robot.comment("Time to centrifuge your cultures")										# of cultures 
	P300.delay(minutes =5)
	tempdeck.disengage()
	robot.pause()

#STOCK ALIQUOT 

for i in range(1):																			# Removes supernatant 
	P300.pick_up_tip()
	P300.transfer(
		200,
		target1(),
		Microbial_waste('A1').top(-37))
	P300.pick_up_tip()																		# Adds buffer again in smaller volume for storage 
	P300.transfer(																			# Will mix to resuspend the pellet 
		100,
		Buffers_positions,
		target1(),
		mix_after=(3, 70),
		new_tip='always',
		rate=0.5)																			# Can be frozen or used immediately depending on your wash buffer 
	
robot.comment("Protocol Finished")