from gpiozero import MotionSensor
from gpiozero import Button
from signal import pause
from time import sleep
import datetime

motion = MotionSensor(pin=18, sample_rate=1000)
button = Button(5)

counter = -1
last_lap_start_time = None
race_result = {}
sleep_after_detection = 0.5

def reset():
    global counter
    global race_result
    
    if len(race_result) > 0:
        print('')
        
        total_time = datetime.timedelta(0)
        total_laps = 0
        for k, v in race_result.items():
            #print(k, v)
            total_time += v
            total_laps += 1
        
        print('Total laps: ' + str(total_laps) + ' Average lap time: ' + str(total_time / total_laps))    
    
    counter = -1
    race_result = {}
    print('Race reset.\n')
    
    
    
def handle_motion():
    global counter
    global last_lap_start_time 
    
    if counter == -1:
        counter = 0
        last_lap_start_time = datetime.datetime.now()
        print('Race started.' + '(' + str(last_lap_start_time ) + ')\n')
    else:   
        counter += 1
        timespan = datetime.datetime.now() - last_lap_start_time 
        last_lap_start_time = datetime.datetime.now()
        lap = 'Lap:' + str(counter)
        print( lap + ' (' + str(timespan) + ')')
        race_result[lap] = timespan
    
    sleep(sleep_after_detection)
        
motion.when_no_motion = handle_motion
button.when_pressed = reset

pause()
