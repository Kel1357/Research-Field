import cv2
def frame_video(output, fps, size, prefix="frame", start=0, end=1, step=1):
    """
    Build a video from a sequence of frame images.
    start: First frame index to include (default 0)
    end: Last frame index to include, exclusive (must be given)
    step: Take every Nth frame -> step=5 means 0,5,10,15,...
    """
    path=cv2.VideoWriter_fourcc(*"mp4v")
    out=cv2.VideoWriter(output,path,fps,size)
    u=0
    for i in range(start,end,step):
        p=f"{prefix}_{i:04d}.jpg"
        f=cv2.imread(p)
        if f is None:
            print(f"Can't Find Image {p} so, Skipping.")
            continue
        f=cv2.resize(f,size) 
        out.write(f)
        u=u+1
    out.release()
    print(f"Video saved as {opt}. Used {u} frames (step={step}).")
if __name__=='__main__':
    opt=input("Output Video Filename (e.g. Kel_FULLHD_24fps(Condition).mp4):").strip()
    fps=int(input("FPS:").strip())
    start=int(input("Start Frame Index:").strip())
    end=int(input("End Frame Index:").strip())
    step=int(input("Interval Between Frames (e.g.: 5 for 0,5,10,...):").strip())
    frame_video(opt,fps=fps,size=(1920,1080),prefix="frames",start=start,end=end,step=step)
