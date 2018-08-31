#Author(s): Matt Burridge
#Last modified: 11:37, 06/08/18
#Python 3.6.4
#Please keep the author(s) attached to the code segment for traceability, if changes are made please append the authour list and modify the timestamp

#####################################################################################################################################
#The input from the code must be in list within a list, the sublist must contain the appropriate float type value and no whitespaces

from opentrons import labware, robot, instruments 											# Import all opentrons API 
from sqlite3 import IntegrityError															# Import sqlite3 for custom container support
from opentrons.drivers.temp_deck import TempDeck											# Import TempDeck driver for usable temp deck 


Tiprack10uL = labware.load('tiprack-10ul', slot ='11')										# Import all labware 
Tiprack200uL = labware.load('tiprack-200ul', slot ='9')
Compcells = labware.load('96-flat', slot='6')
trash = robot.fixed_trash
DNA = labware.load('tube-rack-2ml', slot='10')
SOB = labware.load('duran_100', slot ='7')
CAM_plate = labware.load('96-flat', slot='1')

P300 = instruments.P300_Single(
	mount='right',
    aspirate_flow_rate=200,
    dispense_flow_rate=200,
    tip_racks=[Tiprack200uL],
    trash_container=trash
)

P10 = instruments.P10_Single(
	mount='left',
	tip_racks=[Tiprack10uL],
	trash_container=trash
)
#########################################################################################
#########################################################################################

Even_wells= [
	'B2', 'B4', 'B6', 'B8', 'B10', 'B12', 													# Specify the target wells that you want to have bacterial aliquots in 
	'C1', 'C3', 'C5', 'C7', 'C9', 'C11',
	'D2', 'D4', 'D6', 'D8', 'D10', 'D12', 
	'E1', 'E3', 'E5', 'E7', 'E9', 'E11',
	'F2', 'F4', 'F6', 'F8', 'F10', 'F12'
]

	
#########################################################################################
#########################################################################################
	
tempdeck = TempDeck()																		# Specified temperatures for cold incubated,
target_temperature1 = 4																		#  heat shock and recovery incubation 
target_temperature2 = 42
target_temperature3 = 37 

if not robot.is_simulating():
	tempdeck.connect('/dev/ttyACM0')														# Connects to and begins cooling 
	tempdeck.set_temperature(target_temperature1)
	
target = Compcells(Even_wells)
SOB_wells = [well.top(1) for well in target()]

robot.pause()
#Transfer DNA 
for i in range(1):																			# transfers plasmid DNA into competent cell aliquots 
	P10.distribute(																			# Presumes same plasmid for all cells 
	3, 
	DNA('A1'), 
	Compcells(Even_wells),
	blow_out=True,
	new_tip='always'
)

robot.pause()
robot.home()																				# Heat shock and post cooling 
tempdeck.set_temperature(target_temperature2)
P10.delay(seconds=100)
tempdeck.set_temperature(target_temperature1)
robot.pause()

#Transfer Growth media 
for i in range(1):																			# transferring in growth media for recovery 
	P300.pick_up_tip(),
	P300.transfer(
		150,
		SOB('A1'),
		SOB_wells,
		blow_out=True,
		new_tip='once'
)
tempdeck.set_temperature(target_temperature3)												# Temperature for incubation 





	


	
