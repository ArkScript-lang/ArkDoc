#!/usr/bin/env ruby -wKU

# special chars
NewLine = 10.chr
Bold = "**"
Brackets = ['[', ']']
Parenthesis = ['(', ')']

# parser key elements format
Title = "### "
Function = "#### "
Code = "```"
Details = "_"

# generator
Each = '-'
Separator = ' '
Page = "#### "

# theming
ThemeMarkup = "theme:"
ThemeNameMarkup = "name:"
ThemeDirMarkup = "custom_dir:"
ThemeDir = "../../themes/"
# default themes
DarkTheme = "dark"