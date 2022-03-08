from numpy import *
import cv2, time, tkinter, random

R=600
C=800

#STIMULUS PARAMETERS FOR SACCADE
PL_step=0.16
PL=(array([-3,-2,-1,1,2,3])*PL_step*C+0.5*C).astype(int)
PL_LBL=['-3','-2','-1','+1','+2','+3']        


radius = 10
color = (0, 0, 0)
thickness = -1
    
def stim_blank(txt:str=''):
    global R,C
    Z=zeros((R,C,3)).astype(float)+255
    if not txt=='':
        Z = cv2.putText(Z, txt, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (0, 0, 0), 1, cv2.LINE_AA)
    return Z

def add_grid(img):
    global PL, PL_LBL
    y=int(R/2-60)
    dy=20
    img=cv2.line(img,(PL[0],y),(PL[-1],y),color=(0.5,0.5,0.5),thickness=1)
    PL2=list(PL)+[int(C/2)]
    PL2_LBL=PL_LBL+['0']
    for ip in range(7):
        x=PL2[ip]
        lbl=PL2_LBL[ip]
        img=cv2.line(img,(x,y),(x,dy+y),color=(0.5,0.5,0.5),thickness=1)
        img=cv2.putText(img, lbl, (x-15,y-5), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, (0.5, 0.5, 0.5), 1, cv2.LINE_AA)

    

DEF_T2=2#s
DEF_T3=1#s
DEF_L3=100#px
class neuronstim(tkinter.Tk):
    def stim1(self):
        global R,C,PL
        global radius,color,thickness
        title="Saccade"
        
        center_coordinates = (int(C/2), int(R/2))

        jmpx=random.choice(PL)
        jmp_coordinates = (jmpx, int(R/2))


        A = cv2.circle(stim_blank("Press any key when ready"), center_coordinates, radius, color, thickness)
        add_grid(A)
        cv2.imshow(title,A)
        cv2.waitKey(0)
        B= cv2.circle(stim_blank("Press any key when ready"), jmp_coordinates, radius, color, thickness)
        add_grid(B)
        cv2.imshow(title,B)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def stim3(self):
        T=float(self.txtT3.get())
        
        L=float(self.txtL3.get())
        thr=0.8
        global radius,color,thickness
        
        title="Nystagmus: Esc to stop"
        announce="Press any key to start, Esc to stop"
        center_coordinates = (int(C/2), int(R/2))
        Y, X = meshgrid(arange(R), arange(C), indexing='ij')
        
        Z=1.0*(sin(2*pi*X/L)<thr)
        Z = cv2.putText(Z, announce, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.8, (0.8, 0.1, 0.1), 2, cv2.LINE_AA)
        cv2.imshow(title,Z)
        cv2.waitKey(0)
        
        t0=time.time() 
        t=time.time()-t0
        i=0
        cont=True
        while cont:
            t=time.time()-t0
            Z=1.0*(sin(2*pi*X/L-2*pi*t/T)<thr)
            #Z = cv2.putText(Z, "Esc to stop" , (20,60), cv2.FONT_HERSHEY_SIMPLEX, 
            #               2, (0.1, .5, .5), 2, cv2.LINE_AA)
            cv2.imshow(title,Z)
            cont=not (cv2.waitKey(1)==27)
            i+=1
        cv2.destroyAllWindows()
           # time.sleep(10)"""
           
       
    def stim2(self):
        T=float(self.txtT2.get())
        global radius,color,thickness
        title="Smooth Pursuit"
        announce="Press any key to start, Esc to stop"
        center_coordinates = (int(C/2), int(R/2))
        
        #T=10
        L=int(C*0.8)
        A = cv2.circle(stim_blank(announce), (int(C*0.1),int(R/2)), radius, color, thickness)
        cv2.imshow(title,A)
        cv2.waitKey(0)
        t0=time.time() 
        t=time.time()-t0
        i=0
        cont=True
        while cont:
            t=time.time()-t0
            if floor(t/T)%2==0:
                x= int(t/T*L)%L+int(C*0.1)
            else:
                x= L-int(t/T*L)%L+int(C*0.1)
            circ_coord= (x, int(R/2))
            A = cv2.circle(stim_blank(), circ_coord, radius, color, thickness)
            cv2.imshow(title,A)
            cont=not (cv2.waitKey(1)==27)
            i+=1
        cv2.destroyAllWindows()
        
    def __init__(self):
        tkinter.Tk.__init__(self)
        
    
        self.geometry("500x200")
        self.title('Neurobiology: VOR 2022')
        tkinter.Label(self,text="Neurobiology: VOR 2022").place(x=2,y=10)
        
        tkinter.Label(self,text="Vitaly Lerner 2022").place(x=2,y=30)
        
        #STIM 1
        Y=40
        self.cmdStim1=tkinter.Button(self,text="Sacdade",command=self.stim1)
        self.cmdStim1.place(x=400,y=Y)
        
        
        #STIM 2
        Y=100
        self.txtT2=tkinter.Entry(self)
        self.txtT2.place(x=300,y=Y,width=50)
        self.txtT2.insert(0,"{}".format(DEF_T2))
        tkinter.Label(self,text="Period(s)").place(x=230,y=Y)
        
        self.cmdStim2=tkinter.Button(self,text="Smooth Pursuit",command=self.stim2)
        self.cmdStim2.place(x=400,y=Y)

        #STIM 3
        Y=160
        self.txtT3=tkinter.Entry(self)
        self.txtT3.place(x=300,y=Y,width=50)
        self.txtT3.insert(0,"{}".format(DEF_T3))
        tkinter.Label(self,text="Period(s)").place(x=230,y=Y)
        
        
        self.txtL3=tkinter.Entry(self)
        self.txtL3.place(x=160,y=Y,width=50)
        self.txtL3.insert(0,"{}".format(DEF_L3))
        tkinter.Label(self,text="Spacing(px)").place(x=90,y=Y)
        
        
        self.cmdStim3=tkinter.Button(self,text="Nystamus",command=self.stim3)
        self.cmdStim3.place(x=400,y=Y)
    

        
N=neuronstim()
N.mainloop()