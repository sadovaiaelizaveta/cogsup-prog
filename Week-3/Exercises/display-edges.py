import expyriment
from expyriment import design, stimuli, control

exp = expyriment.design.Experiment()
control.set_develop_mode()
control.initialize(exp)

width, height = exp.screen.size
print(width, height)

rectangle1 = stimuli.Rectangle(size=(width*0.5, height**0.5), colour=(250,0,0), line_width=1, position=(-width // 2, -height // 2))
rectangle2 = stimuli.Rectangle(size=(width*0.05, height**0.05), colour=(250,0,0), line_width=1, position=(width // 2, height // 2))
rectangle3 = stimuli.Rectangle(size=(width*0.05, height**0.05), colour=(250,0,0), line_width=1, position=(-width // 2, height // 2))
rectangle4 = stimuli.Rectangle(size=(width*0.05, height**0.05), colour=(250,0,0), line_width=1, position=(width // 2, -height // 2))
rectangle1.present(update=False, clear=True)
rectangle2.present(update=False, clear=False)
rectangle3.present(update=False, clear=False)
rectangle4.present(update=True, clear=False)

exp.clock.wait(10000)

control.end()