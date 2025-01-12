import cv2 as cv
import time, math, threading
import emailling, utils
import streamlit as st
 


############ streamlit frontend ############
st.header('Object Detector')
st.text('Make sure you start with no object (static background) before enable camera.')


col1_1,col1_2,col1_3 = st.columns([1,1,2])

with col1_1:
    enable = st.checkbox("Enable camera")
with col1_2:
    st_threshold_input = st.number_input('detect threshold (0-255)',0,255,value=75,step=5)
with col1_3:
    st_email_receiver = st.text_input('Send imgs to email once an object is detected:')


col2L, col2R= st.columns([4,1])
with col2L:
    webcam = st.image([],width=640)


with col2R:
    st.text("1. middle frame")
    stimg_mid_frame = st.image([])

    st.text("2. largest detection")
    stimg_largest_obj = st.image([])

    st.text("3. nearest to center")
    stimg_min_dist = st.image([])


st.subheader('What is this App?')
st.text('This is an object detection app written in Python')
st.subheader('How to use?')
st.subheader('Inputs')
st.text('1. Enable Camera: ')
st.text('Enable / Disable your web camera. Make sure there is no object in view before enable camera. You need to start with a static background.')
st.text('2. Detect Threshold (0-255): ')
st.text('How much contrast is needed for the app to differenciate object vs background. Play with this number according to your lighting condition. The higher the number, the more contrast is needed for objected to be identified.')
st.text('3. Email: ')
st.text(' Enter an email address to receive images of detected objects. Email is send everytime object enter and exit the frame. Can be leave blank.')
st.subheader('Images Generated')
st.text('Three images are generated every time an object enters and then leave the frame.')
st.text('1. Middle frame: ')
st.text('For example, the object is in frame for 5 sceonds, middle frame is image on the 2.5 second.')
st.text('2. Largest Detection: ')
st.text('The image that had the largest detection box area while in frame.')
st.text('3. Nearest to Center: ')
st.text('The image that had the detection box cloest to the center while in frame.')
####### camera loop object detection #######
# Initial variables
obj_dected_status = [False,False] # Send email if obj exit frame --> Send email if status = [True,False]
img_seq_data = utils.return_initial_img_seq_data()

if enable:
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
        delta_frame_threshold = cv.threshold(delta_frame,st_threshold_input,255,cv.THRESH_BINARY)[1]
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
            
                p1,p2,p3 = utils.return_img_seq_data_file_paths(img_seq_data)
                stimg_mid_frame.image(p1)
                stimg_largest_obj.image(p2)
                stimg_min_dist.image(p3)

                if(st_email_receiver):
                    # send email + clean image folder + reset img_seq_data
                    msg = emailling.return_EmailMessage_with_att(img_seq_data,st_email_receiver)
                    t1 = threading.Thread(target=emailling.send_emailMsg,args=(msg,))
                    t1.start()

                utils.clean_folder('images/')
                img_seq_data = utils.return_initial_img_seq_data()
            
        frame = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        webcam.image(frame)