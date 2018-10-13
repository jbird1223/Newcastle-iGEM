#Author(s): Matt Burridge, Joshua Loh 
#Last modified: 19:34, 13/10/18
#Python 3.6.4
#Please keep the author(s) attached to the code segment for traceability, if changes are made please append the authour list and modify the timestamp

#####################################################################################################################################################
#####################################################################################################################################################
# The input from the code must be in list within a list, the sublist must contain the appropriate float type value and no whitespaces
# IMPORT


from opentrons import labware, instruments, robot      										# Import Opentrons Api 
from sqlite3 import IntegrityError															# Import sqlite IntegrityError for any custom containers 	

#####################################################################################################################################################
#####################################################################################################################################################		
# IMPORT ALL LABWARE 

tiprack_300 = labware.load("opentrons-tiprack-300ul", '1')								# Stock 1/2, stocks of concentrated reagent that are being used
tiprack_10 = labware.load("tiprack-10ul", '4')											# Universals_Cold_Box = custom container for 30 mL universal tubes
Stock1 = labware.load("Universals_Cold_Box", '2')										# Will have to create or change to labware that you own
Stock2 = labware.load("Universals_Cold_Box", '5')           							# Import all labware and trash 
#Stock3 = labware.load("Universals_Cold_Box", '8')										# Remove # if extra stock labware is needed
well_buffers96 = labware.load("96-deep-well", '3')											
trash = robot.fixed_trash

#####################################################################################################################################################
#####################################################################################################################################################
# IMPORT ALL PIPETTES
# REQUIRES A PIPETTE THAT REACHES 1 uL 

P300 = instruments.P300_Single(																# Import pipette types 
	mount='right',																			# If using different pipette tips, modify float 
	aspirate_flow_rate=300,																	# and pipette commands in command block (see below)
	dispense_flow_rate=300,																	# Assign tiprack and trash, make sure aspirate/dispense speeds
	tip_racks=[tiprack_300],																# are suitable for reagent viscosity (can be further altered below)
	trash_container=trash 
)

P10 = instruments.P10_Single(
	mount='left',
	aspirate_flow_rate=10,
	dispense_flow_rate=10,
	tip_racks=[tiprack_10],
	trash_container=trash
)

#####################################################################################################################################################
#####################################################################################################################################################

# IMPORTANT - DO NOT ASSIGN PIPETTE TIPS TO A PIPETTE THAT HAVE A SMALLER MAX VOLUME THAN PIPPET ie. P200 TIPS TO P300 PIPETTE 
# WILL CAUSE CONTAMINATION AND/OR DAMAGE 
# ALTER VALUES AND POSITIONS BELOW

#####################################################################################################################################################
#####################################################################################################################################################
# Example of preamble below:

# Input volumes in list within a list, must have no whitespaces
# First value = well A1, second value = well B1 etc...

# reagents1 = [																									
#	[40,7.5,40,40,7.5,40,7.5,40,7.5,40,7.5,40,0,40,0,40,20,40,40,0,20,40,0,20,0],
#	[40,7.5,7.5,40,7.5,7.5,7.5,7.5,40,40,23.75,7.5,7.5,7.5,40,40,23.75,40,23.75,7.5,7.5,40,40,40,40]
#]

# Input stock destinations 

#reagent_pos1 = ['A1','A3']	

# Well A1 will be assigned to first list within a list, so all of the first lists values will be assigned to that stock
# ie, if A1 = MgCl2, the list [40,7.5,40,40,7.5,40,7.5,40,7.5,40,7.5,40,0,40,0,40,20,40,40,0,20,40,0,20,0], will be MgCl2 volumes taken from stock


#####################################################################################################################################################
#####################################################################################################################################################
# PREAMBLE - INSERT VALUES IN uL BELOW
# If more stocks are needed, remove # from reagents 3 and pos3 and use them.  


reagents1 = [[,]]																								

reagent_pos1 = []																								
										
reagents2 = [[]]	

reagent_pos2 = []	

#reagents3 = [[]]	

#reagent_pos3 = []																						
																							
#####################################################################################################################################################
#####################################################################################################################################################  

# THE FOLLOWING ALLOWS FOR ALTERNATING PIPETTE USE AND THE USE OF UP TWO LABWARE CONTAINING STOCKS
# IF WORKING WITH HIGHLY VISCOUS LIQUIDS, LOWER THE rate=1 TO rate=0.5 FOR ACCURACY
# IF WORKING WITH PIPETTES OTHER THAN P10 AND P300, CHANGE THE FLOAT VALUE TO THE MINIMUM WORKING VOLUME 
# OF LARGEST PIPETTE, KEEP SMALLEST PIPETTE IN THE IF LOOP AND LARGEST PIPETTE IN THE ELIF LOOP
# IF USING DIFFERENT LABWARE MAY NEED TO ALTER TOP/BOTTOM DISTANCE  
# DO NOT NEED TO ALTER ANYTHING ELSE 

#####################################################################################################################################################
#####################################################################################################################################################
# STOCK LABWARE 1

robot.home()																				# Homes robot and prevents any pipette bugs 
for counter, reagent in enumerate(reagents1,0):												
																							# These objects are temporary and will only exist within this loop
	source		= reagent_pos1[counter]														# Counter is use to index an independent list (e.g. reagent_pos)
	P10list 	= [source]																	# This is then added to both list - used in testing 				
	P300list	= [source]


	P300.pick_up_tip()																		# Picks up pipette tip for both P10 and P300 to allow to alternate
	P10.pick_up_tip()														
	for well_counter, values in enumerate(reagent):											# Specifies the well position and the volume of reagent being 
		if values == float(0):																# If volume is 0, well is skipped 
			pass
		elif values < float(30):															
			P10.distribute(																	# If volume below 30, P10 used not p300, if over P300 used
				values, 
				Stock1(source), 
				well_buffers96(well_counter).top(0.5),										# Prevents submerging tip in solution, not completely sterile, but beneficial
				blow_out=True,																# Removes excess from tip
				rate=1,																		# How quick it aspirates/dispenses, lower (ie 0.5) if stock viscous
				new_tip='never')
			P10.touch_tip(well_buffers96(well_counter))										# Touches tip to remove any droplets
			P10.blow_out(well_buffers96(well_counter))
		else: 
			P300.distribute(
				values, 
				Stock1(source), 
				well_buffers96(well_counter).top(0.5),
				blow_out=True,
				rate=1,
				new_tip='never')
			P300.touch_tip(well_buffers96(well_counter))
			P300.blow_out(well_buffers96(well_counter))
	P300.drop_tip()																			
	P10.drop_tip()

#####################################################################################################################################################
#####################################################################################################################################################
# STOCK LABWARE 2

robot.home()
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
				Stock2(source), 
				well_buffers96(well_counter).top(0.5),
				blow_out=True,
				rate=1,
				new_tip='never')
			P10.touch_tip(well_buffers96(well_counter))
			P10.blow_out(well_buffers96(well_counter))
		else: 
			P300.distribute(
				values, 
				Stock2(source), 
				well_buffers96(well_counter).top(0.5),
				blow_out=True,
				rate=1,
				new_tip='never')
			P300.touch_tip(well_buffers96(well_counter))
			P300.blow_out(well_buffers96(well_counter))
	P300.drop_tip()																			# Drops tips at end of single reagent run to prevent contamination 
	P10.drop_tip()

#####################################################################################################################################################
#####################################################################################################################################################
# STOCK LABWARE 3 - remove ''' if needed '''
'''
robot.home()
for counter, reagent in enumerate(reagents3,0):												
																							# These objects are temporary and will only exist within this loop
	source		= reagent_pos3[counter]														# Counter is use to index an independent list (e.g. reagent_pos)
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
				Stock3(source), 
				well_buffers96(well_counter).top(0.5),
				blow_out=True,
				rate=1,
				new_tip='never')
			P10.touch_tip(well_buffers96(well_counter))
			P10.blow_out(well_buffers96(well_counter))
		else: 
			P300.distribute(
				values, 
				Stock3(source), 
				well_buffers96(well_counter).top(0.5),
				blow_out=True,
				rate=1,
				new_tip='never')
			P300.touch_tip(well_buffers96(well_counter))
			P300.blow_out(well_buffers96(well_counter))
	P300.drop_tip()																			# Drops tips at end of single reagent run to prevent contamination 
	P10.drop_tip()

'''
robot.comment("Protocol finished")
