import smtplib, datetime, mimetypes
from email.message import EmailMessage
import streamlit as st



def emailMessage_att_helper(filepath):
    # content, maintype, subtype = create_EmailMessage_attachment(filepath)
    # msg.add_attachment(content,maintype=maintype,subtype=subtype,filename='filename.extention')
    with open(filepath,'rb') as file:
        content = file.read()
        ctype, encoding = mimetypes.guess_type(filepath)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream' # No guess could be made, or the file is encoded (compressed), so # use a generic bag-of-bits type.
        maintype, subtype = ctype.split('/',1)
    return content, maintype, subtype



def return_EmailMessage_with_att(img_seq_data,receiver):
    # email content
    msg = EmailMessage()
    msg['To'] = receiver
    msg['From'] = st.secrets["EMAIL_ACC"]
    msg['Subject'] = f'Object detected on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    msg.set_content(f'I think this will be override. No it won"t.\n\nHere is object detected on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    # add attachments
    # mid_frame.jpg
    content, maintype, subtype = emailMessage_att_helper(f'images/{img_seq_data['img_mid_frame']}.jpg')
    msg.add_attachment(content,maintype=maintype,subtype=subtype,filename='mid_frame.jpg')
    # largest_obj.jpg
    content, maintype, subtype = emailMessage_att_helper(f'images/{img_seq_data['img_largest_obj']}.jpg')
    msg.add_attachment(content,maintype=maintype,subtype=subtype,filename='largest_obj.jpg')
    # closest_to_center.jpg
    content, maintype, subtype = emailMessage_att_helper(f'images/{img_seq_data['img_min_dist_to_ctr']}.jpg')
    msg.add_attachment(content,maintype=maintype,subtype=subtype,filename='closest_to_center.jpg')   

    return msg



def send_emailMsg(emailMsg):
    print('Start send email')

    # start gmail TLS server and login
    gmail_server = smtplib.SMTP('smtp.gmail.com', 587)
    gmail_server.ehlo()
    gmail_server.starttls()
    gmail_server.login(st.secrets["EMAIL_ACC"],st.secrets["GMAIL_APP_PW_1"])

    # send email
    gmail_server.send_message(emailMsg)
    
    #close TLS server
    gmail_server.quit()

    print('Email was sent')