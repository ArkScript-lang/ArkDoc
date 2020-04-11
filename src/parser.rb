#!/usr/bin/env ruby -wKU
$LOAD_PATH << '.'
require "common.rb"
require "syntax.rb"


def get_files(paths)
	files = []	

	paths.each { |e|
		files << File.new(e)
	}

	return files
end

def get_text(src)
	files = get_files(Dir.glob(src))
	take = false
	str = ""

	files.each_index { |i|
		files[i].each { |line|
			buf = ""
			i = 0
			while i < line.size
				if i <= (line.size - 2)
					if line[i] == '#' && line[i + 1] == OPar
						take = true
					elsif line[i] == '#' && line[i + 1] == CPar
						buf << line[i]
						buf << line[i + 1]
						buf << NewLine
						take = false	
					end
				end

				buf << line[i] if take
				i += 1  
			end

			str << buf
		}
	}

	return str
end

def rm_tab(str_src)
	buf = ""

	str_src.each_char { |c|  
		next if c == Tab
		buf << c
	}

	return buf
end

def auto_gen_proto(buf)
	buff = ""

	

	return buff
end

def to_psmd(buf)
	buff = ""
	old_c = ''

	buf.each_char { |c|
		# function arranging
		## function brief
		if c == FuncBrief[:ark_doc]
			old_c = c
			buff << FuncBrief[:md]
			buff << Bold
			next
		end 

		## function description
		if old_c == FuncBrief[:ark_doc] && c == Space
			old_c = Space
			buff << Bold
			buff << Desc
			next
		end

		## function paramaters
		if c == FuncParam
			buff << NewLine
			next
		end

		### parameter spec
		if c == ObjectType[0][:ark_doc] || c == ObjectType[1][:ark_doc] 
			buff << ObjectType[0][:md]
			next 
		end

		if c == ObjectPseudo[0][:ark_doc] || c == ObjectPseudo[1][:ark_doc]
			buff << ObjectPseudo[0][:md]
			next 
		end

		buff << c
	}

	return buff
end

def uncomment(buf)
	buff = ""

	buf.each_line { |line|
		bline = ""
		i = 0
		while i < line.size
			bline << line[i] if i > 0
			i += 1
		end

		buff << bline
	}

	return buff
end

def get_labels(psmd)
	labels = [] 
		
	psmd.each_line { |line| 
		label = ""
		if line[0] == OPar && line[1] == OPar
			line.each_char { |c|
				label << c
			}

			labels.push(label) if !(labels.include?(label))
		end
	}

	return labels
end

def get_content(psmd)
	psmd_ary = psmd.to_a
	labels = get_labels(psmd)
	files = []
	take = false

	labels.each_index { |i|
		str = ""
		key = ""
		psmd_ary.each { |e|
			take = true if labels[i] == e || e == (OPar + NewLine)
			take = false if e == (CPar + NewLine)
			next if e == labels[i]
			str << e if take
		}

		labels[i].each_char { |c|
			next if c == OPar || c == CPar || c == NewLine
			key << c
		}

		files.push({ key => str})
	}

	return files
end

def parser(src_dir)
	puts("INFO	-  Getting of documentation content")
	str_src = rm_tab(get_text(src_dir + "*.ark"))
	puts(uncomment(str_src))

	return get_content(to_psmd(uncomment(str_src)))
end

#puts parser("../ark/")