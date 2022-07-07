#!/usr/bin/env python3
# 
# bbb_mic_console_static.py
# 
# volume: "volume" factor, 0.0 to 1.0 = 0% to 100%
# volume: “mute” gboolean True/False. default False
#
# See Description: https://github.com/irsbugs/bbb-microphone
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
