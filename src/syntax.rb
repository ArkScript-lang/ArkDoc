#!/usr/bin/env ruby -wKU


Bold = "**"
Tab = 9.chr
NewLine = 10.chr
OPar = '('
CPar = ')'
OBracket = '['
CBracket = ']'
Each = '-'
Underscore = '_'

FuncBrief = {:ark_doc => '\\', :md => "##"} 
FuncParam = {:ark_doc => '@', :md => '    '}
ObjectType = [{:ark_doc => '<', :md => Bold}, {:ark_doc => '>', :md => ""}]
ObjectPseudo = [{:ark_doc => '{', :md => Underscore}, {:ark_doc => '}', :md => ""}]
Desc = {:ark_doc => ':', :md => NewLine}