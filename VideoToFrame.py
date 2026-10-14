import cv2
def video_frame(video,prefix="frame"):
    #Opens the Video File so, frames Can Be Read
    path=cv2.VideoCapture(video)
    c=0
    while (True):
        r,frame=path.read()
        if not r:
            break
        #Saves the frame as an image file
        cv2.imwrite(f"{prefix}_{c:04d}.jpg",frame)
        c=c+1
    print(f"Extracted {c} frames from {video}.")
    return c
if __name__=='__main__':
    frames=video_frame("Kel(24fps).mp4",prefix="frames")