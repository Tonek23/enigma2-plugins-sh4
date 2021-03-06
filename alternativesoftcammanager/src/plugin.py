from . import _

from os import mkdir, path, remove
from time import sleep

from Components.config import config, ConfigSubsection, ConfigText
from Components.Console import Console
from Plugins.Plugin import PluginDescriptor

from Softcam import checkconfigdir, getcamcmd, stopcam


config.plugins.AltSoftcam = ConfigSubsection()
config.plugins.AltSoftcam.actcam = ConfigText(default="none")
config.plugins.AltSoftcam.camconfig = ConfigText(default="/var/keys",
	visible_width=100, fixed_size=False)
config.plugins.AltSoftcam.camdir = ConfigText(default="/var/emu",
	visible_width=100, fixed_size=False)

checkconfigdir()

def main(session, **kwargs):
	from Manager import AltCamManager
	session.open(AltCamManager)

EnigmaStart = False

def startcam(reason, **kwargs):
	if config.plugins.AltSoftcam.actcam.value != "none":
		global EnigmaStart
		if reason == 0 and not EnigmaStart: # Enigma start and not use reloadPlugins
			EnigmaStart = True
			sleep(2)
			cmd = getcamcmd(config.plugins.AltSoftcam.actcam.value)
			Console().ePopen(cmd)
			print "[Alternative SoftCam Manager] ", cmd
		elif reason == 1: # Enigma stop
			stopcam(config.plugins.AltSoftcam.actcam.value)

def Plugins(**kwargs):
	return [PluginDescriptor(name=_("Alternative SoftCam Manager"),
		description=_("Start, stop, restart SoftCams, change settings."),
		where=[PluginDescriptor.WHERE_PLUGINMENU, 
		PluginDescriptor.WHERE_EXTENSIONSMENU],
		icon="images/softcam.png", fnc=main),
	PluginDescriptor(where=PluginDescriptor.WHERE_AUTOSTART,
		needsRestart=True, fnc=startcam)]

