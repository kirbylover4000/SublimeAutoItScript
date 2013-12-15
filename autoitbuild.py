from __future__ import print_function
import sublime, sublime_plugin
import subprocess
import os

# The autoitbuild command is called as target by AutoIt.sublime-build
class autoitbuild(sublime_plugin.WindowCommand):
	def run(self):
		filepath = self.window.active_view().file_name()
		AutoIt3WrapperPath = sublime.load_settings("AutoIt.sublime-settings").get("AutoIt3WrapperPath")
		cmd = [AutoIt3WrapperPath, "/run", "/prod", "/ErrorStdOut", "/in", filepath]
		self.window.run_command("exec", {"cmd": cmd})

class autoitcompile(sublime_plugin.WindowCommand):
	def run(self):
		filepath = self.window.active_view().file_name()
		AutoItCompilerPath = sublime.load_settings("AutoIt.sublime-settings").get("AutoItCompilerPath")
		cmd = [AutoItCompilerPath, "/ShowGui", "/in", filepath]
		self.window.run_command("exec", {"cmd": cmd})

class autoitinfo(sublime_plugin.WindowCommand):
	def run(self):
		filepath = self.window.active_view().file_name()
		AutoIt3InfoPath = sublime.load_settings("AutoIt.sublime-settings").get("AutoIt3InfoPath")
		cmd = [AutoIt3InfoPath]
		self.window.run_command("exec", {"cmd": cmd})

class autoitincludehelper(sublime_plugin.WindowCommand):
	def run(self):
		self.window.run_command("save")

		filepath = self.window.active_view().file_name()
		AutoItExePath = sublime.load_settings("AutoIt.sublime-settings").get("AutoItExePath")
		AutoItIncludeFolder = os.path.dirname(AutoItExePath) + "\\Include"

		IncludeHelperAU3Path = sublime.load_settings("AutoIt.sublime-settings").get("IncludeHelperAU3Path")
		if (IncludeHelperAU3Path is None):
			IncludeHelperAU3Path = "{PACKAGE_PATH}\\AutoItScript\\Include_Helper.au3"
		IncludeHelperAU3Path = IncludeHelperAU3Path.replace("{PACKAGE_PATH}", sublime.packages_path())

		AutoItIncludeCmd = [AutoItExePath, IncludeHelperAU3Path, filepath, AutoItIncludeFolder]

		try:
			subprocess.call(AutoItIncludeCmd)
			self.window.run_command("revert")
			sublime.status_message("AutoIt IncludeHelper Finished")
		except Exception as e:
			sublime.active_window().run_command("show_panel", {"panel": "console"})
			print("------------ ERROR: Python exception trying to run following command ------------")
			print(AutoItIncludeCmd)
			print("Error {0}".format(str(e)))
