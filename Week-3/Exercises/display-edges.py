import expyriment
from expyriment import design, stimuli, control

exp = expyriment.design.Experiment()
control.set_develop_mode()
control.initialize(exp)

rectangle1 = stimuli.Rectangle(size=(width**0.05, height**0.05 colour=[250,0,0]), colour=(250,0,0), line_width=1, position=(0,0))
rectangle2 = stimuli.Rectangle(size=(width**0.05, height**0.05 colour=[250,0,0]), colour=(250,0,0), line_width=1, position=(0,0))
rectangle3 = stimuli.Rectangle(size=(width**0.05, height**0.05 colour=[250,0,0]), colour=(250,0,0), line_width=1, position=(0,0))
rectangle4 = stimuli.Rectangle(size=(width**0.05, height**0.05 colour=[250,0,0]), colour=(250,0,0), line_width=1, position=(0,0))