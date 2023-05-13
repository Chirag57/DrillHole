import cv2
import numpy as np
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='pass',
    port='3306',
    database='Drill_Hole'
)
cursor = mydb.cursor()

# input
target = float(input('Enter the Basic Value : '))
allowance = float(input('Enter the Allowance Value : '))

# Load the image
image = '/Users/chiraggupta/Downloads/WhatsApp Image 2023-05-09 at 2.12.53 PM.jpeg'
img = cv2.imread(image, 0)

# Define the calibration factor in pixels per millimeter
calibration_factor = 0.09136175

# Apply Gaussian blur and thresholding
blur = cv2.GaussianBlur(img, (5, 5), 0)

thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Detect edges using Canny
edges = cv2.Canny(thresh, 50, 150)

# Detect circles using HoughCircles
circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)

# Draw circles on the original image and color-code based on quality
if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    if len(circles) > 0:
        (x, y, r) = circles[0]

        color = (255, 133, 233)

        # Draw the circle with the appropriate color
        cv2.circle(img, (x, y), r, color, 2)

        # Calculate the radius in micrometers using the calibration factor
        radius = r * calibration_factor

        # Add the radius text to the image
        radius_text = 'Diameter: {:.2f} millimeters'.format(2 * radius)
        cv2.putText(img, radius_text, (x - r, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

dia = 2 * radius
# Display the output image
print(f"Diameter in mm : {2 * radius}")
cv2.imshow('Output Image', img)
lsl = target - allowance
usl = target + allowance
flag = True
if dia >= lsl and dia <= usl:
    flag = False
    print("The radius of the Drill Hole is within the Specification Limit")
else:
    flag = True
    print("The radius of the Drill Hole is Out of the Bound")
Date = "2023-05-10"
s = "INSERT INTO Analysis (Image_Address,Date,Diameter,LSL,USL,BOUND_OUT) VALUES(%s,%s,%s,%s,%s,%s)"
b = (image, Date, float(dia), float(lsl), float(usl), bool(flag))
cursor.execute(s, b)
mydb.commit()
cv2.waitKey(1)
cv2.destroyAllWindows()

