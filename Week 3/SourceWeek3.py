# Stopwatch: The Game
# by @jbutewicz
import simplegui

# define global variables
is_running = False
stops = successes = time = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    return str(t / 600) + ":" + "%02d" % ((t / 10) % 60,) + "." + str(t % 10)

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global is_running
    timer.start()
    is_running = True

def stop():
    global is_running, stops, successes

    if is_running == True :
        timer.stop()
        stops += 1
        is_running = False

        if time % 10 == 0:
            successes += 1

def reset():
    global is_running, stops, successes, time
    timer.stop()
    is_running = False
    stops = successes = time = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global time
    time += 1

# define draw handler
def draw_handler(canvas):
    canvas.draw_text((str(successes) + "/" + str(stops)).rjust(11), (50, 35), 25, "Lime", "monospace")
    canvas.draw_text((format(time)).rjust(7), (10, 85), 50, "Lime", "monospace")

# create frame
stopwatch_frame = simplegui.create_frame("Stopwatch: The Game", 225, 110)
stopwatch_frame.set_draw_handler(draw_handler)

# register event handlers
btn_start = stopwatch_frame.add_button("Start", start, 50)
btn_stop = stopwatch_frame.add_button("Stop", stop, 50)
btn_reset = stopwatch_frame.add_button("Reset", reset, 50)

# start frame
timer = simplegui.create_timer(100, timer_handler)
stopwatch_frame.start()