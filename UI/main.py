from kivy.uix.video import Video
from kivy.uix.videoplayer import VideoPlayer
import sys
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from numpy import *
from functools import partial
import matplotlib
matplotlib.use('Agg')
import pylab as pl
from kivy.garden.graph import Graph, LinePlot
from kivy.uix.widget import Widget
import numpy as np
import math
from kivy.core.window import Window
import datetime
import time

#get data for patient
#with open('choosePatient.txt','r') as f:
#    patientName=f.read()
#data = dta.split(',')
#fileName ='videos/' + patientName + ".mp4"

#dataMatrix1 = genfromtxt('DemoEEGFile.txt')
#x = dataMatrix1[:,0]
#x = x - 5.539
#y = dataMatrix1[:,1]

xmin = 0#math.trunc(x[0])
global ymin #math.trunc(min(y))
xmax = xmin+1
xGlobalmax = 60#math.trunc(x[len(x)-1])
global ymax #math.trunc(max(y))#math.trunc(y[len(y)-1])

#ymax = math.trunc(max(y))#math.trunc(y[len(y)-1])

class HomeScreen(Screen):
    pass
class FirstScreen(Screen):
    pass
class SecondScreen(Screen):
    pass
class ThirdScreen(Screen):
    pass
class FourthScreen(Screen):
    pass
class FifthScreen(Screen):
    pass
class MyScreenManager(ScreenManager):
    pass


load_screen = Builder.load_string('''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
ScreenManager:
    id: 'MyScreenManager'
    transition: FadeTransition()
    HomeScreen:
    SecondScreen:
    FirstScreen:
    ThirdScreen:
    FourthScreen:
    FifthScreen:
<ThirdScreen>:
    name: 'Third'
    FloatLayout:
	BoxLayout:
	    Button:
    		text: 'Home'
    		size_hint: .1, .1
    		on_release: app.root.current = 'Home'
	    Button:
    		text: 'Back'
    		size_hint: .1, .1
    		on_release: app.root.current = 'Home'
	    Button:
    		text: 'Next'
    		size_hint: .1, .1
    		on_press: app.chooseMontage(app.root.get_screen('Fifth'))
    		on_release: app.root.current = 'Fifth'
<FifthScreen>:
    name: 'Fifth'
    FloatLayout:
        BoxLayout:
            Button:
                text: 'Home'
                size_hint: .1, .1
                on_release: app.root.current = 'Home'
            Button:
                text: 'Back'
                size_hint: .1, .1
                on_release: app.root.current = 'Third'
            Button:
                text: 'Next'
                size_hint: .1, .1
                on_press: app.playVideo(app.root.get_screen('Fourth'))
                on_release: app.root.current = 'Fourth'


<HomeScreen>:
    name: 'Home'
    FloatLayout:
        Label:
            text: 'Neonatal EEG Monitoring System'
            font_size: 50
        BoxLayout:
            Button:
                text: 'Home'
                size_hint: .1, .1
                on_release: app.root.current = 'Home'
            Button:
                text: 'Run'
                size_hint: .1, .1
                on_release: app.root.current = 'First'
            Button:
                text: 'Review Data'
                size_hint: .1, .1
                on_press: app.makeGrid(app.root.get_screen('Third'))
                on_release: app.root.current = 'Third'
<SecondScreen>:
    name: 'Second'
    BoxLayout:
	#Label:
	    #text: 'Neonatal EEG Monitoring System'
	BoxLayout:
	    Button:
	    	text: 'Home'
    		size_hint: .1,.1
    		on_release: app.root.current = 'Home'
	    Button: 
	    	text: 'Run EEG System'
	    	size_hint: .1,.1
#                on_release: sys.execfile('spiTest.py')
<FirstScreen>:
    name: 'First'
    FloatLayout:
	Label: 
		text: 'Patient Name (ex. MomonaYamagami)'
		pos_hint: {'x':0.2,'y':0.6}
		size_hint: .1,.1
		font_size: 15
	TextInput:
		id: name_input
		multiline: False
		size_hint: .2,.1
		pos_hint: {'x':0.5,'y':0.6}
	Label:
		text: 'Date (ex. 03.28.16)'
		pos_hint: {'x':0.2,'y':0.8}
		size_hint: .1,.1
		font_size: 15
	TextInput:
		id: date_input
		multiline: False
#		hint_text: app.getDate()#time.strftime('%m.%d.%y') #datetime.date.today()#'04.13.16' 
		size_hint: .2,.1
		pos_hint: {'x':0.5,'y':0.8}
    FloatLayout:
        BoxLayout:
            Button:
                text: 'Home'
                size_hint: .1, .1
                on_release: app.root.current = 'Home'
            Button:
                text: 'Back'
                size_hint: .1, .1
                on_release: app.root.current = 'Home'
            Button:
                text: 'Next'
                size_hint: .1, .1
                on_press: app.save(name_input.text, date_input.text)
                on_release: execfile("capture-file.py") 
                on_release: app.root.current = 'Home'
		#on_release: app.save(name_input.text, date_input.text)
<FourthScreen>:
    name: 'Fourth'
    FloatLayout:
        BoxLayout:
            Button:
                text: 'Home'
                size_hint: .1, .1
                on_release: app.root.current = 'Home'
            Button:
                text: 'Back'
                size_hint: .1, .1
#                on_press: app.do_screenshot(app.root.get_screen('Fourth'))
                on_release: app.root.current = 'Third'
            #Button:
            #    text: 'Next'
            #    size_hint: .1, .1
            #    on_release: app.root.current = 'Second'
''')

class ScreenManagerApp(App):

    Window.allow_vkeyboard = True
    Window.single_vkeybboard = True
    Window.docked_vkeyboard = True

#    def do_screenshot(self,screen):
        #Window.screenshot(name='screenshot.jpg')
#        screen.export_to_png('screenshot.png')

    def build(self):
        layout = GridLayout(cols=1,spacing=10,size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for i in range(30):
            btn = Button(text=str(i),size_hint_y=None,height=40)
            layout.add_widget(btn)
        root = ScrollView(size_hint=(None,None),size=(400,400),pos_hint={'center_x':.5, 'center_y':.5})
        return load_screen
    
    def save(self, name, date):
	f = open('patientData.txt','a')
	f.write('\n' + name + ',')
	f.write(date)
	f.close()
#    def saveName(self,name,btn):
#        btn.background_color = [0,1,0,1]
#        f = open('choosePatient.txt','w')
#        f.write(name)
#        f.close()
        #btn.background_color = [0,1,0,1]
#    def getDate(self):
#        return(time.strftime('%m.%d.%y'))    

    def chooseMontage(self,FifthScreen):
        # create scrolling for viewing patient data
        layout = GridLayout(cols=1,spacing=10,size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        #updated the for loop range
        for i in range(12):
            montageNum = 'Montage' + str(i)
            btn = Button(text=montageNum,size_hint_y=None,height=40)#,background_color=[1,0,0,1])
            btn.bind(on_release=partial(self.saveMontage,str(i),btn))
            layout.add_widget(btn)
        root = ScrollView(size_hint=(None,None),size=(800,420),pos_hint={'right':1,'top':1})#'Cen$
        root.add_widget(layout)
        FifthScreen.add_widget(root)

    def saveMontage(self,montageNum,btn, *args):
        if btn.background_color == [0,1,0,1]:
            btn.background_color = [1,1,1,1]
        else:
            btn.background_color = [0,1,0,1]
        f = open('chooseMontage.txt','w')
        f.write(montageNum)
        f.close()


    def makeGrid(self,ThirdScreen):
#    def __init__(self, **kwargs):
    	#get all patients stored in the file
	with open('patientData.txt','r') as f:
	    data=f.read()
	data = data.splitlines()
	num_lines = sum(1 for line in open('patientData.txt'))

	# create scrolling for viewing patient data
        layout = GridLayout(cols=1,spacing=10,size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        #updated the for loop range
        for i in range(sum(1 for line in open('patientData.txt'))):
            btn = Button(text=data[i],size_hint_y=None,height=40)#,background_color=[1,0,0,1])
            btn.bind(on_release=partial(self.saveName,data[i],btn))
            layout.add_widget(btn)
        root = ScrollView(size_hint=(None,None),size=(800,420),pos_hint={'right':1,'top':1})#'Center_x':.7, 'Center_y':.8})
        root.add_widget(layout)
        ThirdScreen.add_widget(root)
    def saveName(self,name,btn, *args):
        if btn.background_color == [0,1,0,1]:
            btn.background_color = [1,1,1,1]
        else:
            btn.background_color = [0,1,0,1]
        f = open('choosePatient.txt','w')
        f.write(name)
        f.close()
        

    def playVideo(self,FourthScreen):
	#get data for patient
	with open('choosePatient.txt','r') as f:
     	    patientName=f.read()
      	#data = data.split(',')
      	fileName ='videos/' + patientName + ".mp4"
        dataName = 'data/' + patientName + '_0.txt'	


	dataMatrix1 = genfromtxt('DemoEEGFile.txt')
	x = dataMatrix1[:,0]
	#x = x - 5.539
	y = dataMatrix1[:,1]
	
	xmin = math.trunc(x[0])
	ymin = math.trunc(min(y))#math.trunc(y[0])
	xmax = xmin+1
	xGlobalmax = math.trunc(x[len(x)-1])
	ymax = math.trunc(max(y))#math.trunc(y[len(y)-1])
	# create buttons
        btnRight = Button(text='Scroll', size_hint=(.05,1),pos_hint={'x':0.45})#,'y':0})
        btnLeft = Button(text='Scroll', size_hint=(.05,1),pos_hint={'left':1})			
        FourthScreen.add_widget(btnRight)
        FourthScreen.add_widget(btnLeft)
        
	# create graph
        graph = Graph()
        plot = LinePlot(mode='line_strip',color=[1,0,0,1])
        plot.points = [(x[i],y[i]) for i in xrange(len(x))]
        graph.add_plot(plot)
        graph.x_ticks_major=.5
        graph.xmin=xmin
        graph.xmax=xmax
        graph.ymin=ymin
        graph.ymax=ymax
        graph.y_ticks_major=10
        graph.xlabel='Time (min)'
        graph.ylabel='Brain Wave Amplitude (mV)'
        graph.y_grid = True
        graph.x_grid = True
        graph.size_hint=(0.4,0.9)
        graph.x_grid_label=True
        graph.y_grid_label=True

        # create video player
        video = VideoPlayer(source=fileName)
        video.play=False
        video.size_hint=(0.5,0.9)
        video.pos_hint={'right':1,'top':1}       

        graph.pos_hint={'x':0.05,'top':1}
        def moveRight(obj):
	    global xmin
            global xmax
            global xGlobalmax
            xmin=xmin+.5
            xmax=xmax+.5
            graph.xmin=xmin
            graph.xmax=xmax
            
            percent = 1-(xGlobalmax-xmin)/xGlobalmax
            video.seek(percent)

        btnRight.bind(on_release=moveRight)
        def moveLeft(obj):
            global xmin
            global xmax
            global xGlobalmax
            xmin=xmin-.5
            xmax=xmax-.5
            graph.xmin=xmin
            graph.xmax=xmax

            percent = 1-(xGlobalmax-xmin)/xGlobalmax
            video.seek(percent)
        btnLeft.bind(on_release=moveLeft)
        FourthScreen.add_widget(graph)
        FourthScreen.add_widget(video)



ScreenManagerApp().run()
