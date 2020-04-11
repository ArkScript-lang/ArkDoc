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
ObjectType = [{:ark_doc => '<', :md => Bold}, {:ark_doc => '>', :md => ""}]
ObjectPseudo = [{:ark_doc => '{', :md => Italic}, {:ark_doc => '}', :md => ""}]
Desc = NewLine