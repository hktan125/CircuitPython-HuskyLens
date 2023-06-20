# find_largest_area.py
# Which ID has the largest area?

import board
import digitalio
import time
from circuitPyHuskyLib import HuskyLensLibrary

hl = HuskyLensLibrary('UART', TX=board.GP8, RX=board.GP9)
hl.algorithm("ALGORITHM_COLOR_RECOGNITION") # Redirect to Color Recognition Function
#hl.algorithm("ALGORITHM_FACE_RECOGNITION") # Redirect to Face Recognition Function

# Forget button
forget = digitalio.DigitalInOut(board.GP20)
forget.direction = digitalio.Direction.INPUT

def get_area(result):
    return result.ID, result.width * result.height

def get_max_area(list_of_id_area):
    # Sort the list_of_id_area based on the ID
    sorted_list = sorted(list_of_id_area, key=lambda x: x[0])

    # Create a dictionary to store the grouped data
    grouped_data = {}

    # Iterate over the sorted list and group the data by the ID
    for item in sorted_list:
        id = item[0]
        area = item[1]
        
        if id not in grouped_data:
            grouped_data[id] = []
        
        grouped_data[id].append(area)

    # Find the maximum area and corresponding ID
    max_area = 0
    max_id = None

    for id, areas in grouped_data.items():
        max_area_in_group = max(areas)
        
        if max_area_in_group > max_area:
            max_area = max_area_in_group
            max_id = id

    # Print the maximum area and corresponding ID
    return max_id, max_area

while True:
    if forget.value == False:
        hl.forget()
        
    results = hl.learnedBlocks() # Only get learned results
    
    if results: # if result not empty
        all_id = list(set([result.ID for result in results])) # Get distinct ID on the screen
        all_id.sort()
        print(f"All Color ID: {all_id}")
        
        area_list = list(map(get_area, results)) # Calculate area for each result
        print(f"(ID, Area): {area_list}")
        
        max_id, max_area = get_max_area(area_list)
        
        print(f"ID: {max_id}, Area: {max_area}")
        
    time.sleep(0.5)
