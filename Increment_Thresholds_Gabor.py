'''
This experiment was created using PsychoPy v.2021.2.3 for a monitor with an 85-Hz refresh rate and a screen resolution of 800 x 600. 
The monitor was calibrated using a Photo Research PR-650 Spectrophotometer, and the viewing distance was 70 cm.
Each observer was allocated pre-determined (psuedorandomized) experimental conditions (see VF_conds.py).
'''
from __future__ import division, print_function
from psychopy import visual, core, data, event, sound, logging, gui, prefs
from psychopy import monitors
from psychopy.visual import ShapeStim, Line, TextStim
from psychopy.constants import * #things like STARTED, FINISHED
from psychopy.preferences import prefs
import os #handy system and path functions
import sys
from math import *
from builtins import next, range
import copy, time #from the std python libs
from psychopy.data import MultiStairHandler
import random
import Gabor_conds # Conditions for pulsed- and steady-pedestal paradigms

random.seed()
   
#logging.console.setLevel(logging.DEBUG)  # get messages about the sound lib as it loads
event.globalKeys.add(key='escape', func=core.quit)


#============================= setup files for saving ===================================================#
expName='Gabor'
expInfo={'1. Participant Number':'','2. Nth Set':'','3. Nth Experiment':''}
dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)

if dlg.OK==False: core.quit() #user pressed cancel
expInfo['date']=data.getDateStr()#add a simple timestamp
expInfo['expName']=expName

sbjIdx = str(expInfo['1. Participant Number'])
setIdx = str(expInfo['2. Nth Set'])
expIdx = str(expInfo['3. Nth Experiment'])
myDlg = gui.Dlg(title="Information check")
myDlg.addText('Is this information correct?')
myDlg.addText('Participant Number:'+ sbjIdx)
myDlg.addText('Nth Set:' + setIdx)
myDlg.addText('Nth Experiment:' + expIdx)

ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
if myDlg.OK:  # or if ok_data is not None
    pass
else:
    print('user cancelled')
    core.quit()
#=======================  Conditions ============================#
WHor = 800; WVer = 600; Wsize = (WHor, WVer)
size = 6
Numframe = 3
#Numframe = 3 # 85HZ : 11.77 *3 frames = 35.31 ms

trialN=30
adaptTime=30
   
beforebeep=3; BeepDur=0.2; afterbeep=0.3
Textheight = 0.6; Tcolor= 'black'; textPos=(0,1)
lineWid = 0.5  # Fixation

ThisExp = Gabor_conds.participants[int(sbjIdx)-1][int(setIdx)-1][int(expIdx)-1]
#print(ThisExp)

color = ThisExp[0]          # color
PulsedSteady = ThisExp[1]   # Pulsed or Steady
opac = ThisExp[2]           # contrast
sf = ThisExp[3]             # sf

# Random location of Target: Left or Right 
preLR=list(range(trialN)) 
random.shuffle(preLR)
TargRan=[];
for randomLR in preLR:
    #print(preLR[randomLR]%2)
    if preLR[randomLR]%2 == 0: #Target on Left
        TargRan.append([0,1])
    else: #Target on Right
        TargRan.append([1,0])
#print(TargRan)

# ======= To print out the details of the current condition that the observer has started ===== #
if color == Gabor_conds.re:
    colorStr='R'
    colorfStr='Red'
elif color == Gabor_conds.gn:
    colorStr='G'
    colorfStr='Green'
if PulsedSteady == Gabor_conds.pulsed:
    pedStr='P'
    pedfStr='Pulsed'
elif PulsedSteady == Gabor_conds.steady:
    pedStr='S'
    pedfStr='Steady'
if sf == Gabor_conds.lowSF:
    sfStr='L'
    sffStr='LowSF'
elif sf == Gabor_conds.highSF:
    sfStr='H'
    sffStr='HighSF'
    
#======================================
def sum():
    print("="*20+" SUMMARY "+"="*21) 
    print("Participant number: %s" %sbjIdx)
    print("Set Number: %s" %setIdx)
    print("Experiment number: %s" %expIdx)
    print(colorfStr+', ', pedfStr+', ', sffStr+', ', "%0.2f" % opac)
    print("="*50) 
#sum()

#======================================
# Directory
if int(sbjIdx) == 1:
    Pdir = "P1_Jaeseon"
elif int(sbjIdx) == 2:
    Pdir = "P2_Jeff"
elif int(sbjIdx) == 3:
    Pdir = "P3_Jim"
elif int(sbjIdx) == 4:
    Pdir = "P4_Rich"
elif int(sbjIdx) == 5:
    Pdir = "P5_Colin"
elif int(sbjIdx) == 6:
    Pdir = "P6_Austin"
elif int(sbjIdx) == 7:
    Pdir = "P7_Ben"
    
if int(setIdx) == 1:
    Sdir = "Set1"
elif int(setIdx) == 2:
    Sdir = "Set2"
elif int(setIdx) == 3:
    Sdir = "Set3"

# Set parent directory path
# Change the path below to the folder of your choice
parent_dir = r"C:\Users\UserName\Desktop\Gabor_data"

# Create parent directory if it doesn't exist
if not os.path.exists(parent_dir + os.path.sep + Pdir):
    path = os.path.join(parent_dir, Pdir)
    os.makedirs(path) # Create the directory 
    
# Create subdirectory if it doesn't exist
if not os.path.exists(parent_dir + os.path.sep + Pdir+ os.path.sep + Sdir):
    path = parent_dir + os.path.sep + Pdir
    subpath= os.path.join(path, Sdir)
    os.makedirs(subpath)
    
# Generate file name based on experiment information
fileName = parent_dir+ os.path.sep + Pdir + os.path.sep + Sdir + os.path.sep + '%s_%s%0.2f_P%s_Set%s_Exp%s_%s' %(expName, colorStr+pedStr+sfStr, opac, sbjIdx, setIdx, expIdx, expInfo['date'])
#print(fileName)

# Create a text file to save data
dataFile = open(fileName+'.txt', 'w')

# Write experiment details to the file
dataFile.write('P%s-Set%s-Exp%s: ' '%s, %s, %s, %0.2f\n\n' 
    % (sbjIdx, setIdx, expIdx, colorfStr, pedfStr, sffStr, opac))
    
# Write column headers to the file
dataFile.write('trial\t' 'QuestV\t' 'resp\t' 'correct\n')

# Set global clock for timing
globalClock = core.Clock()

# ======================== open window ============================== #

#DON'T FORGET TO CHECK YOUR MONITOR SETTING
win = visual.Window(allowGUI=False, colorSpace= "rgb255", color = color, monitor='testMonitor', allowStencil=True)

# Set parameters for recording frame intervals and dropped frames
win.recordFrameIntervals = True
win.refreshThreshold = 1/85 + 0.005

# Set logging level to warning and print number of dropped frames
logging.console.setLevel(logging.WARNING)
print('Overall, %i frames were dropped.' % win.nDroppedFrames)

fullScreen = (-WHor/2, WVer/2), (-WHor/2, -WVer/2), (WHor/2, -WVer/2), (WHor/2, WVer/2)
halfLeft= (-WHor/2, WVer/2), (-WHor/2, -WVer/2), (0, -WVer/2), (0, WVer/2)

# Create text stimuli for display in the window
afterAdapt = TextStim(win, text='Press the spacebar when you are ready \n\n'
    'to start to find your threshold.', colorSpace= "rgb255", height=Textheight, 
    pos=textPos, units='deg', color=Tcolor)
startText = TextStim(win, text='Adaptation for 30sec? \n\n\n' 
    '   <-- Yes / No -->' , 
    colorSpace= 'rgb255', pos=textPos, height=Textheight, units='deg', color=Tcolor)

#----------------------- Draw Fixation Guides ------------------------------------#
Line1= Line(win, start=(0,3.6), end=(0,8.5), units= 'deg', lineWidth= lineWid, lineColor= 'black', interpolate=True)
Line2= Line(win, start=(0,-3.6), end=(0,-8.5), units= 'deg', lineWidth= lineWid, lineColor='black', interpolate=True)
Line3= Line(win, start=(3.6,0), end=(8.5,0), units= 'deg', lineWidth= lineWid, lineColor='black', interpolate=True)
Line4= Line(win, start=(-3.6,0), end=(-8.5,0), units= 'deg', lineWidth= lineWid, lineColor='black', interpolate=True)

def Fixation():
    Line1.draw()
    Line2.draw()
    Line3.draw()
    Line4.draw()
    

# ===========<Contrasts for QUEST startVals> ============== #
# Contrast: opacity*stimRGB + (1-opacity)*backgroundRGB

if opac == Gabor_conds.c1:   # 0
    startV = opac+0.05
elif opac == Gabor_conds.c2: # 0.08
    startV = opac+0.055
elif opac == Gabor_conds.c3: # 0.16
    startV = opac+0.07
elif opac == Gabor_conds.c4: # 0.32
    startV = opac+0.09
elif opac == Gabor_conds.c5: # 0.48
    if PulsedSteady == Gabor_conds.pulsed:
        startV = opac+0.11
    elif PulsedSteady == Gabor_conds.steady:
        startV = opac+0.09
elif opac == Gabor_conds.c6: # 0.64
    if PulsedSteady == Gabor_conds.pulsed:
        startV = opac+0.12
    elif PulsedSteady == Gabor_conds.steady:
        startV = opac+0.1
        
#========================================== QUEST ==================================================================== #

quest = data.QuestHandler(startV, 0.05, pThreshold=0.7, gamma=0.01, ntrials=trialN, stopInterval=0.095, minVal=opac, maxVal=1)

#===================================================================================================================== #

GratingT = visual.GratingStim(win, tex='sin', colorSpace= "rgb255", color = color, units = 'deg', sf = sf, 
    size=size, pos=(0, 0), mask='gauss')
GratingTa = visual.GratingStim(win, tex='sin', colorSpace= "rgb255", color = color, units = 'deg', sf = sf, 
    opacity=opac, size=size, pos=(0, 0), mask='gauss')
GratingB = visual.GratingStim(win, tex='sin', colorSpace= "rgb255", color = color, units = 'deg', sf = sf, 
    size=size, pos=(0, 0), mask='gauss')
    
#--------------------------< Open Screen >--------------------------------#
event.Mouse(visible=False, newPos=None, win=None)
stencil = visual.Aperture(win, shape=halfLeft, units='pix')  # try shape='square'
trial = 0; trialDesign  = []; responses = ['left', 'right']
response = 0; correct= 0

def MMM():
    """
    Calculates the mean, mode, and median of a given set of data.
    Returns:
    bool: A Boolean value indicating whether the data has been successfully written to a file.
    """
    Mean=quest.mean()
    Mode=quest.mode()
    Median=quest.quantile(0.5)  # gets the median
    mmm=[round(Mean, 3), round(Mode, 3), round(Median,3)] 
    
    # Ensure that the calculated values are not less than a given opacity value.
    if Mean < opac:
        Mean = opac
    elif Mode < opac:
        Mode = opac
    elif  Median < opac:
        Median = opac
        
    # Print the mean value to the console.
    print("Threshold (mean): %0.3f" %Mean)
    
    # Add the calculated values to the data file.
    dataFile.write('Mean: %s\t Mode: %s\t Median: %s'% (mmm[0], mmm[1], mmm[2]))
    dataFile.flush()
    os.fsync(dataFile)
    written =True

def Beep():
    """
    Plays a high pitched beep sound and displays stimuli on the screen.
    If the platform is Windows, a fixation point is displayed on the screen.
    If the PulsedSteady variable is equal to Pedestal[1], two stimuli are displayed on the screen.
    Finally, a 'ding' sound is played and the screen is flipped.
    """
    
    # Create a high pitched beep sound.
    highA = sound.Sound('A', octave=5, sampleRate=44100, secs=BeepDur, stereo=True)
    highA.setVolume(0.6)
    highA.play()
    
    # Check if the platform is Windows.
    if sys.platform == 'win32':
        Fixation()
        
        # Display two stimuli on the screen if it is a steady-pedestal condition.
        if PulsedSteady == Gabor_conds.Pedestal[1]:
            GratingTa.draw()
            
        # Play a 'ding' sound.
        ding = sound.Sound('ding')
        ding.play()
        win.flip()

def Mainloop():
    global trial, response, correct

    tarLR=TargRan[trial]
    TA=int(tarLR[0])
    TB=int(tarLR[1])
    
    T1=round(core.getTime(), 1)
    T2=round(core.getTime(), 1)
    while T2-T1 < beforebeep:
        T2=round(core.getTime(), 1)
        if PulsedSteady == Gabor_conds.Pedestal[1]:
            GratingTa.draw()
        Fixation()
        win.flip() 
    
    Beep()
    
    if PulsedSteady == Gabor_conds.pulsed:
        GratingT.opacity=opacities[TA]
        GratingB.opacity=opacities[TB]
        T3=round(core.getTime(), 1)
        T4=round(core.getTime(), 1)
        while T4-T3 < afterbeep:
            T4=round(core.getTime(), 1)
            Fixation()
            win.flip() 
        for frameN in range(Numframe): #for exactly 'Numframe'
            stencil.enabled = True
            stencil.inverted = False
            Fixation()
            GratingT.draw()
            stencil.inverted = True
            Fixation()
            GratingB.draw()
            win.flip()
        stencil.enabled = False
        Fixation()
        win.flip()
    elif PulsedSteady == Gabor_conds.steady:
        GratingT.opacity=opacities[TA]
        GratingB.opacity=opacities[TB]
        T3=round(core.getTime(), 1)
        T4=round(core.getTime(), 1)
        while T4-T3 < afterbeep:
            T4=round(core.getTime(), 1)
            GratingTa.draw()
            Fixation()
            win.flip() 
        for frameN in range(Numframe): #for exactly 'Numframe'
            stencil.enabled = True
            stencil.inverted = False
            Fixation()
            GratingT.draw()
            stencil.inverted = True
            Fixation()
            GratingB.draw()
            win.flip()
        stencil.enabled = False
        Fixation()
        GratingTa.draw()
        win.flip()

    # wait for response
    keys = []
    while not keys:
        keys = event.waitKeys(keyList=['left', 'right'])
        #print(keys, GratingT.opacity, GratingB.opacity)
        
    # check if it's the correct response:
    if opacities[TA] > opacities[TB]:
        #print("GratingT.opacity > GratingB.opacity")
        if responses[0] in keys:
            response = 0 #Left
            correct = 1
        else:
            response = 1 #Right
            correct = 0
            
    elif opacities[TB] > opacities[TA]:
        #print("GratingT.opacity < GratingB.opacity")
        if responses[1] in keys:
            response = 1 # Right
            correct = 1
        else:
            response = 0 # Left
            correct = 0
    elif opacities[TB] == opacities[TA]:
            correct = 0
        
    #print(GratingT.opacity, GratingB.opacity, response, correct) 
    
    # inform QUEST of the response, needed to calculate next level
    quest.addResponse(correct)
    trial = trial+1
    trialDesign.append([trial])
    trialDesign[trial-1].append(T_Opacity)
    trialDesign[trial-1].append(response)
    trialDesign[trial-1].append(correct)

    line = '\t'.join(str(i) for i in trialDesign[trial-1])
    line += '\n'
    dataFile.write(line)
    dataFile.flush()
    os.fsync(dataFile)
    written =True

    event.clearEvents()
    Fixation()
    win.flip()
    event.waitKeys(keyList=['space'])
    win.flip()

stencil.enabled = False

def adapt():
    Fixation()
    win.flip()
    core.wait(adaptTime)
    win.flip()

startText.draw()
win.flip()
KL = event.waitKeys(keyList=['left', 'right']) #Yes/No
#print(KL)
if KL == ['left']:
    adapt()
elif KL == ['right']:
    pass

afterAdapt.draw()
win.flip()
event.waitKeys()
win.flip()


for thisOpacity in quest:
    T_Opacity=round(thisOpacity,4)
    opacities = [T_Opacity, opac]
    Mainloop()
win.close() #closes the window
sum()
MMM()
#print(trial)
print("P%s-Set%s-Exp%s completed" %(sbjIdx, setIdx, expIdx))
core.quit()
