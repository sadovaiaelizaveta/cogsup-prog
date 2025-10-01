from expyriment import design, control, stimuli
import expyriment.misc.geometry as geo
from expyriment.misc.constants import C_GREY

control.set_develop_mode()

experiment = design.Experiment(name="Shape Display", background_colour=C_GREY)
control.initialize(experiment)

screen_width, screen_height = experiment.screen.size
center_x, center_y = screen_width // 2, screen_height // 2
print((center_x, center_y))

rect_width = screen_width / 4
circle_radius = screen_width / 12

positions = [
    (rect_width, rect_width),
    (-rect_width, rect_width),
    (-rect_width, -rect_width),
    (rect_width, -rect_width)
]

main_square = stimuli.Rectangle((rect_width * 2, rect_width * 2), colour=C_GREY, position=(0, 0))

circle_colors = ["black", "black", "white", "white"]
circles = [stimuli.Circle(circle_radius, colour=col, position=pos) for col, pos in zip(circle_colors, positions)]

control.start(subject_id=1)

experiment.screen.clear()

for circle in circles:
    circle.present(clear=False, update=False)

main_square.present(clear=False, update=True)

experiment.keyboard.wait()

control.end()