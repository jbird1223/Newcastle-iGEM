#Author(s): Matt Burridge, Joshua Loh, Sam Went 
#Last modified: 19:18, 11/08/18
#Python 3.6.4
#Please keep the author(s) attached to the code segment for traceability, if changes are made please append the authour list and modify the timestamp

#####################################################################################################################################
#The input from the code must be in list within a list, the sublist must contain the appropriate float type value and no whitespaces


from opentrons import labware, instruments, robot      										# Import Opentrons Api 
from sqlite3 import IntegrityError												# Import sqlite IntegrityError for any custom containers 			
		
tiprack_200 = labware.load("opentrons-tiprack-300ul", slot='3')
tiprack_10 = labware.load("tiprack-10ul", slot='6')										# Universals_Cold_Box = custom container for 30 mL universal tubes
source_rack = labware.load("Falcon1_24", slot='1')		#Source wells								
dest_6rack = labware.load("Falcon50ml_Cold_Box1", slot='9')     #Destination wells							# Import all labware and trash 
dest_rack = labware.load("Falcon1_24", slot ='2')               #Destination wells
trash = robot.fixed_trash

P300 = instruments.P300_Single(									# Import pipette types 
	mount='right',										# If using different pipette tips, modify float 
	aspirate_flow_rate=300,									# and pipette commands in command block (see below)
	dispense_flow_rate=300,									# Assign tiprack and trash, make sure aspirate/dispense speeds
	tip_racks=[tiprack_200],									# are suitable for reagent viscosity (can be further altered below)
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
reagents1 = [
	[1000,500,1000,500,0,1000,1000,1000,1000,0,1000,0,1000,0,1000,0,0,0,0,1000,1000,0,0,0],						        #1 MgSO4
	[0,100,200,100,200,200,200,0,0,0,0,200,200,200,0,0,0,0,0,0,200,200,0,0],  								#2 amino Benzoic acid
	[0,75,150,75,150,150,0,0,150,0,0,150,150,0,150,0,150,150,150,0,150,0,0,150],  							        #3 Arginine 100
	[0,50,100,50,0,100,100,100,0,0,100,100,100,100,100,100,0,100,100,100,0,0,100,0], 							#4 Aspartate
	[0,50,100,50,100,100,100,0,100,100,0,0,0,0,100,100,100,0,0,100,0,0,100,0],   								#5 Calcium pantothenate	
	[0,100,0,100,0,200,200,200,0,200,200,0,200,0,0,200,200,0,0,0,0,200,0,200],  								#6 Citrate
	[100,550,1000,550,1000,100,1000,1000,100,1000,100,100,1000,100,100,100,100,100,1000,1000,1000,100,1000,1000], 			        #7 Glycerol
	[0,250,0,250,0,500,500,500,500,0,0,0,0,0,0,0,500,500,500,500,500,500,500,500],    							#8 Histidine
	[500,250,500,250,0,0,500,0,500,500,0,0,500,500,0,0,500,500,500,500,0,500,0,0],   							#9 K2HPO4	
	[0,750,1500,750,1500,0,0,1500,1500,0,1500,0,0,1500,0,1500,0,0,1500,1500,0,0,0,1500],  						        #10 KH2PO4
	[500,250,500,250,0,500,0,500,0,0,0,0,0,500,500,500,500,0,500,0,500,0,0,500],   							        #11 KSO4
	[0,250,0,250,500,0,500,500,0,0,0,500,0,500,500,0,500,0,500,500,0,500,0,0],   								#12 Leucine
	[0,250,500,250,0,0,0,500,500,500,500,500,0,0,500,0,0,0,500,0,500,500,500,0], 							        #13 Methionine
	[0,500,0,500,0,0,1000,1000,1000,0,0,1000,1000,1000,1000,0,1000,0,0,0,0,0,1000,1000],    						#14mops
	[0,50,0,50,100,0,100,0,100,100,100,0,100,100,100,100,100,0,100,0,100,100,0,0],    							#15Na EDTA
	[0,500,0,500,1000,1000,0,1000,1000,1000,1000,1000,0,1000,0,0,1000,1000,0,1000,1000,0,0,0],      					#16Na2HPO4
	[0,50,0,0,0,50,50,0,50,0,0,0,0,50,0,50,0,50,50,0,50,0,50,0],       									#17Trace metals
	[500,255,0,255,500,500,500,0,500,0,500,0,0,500,500,0,0,0,0,500,500,500,500,500],       							#18Thiamine HCl 100mg
	[0,0,100,0,0,0,0,100,0,100,0,100,100,0,0,100,100,100,100,0,0,0,0,0],    								#19Thiamine HCl 10mg
	[0,500,1000,500,0,1000,1000,0,1000,1000,0,1000,0,0,1000,1000,0,0,1000,1000,0,1000,0,1000],    						#20Tricine	
	[0,100,200,100,0,0,0,0,200,0,200,200,200,200,0,200,200,0,0,200,200,200,200,200],    							#21NH4Cl2
	[0,200,0,200,0,400,0,0,0,400,400,0,400,400,400,0,400,0,400,400,0,0,400,0]								#22NH4PO4
]
	
        
# Input volumes in list within a list, must have no whitespaces
#eg	[40,7.5,40,40,7.5,40,7.5,40,7.5,40,7.5,40,0,40,0,40,20,40,40,0,20,40,0,20,0],
#	[40,7.5,7.5,40,7.5,7.5,7.5,7.5,40,40,23.75,7.5,7.5,7.5,40,40,23.75,40,23.75,7.5,7.5,40,40,40,40]


reagent_pos1 = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3', 'D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2', 'F3', 'G1', 'G2', 'G3', 'H1', 'H2', 'H3']
#eg	['A1','A3']																		     # Specify reagent positions, 1st list within list equates to 
# list sequence A1 = MgCl2 stock, A3 = CaCL2 stock														     # first position in reagent_pos list
																							
reagents2 = [	
	[0,1000,1000,1000,1000,1000],			#2 MgSO4
	[200,0,200,0,0,200],				#3 amino Benzoic acid
	[0,0,0,150,150,0],				#4 Arginine 100
	[0,0,0,0,0,0],					#5 Aspartate
	[0,0,100,100,0,0],				#6 Calcium pantothenate
	[200,0,0,200,200,0],				#7 Citrate
	[1000,1000,100,100,1000,100],			#8 Glycerol
	[0,0,500,0,0,500],				#9 Histidine		
	[500,0,0,500,0,0],				#10 K2HPO4
	[1500,0,1500,1500,0,1500],			#11 KH2PO4
	[500,500,500,0,0,0],				#12 KSO4
	[0,500,500,500,500,0],				#13 Leucine
	[500,0,500,500,0,0],				#14 Methionine
	[1000,1000,0,1000,0,1000],			#15mops
	[0,100,0,0,0,100],				#16Na EDTA
	[500,500,0,0,0,0],				#17Na2HPO4
	[50,50,50,50,50,0],				#18Trace metals
	[500,0,0,0,500,0],				#19Thiamine HCl 100mg
	[0,100,100,100,0,100],				#20Thiamine HCl 10mg
	[1000,1000,0,0,1000,1000],			#21Tricine
	[0,200,200,0,200,0],				#22NH4Cl2
	[400,0,400,0,400,400]				#23NH4PO4																		# Input volumes in list within a list must have no whitespaces
]

#reagent_pos2 = [A1, A2, A3, B1, B2, B3]															     # Specify reagent positions, 1st list within list equates to 
																			     # first position in reagent_pos list
																							
#########################################################################################
#########################################################################################   

# THE FOLLOWING ALLOWS FOR ALTERNATING PIPETTE USE AND THE USE OF UP TWO LABWARE CONTAINING STOCKS
# IF WORKING WITH HIGHLY VISCOUS LIQUIDS, LOWER THE rate=1 TO rate=0.5 FOR ACCURACY
# IF WORKING WITH PIPETTES OTHER THAN P10 AND P300, CHANGE THE FLOAT VALUE TO THE MINIMUM WORKING VOLUME 
# OF LARGEST PIPETTE, KEEP SMALLEST PIPETTE IN THE IF LOOP AND LARGEST PIPETTE IN THE ELIF LOOP 
# DO NOT NEED TO ALTER ANYTHING ELSE 

robot.home()																		     # Homes robot and prevents any pipette bugs 

#No.1
for counter, reagent in enumerate(reagents1,0):												
									# These objects are temporary and will only exist within this loop
	source	= reagent_pos1[counter]					# Counter is use to index an independent list (e.g. reagent_pos)
	P10list 	= [source]					# This is then added to both list				
	P300list	= [source]


	P300.pick_up_tip()						# Picks up pipette tip for both P10 and P300 to allow to alternate
	P10.pick_up_tip()														
	for well_counter, values in enumerate(reagent):			# Specifies the well position and the volume of reagent being 
		if values == float(0):
			pass
		elif values < float(30):				# transfered in
			P10.distribute(					# If volume below 30, P10 used not p300, if over P300 used
				values, 
				source_rack(source), 
				dest_rack(well_counter).top(-40),
				blow_out=True,
				rate=1,
				new_tip='never')
		else: 
			P300.distribute(
				values, 
				source_rack(source), 
				dest_rack(well_counter).top(0.5),
				blow_out=True,
				rate=1,
				new_tip='never')
	P300.drop_tip()																											# Drops tips at end of single reagent run to prevent contamination 
	P10.drop_tip()
	
#No.2
for counter, reagent in enumerate(reagents2,0):												
																										# These objects are temporary and will only exist within this loop
	source		= reagent_pos1[counter]		            # Counter is use to index an independent list (e.g. reagent_pos)
	P10list 	= [source]				    # This is then added to both list				
	P300list	= [source]


	P300.pick_up_tip()					    # Picks up pipette tip for both P10 and P300 to allow to alternate
	P10.pick_up_tip()														
	for well_counter, values in enumerate(reagent):		    # Specifies the well position and the volume of reagent being 
		if values == float(0):
			pass
		elif values < float(30):			    #transfered in
			P10.distribute(			            # If volume below 30, P10 used not p300, if over P300 used
				values, 
source_rack(source), 
				dest_6rack(well_counter).top(-40),
				blow_out=True,
				rate=1,
				new_tip='never')
		else: 
			P300.distribute(
				values, 
				source_rack(source), 
				dest_6rack(well_counter).top(0.5),
				blow_out=True,
				rate=1,
				new_tip='never')
	P300.drop_tip()					            # Drops tips at end of single reagent run to prevent contamination 
	P10.drop_tip()
		
robot.comment("Protocol finished")

#End
