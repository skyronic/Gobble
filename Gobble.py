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

		cursorPoint = sel[0].begin();
		lineRegion = self.view.line(cursorPoint)

		# In whitespace-indented languages, if someone presses backspace on an empty line, 
		# it probably means "go to the previous level of indentation"
		# So in that case, just pass-through!
		if(cursorPoint == lineRegion.end()):
			passThrough = True

		if(passThrough):
			self.view.run_command("left_delete")
			return

		lineStartPoint = lineRegion.begin()
		lineUptilPoint = self.view.substr(sublime.Region(lineStartPoint, cursorPoint))

		if(not re.match('^\s+$', lineUptilPoint)):
			# This is a regular delete, as there is 
			self.view.run_command("left_delete")
			return

		# Run the erase in two separate commands
		# so this way, if the user hits "undo", it will undo one step instead of both

		# Get the kill region (The region of code we're going to erase, and store the exact 
		# String later in case we're going to need to re-indent better
		killRegion = sublime.Region(lineStartPoint, cursorPoint)
		whiteSpaceString = self.view.substr(killRegion)

		self.view.erase(edit, sublime.Region(lineStartPoint, cursorPoint))
		self.view.run_command("left_delete")

		# Get the current index of the cursor after delete
		indexAfterDelete = self.view.sel()[0].a

		# Get the new line region
		newLineRegion = self.view.line(indexAfterDelete);

		# If the index after delete is the same as the first part of the new line region,
		# This probably means that the backspace lead to an indentation boo-boo
		if(indexAfterDelete == newLineRegion.a):
			# Now we just need to re-insert the old string from the original indent into here:
			self.view.insert(edit, indexAfterDelete, unicode(whiteSpaceString))
