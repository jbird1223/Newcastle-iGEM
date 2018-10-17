#Author(s): 2018 Newcastel iGEM 
#Last modified: 19:18, 17/10/18
#Python 3.6.4
#Please keep the author(s) attached to the code segment for traceability, if changes are made please append the authour list and modify the timestamp

#####################################################################################################################################

from opentrons import instruments, labware, robot

#####################################################################################################################################
#####################################################################################################################################

tiprack_300= labware.load("opentrons-tiprack-300ul", slot='7') 
tiprack_10= labware.load("tiprack-10ul", slot='4') 
cold_box= labware.load('Universals_Cold_Box',slot='8')	
cold_box2= labware.load('Universals_Cold_Box',slot='9')	
rack=labware.load('96-PCR-flat', slot='5')
rack2=labware.load('96-PCR-flat', slot='6')
trash= robot.fixed_trash

#####################################################################################################################################
#####################################################################################################################################
robot.home()

sterile_broth = cold_box('C1')
sterile_broth2= cold_box2('C1')
sterile_broth3= cold_box('C3')
sterile_broth4= cold_box2('C3')
sterile_broth5= cold_box('C5')
sterile_broth6= cold_box2('C5')

water = cold_box('A1')
water2 = cold_box2('A1')

innoc_broth = cold_box('A3')
innoc_broth2 = cold_box2('A3')

anti_biotic = cold_box('A5')
anti_biotic2 = cold_box2('A5')

#####################################################################################################################################
#####################################################################################################################################
#--------------------------------------------fill sterile broth to 10ml and others to 7ml

P300= instruments.P300_Single(mount='right',
		aspirate_flow_rate=300,
		dispense_flow_rate=300,
		tip_racks=[tiprack_300],
		trash_container=trash
)

P10= instruments.P10_Single(mount='left',
		aspirate_flow_rate=10,
		dispense_flow_rate=10,
		tip_racks=[tiprack_10],
		trash_container=trash
)

#####################################################################################################################################
#####################################################################################################################################

perimeter= [
			'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9','A10', 'A11', 'A12',
			'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9','H10', 'H11', 'H12',
			'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'B12', 'C12', 'D12', 'E12', 'F12', 'G12'
			]

a=[ 
	'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11',
	'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11',
	'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11',
	'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11',
	'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11',
	'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11',
	]

b=[
	20, 20, 20, 20, 19, 19, 19, 19, 18, 18,
	18, 18, 17, 17, 17, 17, 16, 16, 16, 16,
	15, 15, 15, 15, 14, 14, 14, 14, 13, 13,
	13, 13, 12, 12, 12, 12, 11, 11, 11, 11,
	10, 10, 10, 10, 9, 9, 9, 9, 8, 8,
	8, 8, 10, 10, 10, 10, 0, 0, 0, 0
]

c=[
	0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 
	2, 2, 3, 3, 3, 3, 4, 4, 4, 4,
	5, 5, 5, 5, 6, 6, 6, 6, 7, 7,
	7, 7, 8, 8, 8, 8, 9, 9, 9, 9,
	10, 10, 10, 10, 11, 11, 11, 11, 12, 12,
	12, 12, 0, 0, 0, 0, 0, 0, 0, 0
	]

d=[
	10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
	10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
	10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
	10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
	10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
	10, 10, 0, 0, 0, 0, 0, 0, 0, 0
	]	

#####################################################################################################################################
#####################################################################################################################################
#-------------------------------------------------------

P300.transfer(
	200,
	sterile_broth,
	rack.wells(perimeter),
	blow_out=True
	)

#------------------------------------------------------- second perimeter

P300.transfer(
	200,
	sterile_broth2,
	rack2.wells(perimeter),
	blow_out=True
	)
#-------------------------------------------------------

P300.transfer(
	170,
	sterile_broth3,
	rack.rows['B'][1:11],
	blow_out=True
	)

P300.transfer(
	170,
	sterile_broth3,
	rack.rows['C'][1:11],
	blow_out=True
	)

P300.transfer(
	170,
	sterile_broth3,
	rack.rows['D'][1:11],
	blow_out=True
	)

P300.transfer(
	170,
	sterile_broth4,
	rack.rows['E'][1:11],
	blow_out=True
	)



P300.transfer(
	170,
	sterile_broth4,
	rack.rows['F'][1:11],
	blow_out=True
	)



P300.transfer(
	170,
	sterile_broth4,
	rack.rows['G'][1:3],
	blow_out=True
	)

	

P300.transfer(
	190,
	sterile_broth4,
	rack.rows['G'][3:7],
	blow_out=True
	)
	
P300.transfer(
	200,
	sterile_broth4,
	rack.rows['G'][7:11],
	blow_out=True
	)
#-------------------------------------------------------

P300.transfer(
	170,
	sterile_broth5,
	rack2.rows['B'][1:11],
	blow_out=True
	)

P300.transfer(
	170,
	sterile_broth5,
	rack2.rows['C'][1:11],
	blow_out=True
	)

P300.transfer(
	170,
	sterile_broth5,
	rack2.rows['D'][1:11],
	blow_out=True
	)

P300.transfer(
	170,
	sterile_broth6,
	rack2.rows['E'][1:11],
	blow_out=True
	)

P300.transfer(
	170,
	sterile_broth6,
	rack2.rows['F'][1:11],
	blow_out=True
	)

P300.transfer(
	170,
	sterile_broth6,
	rack2.rows['G'][1:3],
	blow_out=True
	)

P300.transfer(
	190,
	sterile_broth6,
	rack2.rows['G'][3:7],
	blow_out=True
	)

P300.transfer(
	200,
	sterile_broth6,
	rack2.rows['G'][7:11],
	blow_out=True
	)

#-----------------------------------------------

P10.transfer( 
	b,
	water,
	rack.wells(a),
	blow_out=True,
	new_tip='once'
	)	

		
P10.transfer( 
	b,
	water2,
	rack2.wells(a),
	blow_out=True,
	new_tip='once'
		)	

		

#-------------------------------------------------------

P10.transfer( 
	c,
	anti_biotic,
	rack.wells(a),
	blow_out=True,
	new_tip='once'
	)			

P10.transfer( 
	c,
	anti_biotic2,
	rack2.wells(a),
	blow_out=True,
	new_tip='once'
	)			

#-------------------------------------------------------

P10.transfer( 
	d,
	innoc_broth,
	rack.wells(a),
	blow_out=True,
	new_tip='once'
	)	

P10.transfer( 
	d,
	innoc_broth2,
	rack2.wells(a),
	blow_out=True,
	new_tip='once'
	)	
