import cv2
def frame_video(output,fps,frames,size,prefix="frame"):
    #Tells OpenCV to use the MPEG‑4 video codec
    path=cv2.VideoWriter_fourcc(*"mp4v")
    o=cv2.VideoWriter(output,path,fps,size)
    for i in range(frames):
        f=cv2.imread(f"{prefix}_{i:04d}.jpg")
        f=cv2.resize(f,(1920,1080))  #Upscale Video to Full HD
        o.write(f)
    print(f"Video saved as {output}.")
if __name__ =='__main__':
    #Try Maintaining Original fps because of time taken to Upscale Video increases on High fps
    frame_video("Kel_FULLHD_24fps.mp4",fps=24,frames=332,size=(1920,1080),prefix="frames")

