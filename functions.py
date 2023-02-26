import cv2
import numpy as np
from matplotlib import pyplot as plt
from tensorflow.python.keras.models import load_model

model_path = "PYTHON VISUAL CODE/opencv-tutorial/tutorials/sudoku_solver/digits.h5"
model = load_model(model_path)


def prepare_image(img,method):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray,(5,5),0)

    th1 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,method,11,6)

    return th1

def find_biggest_contour(contours):
    max_area = 0
    biggest_contour = np.array([])
    for contour in contours:

        if cv2.contourArea(contour) > 100: #getting rid of all the contours that has less area than 100
            perimeter = cv2.arcLength(contour,closed=True)
            corners = cv2.approxPolyDP(contour,0.02 * perimeter,closed=True) #to identify geometrical shapes
            if cv2.contourArea(contour) > max_area and len(corners) == 4:
                max_area = cv2.contourArea(contour)
                biggest_contour = corners
    return max_area,biggest_contour

def order_points(points): 
    reshaped_points = points.reshape((4,2))  # our points had [[]] , we converted to [] so that we can use it on warp perspective

    # sort the points based on their x-coordinate (left-to-right order)
    sorted_x = reshaped_points[np.argsort(reshaped_points[:, 0])]

    # sort the leftmost two points based on their y-coordinate (top-to-bottom order)
    sorted_left = sorted_x[:2][np.argsort(sorted_x[:2, 1])]

    # sort the rightmost two points based on their y-coordinate (top-to-bottom order)
    sorted_right = sorted_x[2:][np.argsort(sorted_x[2:, 1])]

    # concatenate the sorted points into a new list
    sorted_list = np.concatenate([sorted_left, sorted_right])
    
    #top left
    #bot left
    #top right
    #bot right

    return sorted_list



def warp_perspective(img,points,width,height):
    
    perspective_points = np.float32([[0,0],[0,height],[width,0],[width,height]])

    matrix = cv2.getPerspectiveTransform(points,perspective_points)

    image_output = cv2.warpPerspective(img,matrix,(width,height))

    image_output = cv2.cvtColor(image_output,cv2.COLOR_BGR2GRAY)

    return image_output


def divide_81_pieces(img):
    rows = np.vsplit(img,9) #spliting the rows into 9 equal pieces.

    cells = []
    for row in rows:
        columns = np.hsplit(row,9)

        for cell in columns:
            cells.append(cell)
        
    return cells

def roi(img_list):
    new_list = []
    for img in img_list:
        img = img[5:45, 5:45]
        new_list.append(img)
    return new_list

def predict(img_list):

    predicted_numbers = []
    for img in img_list:
        img = cv2.resize(img, (28,28))
        img = img / 255
        img = img.reshape(1,28,28,1)

        predict = model.predict(img)
        prob = np.amax(predict)
        class_index = np.argmax(predict, axis=-1)
        result = class_index[0]

        if prob < 0.75:
            predicted_numbers.append(0)
        else:
            predicted_numbers.append(result)

    return predicted_numbers

def convert_to_grid(lst):
    grid = []
    for i in range(0, 81, 9):
        row = lst[i:i+9]
        grid.append(row)
    return grid

def display_sudoku_number(img,sudoku_answers):

    #Sudoku_answers list is a 2D grid list so i will convert it to a 1D list 
    #in order to display them easier.
    try:
        img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

        sudoku_answers_1d = []
        for sublist in sudoku_answers:
            for item in sublist:
                sudoku_answers_1d.append(item)


        height = img.shape[0] / 9
        width = img.shape[1] / 9

        for row in range(0,9):
            for column in range(0,9):
                current_number = sudoku_answers_1d[(row * 9) + column]
                if current_number != 0:
                    x_cord = (height/2) + height*column
                    y_cord = (width/2) + width*row
                    cv2.putText(img,str(current_number),(int(x_cord),int(y_cord)),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0))
        return img
    except:
        print("There has been an ,error recognizing the numbers")
def extract_answers(sudoku_grid,sudoku_answers):

    try:
        for i in range(0,9):
            for j in range(0,9):
                if sudoku_grid[i][j] == sudoku_answers[i][j]:
                    sudoku_answers[i][j] = 0
        return sudoku_answers
    except:
        print("There has been an ,error recognizing the numbers")