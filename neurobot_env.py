import os
import sys

os.chdir("/home/pi/project/neurobot")
sys.path.extend(["/home/pi/project/neurobot","/home/pi/project/neurobot/src"])

from recognizers.distance_interpolator import DistanceInterpolator
from utils.interactive_parameter_selector import InteractiveParameterSelector
from hardware.actuators.wheels_driver import left_wheel, right_wheel
from goal_logic.genetic_persecutor.genetic_persecutor import GeneticPersecutor
from hardware.sensors.pi_camera import PiCameraWrapper
from watcher.watcher import Watcher
import threading

camera = PiCameraWrapper()
watcher = Watcher(camera=camera, distance_calculator=DistanceInterpolator("brandina.json"))
selector = InteractiveParameterSelector(distance_interpolator_settings_file="brandina.json", camera=camera)

gp = GeneticPersecutor("first_try", watcher=watcher)
i = gp.current_generation.individuals[0]
s = threading.Thread(target=selector.start)
