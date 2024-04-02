import cv2
import os
from datetime import datetime
import time
import socket
import subprocess
import Helper
import pandas as pd

#class_counts, bounding_boxes, bounding_box_centers, liquid_height_percentages = process_predictions(predictions)
def process_predictions(predictions):
    #Initialize structures to hold counts, bounding box coordinates, center points, and liquid height percentages for each class
    class_counts = {'Tip': 0, 'Liquid': 0}
    bounding_boxes = {'Tip': [], 'Liquid': []}
    bounding_box_centers = {'Tip': [], 'Liquid': []}
    liquid_height_percentages = {'Liquid': []}

    #Process each prediction object in the list
    for image_prediction in predictions._images_prediction_lst:
        #Access the prediction details
        prediction = image_prediction.prediction
        labels = prediction.labels  #Class labels for detected objects
        bboxes = prediction.bboxes_xyxy  #Bounding box coordinates

        #Iterate through each detection
        for label, bbox in zip(labels, bboxes):
            class_name = image_prediction.class_names[int(label)]
            #Update counts
            class_counts[class_name] += 1
            #Append the bounding box coordinates
            bbox_list = bbox.tolist()  #Converting numpy array to list for easier handling
            bounding_boxes[class_name].append(bbox_list)
            
            #Calculate and append the center point of the bounding box
            x_center = (bbox[0] + bbox[2]) / 2
            y_center = (bbox[1] + bbox[3]) / 2
            center_point = [x_center.item(), y_center.item()]  #Convert numpy float to Python float for easier handling
            bounding_box_centers[class_name].append(center_point)
            
            #Calculate the height of the liquid box compared to the tip box
            if class_name == 'Liquid':
                tip_box = bounding_boxes['Tip'][-1]  #Get the corresponding tip box
                liquid_height = bbox[3] - bbox[1]
                tip_height = tip_box[3] - tip_box[1]
                percentage = (liquid_height / tip_height) * 100
                liquid_height_percentages['Liquid'].append(percentage)

    #Sort the bounding box center values based on horizontal positions
    bounding_box_centers['Tip'] = sorted(bounding_box_centers['Tip'], key=lambda x: x[0])
    bounding_box_centers['Liquid'] = sorted(bounding_box_centers['Liquid'], key=lambda x: x[0])

    #Return the results including liquid height percentages and sorted center points
    return class_counts, bounding_boxes, bounding_box_centers, liquid_height_percentages


#Print the results including liquid height percentages and sorted center points
print("Detection counts:", class_counts)
print("Bounding boxes:", bounding_boxes)
print("Bounding box centers sorted by horizontal position:", bounding_box_centers)
print("Liquid Height Percentages:", liquid_height_percentages)'''




####################################################################################################

#tip_presence, missing_tip_positions = find_missing_tips(bounding_box_centers)


def find_missing_tips(bounding_box_centers):
    #Assuming there are 8 tips expected
    expected_tip_count = 8

    #Get the sorted center points of detected tips
    detected_tip_centers = bounding_box_centers['Tip']

    #Initialize a list to store whether each tip is present (1) or missing (0)
    tip_presence = [1] * expected_tip_count
    missing_tip_positions = []  #List to store the positions of missing tips

    #Check if any tips are missing
    if len(detected_tip_centers) != expected_tip_count:
        #Calculate the expected horizontal distance between tips
        expected_horizontal_distance = (detected_tip_centers[-1][0] - detected_tip_centers[0][0]) / (expected_tip_count - 1)

        #Iterate through the expected tips
        for i in range(expected_tip_count):
            expected_center_x = detected_tip_centers[0][0] + i * expected_horizontal_distance
            found = False

            #Check if there is a detected tip close to the expected position
            for detected_center in detected_tip_centers:
                if abs(detected_center[0] - expected_center_x) <= expected_horizontal_distance / 2:
                    found = True
                    break

            if not found:
                #If no detected tip is close to the expected position, mark it as missing
                tip_presence[i] = 0
                missing_tip_positions.append(i + 1)  #Append the position of the missing tip

    return tip_presence, missing_tip_positions

'''# 'bounding_box_centers' contains the sorted center points of detected tips
tip_presence, missing_tip_positions = find_missing_tips(bounding_box_centers)

#Print the presence or absence of each tip and the positions of missing tips
print("Tip Presence:", tip_presence)
print("Missing Tip Positions:", missing_tip_positions)'''

##########################################################################################################
#capture_hd_image_with_lock(project_name="default_project")
def capture_hd_image_with_lock(project_name="default_project"):
    #Set up the project folder
    project_folder = os.path.join(os.path.abspath('.'), project_name)
    os.makedirs(project_folder, exist_ok=True)
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    image_name = f'{project_name}_{current_time}_hd.jpg'
    image_path = os.path.join(project_folder, image_name)

    #Initialize the camera
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  #'0' is typically the default camera ID. Adjust if necessary.

    #Set camera parameters
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  #Set the width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  #Set the height
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))  #Set the codec
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)  #Turn off autofocus
    
    #Set focus value for closer objects (adjust as needed)
    focus_value = 50.0  #Change this value to your desired focus setting
    cap.set(cv2.CAP_PROP_FOCUS, focus_value)  #Set the focus property

    #Capture the image
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(image_path, frame)  #Save the image to the specified path
        print(f'HD Image captured with locked focus: {image_name}')
    else:
        print("Failed to capture image")

    #Release the camera
    cap.release()

    return image_path


#####################################################################################################33
import os
from datetime import datetime

def save_predictions(predictions, output_folder="output_predictions"):
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    predictions.save(output_folder=output_folder) #Save the file with the original name "pred_0.jpg" 
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")  #current datetime
    original_file_path = os.path.join(output_folder, "pred_0.jpg") #Rename the file to include the timestamp
    new_file_path = os.path.join(output_folder, f"pred_{current_datetime}.jpg")

    os.rename(original_file_path, new_file_path)


    #####################################################################################################

    #March Addition ...
def create_project(project_name = 'default_project'):
    #Join the current directory with the project name to create the project folder path
    project_folder = os.path.join(os.path.abspath('.'), project_name)
    #Create the project folder if it doesn't exist
    os.makedirs(project_folder, exist_ok=True)
    #Get the current time and format it
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    #Create the image name using project name and current time
    image_name = f'{project_name}_{current_time}_hd.jpg'
    #Join the project folder with the image name to get the full image path
    image_path = os.path.join(project_folder, image_name)
    #Return the image path
    return image_path

def initialize_camera():
    #Initialize the camera
    cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)  #'0' is typically the default camera ID. Adjust if necessary.
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  #Set the width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  #Set the height
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))  #Set the codec
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)  #Turn off autofocus

    #Set focus value for closer objects (adjust as needed)
    focus_value = 50.0  #Change this value to your desired focus setting
    cap.set(cv2.CAP_PROP_FOCUS, focus_value)  #Set the focus property

    return cap

def capture_live_image(cap, project_name):
    #Discard any previously read frames
    for _ in range(10):  #Read and discard 10 frames
        cap.read()

    #Read the latest frame from the camera
    ret, frame = cap.read()

    #Check if frame is successfully captured
    if not ret:
        print("Failed to capture image")
        return None

    #Create unique image path for each capture
    image_path = create_project(project_name)

    #Save the image to the specified path
    cv2.imwrite(image_path, frame)
    print(f'Image captured with locked focus: {image_path}')

    return image_path

def release_camera(cap):
    #Release the camera
    cap.release()
    print("Camera released")

#project_name = "one"
#cap = initialize_camera()
#capture_live_image(cap, project_name)
#release_camera(cap)

