import os
import cv2
import numpy as np

# Load the template and image files
template = cv2.imread(r"C:\Users\Brtsnsn\PycharmProjects\flyff-bots\Bert_Bot\maid.png")
img = cv2.imread(r"C:\Users\Brtsnsn\PycharmProjects\flyff-bots\Bert_Bot\maid_compare.png")

# cv2.imshow("Image with bounding box", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# # Convert the template and image to grayscale
# template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Resize the template to the same size as the image
# template = cv2.resize(template, (image.shape[1], image.shape[0]))

# # Calculate the absolute difference between the template and the image
# diff = cv2.absdiff(template, image)

# # Threshold the difference image to create a binary mask
# mask = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)[1]

# # Find the contours in the mask
# contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # Get the bounding box of the largest contour
# bounding_box = cv2.boundingRect(contours[0])

# # Draw the bounding box on the image
# cv2.rectangle(image, bounding_box, (0, 255, 0), 2)

# # Display the image with the bounding box
# cv2.imshow("Image with bounding box", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



#--- performs Otsu threshold ---
def threshold(img, st):
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # cv2.imwrite(os.path.join(path, 'res_' + str(st) + '.jpg'), thresh) 
    return  thresh

# path = r'C:\Users\Desktop'
# filename = 'digits.jpg'

# img = cv2.imread(os.path.join(path, filename))
# img = cv2.resize(img, (0, 0), fx = 0.5, fy = 0.5)   #--- resized the image because it was to big 
cv2.imshow('Original', img)

#--- see each of the channels individually ---
# cv2.imshow('b', img[:,:,0])
# cv2.imshow('g', img[:,:,1])
# cv2.imshow('r', img[:,:,2])

m1 = threshold(img[:,:,0], 1)   #--- threshold on blue channel
m2 = threshold(img[:,:,1], 2)   #--- threshold on green channel
m3 = threshold(img[:,:,2], 3)   #--- threshold on red channel

#--- adding up all the results above ---
res = cv2.add(m1, cv2.add(m2, m3))

image = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

cv2.imshow('res', res)
cv2.imshow('res2', image)
# cv2.imwrite(os.path.join(path, 'res.jpg'), res)

cv2.waitKey()
cv2.destroyAllWindows()