###############################
# Marks.

def mark_class(f, l, c):
	f.write('markClass [ ' + ' '.join(l) + ' ] <anchor 0 0> ' + c + ';\n')

###############################
# Lookups.

n_lookups = 0

def start_feat(f, t='liga'):
	global n_lookups
	n_lookups = 0
	f.write('feature ' + t + ' {\n\n')

def end_feat(f, t='liga'):
    f.write('\n} ' + t + ';\n\n')

def start_named_lookup(f, name):
	f.write('lookup ' + name + ' {\n')

def end_named_lookup(f, name):
	f.write('} ' + name + ';\n')

def start_lookup(f, t='liga'):
	global n_lookups
	name = t + str(n_lookups)
	start_named_lookup(f, name)
	print "starting {}".format(name)

def start_mark_lookup(f):
	start_lookup(f)
	ignore_base_feature(f)

def start_reversal_mark_lookup(f):
	start_mark_lookup(f)
	right_to_left_feature(f)

def end_lookup(f, t='liga'):
	global n_lookups
	name = t + str(n_lookups)
	end_named_lookup(f, name)
	print "ending {}".format(name)
	n_lookups += 1

def named_lookup_call(f, name):
	f.write('    lookup ' + name + ';\n')

def ignore_base_feature(f):
	f.write('lookupflag IgnoreBaseGlyphs;\n')

def right_to_left_feature(f):
	f.write('lookupflag RightToLeft;\n')

###############################
# Rules.

# Make middle part of elems.
def to_mid(elems):
	return [elem + "'" for elem in elems]

# Create substitution.
def create_sub(f, elems_in, elems_out):
	f.write('    sub ' + ' '.join(elems_in) + ' by ' + ' '.join(elems_out) + ';\n')

# Create substitution with middle part.
def create_sub_mid(f, begin, mid, end, target, to_print = False):
	s = '    sub ' + ' '.join(begin + to_mid(mid) + end) + ' by ' + target + ';\n'
	if to_print:
		print s
	f.write(s)

# Create position.
def create_pos(f, begin, mid, end, x, y, x_adv, y_adv):
	f.write('    pos ' + ' '.join(begin + to_mid(mid)) + \
			' <' + str(x) + ' ' + str(y) + ' ' + str(x_adv) + ' ' + str(y_adv) + '> ' + \
			' '.join(end) + ';\n')

# Create ignore position.
def create_ignore_pos(f, begin, mid, end):
	f.write('    ignore pos ' + ' '.join(begin + to_mid(mid) + end) + ';\n')
