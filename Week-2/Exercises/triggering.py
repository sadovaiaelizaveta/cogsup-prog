from expyriment import design, control, stimuli

exp = design.Experiment(name="Launching with Spatial Gap")
control.set_develop_mode()
control.initialize(exp)

spatial_gap = 50  
red_square = stimuli.Rectangle(size=(50, 50), colour=[250, 0, 0], position=[-400, 0])
green_square = stimuli.Rectangle(size=(50, 50), colour=[0, 250, 0], position=[0 + spatial_gap, 0])

control.start(subject_id=1)

red_square.present(clear=True, update=False)
green_square.present(clear=False, update=True)
exp.clock.wait(1000)


for step in range(40):
    red_square.move((10, 0))
    red_square.present(clear=True, update=False)
    green_square.present(clear=False, update=True)
    exp.clock.wait(20)

for step in range(40):
    green_square.move((10, 0))
    red_square.present(clear=True, update=False)
    green_square.present(clear=False, update=True)
    exp.clock.wait(20)

exp.clock.wait(1000)

control.end()
