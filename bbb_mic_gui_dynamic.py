#!/usr/bin/env python3
# 
# bbb_mic_gui_dynamic.py
# 
# volume: "volume" factor, 0.0 to 1.0 = 0% to 100%
# volume: “mute” gboolean True/False. default False
#
# See Description: https://github.com/irsbugs/bbb-microphone
#
# Ian Stewart - 2022-07-07 - CC0
import argparse
import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gst, Gtk

START_MUTED = False  # <-- Boolean. True or False
START_VOLUME = 100  # <--- Integer. Range from 0 to 100

def create_gui():
    'Initialize and instantiate pipeline'
    pipeline = start_pipeline()

    # Create the window
    window = Gtk.Window()
    window.set_title("BBB Mic")
    window.set_default_size(300, 50)
    window.connect("destroy", Gtk.main_quit, "WM destroy")
    window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
    # 'CENTER', 'CENTER_ALWAYS', 'CENTER_ON_PARENT', 'MOUSE', 'NONE',    

    # Box for volume control and muting switch
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing = 10)
    box.set_margin_top(10)
    box.set_margin_bottom(10)
    box.set_margin_start(10)
    box.set_margin_end(10)


    # Add the muting. Using a switch. Easy to click on/off than a checkbox
    def cb_switch(switch, x):
        'Mute switch on / off'
        if switch.get_active():
            pipeline.get_by_name('volume').set_property('mute', True)
        else:
            pipeline.get_by_name('volume').set_property('mute', False) 


    switch = Gtk.Switch()
    switch.connect('state-set', cb_switch)
    switch.set_active(args.muting)
    box.pack_start(switch, False, False, 0) # object, Expand, Fill, Padding

   
    # Volume control using Scale widget
    def cb_scale_moved(scale):
        'Adjust the volume 0 to 100 to be in range 0 to 1'
        pipeline.get_by_name('volume').set_property('volume', scale.get_value()/100)


    scale = Gtk.Scale.new_with_range(orientation=Gtk.Orientation.HORIZONTAL, 
            min=0, max=100, step=1)
    scale.connect("value-changed", cb_scale_moved)
    # Set initial volume based on args.volume or default of START_VOLUME
    scale.set_value(args.volume)
    box.pack_start(scale, True, True, 0)
 
    window.add(box)
    window.show_all()

    Gtk.main()
    pipeline.set_state(Gst.State.NULL)
    window.destroy()


def start_pipeline():
    'Initialize and instantiate the pipeline'
    Gst.init(None)
    pipeline = Gst.Pipeline()    
    pipeline = Gst.parse_launch ("autoaudiosrc ! volume name=volume ! pulsesink")    
    #pipeline = Gst.parse_launch ("autoaudiosrc ! volume name=volume ! alsasink") 
    pipeline.set_state(Gst.State.PLAYING)   
    return pipeline


if __name__ == "__main__":
    # Use argparse for volume and muting    
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--volume", 
                        type=int, 
                        default=START_VOLUME,
                        help="Set initial Volume level. Range 0 to 100")
  
    parser.add_argument('--muting', dest='muting', action='store_true')
    parser.add_argument('--no-muting', dest='muting', action='store_false')
    parser.set_defaults(muting=START_MUTED)

    args = parser.parse_args()

    create_gui()
