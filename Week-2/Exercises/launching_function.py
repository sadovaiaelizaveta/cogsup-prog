from expyriment import design, control, stimuli


def launching_event(temporal_gap=0, spatial_gap=0, speed_factor=1.0):
    """
    Display a horizontal launching event with configurable parameters.

    Parameters
    ----------
    temporal_gap : int
        Time in ms to wait between red reaching green and green starting to move.
        (0 = no temporal gap)
    spatial_gap : int
        Distance in pixels between the red and green squares at the start.
        (0 = no spatial gap, touching)
    speed_factor : float
        Speed of the green square relative to the red one.
        (1.0 = same speed, >1 = faster, <1 = slower)
    """

    exp = design.Experiment(name="Custom Launching Event")
    control.set_develop_mode()
    control.initialize(exp)

    steps = 40
    step_size = 10
    delay_per_step = 20 

    red_square = stimuli.Rectangle(size=(50, 50), colour=[250, 0, 0],
                                   position=[-400, 0])
    green_square = stimuli.Rectangle(size=(50, 50), colour=[0, 250, 0],
                                     position=[0 + spatial_gap, 0])

    control.start(subject_id=1)

    red_square.present(clear=True, update=False)
    green_square.present(clear=False, update=True)
    exp.clock.wait(1000)

    for _ in range(steps):
        red_square.move((step_size, 0))
        red_square.present(clear=True, update=False)
        green_square.present(clear=False, update=True)
        exp.clock.wait(delay_per_step)

    if temporal_gap > 0:
        exp.clock.wait(temporal_gap)

    for _ in range(steps):
        green_square.move((step_size * speed_factor, 0))
        red_square.present(clear=True, update=False)
        green_square.present(clear=False, update=True)
        exp.clock.wait(delay_per_step)

    exp.clock.wait(1000)

    control.end()
