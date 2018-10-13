#################################################################
#Author(s): Matt Burridge
#Last modified: 02:30, 13/10/18
#Python 3.6.4
#Please keep the author(s) attached to the code segment for traceability, if changes are made please append the authour list and modify the timestamp
####################################################################################################################################################
######################################################################################################################################################

from opentrons import labware, instruments, robot      										                  # Import Opentrons Api 
from sqlite3 import IntegrityError															                            # Import error for any new containers 

#####################################################################################################################################################
#####################################################################################################################################################

tiprack_300 = labware.load("opentrons-tiprack-300ul", '11')									                # Can change positions
tiprack_300_2 = labware.load("opentrons-tiprack-300ul", '10')								                # This is 96 well not 24 falcon just for example
Test_Devices = labware.load("96-PCR-flat", '2')										
Test_Device_Plate = labware.load("96-PCR-flat", '3')              								 
trash = robot.fixed_trash

#####################################################################################################################################################
#####################################################################################################################################################

P300 = instruments.P300_Single(																                              # Import pipette types, P300 or P10 
	mount='right',																			                                      # If using different pipette tips, modify float 
	aspirate_flow_rate=200,																	                                  # and pipette commands in command block 
	dispense_flow_rate=200,																	                                  # Assign tiprack and trash, make sure aspirate/dispense speeds
	tip_racks=[tiprack_300],																                                  # are suitable for reagent viscosity
	trash_container=trash 
)

#####################################################################################################################################################
#####################################################################################################################################################
# Preamble 

Volume = 100																				                                        # Volume of device to be transfered to plate

# Positions

LB_CAM = Test_Devices('H1')																	                                # Location of LB_CAM stock

Cultures_Co1 = [
	'A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2']											                      # Location of colony 1 test device cultures as follows
																							                                              # neg/pos/1/2/3/4/5/6
Cultures_Co2 = [
	'D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2']											                      # Location of colony 2 test device cultures as follows
																							                                              # neg/pos/1/2/3/4/5/6											

# Destinations in 96 well plate of colony 1 devices
Neg_Co1 = Test_Device_Plate.wells('A1', to='D1')
Pos_Co1 =  Test_Device_Plate.wells('A2', to='D2')
TD1_Co1 = Test_Device_Plate.wells('A3', to='D3')
TD2_Co1 =  Test_Device_Plate.wells('A4', to='D4')
TD3_Co1 = Test_Device_Plate.wells('A5', to='D5')
TD4_Co1 =  Test_Device_Plate.wells('A6', to='D6')
TD5_Co1 = Test_Device_Plate.wells('A7', to='D7')
TD6_Co1 =  Test_Device_Plate.wells('A8', to='D8')

# Variable of destination list to make transfer command simple
Co1_Destinations = [Neg_Co1, Pos_Co1, TD1_Co1, 
	TD2_Co1, TD3_Co1, TD4_Co1,
	TD5_Co1, TD6_Co1]

# Destinations in 96 well plate of colony 2 devices
Neg_Co2 = Test_Device_Plate.wells('E1', to='H1')
Pos_Co2 =  Test_Device_Plate.wells('E2', to='H2')
TD1_Co2 = Test_Device_Plate.wells('E3', to='H3')
TD2_Co2 =  Test_Device_Plate.wells('E4', to='H4')
TD3_Co2 = Test_Device_Plate.wells('E5', to='H5')
TD4_Co2 =  Test_Device_Plate.wells('E6', to='H6')
TD5_Co2 = Test_Device_Plate.wells('E7', to='H7')
TD6_Co2 =  Test_Device_Plate.wells('E8', to='H8')

# Variable of destination list to make transfer command simple
Co2_Destinations = [Neg_Co2, Pos_Co2, TD1_Co2, 
	TD2_Co2, TD3_Co2, TD4_Co2,
	TD5_Co2, TD6_Co2]




#####################################################################################################################################################
#####################################################################################################################################################
# Step 1, Make a 1:10 dilution of O/N in LB+CAM 
	# Easier to do by hand 


#####################################################################################################################################################
#####################################################################################################################################################
# Step 2, Dilute the cultures further to target Abs600 of 0.02
	# Should be a final volume of 12 mL LB+CAM 
		# Easier to do by hand 
		

#####################################################################################################################################################
#####################################################################################################################################################
# Step 3, take 100 mL of diluted culture and pipette into plate 
																							                                        # zip allows for lists to be iterated together
for TD1, CTD1 in zip(Cultures_Co1,Co1_Destinations):										              # TD1 = Test Device cultures 1											
    P300.distribute(																		                              # CTD1 = Test Devices 100 mL aliquot destination for culture 1
        Volume,
        Test_Devices(TD1),
        CTD1,
        new_tip ='always') 
        
robot.comment("Finished Colony 1")

for TD2, CTD2 in zip(Cultures_Co2, Co2_Destinations):										              # TD2 = Test Device colony 2 
    P300.distribute(																		                              # CTD2 = Test Devices 100 mL aliquot destination for culture 2
        Volume,
        Test_Devices(TD2),
        CTD2,
        new_tip ='always')
    
robot.comment("Finished Colony 2")

P300.transfer(																				                                # Transfering the LB+CAM control 
    Volume,
    LB_CAM,
    Test_Device_Plate.cols(9))
robot.comment("Finished LB+CAM")

robot.pause()
robot.comment("Pausing")
    


#####################################################################################################################################################
# Step 4, take 500 mL of 6 hour sample and pipette into plate 
	# If buggy and step 3 is cycled through twice, delete this section 

for TD1, CTD1 in zip(Cultures_Co1,Co1_Destinations):
    P300.distribute(
        Volume,
        Test_Devices(TD1),
        CTD1,
        new_tip ='always') 
        
robot.comment("Finished Colony 1")

for TD2, CTD2 in zip(Cultures_Co2, Co2_Destinations):
    P300.distribute(
        Volume,
        Test_Devices(TD2),
        CTD2,
        new_tip ='always')
    
robot.comment("Finished Colony 2")

P300.transfer(
    Volume,
    LB_CAM,
    Test_Device_Plate.cols(9))
robot.comment("Finished LB+CAM")

robot.pause()
robot.comment("Pausing")
    

#####################################################################################################################################################
