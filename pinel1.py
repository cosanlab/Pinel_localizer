
from __future__ import division
from psychopy import prefs
from psychopy import sound, visual, event, core, gui, logging
from collections import OrderedDict
import random
import os
import glob 
import random, copy, time
import pandas as pd

prefs.general['audioLib'] = ['pyo']

# # CREATE DIALOGUE SCREEN - enter subject ID and Run number 
# config_dialog = psy.gui.Dlg(title="Experiment Info")
# config_dialog.addField("Subject ID: ")
# config_dialog.show()

# # create dialogue screen that will show if file already exists- must choose to manually overwrite
# exists_dialog= psy.gui.Dlg(title="File Already Exists", labelButtonOK=u'Yes/overwrite', labelButtonCancel=u'Quit Program!',)
# exists_dialog.addText('File name already exists. Are you sure you want to overwrite?')

# #if user enters both subID and run number save these otherwise exit system
# if config_dialog.OK:
#         subID = config_dialog.data[0]
# else:
#         sys.exit("Canceled at configuration dialog.")

# #create file w/subId and RunNum in name
# fName= 'Pinel_id%s.txt' % (subID)

#Set experiment globalss
base_dir='/Users/antoniahoidal/Desktop/Cosan/Projects/test_scan_params/'
data_dir=os.path.join(base_dir, 'Data')
stim_dir=os.path.join(base_dir, 'stim')

testWinSize=(640,480)
expWinSize=(1280,1024)

#triggers
testTrigger='space'
expTrigger='k'

textColor = 'white'
textFont = 'Arial'
textHeight = .25


#set durations for different stimuli types
visual_dur=.250
visual_black_dur=.100
click_dur= .800
checker_dur= 1.3
blank_dur= .800


# #SETUP DATAFILE
# if not os.path.exists(data_dir):
#     os.mkdir(data_dir)
# #make sure we don't overwrite a file- must click okay to overwrite
# fPath= os.path.join(data_dir,fName)

# if os.path.exists(fPath):
#     exists_dialog.show()
#     if exists_dialog.OK: 
#         data_file= open(fPath,'w')
#     else: 
#         sys.exit('Program ending!')
# else:
#     data_file= open(fPath, 'w')


#create window and clocks
window = visual.Window([800, 800], color=[-1])
window.setRecordFrameIntervals(True)
logging.console.setLevel(logging.WARNING)
timer = core.Clock()
clock = core.Clock()


#create screens
fixation= visual.TextStim(win=window, name='fixation',
    text='+',
    color= textColor,
    font= textFont,
    height= textHeight)

Text=visual.TextStim(win=window,name='Text',
    text="", 
    color= textColor,
    font= textFont, 
    height= textHeight)

wait_stim = visual.TextStim(win=window,name='waitText',
    text="Waiting for scanner", 
    color= textColor,
    font= textFont, 
    height= textHeight)

blank= ''

vert_pic1=os.path.join(stim_dir, 'checherboardVnb.bmp')
vert_pic2= os.path.join(stim_dir, 'checherboardVpb.bmp')

ho_pic1=os.path.join(stim_dir, 'checherboardHnb.bmp')
ho_pic2= os.path.join(stim_dir, 'checherboardHpb.bmp')

#calc tasks
calc1=['calculate', 'sixteen', 'minus', 'eight']
calc2=['calculate', 'ten', 'minus', 'two']
calc3=['calculate', 'eleven', 'minus', 'nine']
calc4=['calculate', 'twelve', 'minus', 'four']
calc5= ['calculate', 'nineteen', 'minus', 'six']
calc6=['calculate', 'sixteen', 'minus', 'two']
calc7=['calculate', 'thirteen', 'minus', 'seven']
calc8=['calculate', 'nineteen', 'minus', 'seven']
calc9=['calculate', 'eleven', 'minus', 'three']
calc10=['calculate', 'seventeen', 'minus', 'six']

vis_subtraction=[calc1,calc2,calc3, calc4,calc5,calc6,calc7,calc8,calc9,calc10]

#visual reading tasks
read1=['the storm', 'frightened', 'the animals', 'at the zoo']
read2=['the cats', 'are looking', 'for a bird', 'on the wall']
read3=['the keep', 'of the castle', 'falls', 'into ruin']
read4=['we saw', 'the march', 'from', 'the balcony']
read5=['bears', 'are fond of', 'salmon', 'and honey']
read6=['in town', 'we easily', 'find', 'a taxi']
read7=['the cold', 'of winter', 'froze', 'the lake']
read8= ['there are', 'many', 'bridges', 'in Paris']
read9= ['the rain', 'has made', 'the road', 'dangerous']
read10= ['roses', 'are nice', 'but', 'they prick']

sentences=[read1,read2,read3,read4,read5,read6,read7,read8,read9,read10]

# visual motor tasks
visual_left= ['press', 'three times', 'on the', 'left button']
visual_right= ['press', 'three times', 'on the', 'right button']
vis_motor= [visual_left,visual_right]
#create lists of audio files
subtraction= glob.glob(os.path.join(stim_dir,'calc*'))  #make list of image path names
#subtraction= random.shuffle(audio_sub)

audio_sentence = glob.glob(os.path.join(stim_dir,'ph*'))  #make list of image path names
print audio_sentence
#audio_sentence= random.shuffle(audio_sentence)

press_left= os.path.join(stim_dir, 'clic3G.wav')
press_right= os.path.join(stim_dir, 'clic3D.wav')
    
# Make two wedges (in opposite contrast) and alternate them for flashing
ho_check1 = visual.ImageStim(window, image= ho_pic1,name= os.path.split(ho_pic1)[-1], pos=(0.0,0.0))  # this stim changes too much for autologging to be useful
  
ho_check2 = visual.ImageStim(window, image= ho_pic2,name= os.path.split(ho_pic2)[-1], pos=(0.0,0.0))# this stim changes too much for autologging to be useful

vert_check1 = visual.ImageStim(window, image= vert_pic1, name= os.path.split(vert_pic1)[-1], pos=(0.0,0.0))  # this stim changes too much for autologging to be useful
    
vert_check2 = visual.ImageStim(window, image= vert_pic2, name= os.path.split(vert_pic2)[-1], pos=(0.0,0.0))# this stim changes too much for autologging to be useful
check=[vert_check1, vert_check2, ho_check1, ho_check2]
print check

#onset type
task_order = OrderedDict([("audio1", audio_sentence[0]), 
("audio2", audio_sentence[1]),
("visual3", "blank"),
("checker4", "ho_check"),
("visual5", vis_motor[0]),
("audio6", subtraction[0]),
("audio7", "press_left"),
("audio8", subtraction[1]),
("visual9", visual_right),
("audio10", "press_right"),
("audio11", subtraction[2]),
("checker12", "vert_check"),
("visual13", sentences[0]),
("visual14", vis_subtraction[0]),
("visual15", vis_subtraction[1]),
("visual16", sentences[1]),
("visual17", sentences[2]),
("visual18",  "blank"),
("visual19",  "blank"),
("visual20", vis_subtraction[2]),
("visual21",  "ho_check"),
("visual22", visual_right),
("visual23",  "blank"),
("audio24",  "press_left"),
("audio25", "press_right"),
("visual26", vis_subtraction[3]),
("visual27",  "blank"),
("visual28",  "blank"),
("visual29", sentences[3]),
("visual30", vis_motor[0]),
("audio31", subtraction[3]),
("visual32",  "blank"),
("checker33", "vert_check"),
("visual34",  "blank"),
("visual35",  "blank"),
("visual36",  "blank"),
("visual37", sentences[4]),
("visual38",  "blank"),
("visual39",  "blank"),
("audio40", "press_right"),
("audio41", subtraction[4]),
("checker42", "vert_check"),
("audio43",  sentences[2]),
("visual44",  "blank"),
("visual45", vis_subtraction[4]), 
("visual46", sentences[5]),
("visual47", sentences[6]), 
("checker48", "vert_check"), 
("visual49", vis_motor[0]),
("audio50", subtraction[5]), 
("visual51",  "ho_check"),
("audio52",  sentences[3]), 
("checker53", "vert_check"), 
("visual54", vis_subtraction[5]), 
("visual55", vis_motor[0]),
("audio56",  sentences[4]), 
("visual57", vis_subtraction[6]), 
("visual58", visual_right), 
("visual59", sentences[7]), 
("visual60",  "ho_check"),
("visual61",  "blank"),   
("visual62",  "blank"), 
("visual63",  "blank"),   
("visual64",  "ho_check"), 
("visual65", sentences[8]), 
("visual66", vis_subtraction[7]),
("audio67",  sentences[5]),
("audio68",  sentences[6]), 
("checker69", "vert_check"),
("checker70", "vert_check"),
("checker71", "vert_check"),
("audio72", "press_right"),
("audio73", "press_right"),
("visual74",  "ho_check"),
("audio75",  sentences[7]),
("visual76",  "ho_check"),
("audio77",  "press_left"),
("visual78", vis_motor[0]),
("audio79",  sentences[8]),
("audio80", subtraction[6]),
("visual81",  "blank"),
("visual82",  "blank"),
("visual83", vis_subtraction[8]),
("visual84",  "ho_check"),
("visual85", sentences[9]),
("visual86", visual_right),
("visual87", visual_right),
("audio88",  sentences[9]),
("checker89", "vert_check"),
("visual90",  "ho_check"),
("visual91",  "ho_check"),
("visual92",  "blank"),
("audio93",  "press_left"),
("checker94", "vert_check"),
("visual95",  "blank"),
("audio96", subtraction[7]),
("visual97", vis_subtraction[9]),
("audio98",  "press_left"),
("audio99", subtraction[8]),
("audio100", subtraction[9])])

#print task_order
ITIs=[2.4, 3.3, 3.0, 2.7, 3.6, 3.0, 2.7, 3.0, 3.0, 3.0, 3.3, 2.4, 3.6, 2.7, 3.0, 3.3, 2.7, 3.0, 2.7, 3.3, 2.7, 3.6, 3.0, 2.4, 3.6, 3.0, 2.4, 3.0, 3.6, 2.7, 3.3, 3.0, 3.0, 3.0, 3.0, 3.0, 2.4, 3.3, 3.0, 2.7, 3.3, 2.7, 3.6, 2.4, 3.6, 2.7, 2.7, 3.0, 3.3, 2.7, 3.6, 3.0, 3.0, 3.0, 2.4, 3.3, 2.7, 3.3, 3.0, 3.0, 3.0, 3.3, 2.4, 3.3, 3.3, 3.0, 3.0, 2.7, 3.3, 3.0, 2.7, 3.0, 3.0, 2.7, 3.3, 3.0, 3.0, 3.3, 2.7, 3.3, 3.0, 3.0, 2.4, 3.3, 3.0, 2.7, 3.0, 3.6, 2.7, 3.0, 3.0, 2.7, 3.0, 3.3, 2.7, 3.6, 3.0, 2.4, 3.3]


experimentStart=clock.getTime()
timer = core.Clock()
#main experiment loop
ITI_counter=0
for key, task in task_order.items():
    print key
    # if task is 
    if "checker" in key:
        t = 0
        rotationRate = 0.1  # revs per sec
        flashPeriod = 0.1  # seconds for one B-W cycle (ie 1/Hz)
        
        preztime=clock.getTime()- experimentStart

        timer.add(checker_dur)
        while timer.getTime()<0:
            if "vert_check" in task:
                t = clock.getTime()
                if t % flashPeriod < flashPeriod / 4.0:  # more accurate to count frames

                    stim = check[0]
                else:
                    stim = check[1]
                #stim.ori = t * rotationRate * 360.0  # set new rotation
                stim.draw()
                window.flip()

            else:
                t = clock.getTime()
                if t % flashPeriod < flashPeriod / 2.0:  # more accurate to count frames
                   stim = check[2]
                else:
        
                   stim = check[3]
                #stim.ori = t * rotationRate * 360.0  # set new rotation
                stim.draw()
                window.flip()
 
    elif "audio" in key:

        if "press_right" in task:
                        #create sound stimuli
            audio_file=sound.Sound(press_right)
            
            # get duration of sound stimuli
            dur=audio_file.getDuration()
            
            #get presentation time and write to file
            preztime=clock.getTime()- experimentStart
            #play sound file
            audio_file.play()
            time.sleep(dur)
            
            #wait for audio file to play
            #timer.add(dur)
            #timer.add(.800)
            #while timer.getTime()<0:
               #pass
  
        elif "press_left" in task:
                                    #create sound stimuli
            audio_file=sound.Sound(press_left)
            
            # get duration of sound stimuli
            dur=audio_file.getDuration()
            
            #get presentation time and write to file
            preztime=clock.getTime()- experimentStart
            #play sound file
            audio_file.play()
            time.sleep(dur)

        else:
            print task
            #create sound stimuli
            audio_file=sound.Sound(task)
            
            # get duration of sound stimuli
            dur= audio_file.getDuration()
            
            #get presentation time and write to file
            preztime=clock.getTime()- experimentStart
            print preztime
            #play sound file
            audio_file.play()
            time.sleep(dur)
            print clock.getTime()- experimentStart
               
    else: 
    #"visual" in key:
        if "blank" in task:
            Text.text= ""
            Text.draw()
            window.flip()
            timer.add(blank_dur)
            while timer.getTime()<0:
               pass

        else:
            for word in task:
                Text.text= word
                Text.draw()
                window.flip()
            
                preztime=clock.getTime()- experimentStart
                timer.add(visual_dur)
                while timer.getTime()<0:
                   pass
                
                Text.text=''
                Text.draw()
                window.flip()
                timer.add(visual_black_dur)
                while timer.getTime()<0:
                   pass
    #present the SOA
    print("SOA%s" % str(ITI_counter+1)) 
    print clock.getTime()- experimentStart
    Text.text='+'
    Text.draw()
    window.flip()
    timer.add(ITIs[ITI_counter])
    while timer.getTime()<0:
        pass
    print clock.getTime()- experimentStart
    ITI_counter+=1             
    if event.getKeys():
        window.close()
        core.quit()

#data_file.close()
window.close()
core.quit()