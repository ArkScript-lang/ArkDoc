#!/usr/bin/env ruby -wKU


Bold = "**"
Italic = '_'
Tab = 9.chr
NewLine = 10.chr
OPar = '('
CPar = ')'
OBracket = '['
CBracket = ']'
Each = '-'
Coma = ','
Space = ' '

FuncBrief = {:ark_doc => '\\', :md => "##"} 
FuncParam = '@'
CodeExample = [{:ark_doc => '`', :md => "```"}, {:ark_doc => '`', :md => "```"}]
Desc = NewLine