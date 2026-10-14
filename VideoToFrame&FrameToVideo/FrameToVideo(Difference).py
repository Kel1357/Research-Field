import cv2
import numpy as np
import time
def frame_diff_scores(prefix,start,end):
    diffs=[0.0]
    prev=cv2.imread(f"{prefix}_{start:04d}.jpg")
    if prev is None:
        raise FileNotFoundError(f"Can't find {prefix}_{start:04d}.jpg")
    for i in range(start+1,end):
        cur=cv2.imread(f"{prefix}_{i:04d}.jpg")
        if cur is None:
            diffs.append(0.0)
            continue
        d=float(np.mean(cv2.absdiff(cur,prev).astype(np.float64)))
        diffs.append(d)
        prev=cur
        # Feature: progress indicator
        if (i-start)%5==0 or i==end-1:
            print(f"Processing frame {i}/{end-1}...")
    return np.array(diffs)
def select_frames_by_difference(prefix,start,end,n_out):
    diff=frame_diff_scores(prefix,start,end)   
    c=np.zeros(len(diff))
    total=0.0
    for k in range(len(diff)):
        total=total+diff[k]
        c[k]=total
    t=c[-1]                             
    if t==0:
        idx=np.linspace(0,len(diff)-1,n_out).round().astype(int)
    else:
        targets=np.linspace(0,total,n_out)        
        idx=np.searchsorted(c,targets)           
        idx=np.clip(idx,0,len(diff)-1)
    idx=sorted(set((start+idx).tolist()))   
    return idx
def frame_video(output,fps,size,prefix,indices):
    fourcc=cv2.VideoWriter_fourcc(*"mp4v")
    out=cv2.VideoWriter(output,fourcc,fps,size)
    u=0
    for i in indices:
        p=f"{prefix}_{i:04d}.jpg"
        f=cv2.imread(p)
        if f is None:
            print(f"Can't find {p} so, Skipping.")
            continue
        f=cv2.resize(f,size)
        out.write(f)
        u=u+1
    out.release()
    print(f"Video saved as {output}. Used {u} frames.")
# Feature: input with default value + validation, re-prompts on bad input
def feature(prompt,default=None,mini=None,maxi=None):
    while True:
        raw=input(prompt).strip()
        if raw=="" and default is not None:
            return default
        try:
            value=int(raw)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if mini is not None and value<mini:
            print(f"Value must be at least {mini}.")
            continue
        if maxi is not None and value>maxi:
            print(f"Value must be at most {maxi}.")
            continue
        return value
if __name__=="__main__":
    size1=(1920, 1080)
    prefix1="frames"
    out=input("Output Video Filename [output.mp4]:").strip() or "output.mp4"
    #Feature: auto-append .mp4 extension if missing
    if not out.lower().endswith(".mp4"):
        out=out+".mp4"
    fps=feature("FPS [24]:",default=24,mini=1)
    start=feature("Start Frame Index [0]:",default=0,mini=0)
    end=feature("End Frame Index (exclusive):",mini=start + 1)
    #Feature: validate n_out range before running
    n_out=feature(
        f"Number of output frames (2-{end - start}):",
        mini=2,
        maxi=end-start
    )
    t0=time.time()
    selected=select_frames_by_difference(prefix1,start,end,n_out)
    #Feature: summary of selected frames+their timestamps
    print("\nSelected frames:")
    for i in selected:
        print(f"frame {i}->{i/fps:.2f}s")
    frame_video(out,fps=fps,size=size1,prefix=prefix1,indices=selected)
    #Feature: total elapsed time
    print(f"\nDone in {time.time()-t0:.2f} seconds.")
