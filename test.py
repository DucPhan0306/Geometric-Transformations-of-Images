import cv2
import numpy as np

# Rotation + Translation -> Euclidean
# Rotation + Translation + uniform scale -> Similarity transformation
# Rotation + Translation + uniform scale + Shear -> Affine

def Transformations():
    global px, py
    # Translation
    x = cv2.getTrackbarPos('Translate x','GTI')
    x0 = cv2.getTrackbarPos('-x','GTI')
    y = cv2.getTrackbarPos('y','GTI')
    y0 = cv2.getTrackbarPos('-y','GTI')
    translate_matrix = np.float32([[1, 0, y-y0], [0, 1, x-x0]])
    img_transfor1 = cv2.warpAffine(img_transfor, translate_matrix, (width*2, height*2))
    # Rotation
    degree = cv2.getTrackbarPos('Rotate degree','GTI')
    rota_x = cv2.getTrackbarPos('Rotate x','GTI') + (x-x0)
    rota_y = cv2.getTrackbarPos('Rotate y','GTI') + (y-y0)
    rotate_matrix = cv2.getRotationMatrix2D((rota_y, rota_x), degree,1)
    img_transfor2 = cv2.warpAffine(img_transfor1, rotate_matrix, (width*2, height*2))
    
    # Scaling 
    a1 = cv2.getTrackbarPos('Scale x','GTI')
    b1 = cv2.getTrackbarPos('Scale y','GTI')
    scale_matrix = np.float32([[(b1+1)*0.25, 0, 0], [0, (a1+1)*0.25, 0]])
    img_transfor3 = cv2.warpAffine(img_transfor2, scale_matrix, (width*2, height*2))
        ## img_transfor3 = cv2.resize(img_transfor2, ((a+1)*w_trans2, (b+1)*h_trans2), interpolation=cv2.INTER_CUBIC)

    # Shear
    a2 = cv2.getTrackbarPos('Shear x','GTI')
    b2 = cv2.getTrackbarPos('Shear y','GTI')
    shear_matrix = np.float32([[1, b2, 0], [a2, 1, 0]])
    img_transfor4 = cv2.warpAffine(img_transfor3, shear_matrix, (width*2, height*2))

    #Flip
    a3 = cv2.getTrackbarPos('Flip Ox','GTI')
    if a3 == 1:
        img_transfor5 = cv2.flip(img_transfor4, 1)
    else:
        img_transfor5 = img_transfor4
    a4 = cv2.getTrackbarPos('Flip Oy','GTI')
    if a4 == 1:
        img_transfor6 = cv2.flip(img_transfor5, 0)
    else:
        img_transfor6 = img_transfor5
    a5 = cv2.getTrackbarPos('Flip Oxy','GTI')
    if a5 == 1:
        img_transfor7 = cv2.flip(img_transfor6, -1)
    else:
        img_transfor7 = img_transfor6
    cv2.imshow('GTI1', img_transfor7)
    
    # Perspective Transformation
    pts1 = np.float32([[px[0], py[0]],[px[1],py[1]],[px[2],py[2]],[px[3],py[3]]])
    pts2 = np.float32([[0,0],[500,0],[0,600],[500,600]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(img_transfor,M,(500,600))
    cv2.imshow('GTI3', dst)
def click_event(event, x, y, flags, param):
    global img_transfor7
    global px, py
    global i
    img = img_transfor7.copy()
    if event == cv2.EVENT_LBUTTONDOWN:
        if i < 4:
            print(x,y)
            cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
            px[i], py[i] = x,y
            cv2.imshow('GTI2', img)
            i+=1
        else:
            px, py = [0,0,0,0],[0,0,0,0]
            i = 0
            cv2.imshow('GTI2', img_transfor7)
if __name__== '__main__':
    px, py = [0,0,0,0], [0,0,0,0]
    i = 0
    img_transfor = cv2.imread('./images/img2.jpg')
    img_transfor7 = img_transfor
    height, width, channels = img_transfor.shape
    print("Height: ", height)
    print("Width: ", width)
    print("Channels: ", channels)
    cv2.namedWindow('GTI')
    cv2.resizeWindow('GTI', 600, 1000)
    # Trackbar for Translation
    cv2.createTrackbar('Translate x','GTI',0,height, Transformations)
    cv2.createTrackbar('-x','GTI',0,height, Transformations)
    cv2.createTrackbar('y','GTI',0,width, Transformations)
    cv2.createTrackbar('-y','GTI',0,width, Transformations)
    # Trackbar for Rotation
    cv2.createTrackbar('Rotate degree','GTI',0,360, Transformations)
    cv2.createTrackbar('Rotate x','GTI',0,height, Transformations)
    cv2.createTrackbar('Rotate y','GTI',0,width, Transformations)
    # Trackbar for Scaling
    cv2.createTrackbar('Scale x','GTI',3,8, Transformations)
    cv2.createTrackbar('Scale y','GTI',3,8, Transformations)
    # Trackbar for Shear
    cv2.createTrackbar('Shear x','GTI',0,8, Transformations)
    cv2.createTrackbar('Shear y','GTI',0,8, Transformations)
    # Trackbar for Flip
    cv2.createTrackbar('Flip Ox','GTI',0,1, Transformations)
    cv2.createTrackbar('Flip Oy','GTI',0,1, Transformations)
    cv2.createTrackbar('Flip Oxy','GTI',0,1, Transformations)
    while (True):         
        Transformations()
        cv2.setMouseCallback('GTI1', click_event)     
        if cv2.waitKey (1)&0xFF == ord ('q'):
            break
    cv2.destroyAllWindows ()
