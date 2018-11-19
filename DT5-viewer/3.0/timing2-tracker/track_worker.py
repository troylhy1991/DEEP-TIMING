import sys,os
sys.path.append('.')
from cell_tracker import TIMING_Cell_Tracker

def track_worker(input_path, output_path, prefix, t):
    Tracker = TIMING_Cell_Tracker(os.path.join(input_path, prefix + '*.tif'), output_path, t)
    Tracker.get_track()
    Tracker.write_track_img()
    del Tracker
