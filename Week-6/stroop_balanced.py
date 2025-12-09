from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_r, K_b, K_g, K_o
import random
import itertools

COLORS = ["red", "blue", "green", "orange"]
KEYS = [K_r, K_b, K_g, K_o]
COLOR_TO_KEY = dict(zip(COLORS, KEYS))

NUM_BLOCKS = 2
TRIALS_PER_BLOCK = 16

INSTR_START = """
Indicate the font color of each word.

Press:
R for red
B for blue
G for green
O for orange

Press SPACE to continue.
"""

INSTR_MID = """You have completed block {block_num} of {total_blocks}.
Take a short break, then press SPACE to continue."""
INSTR_END = """Well done! The experiment is complete.

Press SPACE to exit."""

FEEDBACK_INCORRECT = "X"

def preload_stimuli(stim_list):
    for s in stim_list:
        s.preload()

def draw_for_time(*stimuli_list):
    t0 = exp.clock.time
    exp.screen.clear()
    for s in stimuli_list:
        s.present(clear=False, update=False)
    exp.screen.update()
    return exp.clock.time - t0

def show_for(*stimuli_list, duration=1000):
    dt = draw_for_time(*stimuli_list)
    exp.clock.wait(max(0, duration - dt))

def show_instructions(text):
    scr = stimuli.TextScreen(text=text, heading="Instructions", text_justification=0)
    scr.present()
    exp.keyboard.wait()

def get_derangements(lst):
    results = []
    for p in itertools.permutations(lst):
        if all(orig != p[i] for i, orig in enumerate(lst)):
            results.append(list(p))
    return results

exp = design.Experiment(
    name="Stroop Balanced",
    background_colour=C_WHITE,
    foreground_colour=C_BLACK
)
exp.add_data_variable_names(['block_id', 'trial_id', 'trial_type', 'word', 'color', 'RT', 'correct'])

control.set_develop_mode()
control.initialize(exp)

fix_cross = stimuli.FixCross()
fix_cross.preload()

text_stims = {w: {c: stimuli.TextLine(w, text_colour=c) for c in COLORS} for w in COLORS}
preload_stimuli([text_stims[w][c] for w in COLORS for c in COLORS])

feedback_correct = stimuli.TextLine("")
feedback_incorrect = stimuli.TextLine(FEEDBACK_INCORRECT)
preload_stimuli([feedback_correct, feedback_incorrect])

def run_trial(block_id, trial_id, trial_type, word, color):
    stim = text_stims[word][color]
    show_for(fix_cross, duration=500)
    stim.present()
    key, rt = exp.keyboard.wait(KEYS)
    correct = key == COLOR_TO_KEY[color]
    exp.data.add([block_id, trial_id, trial_type, word, color, rt, correct])
    feedback = feedback_correct if correct else feedback_incorrect
    show_for(feedback, duration=1000)

PERMS = get_derangements(COLORS)

subject_id = 1
perm_index = (subject_id - 1)
perm = PERMS[perm_index]

trial_list = (
    [{"trial_type": "match", "word": c, "color": c} for c in COLORS] +
    [{"trial_type": "mismatch", "word": w, "color": c} for w, c in zip(COLORS, perm)]
)

blocks = []
repeat_factor = TRIALS_PER_BLOCK // len(trial_list)
for b in range(1, NUM_BLOCKS + 1):
    b_trials = trial_list * repeat_factor
    random.shuffle(b_trials)
    block_trials = [{"block_id": b, "trial_id": i, **t} for i, t in enumerate(b_trials, 1)]
    blocks.append(block_trials)

control.start(subject_id=subject_id)
show_instructions(INSTR_START)
for block_id, block in enumerate(blocks, 1):
    for trial in block:
        run_trial(**trial)
    if block_id != NUM_BLOCKS:
        show_instructions(INSTR_MID.format(block_num=block_id, total_blocks=NUM_BLOCKS))
show_instructions(INSTR_END)
control.end()
