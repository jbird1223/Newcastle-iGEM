#Author(s): Matt Burridge, Joshua Loh 
#Last modified: 11:37, 06/08/18
#Python 3.6.4
#Please keep the author(s) attached to the code segment for traceability, if changes are made please append the authour list and modify the timestamp

#####################################################################################################################################
#The input from the code must be in list within a list, the sublist must contain the appropriate float type value and no whitespaces


from opentrons import labware, instruments, robot      										# Import Opentrons Api 
from sqlite3 import IntegrityError															# Import sqlite IntegrityError for any custom containers 			
		
tiprack_200 = labware.load("opentrons-tiprack-300ul", slot='8')
tiprack_10 = labware.load("tiprack-10ul", slot='11')
Buffers1 = labware.load("Universals_Cold_Box", slot='2')										#Modified the buffers from both 1 to 1 and 2 
Buffers2 = labware.load("Universals_Cold_Box", slot='5')           								 # Import all labware and trash 
well_buffers96 = labware.load("96-deep-well", slot ='3')
trash = robot.fixed_trash

P300 = instruments.P300_Single(																# Import pipette types, P300 or P10 
	mount='right',																			# If using different pipette tips, modify float 
	aspirate_flow_rate=200,																	# and pipette commands in command block 
	dispense_flow_rate=200,																	# Assign tiprack and trash, make sure aspirate/dispense speeds
	tip_racks=[tiprack_200],																# are suitable for reagent viscosity
	trash_container=trash 
)

P10 = instruments.P10_Single(
	mount='left',
	aspirate_flow_rate=5,
	dispense_flow_rate=5,
	tip_racks=[tiprack_10],
	trash_container=trash
)



#########################################################################################
#########################################################################################
reagents1 = [																				# Input volumes in list within a list must have no whitespaces
	[40,0,0,40,40,40,0,40,0,0,0,40,0,40,0,40,20,40,40,0,20,40,0,20,0],
	[40,7.5,7.5,40,7.5,7.5,7.5,7.5,40,40,23.75,7.5,7.5,7.5,40,40,23.75,40,23.75,7.5,7.5,40,40,40,40],
	[5,5,5,0,0,5,0,0,5,2.5,0,5,5,2.5,0,0,2.5,5,5,0,0,0,5,5,0],
	[40,20,0,0,40,0,40,0,40,0,40,40,40,40,40,20,20,0,0,0,0,40,0,40,0],
	[0,0,0,0,0,20,40,40,0,40,0,40,40,0,20,40,20,0,40,40,0,40,40,40,0],
	[0,40,0,40,20,40,40,0,40,0,0,0,0,40,0,0,20,0,40,40,0,40,20,40,40],
	[0,0,12,0,12,0,0,6,6,0,0,0,12,12,12,12,6,12,12,12,0,0,0,12,12],
	[100,0,100,50,0,100,100,100,0,0,100,0,50,100,0,100,50,0,0,0,0,0,100,100,100]
]

reagent_pos1 = ['A1','A3','A5','B2','B4','C1','C3','C5']									#MgCl2, CaCl2, KOAc, MnCl2, RbCl2, NiCl2, Hexamine, KCl											# Specify reagent positions, 1st list within list equates to 
																							# first position in reagent_pos list
reagents2 = [																				# Input volumes in list within a list must have no whitespaces
	[50,50,150,150,150,150,100,50,150,150,150,150,50,50,50,150,100,100,50,150,50,50,50,150,50],
	[25,50,0,0,50,50,0,50,0,50,50,0,50,0,0,0,25,50,0,25,0,50,0,50,50],
	[100,100,100,100,100,0,100,100,0,100,0,50,0,0,100,0,50,0,100,0,0,0,0,100,50],
	[100,227.5,125.5,80,80.5,87.5,72.5,106.5,219,117.5,136.25,167.5,245.5,208,238,98,162.75,253,189.25,225.5,422.5,200,245,0,158]
]

reagent_pos2 = ['A1','A3','A5','B2']	#DMSO, HEPES, PEG8000, water														# Specify reagent positions, 1st list within list equates to 

																				# first position in reagent_pos list
																							
#########################################################################################
#########################################################################################   
robot.home()



#No.1
for counter, reagent in enumerate(reagents1,0):												
																							# These objects are temporary and will only exist within this loop
	source		= reagent_pos1[counter]														# Counter is use to index an independent list (e.g. reagent_pos)
	P10list 	= [source]																	# This is then added to both list				
	P300list	= [source]


	P300.pick_up_tip()																		# Picks up pipette tip for both P10 and P300 to allow to alternate
	P10.pick_up_tip()														
	for well_counter, values in enumerate(reagent):											# Specifies the well position and the volume of reagent being 
		if values == float(0):
			pass
		elif values < float(30):																# transfered in
			P10.distribute(																	# If volume below 30, P10 used not p300, if over P300 used
				values, 
				Buffers1(source).top(-70), 
				well_buffers96(well_counter).top(0.5),
				blow_out=True,
				new_tip='never')
			P10.touch_tip(well_buffers96(well_counter))
			P10.blow_out(well_buffers96(well_counter))
		else: 
			P300.distribute(
				values, 
				Buffers1(source),
				well_buffers96(well_counter).top(0.5),
				blow_out=True,
				new_tip='never')
			P300.touch_tip(well_buffers96(well_counter))
			P300.blow_out(well_buffers96(well_counter))
	P300.drop_tip()																			# Drops tips at end of single reagent run to prevent contamination 
	P10.drop_tip()

#No.2
for counter, reagent in enumerate(reagents2,0):												
																							# These objects are temporary and will only exist within this loop
	source		= reagent_pos2[counter]														# Counter is use to index an independent list (e.g. reagent_pos)
	P10list 	= [source]																	# This is then added to both list				
	P300list	= [source]


	P300.pick_up_tip()																		# Picks up pipette tip for both P10 and P300 to allow to alternate
	P10.pick_up_tip()														
	for well_counter, values in enumerate(reagent):											# Specifies the well position and the volume of reagent being 
		if values == float(0):
			pass
		elif values < float(30):																# transfered in
			P10.distribute(																	# If volume below 30, P10 used not p300, if over P300 used
				values, 
				Buffers2(source).top(-70), 
				well_buffers96(well_counter).top(0.5),
				blow_out=True,
				rate=0.5,
				new_tip='never')
			P10.touch_tip(well_buffers96(well_counter))
			P10.blow_out(well_buffers96(well_counter))
		else: 
			P300.distribute(
				values, 
				Buffers2(source), 
				well_buffers96(well_counter).top(0.5),
				blow_out=True,
				rate=0.5,
				new_tip='never')
			P300.touch_tip(well_buffers96(well_counter))
			P300.blow_out(well_buffers96(well_counter))
	P300.drop_tip()																			# Drops tips at end of single reagent run to prevent contamination 
	P10.drop_tip()

robot.comment("Protocol finished")
