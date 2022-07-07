#!/usr/bin/env python3
# 
# bbb_mic_gui_dynamic.py
# 
# volume: "volume" factor, 0.0 to 1.0 = 0% to 100%
# volume: “mute” gboolean True/False. default False
#
# See Description below.
#
# Ian Stewart - 2022-07-07 - CC0
import sys, os
import argparse
import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gst, Gtk

START_MUTED = False  # <-- Boolean True or False
START_VOLUME = 100  # <--- Range from 0 to 100

def create_gui():
    'Initialize and instantiate pipeline'
    pipeline = start_pipeline()

    # Create the window
    window = Gtk.Window()
    window.set_title("BBB Microphone")
    window.set_default_size(300, 100)
    window.connect("destroy", Gtk.main_quit, "WM destroy")
    window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
    # 'CENTER', 'CENTER_ALWAYS', 'CENTER_ON_PARENT', 'MOUSE', 'NONE',    

    # Box for volume control and muting switch
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 10)
    #box.set_margin_top(10)
    box.set_margin_bottom(10)
    box.set_margin_start(10)
    box.set_margin_end(10)


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
    

    # Add the muting. Using a big switch. Easy to click on/off
    def cb_switch(switch, x):
        'Mute switch on / off'
        if switch.get_active():
            pipeline.get_by_name('volume').set_property('mute', True)
        else:
            pipeline.get_by_name('volume').set_property('mute', False)


    # Add a muting swtich
    switch = Gtk.Switch()
    switch.connect('state-set', cb_switch)
    switch.set_active(args.muting)
    box.pack_start(switch, True, True, 0)


    """
    # Add the muting using a checkbox
    def cb_checkbox(checkbox):
        'Mute toggle on / off'
        if checkbox.get_active():
            pipeline.get_by_name('volume').set_property('mute', True)
        else:
            pipeline.get_by_name('volume').set_property('mute', False)

    # Add a mute checkbox
    checkbox = Gtk.CheckButton(label = "Mute")
    checkbox.connect('toggled', cb_checkbox)
    checkbox.set_active(args.muting)
    box.pack_start(checkbox, True, True, 0)
    """
    
    
    window.add(box)
    # Get the show on the road.
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

"""
Description: 

When using Big Blue Button (BBB) and presenting, then your microphone is 
normally the only audio output stream. Thus, if you run an application that 
generates audio, then this audio will not be heard by the audience, except for 
the audio that is output from the presenters PC speakers and then leaks back 
into their microphone.

When using the Firefox browser, and enabling your microphone, then you get 
the choice of a "Microphone", or "Monitoring the system audio". Select the
"Monitoring the system audio". When you run an audio application then the BBB
audience will hear it.

Running this program, bbb_mic_gui_dynamic.py, then your microphone will be 
added to the system audio.

WARNING: The presenter will need a headset, to avoid feedback. Thus the 
presenter must be remote from any live audience in a room listening over the
rooms public address system.

"""

