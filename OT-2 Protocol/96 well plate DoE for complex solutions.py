#Author(s): Matt Burridge, Joshua Loh 
#Last modified: 17:29, 26/07/18
#Python 3.6.4
#Please keep the author(s) attached to the code segment for traceability, if changes are made please append the authour list and modify the timestamp

#####################################################################################################################################
#The input from the code must be in list within a list, the sublist must contain the appropriate float type value and no whitespaces


from opentrons import labware, instruments, robot      						# Import Opentrons Api 
from sqlite3 import IntegrityError								# Import sqlite IntegrityError for any custom containers 			
		
tiprack_200 = labware.load("opentrons-tiprack-300ul", slot='1')
tiprack_10 = labware.load("tiprack-10ul", slot='3')						# Universals_Cold_Box = custom container for 30 mL universal tubes
Stock1 = labware.load("Universals_Cold_Box", slot='10')										
Stock2 = labware.load("Universals_Cold_Box", slot='5')           				# Import all labware and trash 
well_buffers96 = labware.load("96-flat", slot ='2')
trash = robot.fixed_trash

P300 = instruments.P300_Single(									# Import pipette types 
	mount='right',										# If using different pipette tips, modify float 
	aspirate_flow_rate=300,									# and pipette commands in command block (see below)
	dispense_flow_rate=300,									# Assign tiprack and trash, make sure aspirate/dispense speeds
	tip_racks=[tiprack_200],								# are suitable for reagent viscosity (can be further altered below)
	trash_container=trash 
)

P10 = instruments.P10_Single(
	mount='left',
	aspirate_flow_rate=10,
	dispense_flow_rate=10,
	tip_racks=[tiprack_10],
	trash_container=trash
)

# IMPORTANT - DO NOT ASSIGN PIPETTE TIPS TO A PIPETTE THAT HAVE A SMALLER MAX VOLUME THAN PIPPET ie. P200 TIPS TO P300 PIPETTE 
# WILL CAUSE CONTAMINATION AND/OR DAMAGE 

# ALTER VALUES AND POSITIONS BELOW
#########################################################################################
#########################################################################################
reagents1 = [											# Input volumes in list within a list, must have no whitespaces
#eg	[40,7.5,40,40,7.5,40,7.5,40,7.5,40,7.5,40,0,40,0,40,20,40,40,0,20,40,0,20,0],
#	[40,7.5,7.5,40,7.5,7.5,7.5,7.5,40,40,23.75,7.5,7.5,7.5,40,40,23.75,40,23.75,7.5,7.5,40,40,40,40]
]

reagent_pos1 = [
#eg	'A1','A3'
]												# Specify reagent positions, 1st list within list equates to 
# list sequence A1 = MgCl2 stock, A3 = CaCL2 stock						# first position in reagent_pos list
																							
reagents2 = [											# Input volumes in list within a list must have no whitespaces
	[]
]

reagent_pos2 = []										# Specify reagent positions, 1st list within list equates to 
												# first position in reagent_pos list
																							
#########################################################################################
#########################################################################################   

# THE FOLLOWING ALLOWS FOR ALTERNATING PIPETTE USE AND THE USE OF UP TWO LABWARE CONTAINING STOCKS
# IF WORKING WITH HIGHLY VISCOUS LIQUIDS, LOWER THE rate=1 TO rate=0.5 FOR ACCURACY
# IF WORKING WITH PIPETTES OTHER THAN P10 AND P300, CHANGE THE FLOAT VALUE TO THE MINIMUM WORKING VOLUME 
# OF LARGEST PIPETTE, KEEP SMALLEST PIPETTE IN THE IF LOOP AND LARGEST PIPETTE IN THE ELIF LOOP 
# DO NOT NEED TO ALTER ANYTHING ELSE 

#No.1
for counter, reagent in enumerate(reagents1,0):												
												# These objects are temporary and will only exist within this loop
	source		= reagent_pos1[counter]							# Counter is use to index an independent list (e.g. reagent_pos)
	P10list 	= [source]								# This is then added to both list				
	P300list	= [source]


	P300.pick_up_tip()									# Picks up pipette tip for both P10 and P300 to allow to alternate
	P10.pick_up_tip()														
	for well_counter, values in enumerate(reagent):						# Specifies the well position and the volume of reagent being 
		if values < float(30):								# transfered in
			P10.distribute(								# If volume below 30, P10 used not p300, if over P300 used
				values, 
				Stock1(source), 
				well_buffers96(well_counter).top(0.5),
				blow_out=True,
				rate=1,
				new_tip='never')
		elif values > float(30): 
			P300.distribute(
				values, 
				Stock1(source), 
				well_buffers96(well_counter).top(0.5),
				blow_out=True,
				rate=1,
				new_tip='never')
	P300.drop_tip()										# Drops tips at end of single reagent run to prevent contamination 
	P10.drop_tip()

#No.2
for counter, reagent in enumerate(reagents2,0):												
												# These objects are temporary and will only exist within this loop
	source		= reagent_pos2[counter]							# Counter is use to index an independent list (e.g. reagent_pos)
	P10list 	= [source]								# This is then added to both list				
	P300list	= [source]


	P300.pick_up_tip()									# Picks up pipette tip for both P10 and P300 to allow to alternate
	P10.pick_up_tip()														
	for well_counter, values in enumerate(reagent):						# Specifies the well position and the volume of reagent being 
		if values < float(30):								# transfered in
			P10.distribute(								# If volume below 30, P10 used not p300, if over P300 used
				values, 
				Stock2(source), 
				well_buffers96(well_counter).top(0.5),
				blow_out=True,
				rate=1,
				new_tip='never')
		elif values > float(30): 
			P300.distribute(
				values, 
				Stock2(source), 
				well_buffers96(well_counter).top(0.5),
				blow_out=True,
				rate=1,
				new_tip='never')
	P300.drop_tip()										# Drops tips at end of single reagent run to prevent contamination 
	P10.drop_tip()
