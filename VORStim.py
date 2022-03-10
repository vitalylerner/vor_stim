from numpy import *
import cv2, time, tkinter, random
#import tkinter.font as tkFont


#STIMULUS PARAMETERS FOR SACCADE
     



color = (0, 0, 0)
thickness = -1
    




    

DEF_T2=2#s
DEF_T3=1#s
DEF_L3=100#px

DEF_R=600#px
DEF_C=800#px

DEF_RADIUS= 10
class neuronstim(tkinter.Tk):

    def stim_blank(self,txt:str=''):
        R,C=self.get_geometry()
        Z=zeros((R,C,3)).astype(float)+255
        if not txt=='':
            Z = cv2.putText(Z, txt, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 
                           1, (0, 0, 0), 1, cv2.LINE_AA)
        return Z
        

    def stim1(self):
        global color,thickness
        radius=int(self.txtRadius.get())
        R,C=self.get_geometry()
        PL_step=((C*1./2-radius-10)/3)/C
        
        PL=(array([-3,-2,-1,1,2,3])*PL_step*C+0.5*C).astype(int)
        PL_LBL=['-3','-2','-1','+1','+2','+3']   
        def add_grid(img):
            
            y=int(R/2-50-radius)
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


        
        title="Saccade"
        
        center_coordinates = (int(C/2), int(R/2))

        jmpx=random.choice(PL)
        jmp_coordinates = (jmpx, int(R/2))


        A = cv2.circle(self.stim_blank("Press any key when ready"), center_coordinates, radius, color, thickness)
        add_grid(A)
        cv2.imshow(title,A)
        cv2.waitKey(0)
        B= cv2.circle(self.stim_blank("Press any key when ready"), jmp_coordinates, radius, color, thickness)
        add_grid(B)
        cv2.imshow(title,B)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def stim3(self):
        T=float(self.txtT3.get())
        
        L=float(self.txtL3.get())
        R,C=self.get_geometry()
        thr=0.8
        global color,thickness
        
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
        R,C=self.get_geometry()
        T=float(self.txtT2.get())
        radius=int(self.txtRadius.get())
        global color,thickness
        title="Smooth Pursuit"
        announce="Press any key to start, Esc to stop"
        center_coordinates = (int(C/2), int(R/2))
        
        #T=10
        L=int(C*0.8)
        A = cv2.circle(self.stim_blank(announce), (int(C*0.1),int(R/2)), radius, color, thickness)
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
            A = cv2.circle(self.stim_blank(), circ_coord, radius, color, thickness)
            cv2.imshow(title,A)
            cont=not (cv2.waitKey(1)==27)
            i+=1
        cv2.destroyAllWindows()
        
    def get_geometry(self):
        R=int(self.txtR.get())
        C=int(self.txtC.get())
        return R,C
        
    def __init__(self):
        tkinter.Tk.__init__(self)
        #fontExample = tkFont.Font( size=16, weight="bold", slant="italic")

        
        self.geometry("500x200")
        self.title('Neurobiology: VOR 2022')
        lblTitle=tkinter.Label(self,text="Neurobiology: VOR 2022")
        lblTitle.place(x=2,y=10)
        #lblTitle.configure(font=fontExample)
        
        tkinter.Label(self,text="Vitaly Lerner 2022").place(x=2,y=30)
        
        #STIM 1
        Y=40
        self.cmdStim1=tkinter.Button(self,text="Sacdade",command=self.stim1)
        self.cmdStim1.place(x=400,y=Y)
        
        
        #STIM 2
        Y=80
        self.txtT2=tkinter.Entry(self)
        self.txtT2.place(x=300,y=Y,width=50)
        self.txtT2.insert(0,"{}".format(DEF_T2))
        tkinter.Label(self,text="Period(s)").place(x=230,y=Y)
        
        self.cmdStim2=tkinter.Button(self,text="Smooth Pursuit",command=self.stim2)
        self.cmdStim2.place(x=400,y=Y)

        #STIM 3
        Y=120
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
    
        #General Params
        Y=160
        self.txtR=tkinter.Entry(self)
        self.txtR.place(x=200,y=Y,width=40)
        self.txtR.insert(0,"{}".format(DEF_R))
        #tkinter.Label(self,text="Period(s)").place(x=230,y=Y)
        
        tkinter.Label(self,text="Resolution").place(x=60,y=Y)
        tkinter.Label(self,text="x").place(x=175,y=Y)
        tkinter.Label(self,text="Radius(px)").place(x=260,y=Y)
        
        self.txtC=tkinter.Entry(self)
        self.txtC.place(x=130,y=Y,width=40)
        self.txtC.insert(0,"{}".format(DEF_C))
        
        self.txtRadius=tkinter.Entry(self)
        self.txtRadius.place(x=320,y=Y,width=40)
        self.txtRadius.insert(0,"{}".format(DEF_RADIUS))
        
        #tkinter.Label(self,text="Period(s)").place(x=230,y=Y)
        
N=neuronstim()
N.mainloop()