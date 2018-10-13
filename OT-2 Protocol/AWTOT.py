#Author(s): Matt Burridge, Joshua Loh 
#Last modified: 11:37, 06/08/18
#Python 3.6.4
#Please keep the author(s) attached to the code segment for traceability, if changes are made please append the authour list and modify the timestamp

#####################################################################################################################################
#The input from the code must be in list within a list, the sublist must contain the appropriate float type value and no whitespaces


from opentrons import labware, instruments, robot      										# Import Opentrons Api 
from sqlite3 import IntegrityError															# Import sqlite IntegrityError for any custom containers 			
from opentrons.drivers.temp_deck import TempDeck											# Import TempDeck driver for usable temp deck 
		
tiprack_3001 = labware.load("opentrons-tiprack-300ul", slot='8')
tiprack_3002 = labware.load("opentrons-tiprack-300ul", slot='9')
tiprack_10 = labware.load("tiprack-10ul", slot='11')
Buffers1 = labware.load("Universals_Cold_Box", slot='2')										#Modified the buffers from both 1 to 1 and 2 
Buffers2 = labware.load("Universals_Cold_Box", slot='5')           								 # Import all labware and trash 
Buffers = labware.load("96-deep-well", slot ='3')
Compcells1 = labware.load('96-flat', slot='6')
Culture = labware.load('duran_100', slot='4')
DNA = labware.load('tube-rack-2ml', slot='10')
SOB = labware.load('duran_100', slot ='7')


trash = robot.fixed_trash

P300 = instruments.P300_Single(																# Import pipette types, P300 or P10 
	mount='right',																			# If using different pipette tips, modify float 
	aspirate_flow_rate=200,																	# and pipette commands in command block 
	dispense_flow_rate=200,																	# Assign tiprack and trash, make sure aspirate/dispense speeds
	tip_racks=[tiprack_3001, tiprack_3002],																# are suitable for reagent viscosity
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

																
Even_wells= [
	'B2', 'B4', 'B6', 'B8', 'B10', 															# Specify the target wells that you want to have bacterial aliquots in 
	'C1', 'C3', 'C5', 'C7', 'C9',
	'D2', 'D4', 'D6', 'D8', 'D10', 
	'E1', 'E3', 'E5', 'E7', 'E9',
	'F2', 'F4', 'F6', 'F8', 'F10'
]

Buffers_positions = Buffers.wells('A1', length=25)		

target_temperature = 4																# Specified temperatures for cold incubated,
target_temperature1 = 4																		#  heat shock and recovery incubation 
target_temperature2 = 42
target_temperature3 = 37 									# first position in reagent_pos list
							
tempdeck = TempDeck()																		# Connects the Tempdeck module to OT-2 																
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
				Buffers(well_counter).top(0.5),
				blow_out=True,
				new_tip='never')
			P10.touch_tip(Buffers(well_counter))
			P10.blow_out(Buffers(well_counter))
		else: 
			P300.distribute(
				values, 
				Buffers1(source),
				Buffers(well_counter).top(0.5),
				blow_out=True,
				new_tip='never')
			P300.touch_tip(Buffers(well_counter))
			P300.blow_out(Buffers(well_counter))
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
				Buffers(well_counter).top(0.5),
				blow_out=True,
				rate=0.5,
				new_tip='never')
			P10.touch_tip(Buffers(well_counter))
			P10.blow_out(Buffers(well_counter))
		else: 
			P300.distribute(
				values, 
				Buffers2(source), 
				Buffers(well_counter).top(0.5),
				blow_out=True,
				rate=0.5,
				new_tip='never')
			P300.touch_tip(Buffers(well_counter))
			P300.blow_out(Buffers(well_counter))
	P300.drop_tip()																			# Drops tips at end of single reagent run to prevent contamination 
	P10.drop_tip()

#########################################################################################
#########################################################################################
# COMPETENT CELLS



if not robot.is_simulating():																# Cannot use while simulating,
	tempdeck.connect('/dev/ttyACM0')
	tempdeck.set_temperature(target_temperature)											# Sets the temperature to whats specified above



target1 = Compcells1(Even_wells)															# Where your cells are going 

robot.home()																				# turbulent airflow within the OT-2
robot.pause()
robot.comment("Make sure that centrifuge has been chilled down to 4*C and all buffers are on ice.")
robot.comment("All plates should be chilled at the beginning and culture should be incubated on ice for 15 minutes before start.")
robot.comment("Once at set temperature, insert culture into slot 6 and plate onto TempDeck, then resume!")
 
#bacterial culture																			# This is the first step of protocol, 200 uL bacterial culture at OD 0.4-0.6 
for i in range(1):																			# added to 96 well plate in specified wells 
	P300.pick_up_tip()
	P300.transfer(
		200,
		Culture('A1'),
		target1(),
		blow_out=True)	
	robot.comment("Time to centrifuge your cultures")										# Pause to allow time for bacteria to be pelleted via centrifuge
	robot.pause()
	
# Wash Aliquot
for i in range(1):																			# Wash step
	P300.pick_up_tip()																		# Supernatant is removed from each well to leave the pellet
	P300.transfer(
		200,
		target1(),
		Culture('A1').top(-27),
		blow_out=True)
	P300.drop_tip()

	P300.pick_up_tip()																		# Wash buffer is added to each individual well and mixing occurs
	P300.transfer(																			# to resuspend the pellet
		100,
		Buffers_positions,
		target1(),
		mix_after=(5, 100),
		new_tip='always')
	robot.comment("Time to incubate your cultures")											# Tempdeck recools and switches off while allowing time for centrifugation
	robot.comment("Time to centrifuge your cultures")										# of cultures 
	robot.pause()
														# Can be frozen or used immediately depending on your wash buffer 


#########################################################################################
#########################################################################################
# COMPETENT CELLS

																	# Specified temperatures for cold incubated,
target_temperature1 = 4																		#  heat shock and recovery incubation 
target_temperature2 = 42
target_temperature3 = 37 

													# Connects to and begins cooling 
tempdeck.set_temperature(target_temperature1)
	
target = Compcells1(Even_wells)
SOB_wells = [well.top(1) for well in target()]

robot.pause()
#Transfer DNA 
for i in range(1):																			# transfers plasmid DNA into competent cell aliquots 
	P10.distribute(																			# Presumes same plasmid for all cells 
	3, 
	DNA('A1'), 
	Compcells1(Even_wells),
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

robot.comment("Protocol Finished!")

