import cv2
import numpy as np
from functions import *
from sudoku_solver import *
from matplotlib import pyplot as plt

img = cv2.imread("sudoku test images/sudoku7.jpeg")

img_contours = img.copy()

img_biggest_contour = img.copy()

#Applying Gray Scale, Gaussian Blur, Adaptive Threshold
prepared_image = prepare_image(img,cv2.THRESH_BINARY_INV)

#Finding all the contours and drawing them onto img_contours
contours,_ = cv2.findContours(prepared_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(img_contours,contours,-1,(0,255,0),8)

#Finding the contour that has the biggest area.
_,biggest_contour= find_biggest_contour(contours)


#Note that we are assuming that the biggest area here is the sudoku grid.
cv2.drawContours(img_biggest_contour,biggest_contour,-1,(0,255,255),30)


#Drawing the biggest contour by basically connecting the biggest countor corner points
for i in range(len(biggest_contour)):
    p1 = (biggest_contour[i][0][0],biggest_contour[i][0][1])
    if i < len(biggest_contour) - 1:
        p2 = (biggest_contour[i+1][0][0],biggest_contour[i+1][0][1])
    else:
        p2 = (biggest_contour[0][0][0],biggest_contour[0][0][1])
     
    cv2.line(img_biggest_contour, p1, p2, (0, 0, 255), 6)


#Ordering points. We cannot know which index corresponds for which corner. 
#So we need to order the points with a certain order, so that we can apply warp perspective method.
ordered_points = order_points(np.float32(biggest_contour))

#Setting the dimensions of warped image
width = 450
height = 450

perspective_image = warp_perspective(img,ordered_points,width,height)

blank_image = np.zeros_like(perspective_image)


#Dividing the grid to 81 equal images.
cells = divide_81_pieces(perspective_image)

#Cropping 5 pixels from each side in order to get rid of sudoku lines. (They confuse the ai lol)
cropped_cells = roi(cells)

#Predicting the numbers
sudoku_numbers = predict(cropped_cells)

#Converting the sudoku numbers list to a grid which has 9 rows and 9 columns
#Basically 1D list ---> 2D list
sudoku_grid = convert_to_grid(sudoku_numbers) 

#Solving the sudoku
sudoku_grid_answers = solve(sudoku_grid)

if sudoku_grid_answers is None:
    print("Couldn't solve the sudoku")
else:
    print(sudoku_grid_answers)

#Extracting the answers. Now we have a list with only answers. Other cells will be represented as 0
extracted_answers = extract_answers(sudoku_grid,sudoku_grid_answers)

#Displaying the answers on the right coordinates.
image_sudoku_answers = display_sudoku_number(blank_image,extracted_answers)

print(extracted_answers)

#Inverse perspectiving the image. (Idfk if the word perspectiving exists lol)
points = np.float32([[0,0],[0,height],[width,0],[width,height]])

perspective_points = ordered_points

matrix = cv2.getPerspectiveTransform(points,perspective_points)

inverse_perspective_answer_image = img.copy()

inverse_perspective_answer_image = cv2.warpPerspective(image_sudoku_answers,matrix,(img.shape[1],img.shape[0]))

combined = cv2.addWeighted(inverse_perspective_answer_image,0.75,img,0.5,2)

cv2.imwrite("a.jpg",img_contours)

#Virtualizing

images = [img, prepared_image, img_contours, img_biggest_contour, perspective_image, cropped_cells[0], image_sudoku_answers,inverse_perspective_answer_image,combined]
titles = ["Original Image", "Prepared Image", "Image Contours", "Biggest Contour", "Perspective Image", "Example Cell", "Answers Image","Inverse-Perspective Answers Image","Combined Answers and Original Image"]

fig = plt.figure(figsize=(10, 8))
rows = 3
cols = 3

for i in range(len(images)):
    ax = fig.add_subplot(rows, cols, i+1)
    ax.set_title(titles[i])
    ax.imshow(images[i], cmap='gray')
    ax.axis('off')

plt.show()


