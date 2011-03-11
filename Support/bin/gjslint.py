#!/usr/bin/env python

import os, sys
from cStringIO import StringIO
old_stdout = sys.stdout

# Import Google Things
try:
from closure_linter import checker
from closure_linter import errors
from closure_linter.common import errorprinter
except:
raise Exception("Please install the closure linter first")

style = """
&lt;style&gt;
#header {width: 100%; margin: 0 0 6px 0; padding: 0; border-bottom: 2px solid #333; height: 60px; overflow-x: hidden;}
#header img {height: 64px; width: 64px; position: absolute; top: 2px; left: 2px; margin: 0px 12px 0px 6px;}
#header h1{position: absolute; top: 6px; left: 75px; text-shadow: -1px 1px 1px #999; color: #222; margin: 0px; padding: 0px}
#header h3{position: absolute; top: 28px; left: 75px; color: #222;}
ul{ margin: 0; padding: 0; width: 100%; overflow-x: hidden;}
li { width: 100%; border-bottom: 1px solid #BBB; list-style: none; padding: 4px 6px;}
li:nth-child(even) {background-color: #DDD;}
&lt;/style&gt;
"""
print style
print "&lt;div id='header'&gt;"
print "&lt;img src='http://code.google.com/closure/images/logo128px.png' /&gt;"
print "&lt;h1&gt;Google Closure Linter Results&lt;/h1&gt;"

error_handler = errorprinter.ErrorPrinter(errors.NEW_ERRORS)
error_handler.SetFormat(1)
runner = checker.GJsLintRunner()
# Hijack the stdout to capture the command output
sys.stdout = mystdout = StringIO()

# Run the linter
result = runner.Run([os.environ['TM_FILEPATH'],], error_handler)

# Set the old stdout back
sys.stdout = old_stdout

# Reset the StringIO
mystdout.seek(0)

# Print the File Name
first_line = mystdout.readline()
print "&lt;h3&gt;%s&lt;/h3&gt;" % first_line[first_line.find(':') + 2:-7]
print "&lt;/div&gt;"

# Render the errors as a ul / li list
print "&lt;ul&gt;"
for line in mystdout.readlines():
print "&lt;li&gt;%s&lt;/li&gt;" % line
print "&lt;/ul&gt;"
mystdout.flush()

# Hijack the stdout to capture the command output AGAIN and capture the summary data
sys.stdout = mystdout = StringIO()
result.PrintSummary()
sys.stdout = old_stdout
mystdout.seek(0)
summary = mystdout.readline()
print "&lt;h3&gt;%s&lt;/h3&gt;" % summary