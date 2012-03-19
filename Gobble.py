import sublime, sublime_plugin,re

class GobbleCommand(sublime_plugin.TextCommand):
	def debug(self, msg):
		if(True):
			print(msg)

	def run(self, edit):
		sel = self.view.sel()
		passThrough = True

		if(len(sel) == 1):
			passThrough = not (sel[0].empty())

		if(passThrough):
			self.view.run_command("left_delete")
			return

		# Execute gobble
		cursorPoint = sel[0].a;
		lineStartPoint = self.view.line(cursorPoint).a
		lineUptilPoint = self.view.substr(sublime.Region(lineStartPoint, cursorPoint))

		if(not re.match('^\s+$', lineUptilPoint)):
			# This is a regular delete, as there is 
			self.view.run_command("left_delete")
			return

		# Run the erase in two separate commands
		# so this way, if the user hits "undo", it will undo one step instead of both
		self.view.erase(edit, sublime.Region(lineStartPoint, cursorPoint))
		self.view.run_command("left_delete")
		self.view.run_command("reindent")
