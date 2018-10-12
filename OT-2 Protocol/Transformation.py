#Author(s): Matt Burridge
#Last modified: 19:43, 12/10/18
#Python 3.6.4
#Please keep the author(s) attached to the code segment for traceability, if changes are made please append the authour list and modify the timestamp

#####################################################################################################################################
#The input from the code must be in list within a list, the sublist must contain the appropriate float type value and no whitespaces

from opentrons import labware, robot, instruments, modules 										# Import all opentrons API 
from sqlite3 import IntegrityError													# Import sqlite3 for custom container support


#####################################################################################################################################
#####################################################################################################################################
# LOADED LABWARE

TempDeck = modules.load('tempdeck', '6')												# Loads TempDeck
Tiprack10uL = labware.load('tiprack-10ul','11')												
Tiprack300uL = labware.load('opentrons-tiprack-300ul','9')
Compcells = labware.load('96-flat', '6', "compcells1", share=True)									# Competent Cells 
trash = robot.fixed_trash
DNA = labware.load('tube-rack-2ml', '10')												# Plasmid/DNA wanted to transform
SOB = labware.load('duran_100', '7')													# Recovery media, SOB strongly recommended for E. coli DH5a


#####################################################################################################################################
#####################################################################################################################################
# LOADED PIPETTES 
# CAN CHANGE IF NEEDED

P300 = instruments.P300_Single(
	mount='right',
    aspirate_flow_rate=200,
    dispense_flow_rate=200,
    tip_racks=[Tiprack300uL],
    trash_container=trash
)

P10 = instruments.P10_Single(
	mount='left',
	tip_racks=[Tiprack10uL],
	trash_container=trash
)

#####################################################################################################################################
#####################################################################################################################################
# COMPETENT CELL POSITION 
# This is in a 96 well plate format, each well corresponds to a 100 uL stock of comeptent cells. 
# To change, simply specify the wells you are using

Even_wells= [
	'B2', 'B4', 'B6', 'B8', 'B10', 'B12', 													
	'C1', 'C3', 'C5', 'C7', 'C9', 'C11',
	'D2', 'D4', 'D6', 'D8', 'D10', 'D12', 
	'E1', 'E3', 'E5', 'E7', 'E9', 'E11',
	'F2', 'F4', 'F6', 'F8', 'F10', 'F12'
]

	
#####################################################################################################################################
#####################################################################################################################################
# Preamble - variables, positional commands and TempDeck settings.

target_temperature1 = 4															# Cold Incubation 
target_temperature2 = 42														# Heat Shock
target_temperature3 = 37 														# Recovery incubation


TempDeck.set_temperature(target_temperature1)												# Sets temperature to 4
TempDeck.wait_for_temp()


target = Compcells(Even_wells)														# Specifies the target wells
SOB_wells = [well.top(1) for well in target()]												# Positional argument reducing contamination

#####################################################################################################################################
#####################################################################################################################################
# DNA TRANSFER STEP

P10.distribute(																# Presumes same plasmid for all cells 
	3, 
	DNA('A1'), 
	Compcells(Even_wells),
	blow_out=True,
	new_tip='always'
)

robot.pause()   															 # Change to P10.delay(minutes=40) if delay bug is fixed

robot.home()																 

#####################################################################################################################################
#####################################################################################################################################
# HEAT SHOCK STEP

TempDeck.set_temperature(target_temperature2)												# Heat to 42
TempDeck.wait_for_temp

P10.delay(seconds=60)															# Not 42 to take into account gradual warming and thermal conductivity

TempDeck.set_temperature(target_temperature1)												# Cool to 4
TempDeck.wait_for_temp

robot.pause()  																 # Change to P10.delay(minutes=5) if delay bug is fixed

#####################################################################################################################################
#####################################################################################################################################
# GROWTH MEDIA TRANSFER STEP
# Transfers 150 SOB into transformed aliquots and heats tempdeck to 37 to incubate indefinitely
# Can add a mix step for piece of mind, however successful transformation is seen without and it saves time/tips

P300.transfer(																
	150,
	SOB('A1'),
	SOB_wells,
	blow_out=True,
	new_tip='once'
)

TempDeck.set_temperature(target_temperature3)		



	


	
