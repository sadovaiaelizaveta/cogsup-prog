from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_j, K_f
import random
import itertools

RESPONSE_KEYS = [K_j, K_f]
TRIAL_TYPES = ["match", "mismatch"]

BLOCKS = 2
TRIALS_PER_BLOCK = 16

COLORS = ["red", "blue", "green", "orange"]

def get_derangements(items):
    result = []
    for perm in itertools.permutations(items):
        if all(orig != perm[i] for i, orig in enumerate(items)):
            result.append(list(perm))
    return result

def preload_stims(stim_list):
    for s in stim_list:
        s.preload()

def draw_timed(*stimuli_list):
    start_time = exp.clock.time
    exp.screen.clear()
    for s in stimuli_list:
        s.present(clear=False, update=False)
    exp.screen.update()
    return exp.clock.time - start_time

def show_for(*stimuli_list, duration=1000):
    dt = draw_timed(*stimuli_list)
    exp.clock.wait(max(0, duration - dt))

def show_instructions(text):
    instr = stimuli.TextScreen(text=text, heading="Instructions", text_justification=0)
    instr.present()
    exp.keyboard.wait()

deranged_colors = get_derangements(COLORS)
trials = (
    [{"trial_type": "match", "word": c, "color": c} for c in COLORS] +
    [{"trial_type": "mismatch", "word": w, "color": c} for w, c in zip(COLORS, deranged_colors[0])]
)

INSTR_START = (
    "In this task, indicate whether the meaning of a word and the color of its font match.\n"
    "Press J if they match, F if not.\nPress SPACE to continue."
)
INSTR_MID = (
    "Halfway done! Take a short break, then press SPACE to continue with the second half."
)
INSTR_END = "Well done!\nPress SPACE to exit the experiment."

FEEDBACK_CORRECT = ""
FEEDBACK_INCORRECT = "X"

exp = design.Experiment(
    name="Stroop",
    background_colour=C_WHITE,
    foreground_colour=C_BLACK
)
exp.add_data_variable_names(['block_id', 'trial_id', 'trial_type', 'word', 'color', 'RT', 'correct'])

control.set_develop_mode()
control.initialize(exp)

fix_cross = stimuli.FixCross()
fix_cross.preload()

text_stims = {w: {c: stimuli.TextLine(w, text_colour=c) for c in COLORS} for w in COLORS}
preload_stims([text_stims[w][c] for w in COLORS for c in COLORS])

feedback_correct = stimuli.TextLine(FEEDBACK_CORRECT)
feedback_incorrect = stimuli.TextLine(FEEDBACK_INCORRECT)
preload_stims([feedback_correct, feedback_incorrect])

def run_trial(block_id, trial_id, trial_type, word, color):
    stim = text_stims[word][color]
    show_for(fix_cross, duration=500)
    stim.present()
    key, rt = exp.keyboard.wait(RESPONSE_KEYS)
    correct = (key == K_j) if trial_type == "match" else (key == K_f)
    exp.data.add([block_id, trial_id, trial_type, word, color, rt, correct])
    feedback = feedback_correct if correct else feedback_incorrect
    show_for(feedback, duration=1000)

control.start(subject_id=1)

show_instructions(INSTR_START)

for block_num in range(1, BLOCKS + 1):
    for trial_num in range(1, TRIALS_PER_BLOCK + 1):
        trial_type = random.choice(TRIAL_TYPES)
        word = random.choice(COLORS)
        color = word if trial_type == "match" else random.choice([c for c in COLORS if c != word])
        run_trial(block_num, trial_num, trial_type, word, color)
    if block_num != BLOCKS:
        show_instructions(INSTR_MID)

show_instructions(INSTR_END)

control.end()
