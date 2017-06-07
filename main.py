#main in charge of kivy GUI and scheduling data fetching
import time
from InfotauluData import localSyncTime, updateDataEspoo, updateDataHelsinki
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.instructions import Canvas, CanvasBase
from kivy.graphics import Rectangle


setScreenResolution = (1920, 1200) # 1920, 1200 / 1360, 768
fullScreenMode = True
background = 'kesa2bv2.png'
foreground = 'grafiikka.png'
destinationFontSize = '52sp'
clockFontSize = '82sp'
busDataFont = 100
versionString = "v 2.1929583f TietixLabs™ Inc.©"

class OverLayout(FloatLayout):

    def __init__(self, **kwargs):

        super(OverLayout, self).__init__(**kwargs)

        self.busBoxes = BusBoxLayout(pos_hint={'x':0, 'y':0})
        self.topBar = BoxLayout(orientation='horizontal')
        self.canvas.add(Rectangle(source=background, pos=self.pos, size=setScreenResolution))
        self.canvas.add(Rectangle(source=foreground, pos=self.pos, size=setScreenResolution))

        self.add_widget(Label(markup=True,
                              text='[color=f0dec0]'+versionString+'[/color]',
                              pos_hint={'x':-0.44, 'y':-0.49}))

        self.topBar.add_widget(Label(markup=True,
                                     text='[color=f0dec0][font=Orbitron-Medium]ESPOON SUUNTA[/font][/color]',
                                     font_size=destinationFontSize,
                                     pos_hint={'x':0, 'y':0.45}))

        self.clock = Label(markup=True,
                           text='[color=f44747][font=Orbitron-Regular]'+str(time.strftime("%H:%M"))+'[/font][/color]',
                           size_hint=(0.2, 0.1), pos_hint={'x':0, 'y':0.9},
                           font_size=clockFontSize)

        self.topBar.add_widget(self.clock)
        self.topBar.add_widget(Label(markup=True,
                                     text='[color=f0dec0][font=Orbitron-Medium]HELSINGIN SUUNTA     [/font][/color]',
                                     font_size=destinationFontSize,
                                     pos_hint={'x':0, 'y':0.45}))

        self.add_widget(self.topBar)
        self.add_widget(self.busBoxes)


    def internetUpdate(self, *args):
        self.busBoxes.internetUpdate()


    def localUpdate(self, *args):
        self.busBoxes.localUpdate()
        self.clock.text = '[color=f44747][font=Orbitron-Regular]'+str(time.strftime("%H:%M"))+'[/font][/color]'


class BusBoxLayout(BoxLayout):

    def __init__(self, **kwargs):

        super(BusBoxLayout, self).__init__(**kwargs)
        self.espoo = []
        self.helsinki = []
        self.orientation = 'horizontal'


    def getStack(self, dataIn):

        data = dataIn
        layout = StackLayout(orientation = 'tb-lr', padding=[110,160,0,0])
        currentTime = time.time()

        if len(data) > 0:
            for x in range(0, len(data[0])):
                deltaT = data[0][x] - currentTime
                if deltaT < 0:
                    # alle nollan poisto
                    data[0].pop(x)
                    data[1].pop(x)
                    data[2].pop(x)
                    break

            for x in range(0, len(data[0])):
                if x > 5:
                    break
                deltaT = data[0][x] - currentTime

                txt = ''

                #jos aika on alle 9min
                if deltaT < 540:
                    mins = str(int(deltaT / 60) + 1)
                    txt = mins + " min " + data[1][x] + " " +  data[2][x]
                    entry = Label(markup=True,
                                  text='[color=f44747][font=Oswald-Regular]'+txt+'[/font][/color]',
                                  font_size=busDataFont,
                                  text_size=(900, None),
                                  size_hint=(1.0, 0.15))

                else:
                    txt = time.strftime("%H:%M", time.localtime(data[0][x])) + " " + data[1][x] + " " + data[2][x]
                    entry = Label(markup=True,
                                  text='[color=f0dec0][font=Oswald-Regular]'+txt+'[/font][/color]',
                                  font_size=busDataFont,
                                  text_size=(900, None),
                                  size_hint=(1.0, 0.15))

                layout.add_widget(entry)

                #päivitys jos lista on liian lyhyt
                if len(data[0]) < 8:
                    BusBoxLayout.internetUpdate(self)

        else:
            entry = Label(text='empty',
                          font_size=100,
                          text_size=(900, None))


            layout.add_widget(entry)
            BusBoxLayout.internetUpdate(self)

        return layout


    def internetUpdate(self, *args):
        self.espoo = localSyncTime(updateDataEspoo())
        self.helsinki = localSyncTime(updateDataHelsinki())
        BusBoxLayout.localUpdate(self)


    def localUpdate(self, *args):
        self.clear_widgets()
        self.add_widget(BusBoxLayout.getStack(self, self.espoo))
        self.add_widget(BusBoxLayout.getStack(self, self.helsinki))


class InfotauluApp(App):

    def __init__(self, **kwargs):
        super(InfotauluApp, self).__init__(**kwargs)


    def build(self):

        overLayout = OverLayout()
        Clock.schedule_interval(overLayout.localUpdate, 1.0)
        Clock.schedule_interval(overLayout.internetUpdate, 200.0)

        return overLayout


if __name__ == '__main__':
    Window.size = setScreenResolution
    Window.fullscreen = fullScreenMode
    InfotauluApp().run()
