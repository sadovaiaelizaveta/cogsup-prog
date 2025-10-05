from expyriment import design, control, stimuli
from expyriment.misc.constants import K_SPACE

EXP_NAME = "Ternus demo"
bg_color = (0, 0, 0)
fg_color = (255, 255, 255)
tag_colors = [(255, 80, 80), (80, 255, 80), (80, 80, 255)]

exp = design.Experiment(EXP_NAME)
control.initialize(exp)


def present_for(obj, frames):
    """Present stimulus or list-of-stimuli for N frames (≈16.67 ms/frame)."""
    ms = int(round(frames * 1000.0 / 60.0))
    if isinstance(obj, (list, tuple)):
        # present all on one screen; clear only for the first
        for i, s in enumerate(obj):
            s.present(clear=(i == 0))
    else:
        obj.present()
    exp.clock.wait(ms)


def add_tags(big_circle, color):
    """Plot a small color-tag onto the big circle (before preload)."""
    w = big_circle.surface.get_width()
    h = big_circle.surface.get_height()
    tag_r = max(4, int(min(w, h) * 0.14))
    tag = stimuli.Circle(tag_r, colour=color)
    pos = (int(w * 0.62), int(h * 0.28))
    big_circle.plot(tag, position=pos)
    return big_circle


def make_circles(radius, spacing, add_color=False):
    """Create three circles centered at (-spacing,0),(0,0),(+spacing,0)."""
    xs = [-spacing, 0, spacing]
    circles = []
    for i, x in enumerate(xs):
        c = stimuli.Circle(radius, colour=fg_color)
        c.position = (x, 0)
        if add_color:
            add_tags(c, tag_colors[i % len(tag_colors)])
        c.preload()  # must preload after plotting tags
        circles.append(c)
    return circles


def run_trial(radius=40, isi_frames=1, add_color=False,
              frame_duration_frames=4, spacing_scale=2.2):
    """
    One Ternus trial:
      - show frame1 (three disks)
      - show ISI blank for isi_frames
      - show frame2 (shifted right by spacing)
    """
    spacing = int(radius * spacing_scale)
    frame1 = make_circles(radius, spacing, add_color)
    frame2 = make_circles(radius, spacing, add_color)
    for c in frame2:
        c.move((spacing, 0))

    blank = stimuli.BlankScreen(colour=bg_color)
    blank.preload()
                  
    present_for(frame1, frame_duration_frames)
    if isi_frames > 0:
        present_for(blank, isi_frames)
    present_for(frame2, frame_duration_frames)


control.start(skip_ready_screen=True)
exp.screen.clear()
stimuli.TextLine("Ternus demo\nPress SPACE to start").present()
exp.keyboard.wait(K_SPACE)

run_trial(radius=40, isi_frames=1, add_color=False, frame_duration_frames=4)

exp.clock.wait(300)

run_trial(radius=40, isi_frames=10, add_color=False, frame_duration_frames=4)
exp.clock.wait(300)

run_trial(radius=40, isi_frames=10, add_color=True, frame_duration_frames=4)

stimuli.TextLine("End of demo. Press SPACE to quit.").present()
exp.keyboard.wait(K_SPACE)
control.end()
