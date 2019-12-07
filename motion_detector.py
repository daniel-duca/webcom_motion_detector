import cv2 ,time ,datetime ,pandas

video=cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(3)

first_frame=None
status_list=[0,0]
time_list=[]
df=pandas.DataFrame(columns=["Start","End"])

i=4
while i>0:
    cheak,frame=video.read()
    i-=1
gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
gray1=cv2.GaussianBlur(gray,(21,21),0)

while True:

    cheak,frame=video.read()
    status=0
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)

    if first_frame is None:
        first_frame=gray1
        continue

    delta_frame=cv2.absdiff(first_frame,gray)

    thresh_frame=cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame, None,iterations=2)

    (cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    for countour in cnts:
        if cv2.contourArea(countour)<10000:
           continue 
        
        status=1
        (x,y,h,w)=cv2.boundingRect(countour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

    status_list.append(status)
    status_list=status_list[-2:]


    if (status_list[-1] + status_list[-2]) == 1 :
        time_list.append(datetime.datetime.now())

    cv2.imshow("gray frame",gray)
    cv2.imshow("delta frame",delta_frame)
    cv2.imshow("thresh frame",thresh_frame)
    cv2.imshow("color frame",frame)
    key=cv2.waitKey(1)

    if key==ord('q'):
        if status==1:
            time_list.append(datetime.datetime.now())
        break

for i in range(0,len(time_list),2):
    df=df.append({"Start":time_list[i],"End":time_list[i+1]},ignore_index=True)

df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows()