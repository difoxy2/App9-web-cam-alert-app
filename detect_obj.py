import cv2 as cv
import time, math, threading
import emailling, utils
 


# Initial variables
obj_dected_status = [False,False] # Send email if obj exit frame --> Send email if status = [True,False]
img_seq_data = utils.return_initial_img_seq_data()

# start camera
cap = cv.VideoCapture(0)
time.sleep(1)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Object detection
# Step 1: save the first frame, when open camera, run away from camera to save static background
first_frame = cap.read()[1]
first_frame = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)
first_frame = cv.GaussianBlur(first_frame,(21,21),0)

while True:
    # Capture frame-by-frame
    check, frame = cap.read()
 
    # if frame is read correctly check is True
    if not check:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Step 2: find difference between frame and first_frame
    frame_grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_grey_blur = cv.GaussianBlur(frame_grey,(21,21),0)
    delta_frame = cv.absdiff(frame_grey_blur,first_frame)

    # Step 3: threshold difference into black and white image
    delta_frame_threshold = cv.threshold(delta_frame,75,255,cv.THRESH_BINARY)[1]
    delta_frame_dilate = cv.dilate(delta_frame_threshold,None,iterations=5)

    # Step 4: draw rectangles / contours for difference part (white part)
    obj_dected = False
    contours, hireachy = cv.findContours(delta_frame_dilate,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv.contourArea(contour) > 10000:
            obj_dected = True
            x,y,w,h = cv.boundingRect(contour)
            cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,255),2) # draw rectangle

            # Save all images in images folder
            img_seq_data['counter'] += 1
            cv.imwrite(f'images/{img_seq_data['counter']}.jpg',frame)

            # Update update img_seq_data
            obj_area = w * h
            frame_h,frame_w = frame.shape[0:2]
            obj_dis_to_ctr = math.dist([int(frame_w/2),int(frame_h/2)], [int(x+w/2),int(y+h/2)])
            img_seq_data = utils.update_img_seq_data(img_seq_data,obj_area,obj_dis_to_ctr)


    # Check if obj exit frame --> status = [True,False] --> if so, send email + clean image folder + reset img_seq_data
    obj_dected_status = obj_dected_status[-1:]
    obj_dected_status.append(obj_dected)
    if obj_dected_status == [True,False]:
        
            # send email + clean image folder + reset img_seq_data
            msg = emailling.return_EmailMessage_with_att(img_seq_data)
            t1 = threading.Thread(target=emailling.send_emailMsg,args=(msg,))
            t1.start()
            utils.clean_folder('images/')
            img_seq_data = utils.return_initial_img_seq_data()
        
    cv.imshow('showWindow', frame)

    if cv.waitKey(1) == ord('q'):
        break
 
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()