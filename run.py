import os
import sys

plugindir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(plugindir)
sys.path.append(os.path.join(plugindir, "lib"))
sys.path.append(os.path.join(plugindir, "plugin"))

from plugin.main import ObsidianDailyNote

if __name__ == "__main__":
    ObsidianDailyNote()

