#!/usr/bin/env ruby -wKU
$LOAD_PATH << '.'
require "common.rb"
require "syntax.rb"

# get doc blocks
## get .ark files path
def get_files(paths)
	files = []	

	paths.each { |e|
		files << File.new(e)
	}

	return files
end

## get usable doc blocks from .ark files
def get_blocks(src)
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

## remove all tabulations in blocks
def rm_tab(str_src)
	buf = ""

	str_src.each_char { |c|  
		next if c == Tab
		buf << c
	}

	return buf
end

# generate function prototype
## get end of one doc block 
def end_block(buf)
	i = 0

	while i < buf.size 
		return i if buf[i] == CPar
		i += 1
	end

	return 0
end

# insert prototypes in blocks
def auto_gen_proto(buf)
	buff = ""
	old_c = ''
	i = 0

	buf.each_char { |c|
		old_c = c if c == FuncBrief[:ark_doc]
		if old_c == FuncBrief[:ark_doc] && c == Space
			old_c = c
			block = buf[i..(end_block(buf[i..buf.end]) + i)]
			proto = "("
			take = false

			block.each_char { |chr|
				if chr == FuncParam
					take = true
					proto << Space if proto != OPar
					next 
				end
				take = false if chr == Space || chr == PageTitle[:ark_doc]
				proto << chr if take
			} 

			proto = proto.delete(NewLine).delete(PageTitle[:md])
			proto << CPar
			buff << proto
		end

		buff << c
		i += 1
	}

	return buff
end

# convert blocks to pseudo markdown
## uncomment doc blocks
def uncomment(buf)
	buff = ""

	buf.each_line { |line|
		bline = ""
		i = 0
		jump = nil

		while i < line.size
			jump = line.index('#')
			bline << line[i] if i != jump
			i += 1
		end

		buff << bline
	}

	return buff
end

## to pseudo markdown
def to_psmd(buf)
	buff = ""
	old_c = ''

	buf.each_char { |c|
		### escape char
		if c == Escape
			old_c = c
			next
		end

		if old_c == Escape && c.match(Alpha) == nil
			buff << c
			next			
		end

		### page title
		if c == PageTitle[:ark_doc]
			buff << PageTitle[:md]
			next
		end

		### function arranging
		#### function brief
		if c == FuncBrief[:ark_doc]
			old_c = c
			buff << FuncBrief[:md]
			buff << Bold
			next
		end

		#### function description
		if old_c == FuncBrief[:ark_doc] && c == CPar
			old_c = c
			buff << CPar
			buff << Bold
			buff << Desc
			next
		end

		##### function paramaters
		if c == FuncParam
			old_c = c
			buff << NewLine
			buff <<  Bold
			next
		end

		if old_c == FuncParam && (c == Space || c == NewLine)
			old_c = c
			buff << Bold
		end

		### code examples
		if c == CodeExample[0][:ark_doc]
			buff << CodeExample[0][:md]
			next 
		end

		buff << c
	}

	return buff
end

# hold blocks content in corresponding files
## get markdown files names
def get_labels(blocks)
	labels = [] 
	
	blocks = blocks.delete('#')
	blocks.each_line { |line| 
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

# get markdown files content and organize them
## organize the files content
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

## get page(s) title(s)
def get_title_block(str)
	indexes = {:begin => nil, :end => nil}
	i = 0

	while i < str.size
		if str[i - 1] == NewLine
			if str[i] == PageTitle[:md] && str[i + 1] != PageTitle[:md]
				indexes[:begin] = i					
			end

			if indexes[:begin] != nil
				if (str[i] == PageTitle[:md] || str[i] == CodeExample[0][:md][0]) && i > indexes[:begin]
					indexes[:end] = i - 1
				end
			end
		end

		if i == str.end && indexes[:end] == nil					
			indexes[:end] = str.end
		end

		break if indexes[:begin] != nil && indexes[:end] != nil

		i += 1
	end

	return indexes
end

def find_title(untitled_files)
	files = [] 

	untitled_files.each { |e|
		e.each_key { |key|
			title_block = get_title_block(e[key])
			str = (e[key])[title_block[:begin]..title_block[:end]].add_nw
			i = 0

			while i < e[key].size
				str << e[key][i] if i < title_block[:begin] || i > title_block[:end]
				i += 1
			end

			files.push({key => str})
		}
	}

	return files
end

# main parse function
def parser(src_dir)
	puts("INFO	-  Getting of documentation content")
	doc_blocks =  auto_gen_proto(rm_tab(get_blocks(src_dir + "*.ark")))
	pseudo_md = to_psmd(uncomment(doc_blocks))
	files = find_title(get_content(pseudo_md))

	return files
end