#!/usr/bin/env python3
# 
# bbb_mic_console_static.py
# 
# volume: "volume" factor, 0.0 to 1.0 = 0% to 100%
# volume: “mute” gboolean True/False. default False
#
# See Description below.
#
# Ian Stewart - 2022-07-07 - CC0

import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gst, Gtk
Gst.init(None)

pipeline = Gst.Pipeline()

pipeline = Gst.parse_launch ("autoaudiosrc ! volume volume=1.0 ! volume mute=False ! pulsesink")

pipeline.set_state(Gst.State.PLAYING)

Gtk.main()

"""
Description: 

When using Big Blue Button (BBB) and presenting, then your microphone is 
normally the only audio output stream. Thus, if you run an application that 
generates audio, then this audio will not be heard by the audience, except for 
the audio that is output from the presenters PC speakers and then leaks back 
into their microphone.

When using the Firefox browser, and enabling your microphone, then you get 
the choice of a "Microphone", or "Monitoring the system audio". Select the
"Monitoring he system audio". When you run an audio application then the BBB
audience will hear it.

Running this program, bbb_mic_console_static.py, then your microphone will be 
added to the system audio.

WARNING: The presenter will need a headset, to avoid feedback. Thus the 
presenter must be remote from any live audience in a room listening over the
rooms public address system.

"""

