#!/usr/bin/env python
"""
Simple example of a full screen application with a vertical split.
This will show a window on the left for user input. When the user types, the
reversed input is shown on the right. Pressing Ctrl-Q will quit the application.
"""
from __future__ import unicode_literals

from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import VSplit, HSplit, Window, WindowAlign
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.widgets import RadioList, Button, TextArea
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit import HTML, print_formatted_text
from prompt_toolkit.styles import Style
import os


from prompt_toolkit.shortcuts import message_dialog

class myButton(Button):
    threadsDir = "threads" + os.sep
    def __init__(self, text, name, myControls, args=None, width=22):
        super().__init__(text, self.onClick, width)
        self.name = name
        self.args = args
        self.myControls = myControls

    def read_File(self):
        filename = self.threadsDir + self.name + os.sep + self.name + ".txt"
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
                txt = " "
                for s in lines:
                    txt = txt + s + "\n"
                return txt 
        else:
            return None

    def onClick(self):
        content = self.read_File()
        if  content is not None:
            self.myControls.content.text = HTML( content )


class myControls():
    

    def __init__(self):
        
        self.content = FormattedTextControl(" ",focusable=True)
        self.sender = TextArea (focus_on_click=True, height=2)#, multiline=False)
        self.sender.accept_handler = self.onEnter
        
        
    def onEnter(self,buff):
        #print (buff)
        print (self.content.text)
        #self.content.text =self.content.text.merge_formatted_text(HTML(buff.text))  #self.content.text + HTML(buff.text)
        #self.sender.text = ''
        
ctrls = myControls()
myButtons = list()





threadsDir = "threads" + os.sep
dirs = os.listdir(threadsDir)
for d in dirs:
    myButtons.append(myButton(d,myControls=ctrls, name=d))

body = VSplit([
    HSplit(myButtons),

    # A vertical line in the middle. We explicitly specify the width, to make
    # sure that the layout engine will not try to divide the whole width by
    # three for all these windows.
    Window(width=1, char='|', style='class:line'),

    #Window(content)
    HSplit(list([
            Window(ctrls.content), 
            Window(height=1, char='=', style='class:line'),
            ctrls.sender]))
])

# 2. Key bindings
kb = KeyBindings()

# Key bindings.
kb = KeyBindings()
kb.add('tab')(focus_next)
kb.add('s-tab')(focus_previous)

@kb.add('c-q')
def _(event):
    " Quit application. "
    event.app.exit()

@kb.add('c-a')
def _(event):
    " focus text. "
    event.app.layout.focus(ctrls.sender)

    


# 3. The `Application`
application = Application(
    layout=Layout(body),
    key_bindings=kb,
    full_screen=True)


def run():
    application.run()


if __name__ == '__main__':
    run()