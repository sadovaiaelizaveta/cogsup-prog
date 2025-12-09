from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_SPACE, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_1, K_2

import math

experiment = design.Experiment(
    name="Blindspot",
    background_colour=C_WHITE,
    foreground_colour=C_BLACK
)
control.set_develop_mode()
control.initialize(experiment)

FPS = 60
MS_PER_FRAME = 1000 / FPS

def create_circle(radius, position=(0, 0)):
    circle = stimuli.Circle(radius, position=position, anti_aliasing=10)
    circle.preload()
    return circle

KEY_MAP = {
    K_DOWN: "down",
    K_UP: "up",
    K_LEFT: "left",
    K_RIGHT: "right",
    K_1: "1",
    K_2: "2"
}

def run_trial(eye_side="L"):
    experiment.add_data_variable_names(["eye", "key", "radius", "x", "y"])
    
    eye_name = "left" if eye_side == "L" else "right"
    
    instructions1 = stimuli.TextBox(
        f"Close your {eye_name} eye and fixate the cross. Move the circle until you find the blind spot.",
        size=(300, 100), position=(0, 50)
    )
    instructions2 = stimuli.TextBox(
        "Use arrow keys to move the circle and 1/2 to change its size. Press SPACE to start/stop.",
        size=(300, 100), position=(0, -50)
    )
    instructions1.preload()
    instructions2.preload()

    instructions1.present(True, False)
    instructions2.present(False, True)

    experiment.keyboard.wait(K_SPACE)

    fix_position = [300, 0] if eye_side == "L" else [-300, 0]
    fixation_cross = stimuli.FixCross(size=(150, 150), line_width=10, position=fix_position)
    fixation_cross.preload()

    circle_radius = 75
    circle_stim = create_circle(circle_radius)

    fixation_cross.present(True, False)
    circle_stim.present(False, True)

    x, y = 0, 0
    experiment.screen.clear()

    while True:
        key, _ = experiment.keyboard.wait(
            keys=[K_DOWN, K_UP, K_LEFT, K_RIGHT, K_1, K_2, K_SPACE]
        )

        if key == K_DOWN:
            y -= 8
        elif key == K_UP:
            y += 8
        elif key == K_LEFT:
            x -= 8
        elif key == K_RIGHT:
            x += 8
        elif key == K_1:
            circle_radius += 5
        elif key == K_2:
            circle_radius -= 5
        elif key == K_SPACE:
            experiment.data.add([eye_side, "space", circle_radius, x, y])
            break

        experiment.data.add([eye_side, KEY_MAP[key], circle_radius, x, y])

        circle_stim = create_circle(circle_radius, position=(x, y))
        fixation_cross.present(True, False)
        circle_stim.present(False, True)

control.start(subject_id=1)
run_trial("R")
control.end()
