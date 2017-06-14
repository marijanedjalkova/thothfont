import fontforge

from constants import *
from feature_file_format import *

font_sfd = 'myfont.sfd'
font_otf = 'myfont1.otf'
feature_file_name = 'hiero1.fea'

############################################
# Auxiliary symbols. The type t is indicated by a suffix 'base' or 'mark'.
# The default is 'base'.

# Turn prefix of auxiliary symbol into a based/mark symbol.
def aux_type(a,t):
	return a + t
def auxs_type(l):
	return [aux_type(a,t) for a in l]

# Auxiliary symbols for operators and brackets.
def hor_open(t='base'):
	return 'hor.open.' + t
def hor_op(t='base'):
	return 'hor.op.' + t
def hor_close(t='base'):
	return 'hor.close.' + t
def vert_open(t='base'):
	return 'vert.open.' + t
def vert_op(t='base'):
	return 'vert.op.' + t
def vert_close(t='base'):
	return 'vert.close.' + t
# Classes of symbols.
def hor_any(t=''):
	return [hor_open(t),hor_op(t),hor_close(t)]
def vert_any(t=''):
	return [vert_open(t),vert_op(t),vert_close(t)]

# Generic record field.
def rec_field(record, field, val, t):
	return record + '.' + field + '.' + str(val) + '.' + t

# Record for horizontal group.
def hrec_bw(w,t='mark'):
	return rec_field('hrec','bw',w,t)
def hrec_w(w,t='mark'):
	return rec_field('hrec','w',w,t)
def hrec_h(h,t='mark'):
	return rec_field('hrec','h',h,t)
def hrec_s(s,t='mark'):
	return rec_field('hrec','s',s,t)
def hrec_tx(x,t='mark'):
	return rec_field('hrec','tx',x,t)
def hrec_ty(y,t='mark'):
	return rec_field('hrec','ty',y,t)
def hrec_tw(w,t='mark'):
	return rec_field('hrec','tw',w,t)
def hrec_th(h,t='mark'):
	return rec_field('hrec','th',h,t)
# Initial values.
def hrec_init(t='base'):
	return [hrec_bw('nil',t),hrec_w('nil',t),hrec_h('nil',t),hrec_s('nil',t),
		hrec_tx('nil',t),hrec_ty('nil',t),hrec_tw('nil',t),hrec_th('nil',t)]
# Classes of symbols.
def hrec_bw_any(t=''):
	return [hrec_bw(w,t) for w in ['nil'] + all_glyph_sizes]
def hrec_w_any(t=''):
	return [hrec_w(w,t) for w in ['nil'] + all_group_widths]
def hrec_h_any(t=''):
	return [hrec_h(h,t) for h in ['nil'] + all_glyph_sizes]
def hrec_s_any(t=''):
	return [hrec_s(s,t) for s in ['nil'] + all_group_scalings]
def hrec_tx_any(t=''):
	return [hrec_tx(x,t) for x in ['nil'] + all_coords]
def hrec_ty_any(t=''):
	return [hrec_ty(y,t) for y in ['nil'] + all_coords]
def hrec_tw_any(t=''):
	return [hrec_tw(w,t) for w in ['nil'] + all_coords]
def hrec_th_any(t=''):
	return [hrec_th(h,t) for h in ['nil'] + all_coords]
def hrec_any(t=''):
	return hrec_bw_any(t) + hrec_w_any(t) + hrec_h_any(t) + hrec_s_any(t) + \
		hrec_tx_any(t) + hrec_ty_any(t) + hrec_tw_any(t) + hrec_th_any(t)

# Record for suffix of horizontal group.
def shrec_w(w,t='mark'):
	return rec_field('shrec','w',w,t)
def shrec_h(h,t='mark'):
	return rec_field('shrec','h',h,t)
def shrec_tx(x,t='mark'):
	return rec_field('shrec','tx',x,t)
def shrec_ty(y,t='mark'):
	return rec_field('shrec','ty',y,t)
def shrec_tw(w,t='mark'):
	return rec_field('shrec','tw',w,t)
def shrec_th(h,t='mark'):
	return rec_field('shrec','th',h,t)
# Initial values.
def shrec_init(t='base'):
	return [shrec_w('nil',t),shrec_h('nil',t),
		shrec_tx('nil',t),shrec_ty('nil',t),shrec_tw('nil',t),shrec_th('nil',t)]
def shrec_init_zero(t='base'):
	return [shrec_w(0,t),shrec_h(0,t),
		shrec_tx('nil',t),shrec_ty('nil',t),shrec_tw('nil',t),shrec_th('nil',t)]
# Classes of symbols.
def shrec_w_any(t=''):
	return [shrec_w(w,t) for w in ['nil'] + all_suffix_group_widths]
def shrec_h_any(t=''):
	return [shrec_h(h,t) for h in ['nil'] + all_glyph_sizes_and_zero]
def shrec_tx_any(t=''):
	return [shrec_tx(x,t) for x in ['nil'] + all_coords]
def shrec_ty_any(t=''):
	return [shrec_ty(y,t) for y in ['nil'] + all_coords]
def shrec_tw_any(t=''):
	return [shrec_tw(w,t) for w in ['nil'] + all_coords]
def shrec_th_any(t=''):
	return [shrec_th(h,t) for h in ['nil'] + all_coords]
def shrec_any(t=''):
	return shrec_w_any(t) + shrec_h_any(t) + \
		shrec_tx_any(t) + shrec_ty_any(t) + shrec_tw_any(t) + shrec_th_any(t)

# Record for vertical group.
def vrec_w(w,t='mark'):
	return rec_field('vrec','w',w,t)
def vrec_bh(h,t='mark'):
	return rec_field('vrec','bh',h,t)
def vrec_h(h,t='mark'):
	return rec_field('vrec','h',h,t)
def vrec_tx(x,t='mark'):
	return rec_field('vrec','tx',x,t)
def vrec_ty(y,t='mark'):
	return rec_field('vrec','ty',y,t)
def vrec_tw(w,t='mark'):
	return rec_field('vrec','tw',w,t)
def vrec_th(h,t='mark'):
	return rec_field('vrec','th',h,t)
def vrec_jmp(w,t='mark'):
	return rec_field('vrec','jmp',w,t)
# Initial values.
def vrec_init(t='base'):
	return [vrec_w('nil',t),vrec_bh('nil',t),vrec_h('nil',t),
		vrec_tx('nil',t),vrec_ty('nil',t),vrec_tw('nil',t),vrec_th('nil',t),
		vrec_jmp('nil',t)]
# Classes of symbols.
def vrec_w_any(t=''):
	return [vrec_w(w,t) for w in ['nil'] + all_glyph_sizes]
def vrec_bh_any(t=''):
	return [vrec_bh(h,t) for h in ['nil'] + all_glyph_sizes]
def vrec_h_any(t=''):
	return [vrec_h(h,t) for h in ['nil'] + all_group_heights]
def vrec_tx_any(t=''):
	return [vrec_tx(x,t) for x in ['nil'] + all_coords]
def vrec_ty_any(t=''):
	return [vrec_ty(y,t) for y in ['nil'] + all_coords]
def vrec_tw_any(t=''):
	return [vrec_tw(w,t) for w in ['nil'] + all_coords]
def vrec_th_any(t=''):
	return [vrec_th(h,t) for h in ['nil'] + all_coords]
def vrec_jmp_any(t=''):
	return [vrec_jmp(h,t) for h in ['nil'] + all_coords]
def vrec_any(t=''):
	return vrec_w_any(t) + vrec_bh_any(t) + vrec_h_any(t) + \
		vrec_tx_any(t) + vrec_ty_any(t) + vrec_tw_any(t) + vrec_th_any(t) + \
		vrec_jmp_any(t)

# Record for suffix of vertical group.
def svrec_w(w,t='mark'):
	return rec_field('svrec','w',w,t)
def svrec_h(h,t='mark'):
	return rec_field('svrec','h',h,t)
def svrec_tx(x,t='mark'):
	return rec_field('svrec','tx',x,t)
def svrec_ty(y,t='mark'):
	return rec_field('svrec','ty',y,t)
def svrec_tw(w,t='mark'):
	return rec_field('svrec','tw',w,t)
def svrec_th(h,t='mark'):
	return rec_field('svrec','th',h,t)
# Initial values.
def svrec_init(t='base'):
	return [svrec_w('nil',t),svrec_h('nil',t),
		svrec_tx('nil',t),svrec_ty('nil',t),svrec_tw('nil',t),svrec_th('nil',t)]
def svrec_init_zero(t='base'):
	return [svrec_w(0,t),svrec_h(0,t),
		svrec_tx('nil',t),svrec_ty('nil',t),svrec_tw('nil',t),svrec_th('nil',t)]
# Classes of symbols.
def svrec_w_any(t=''):
	return [svrec_w(w,t) for w in ['nil'] + all_glyph_sizes_and_zero]
def svrec_h_any(t=''):
	return [svrec_h(h,t) for h in ['nil'] + all_suffix_group_heights]
def svrec_tx_any(t=''):
	return [svrec_tx(x,t) for x in ['nil'] + all_coords]
def svrec_ty_any(t=''):
	return [svrec_ty(y,t) for y in ['nil'] + all_coords]
def svrec_tw_any(t=''):
	return [svrec_tw(w,t) for w in ['nil'] + all_coords]
def svrec_th_any(t=''):
	return [svrec_th(h,t) for h in ['nil'] + all_coords]
def svrec_any(t=''):
	return svrec_w_any(t) + svrec_h_any(t) + \
		svrec_tx_any(t) + svrec_ty_any(t) + svrec_tw_any(t) + svrec_th_any(t)

# Record for glyph.
def grec_s(s,t='mark'):
	return rec_field('grec','s',s,t)
def grec_w(w,t='mark'):
	return rec_field('grec','w',w,t)
def grec_h(h,t='mark'):
	return rec_field('grec','h',h,t)
def grec_sw(s,t='mark'):
	return rec_field('grec','sw',s,t)
def grec_sh(s,t='mark'):
	return rec_field('grec','sh',s,t)
def grec_tx(x,t='mark'):
	return rec_field('grec','tx',x,t)
def grec_ty(y,t='mark'):
	return rec_field('grec','ty',y,t)
def grec_tw(w,t='mark'):
	return rec_field('grec','tw',w,t)
def grec_th(h,t='mark'):
	return rec_field('grec','th',h,t)
# Classes of symbols.
def grec_s_any(t=''):
	return [grec_s(s,t) for s in ['nil'] + all_glyph_scalings]
def grec_w_any(t=''):
	return [grec_w(w,t) for w in ['nil'] + all_glyph_sizes]
def grec_h_any(t=''):
	return [grec_h(h,t) for h in ['nil'] + all_glyph_sizes]
def grec_sw_any(t=''):
	return [grec_sw(s,t) for s in ['nil'] + all_group_scalings]
def grec_sh_any(t=''):
	return [grec_sh(s,t) for s in ['nil'] + all_glyph_scalings]
def grec_tx_any(t=''):
	return [grec_tx(x,t) for x in ['nil'] + all_coords]
def grec_ty_any(t=''):
	return [grec_ty(y,t) for y in ['nil'] + all_coords]
def grec_tw_any(t=''):
	return [grec_tw(w,t) for w in ['nil'] + all_coords]
def grec_th_any(t=''):
	return [grec_th(h,t) for h in ['nil'] + all_coords]
def grec_any(t=''):
	return grec_s_any(t) + grec_w_any(t) + grec_h_any(t) +  \
		grec_sw_any(t) + grec_sh_any(t) + \
		grec_tx_any(t) + grec_ty_any(t) + grec_tw_any(t) + grec_th_any(t)

# Position for anchor. Mark iff x and y are nil. Otherwise Base.
def grec_anchor_pos(x,y):
	return 'anchor.pos.' + str(x) + '.' + str(y)
def grec_anchor_pos_all():
	syms = []
	for x in all_coords:
		for y in all_coords:
			syms += [grec_anchor_pos(x,y)]
	return syms
# Anchor for placing glyph.
def grec_anchor():
	return 'period'

# Further auxiliary symbols, treated as base.
def grec_dim(w,h):
	return 'grec.dim.' + str(w) + '.' + str(h)
def grec_dim_all():
	syms = []
	for w in all_glyph_sizes:
		for h in all_glyph_sizes:
			syms += [grec_dim(w,h)]
	return syms
def grec_preaux():
	return 'grec.preaux'
def grec_postaux():
	return 'grec.postaux'
def grec_aux_all():
	return grec_dim_all() + [grec_preaux(),grec_postaux()] + grec_anchor_pos_all()

# Auxiliary symbols for coordinate value to be added or subtracted.
def aux_val(s):
	return 'aux.val.' + str(s)
def aux_val_all():
	return [aux_val(s) for s in all_coords]
# Auxiliary symbols for divisor in division by glyph size. 
def aux_div(d):
	return 'aux.div.' + str(d)
def aux_div_all():
	return [aux_div(d) for d in all_group_sizes]
# Auxiliary symbols for scaling factor.
def aux_times(s):
	return 'aux.times.' + str(s)
def aux_times_all():
	return [aux_times(s) for s in all_group_scalings]
# All of the above. Plus nil anchor position. All mark.
def aux_all():
	return aux_val_all() + aux_div_all() + aux_times_all() + \
		[grec_anchor_pos('nil','nil'),jump('nil')]

# Symbolic names for glyphs, indexed from 0.
def glyph_base_name(i):
	# renaming doesn't work in ASCII range:
	# return 'glyph.base.' + str(i)
	return {
		0: 'A',
		1: 'B',
		2: 'C',
		3: 'D',
		4: 'E',
		5: 'F',
		6: 'G',
		7: 'H',
		8: 'I'
	}[i]

def glyph_mark_unscaled_name(i):
    return 'glyph.mark.unscaled.' + str(i)
def glyph_mark_scaled_name(i):
    return 'glyph.mark.scaled.' + str(i)
def glyph_base_name_all():
	return [glyph_base_name(i) for i in range(n_glyphs)]
def glyph_mark_unscaled_name_all():
	return [glyph_mark_unscaled_name(i) for i in range(n_glyphs)]
def glyph_mark_scaled_name_all():
	return [glyph_mark_scaled_name(i) for i in range(n_glyphs)]
def glyph_mark_name_all():
	return glyph_mark_unscaled_name_all() + glyph_mark_scaled_name_all()

glyph_mark_class = '@GLYPHMARKS'

# Jump to next group. Mark iff w is nil. Otherwise Base.
def jump(w):
	return 'jump.' + str(w)

def jump_all():
	syms = []
	for w in all_coords:
		syms += [jump(w)]
	return syms

# Insertion. Is mark.
def insertion():
	return 'insertion'

############################################

def record_symbols(t):
	return hor_any(t) + vert_any(t) + \
		hrec_any(t) + shrec_any(t) + vrec_any(t) + svrec_any(t) + \
		grec_any(t)

def add_aux_symbols_to(font):
	base_names = record_symbols('base') + grec_aux_all() + jump_all() + [vrec_jmp('none')]
	mark_names = record_symbols('mark') + aux_all() + [insertion()]

	i = aux_code_area
	for name in base_names:
		font.createChar(i, name)
		glyph = font[i]
		glyph.glyphclass = 'baseglyph'
		font[i].width = 0
		i += 1
	for name in mark_names:
		font.createChar(i, name)
		glyph = font[i]
		glyph.glyphclass = 'mark'
		font[i].width = 0
		i += 1
	# comma_glyph = font.createChar(ord(','))
	# comma_glyph.glyphclass = 'baseglyph'
	# h_glyph = font.createChar(ord('h'))
	# h_glyph.glyphclass = 'baseglyph'
	# comma_glyph.glyphclass = 'automatic'
	period_glyph = font.createChar(ord('.'))
	period_glyph.glyphclass = 'baseglyph'

# Make sure glyphs are not marks. Make scaled copies that are marks.
def make_glyphs(font):
	for i in range(n_glyphs):
		glyph = font.createChar(source_unscaled_code_area+i)
		glyph_base = font.createChar(base_code_area+i, glyph_base_name(i))
		glyph_base.glyphclass = 'baseglyph'
		glyph_mark = font.createChar(mark_unscaled_code_area+i, glyph_mark_unscaled_name(i))
		glyph_mark.glyphclass = 'mark'
	font.selection.select(("ranges", None), 
		source_unscaled_code_area, 
		source_unscaled_code_area+n_glyphs-1)
	font.cut()
	font.selection.select(("ranges", None), 
		base_code_area, 
		base_code_area+n_glyphs-1)
	font.paste()
	font.selection.select(("ranges", None), 
		mark_unscaled_code_area, 
		mark_unscaled_code_area+n_glyphs-1)
	font.paste()

	for i in range(n_glyphs):
		glyph_mark = font.createChar(mark_scaled_code_area+i, glyph_mark_scaled_name(i))
		glyph_mark.glyphclass = 'mark'
		glyph_mark.width = 1000
	font.selection.select(("ranges", None), 
		source_scaled_code_area, 
		source_scaled_code_area+n_glyphs-1)
	font.cut()
	font.selection.select(("ranges", None), 
		mark_scaled_code_area, 
		mark_scaled_code_area+n_glyphs-1)
	font.paste()

	for i in range(n_glyphs):
		font.createChar(base_code_area+i).width = 1000
		font.createChar(mark_unscaled_code_area+i).width = 1000
		font.createChar(mark_scaled_code_area+i).width = 1000

	if False:
		font.selection.select(("ranges", None), ord(' '), ord(' '))
		font.copy()
		for x in all_coords:
			for y in all_coords:
				glyph_pos = font.createChar(-1, grec_anchor_pos(x,y))
				code = glyph_pos.encoding
				font.selection.select(("ranges", None), code, code)
				font.paste()

	#font.createChar(-1,'asciicircum').glyphclass = 'mark'
	font.createChar(94).glyphclass = 'mark'

##################################################

# All symbols that are visible (mark rather than base).
mark_aux_symbols = []

# Make the symbols the only mark symbols.
def make_only_visible(f, marks):
	global mark_aux_symbols
	symbols_to_base = list(set(mark_aux_symbols) - set(marks))
	symbols_to_mark = list(set(marks) - set(mark_aux_symbols))
	if len(symbols_to_base) + len(symbols_to_mark) > 0:
		start_lookup(f)
		for sym in symbols_to_base:
			create_sub(f, [aux_type(sym,'mark')], [aux_type(sym,'base')])
		for sym in symbols_to_mark:
			create_sub(f, [aux_type(sym,'base')], [aux_type(sym,'mark')])
		end_lookup(f)
	mark_aux_symbols = marks

##################################################

def make_mark_class(f):
	mark_class(f, glyph_mark_name_all(), glyph_mark_class)
	# mark_class(f, ['a','b','c','d','asciicircum'], '@TESTCLASS')
	mark_class(f, ['asciicircum'], '@TESTCLASS')

def initialize(f):
	start_lookup(f)
	create_sub(f, ['asterisk'],[hor_op()])
	create_sub(f, ['colon'],[vert_op()])
	end_lookup(f)

def add_brackets(f):
	start_lookup(f)
	for (i,w,h) in glyph_dimensions:
		create_sub(f, [glyph_base_name(i)], [grec_preaux(),glyph_base_name(i),grec_dim(w,h)])
	end_lookup(f)

	start_lookup(f)
	create_sub(f, [grec_preaux()], 
		[vert_open(),hor_open(),grec_anchor()])
	for w in all_glyph_sizes:
		for h in all_glyph_sizes:
			create_sub(f, [grec_dim(w,h)], 
				[grec_s('nil','base'),grec_w(w,'base'),grec_h(h,'base'),grec_postaux()])
	end_lookup(f)

	start_lookup(f)
	create_sub(f, [grec_postaux()], 
		[grec_sw('nil','base'),grec_sh('nil','base'), 
			grec_tx('nil','base'),grec_ty('nil','base'),
			grec_tw('nil','base'),grec_th('nil','base'), 
			hor_close(),vert_close()])
	end_lookup(f)

def remove_brackets(f):
	start_lookup(f)
	create_sub(f, [vert_close(),hor_op(),vert_open()], [hor_op()])
	create_sub(f, [vert_close(),vert_op(),vert_open()], [vert_op()])
	end_lookup(f)

	start_lookup(f)
	create_sub(f, [hor_close(),hor_op(),hor_open()], [hor_op()])
	end_lookup(f)

def add_records(f):
	start_lookup(f)
	create_sub(f, [hor_open()], [hor_open()] + hrec_init())
	create_sub(f, [hor_op()], shrec_init() + [hor_op()])
	create_sub(f, [hor_close()], shrec_init_zero() + [hor_close()])
	create_sub(f, [vert_open()], [vert_open()] + vrec_init())
	create_sub(f, [vert_op()], svrec_init() + [vert_op()])
	create_sub(f, [vert_close()], svrec_init_zero() + [vert_close(),jump('nil')])
	end_lookup(f)

def sum_widths(f):
	make_only_visible(f, [hrec_bw('nil','')]+hrec_w_any()+shrec_w_any()+grec_w_any())
	"""
	start_reversal_mark_lookup(f)
	for w1 in all_glyph_sizes:
		w2 = 0
		create_sub_mid(f, [], [shrec_w('nil')], [grec_w(w1),shrec_w(w2)], shrec_w(w1+w2))
	end_lookup(f)
	"""
	# TODO need upper bit
	for n in range(max_hor_group_len-1):
		start_mark_lookup(f)
		for w1 in all_glyph_sizes:
			for w2 in group_sizes_len(n):
				create_sub_mid(f, [], [shrec_w('nil')], [grec_w(w1),shrec_w(w2)],
					shrec_w(w1+w2))
		end_lookup(f)
	
	start_mark_lookup(f)
	for w1 in all_glyph_sizes:
		for w2 in group_sizes_len_zero_to(max_hor_group_len-1):
			create_sub_mid(f, [], [hrec_w('nil')], [grec_w(w1),shrec_w(w2)], 
				hrec_w(w1+w2))
	end_lookup(f)

	start_mark_lookup(f)
	for w in group_sizes_len_one_to(max_hor_group_len):
		create_sub_mid(f, [], [hrec_bw('nil')], [hrec_w(w)], 
			hrec_bw(min(w,max_glyph_size),'base'))
	end_lookup(f)

def max_heights(f):
	make_only_visible(f, [hrec_h('nil','')]+shrec_h_any()+grec_h_any())
	
	start_reversal_mark_lookup(f)
	for h1 in all_glyph_sizes:
		tail_heights = all_glyph_sizes
		for h2 in tail_heights:
			create_sub_mid(f, [], [shrec_h('nil')], [grec_h(h1),shrec_h(h2)], 
				shrec_h(max(h1,h2)))
	end_lookup(f)
	
	start_mark_lookup(f)
	for h1 in all_glyph_sizes:
		for h2 in all_glyph_sizes_and_zero:
			create_sub_mid(f, [], [hrec_h('nil')], [grec_h(h1),shrec_h(h2)], 
				hrec_h(max(h1,h2),'base'))
	end_lookup(f)

def max_widths(f):
	make_only_visible(f, [vrec_w('nil','')]+svrec_w_any()+hrec_bw_any())
	
	start_reversal_mark_lookup(f)
	for w1 in all_glyph_sizes:
		for w2 in all_glyph_sizes:
			create_sub_mid(f, [], [svrec_w('nil')], [hrec_bw(w1),svrec_w(w2)], 
				svrec_w(max(w1,w2)))
	end_lookup(f)

	start_mark_lookup(f)
	for w1 in all_glyph_sizes:
		for w2 in all_glyph_sizes_and_zero:
			create_sub_mid(f, [], [vrec_w('nil')], [hrec_bw(w1),svrec_w(w2)], 
				vrec_w(max(w1,w2),'base'))
	end_lookup(f)

def sum_heights(f):
	make_only_visible(f, [vrec_bh('nil','')]+vrec_h_any()+svrec_h_any()+hrec_h_any())
	
	start_reversal_mark_lookup(f)
	for h1 in all_glyph_sizes:
		for h2 in group_sizes_len(1):
			create_sub_mid(f, [], [svrec_h('nil')], [hrec_h(h1),svrec_h(h2)], svrec_h(h1+h2), True)
	end_lookup(f)
	"""
	# TODO we actually need the bit above
	for n in range(max_vert_group_len-1):
		start_mark_lookup(f)
		for h1 in all_glyph_sizes:
			for h2 in group_sizes_len(n):
				create_sub_mid(f, [], [svrec_h('nil')], [hrec_h(h1),svrec_h(h2)], 
					svrec_h(h1+h2))
		end_lookup(f)
	"""
	start_mark_lookup(f)
	for h1 in all_glyph_sizes:
		for h2 in group_sizes_len_zero_to(max_vert_group_len-1):
			create_sub_mid(f, [], [vrec_h('nil')], [hrec_h(h1),svrec_h(h2)], 
				vrec_h(h1+h2))
	end_lookup(f)

	start_mark_lookup(f)
	for h in group_sizes_len_one_to(max_vert_group_len):
		create_sub_mid(f, [], [vrec_bh('nil')], [vrec_h(h)], 
			vrec_bh(min(h,max_glyph_size),'base'))
	end_lookup(f)

def left_bottom_insert(f):
	start_lookup(f)
	create_sub(f, [jump('nil'),'slash'], [insertion()])
	end_lookup(f)

	make_only_visible(f, vrec_ty_any())
	start_mark_lookup(f)
	create_sub_mid(f, [insertion()], [vrec_ty('nil')], [],
			vrec_ty(unit_coord-2*step_coord))
	end_lookup(f)

	make_only_visible(f, vrec_th_any())
	start_mark_lookup(f)
	create_sub_mid(f, [insertion()], [vrec_th('nil')], [],
			vrec_th(unit_coord-2*step_coord))
	end_lookup(f)

	make_only_visible(f, vrec_jmp_any())
	start_mark_lookup(f)
	create_sub_mid(f, [insertion()], [vrec_jmp('nil')], [],
			vrec_jmp('none'))
	end_lookup(f)

def target_x(f):
	start_lookup(f)
	create_sub(f, [vrec_tx('nil','base')],[vrec_tx(0,'base')])
	end_lookup(f)

def target_y(f):
	start_lookup(f)
	create_sub(f, [vrec_ty('nil','base')],[vrec_ty(unit_coord,'base')])
	end_lookup(f)

def target_width(f):
	make_only_visible(f, vrec_w_any()+[vrec_tw('nil','')])
	start_mark_lookup(f)
	for w in all_glyph_sizes:
		create_sub_mid(f, [vrec_w(w)], [vrec_tw('nil')], [],
			vrec_tw(safe_size_to_coord(w),'base'))
	end_lookup(f)

	make_only_visible(f, vrec_w_any()+[vrec_jmp('nil','')])
	start_mark_lookup(f)
	for w in all_glyph_sizes:
		create_sub_mid(f, [vrec_w(w)], [vrec_jmp('nil')], [],
			vrec_jmp(safe_size_to_coord(w),'base'))
	end_lookup(f)

def target_height(f):
	make_only_visible(f, vrec_bh_any()+[vrec_th('nil','')])
	start_mark_lookup(f)
	for h in all_glyph_sizes:
		create_sub_mid(f, [vrec_bh(h)], [vrec_th('nil')], [],
			vrec_th(max(safe_size_to_coord(h),unit_coord),'base'))
	end_lookup(f)

def prop_vert_x(f):
	make_only_visible(f, vrec_tx_any()+svrec_tx_any())
	start_mark_lookup(f)
	for x in all_coords:
		create_sub_mid(f, [vrec_tx(x)], [svrec_tx('nil')], [],
			svrec_tx(x))
	end_lookup(f)
	
	start_reversal_mark_lookup(f)
	for x in all_coords:
		create_sub_mid(f, [svrec_tx(x)], [svrec_tx('nil')], [],
			svrec_tx(x))
	end_lookup(f)

	make_only_visible(f, hrec_tx_any()+svrec_tx_any())
	start_mark_lookup(f)
	for x in all_coords:
		create_sub_mid(f, [], [hrec_tx('nil')], [svrec_tx(x)], 
			hrec_tx(x))
	end_lookup(f)

def prop_vert_width(f):
	make_only_visible(f, vrec_jmp_any())
	start_mark_lookup(f)
	for w in all_coords:
		create_sub_mid(f, [vrec_jmp(w)], [jump('nil')], [],
			jump(w))
		create_sub_mid(f, [insertion()], [jump('nil')], [],
			jump(1000))
	end_lookup(f)

	make_only_visible(f, vrec_tw_any()+svrec_tw_any())
	start_mark_lookup(f)
	for w in all_coords:
		create_sub_mid(f, [vrec_tw(w)], [svrec_tw('nil')], [],
			svrec_tw(w))
	end_lookup(f)

	
	start_reversal_mark_lookup(f)
	for w in all_coords:
		create_sub_mid(f, [svrec_tw(w)], [svrec_tw('nil')], [],
			svrec_tw(w))
	end_lookup(f)

	make_only_visible(f, hrec_tw_any()+svrec_tw_any())
	start_mark_lookup(f)
	for w in all_coords:
		create_sub_mid(f, [], [hrec_tw('nil')], [svrec_tw(w)],
			hrec_tw(w))
	end_lookup(f)

def prop_vert_y_height(f):
	if None:
		make_only_visible(f, vrec_h_any()+vrec_th_any()+hrec_s_any())
		start_mark_lookup(f)
		for h1 in group_sizes_len_one_to(max_vert_group_len):
			for h2 in all_coords:
				create_sub_mid(f, [vrec_h(h1),vrec_th(h2)], [hrec_s('nil')], [],
					hrec_s(safe_coord_size_div(h2,h1)))
		end_lookup(f)
	make_only_visible(f, vrec_h_any()+hrec_s_any())
	start_mark_lookup(f)
	for h1 in group_sizes_len_one_to(max_vert_group_len):
		create_sub_mid(f, [vrec_h(h1)], [hrec_s('nil')], [], 
			aux_div(h1))
	end_lookup(f)
	make_only_visible(f, vrec_th_any()+hrec_s_any())
	start_mark_lookup(f)
	for h1 in group_sizes_len_one_to(max_vert_group_len):
		for h2 in all_coords:
			create_sub_mid(f, [vrec_th(h2)], [aux_div(h1)], [],
				hrec_s(safe_coord_size_div(h2,h1)))
	end_lookup(f)

	if None:
		make_only_visible(f, vrec_th_any()+hrec_h_any()+hrec_s_any()+hrec_th_any())
		start_mark_lookup(f)
		for h in all_glyph_sizes:
			for s in all_group_scalings:
				create_sub_mid(f, [hrec_h(h),hrec_s(s)], [hrec_th('nil')], [],
					hrec_th(safe_size_mult_to_coord(s,h)))
		end_lookup(f)
	make_only_visible(f, vrec_th_any()+hrec_s_any()+hrec_th_any())
	start_mark_lookup(f)
	for s in all_group_scalings:
		create_sub_mid(f, [hrec_s(s)], [hrec_th('nil')], [],
			aux_times(s))
	end_lookup(f)
	make_only_visible(f, vrec_th_any()+hrec_h_any()+hrec_th_any())
	start_mark_lookup(f)
	for h in all_glyph_sizes:
		for s in all_group_scalings:
			create_sub_mid(f, [hrec_h(h)], [aux_times(s)], [],
				hrec_th(safe_size_mult_to_coord(s,h)))
	end_lookup(f)

	if None:
		make_only_visible(f, vrec_th_any()+hrec_th_any()+svrec_th_any())
		start_mark_lookup(f)
		for h1 in all_coords:
			for h2 in all_coords:
				create_sub_mid(f, [vrec_th(h1),hrec_th(h2)], [svrec_th('nil')], [],
					svrec_th(safe_coord_minus(h1,h2)))
		end_lookup(f)
	make_only_visible(f, vrec_th_any()+hrec_th_any()+svrec_th_any())
	start_mark_lookup(f)
	for h2 in all_coords:
		create_sub_mid(f, [hrec_th(h2)], [svrec_th('nil')], [],
			aux_val(h2))
	end_lookup(f)
	make_only_visible(f, vrec_th_any()+svrec_th_any())
	start_mark_lookup(f)
	for h1 in all_coords:
		for h2 in all_coords:
			create_sub_mid(f, [vrec_th(h1)], [aux_val(h2)], [],
				svrec_th(safe_coord_minus(h1,h2)))
	end_lookup(f)

	if None:
		make_only_visible(f, vrec_ty_any()+hrec_th_any()+svrec_ty_any())
		start_mark_lookup(f)
		for y in all_coords:
			for h in all_coords:
				create_sub_mid(f, [vrec_ty(h),hrec_th(h)], [svrec_ty('nil')], [],
					svrec_ty(safe_coord_minus(y,h)))
		end_lookup(f)
	make_only_visible(f, vrec_ty_any()+hrec_th_any()+svrec_ty_any())
	start_mark_lookup(f)
	for h in all_coords:
		create_sub_mid(f, [hrec_th(h)], [svrec_ty('nil')], [],
			aux_val(h))
	end_lookup(f)
	make_only_visible(f, vrec_ty_any()+svrec_ty_any())
	start_mark_lookup(f)
	for y in all_coords:
		for h in all_coords:
			create_sub_mid(f, [vrec_ty(y)], [aux_val(h)], [],
				svrec_ty(safe_coord_minus(y,h)))
	end_lookup(f)

	for n in range(max_vert_group_len-1,0,-1):
		if None:
			make_only_visible(f, svrec_h_any()+svrec_th_any()+hrec_s_any()+vrec_ty_any())
			start_mark_lookup(f)
			for h1 in group_sizes_len(n):
				for h2 in all_coords:
					create_sub_mid(f, [svrec_h(h1),svrec_th(h2)], [hrec_s('nil')], [],
						hrec_s(safe_coord_size_div(h2,h1)))
			end_lookup(f)
		make_only_visible(f, svrec_h_any()+hrec_s_any()+vrec_ty_any())
		start_mark_lookup(f)
		for h1 in group_sizes_len(n):
			create_sub_mid(f, [svrec_h(h1)], [hrec_s('nil')], [],
				aux_div(h1))
		end_lookup(f)
		make_only_visible(f, svrec_th_any()+hrec_s_any()+vrec_ty_any())
		start_mark_lookup(f)
		for h1 in group_sizes_len(n):
			for h2 in all_coords:
				create_sub_mid(f, [svrec_th(h2)], [aux_div(h1)], [],
					hrec_s(safe_coord_size_div(h2,h1)))
		end_lookup(f)

		if None:
			make_only_visible(f, svrec_th_any()+hrec_h_any()+hrec_s_any()+hrec_th_any()+vrec_ty_any())
			start_mark_lookup(f)
			for h in all_glyph_sizes:
				for s in all_group_scalings:
					create_sub_mid(f, [hrec_h(h),hrec_s(s)], [hrec_th('nil')], [],
						hrec_th(safe_size_mult_to_coord(s,h)))
			end_lookup(f)
		make_only_visible(f, svrec_th_any()+hrec_s_any()+hrec_th_any()+vrec_ty_any())
		start_mark_lookup(f)
		for s in all_group_scalings:
			create_sub_mid(f, [hrec_s(s)], [hrec_th('nil')], [],
				aux_times(s))
		end_lookup(f)
		make_only_visible(f, svrec_th_any()+hrec_h_any()+hrec_th_any()+vrec_ty_any())
		start_mark_lookup(f)
		for h in all_glyph_sizes:
			for s in all_group_scalings:
				create_sub_mid(f, [hrec_h(h)], [aux_times(s)], [],
					hrec_th(safe_size_mult_to_coord(s,h)))
		end_lookup(f)

		if None:
			make_only_visible(f, svrec_th_any()+hrec_th_any()+vrec_ty_any())
			start_mark_lookup(f)
			for h1 in all_coords:
				for h2 in all_coords:
					create_sub_mid(f, [svrec_th(h1),hrec_th(h2)], [svrec_th('nil')], [],
						svrec_th(safe_coord_minus(h1,h2)))
			end_lookup(f)
		make_only_visible(f, svrec_th_any()+hrec_th_any()+vrec_ty_any())
		start_mark_lookup(f)
		for h2 in all_coords:
			create_sub_mid(f, [hrec_th(h2)], [svrec_th('nil')], [],
				aux_val(h2))
		end_lookup(f)
		make_only_visible(f, svrec_th_any()+vrec_ty_any())
		start_mark_lookup(f)
		for h1 in all_coords:
			for h2 in all_coords:
				create_sub_mid(f, [svrec_th(h1)], [aux_val(h2)], [],
					svrec_th(safe_coord_minus(h1,h2)))
		end_lookup(f)

		if None:
			make_only_visible(f, svrec_ty_any()+hrec_th_any()+vrec_ty_any())
			start_mark_lookup(f)
			for y in all_coords:
				for h in all_coords:
					create_sub_mid(f, [svrec_ty(y),hrec_th(h)], [svrec_ty('nil')], [],
						svrec_ty(safe_coord_minus(y,h)))
			end_lookup(f)
		make_only_visible(f, svrec_ty_any()+hrec_th_any()+vrec_ty_any())
		start_mark_lookup(f)
		for h in all_coords:
			create_sub_mid(f, [hrec_th(h)], [svrec_ty('nil')], [],
				aux_val(h))
		end_lookup(f)
		make_only_visible(f, svrec_ty_any()+vrec_ty_any())
		start_mark_lookup(f)
		for y in all_coords:
			for h in all_coords:
				create_sub_mid(f, [svrec_ty(y)], [aux_val(h)], [],
					svrec_ty(safe_coord_minus(y,h)))
		end_lookup(f)

	make_only_visible(f, svrec_ty_any()+hrec_ty_any()+vrec_ty_any())
	start_mark_lookup(f)
	for y in all_coords:
		create_sub_mid(f, [], [hrec_ty('nil')], [svrec_ty(y)],
			hrec_ty(y))
	end_lookup(f)

def prop_hor_x_width(f):
	if None:
		make_only_visible(f, hrec_w_any()+hrec_tw_any()+grec_sw_any())
		start_mark_lookup(f)
		for w1 in group_sizes_len_one_to(max_hor_group_len):
			for w2 in all_coords:
				create_sub_mid(f, [hrec_w(w1),hrec_tw(w2)], [grec_sw('nil')], [],
					grec_sw(safe_coord_size_div(w2,w1)))
		end_lookup(f)
	make_only_visible(f, hrec_w_any()+grec_sw_any())
	start_mark_lookup(f)
	for w1 in group_sizes_len_one_to(max_hor_group_len):
		create_sub_mid(f, [hrec_w(w1)], [grec_sw('nil')], [],
			aux_div(w1))
	end_lookup(f)
	make_only_visible(f, hrec_tw_any()+grec_sw_any())
	start_mark_lookup(f)
	for w1 in group_sizes_len_one_to(max_hor_group_len):
		for w2 in all_coords:
			create_sub_mid(f, [hrec_tw(w2)], [aux_div(w1)], [],
				grec_sw(safe_coord_size_div(w2,w1)))
	end_lookup(f)

	if None:
		make_only_visible(f, hrec_tw_any()+grec_w_any()+grec_sw_any()+grec_tw_any())
		start_mark_lookup(f)
		for w in all_glyph_sizes:
			for s in all_group_scalings:
				create_sub_mid(f, [grec_w(w),grec_sw(s)], [grec_tw('nil')], [],
					grec_tw(safe_size_mult_to_coord(s,w)))
		end_lookup(f)
	make_only_visible(f, hrec_tw_any()+grec_sw_any()+grec_tw_any())
	start_mark_lookup(f)
	for s in all_group_scalings:
		create_sub_mid(f, [grec_sw(s)], [grec_tw('nil')], [],
			aux_times(s))
	end_lookup(f)
	make_only_visible(f, hrec_tw_any()+grec_w_any()+grec_tw_any())
	start_mark_lookup(f)
	for w in all_glyph_sizes:
		for s in all_group_scalings:
			create_sub_mid(f, [grec_w(w)], [aux_times(s)], [],
				grec_tw(safe_size_mult_to_coord(s,w)))
	end_lookup(f)

	if None:
		make_only_visible(f, hrec_tw_any()+grec_tw_any()+shrec_tw_any())
		start_mark_lookup(f)
		for w1 in all_coords:
			for w2 in all_coords:
				create_sub_mid(f, [hrec_tw(w1),grec_tw(w2)], [shrec_tw('nil')], [],
					shrec_tw(safe_coord_minus(w1,w2)))
		end_lookup(f)
	make_only_visible(f, hrec_tw_any()+grec_tw_any()+shrec_tw_any())
	start_mark_lookup(f)
	for w2 in all_coords:
		create_sub_mid(f, [grec_tw(w2)], [shrec_tw('nil')], [],
			aux_val(w2))
	end_lookup(f)
	make_only_visible(f, hrec_tw_any()+shrec_tw_any())
	start_mark_lookup(f)
	for w1 in all_coords:
		for w2 in all_coords:
			create_sub_mid(f, [hrec_tw(w1)], [aux_val(w2)], [],
				shrec_tw(safe_coord_minus(w1,w2)))
	end_lookup(f)

	if None:
		make_only_visible(f, hrec_tx_any()+grec_tw_any()+shrec_tx_any())
		start_mark_lookup(f)
		for x in all_coords:
			for w in all_coords:
				create_sub_mid(f, [hrec_tx(x),grec_tw(w)], [shrec_tx('nil')], [],
					shrec_tx(safe_coord_plus(x,w)))
		end_lookup(f)
	make_only_visible(f, hrec_tx_any()+grec_tw_any()+shrec_tx_any())
	start_mark_lookup(f)
	for w in all_coords:
		create_sub_mid(f, [grec_tw(w)], [shrec_tx('nil')], [],
			aux_val(w))
	end_lookup(f)
	make_only_visible(f, hrec_tx_any()+shrec_tx_any())
	start_mark_lookup(f)
	for x in all_coords:
		for w in all_coords:
			create_sub_mid(f, [hrec_tx(x)], [aux_val(w)], [],
				shrec_tx(safe_coord_plus(x,w)))
	end_lookup(f)

	make_only_visible(f, hrec_tx_any()+grec_tx_any())
	start_mark_lookup(f)
	for x in all_coords:
		create_sub_mid(f, [hrec_tx(x)], [grec_tx('nil')], [],
			grec_tx(x))
	end_lookup(f)

	for n in range(max_hor_group_len-1,0,-1):
		if None:
			make_only_visible(f, shrec_w_any()+shrec_tw_any()+grec_sw_any()+hrec_tx_any())
			start_mark_lookup(f)
			for w1 in group_sizes_len(n):
				for w2 in all_coords:
					create_sub_mid(f, [shrec_w(w1),shrec_tw(w2)], [grec_sw('nil')], [],
						grec_sw(safe_coord_size_div(w2,w1)))
			end_lookup(f)
		make_only_visible(f, shrec_w_any()+grec_sw_any()+hrec_tx_any())
		start_mark_lookup(f)
		for w1 in group_sizes_len(n):
			create_sub_mid(f, [shrec_w(w1)], [grec_sw('nil')], [],
				aux_div(w1))
		end_lookup(f)
		make_only_visible(f, shrec_tw_any()+grec_sw_any()+hrec_tx_any())
		start_mark_lookup(f)
		for w1 in group_sizes_len(n):
			for w2 in all_coords:
				create_sub_mid(f, [shrec_tw(w2)], [aux_div(w1)], [],
					grec_sw(safe_coord_size_div(w2,w1)))
		end_lookup(f)

		if None:
			make_only_visible(f, shrec_tw_any()+grec_w_any()+grec_sw_any()+grec_tw_any()+hrec_tx_any())
			start_mark_lookup(f)
			for w in all_glyph_sizes:
				for s in all_group_scalings:
					create_sub_mid(f, [grec_w(w),grec_sw(s)], [grec_tw('nil')], [],
						grec_tw(safe_size_mult_to_coord(s,w)))
			end_lookup(f)
		make_only_visible(f, shrec_tw_any()+grec_sw_any()+grec_tw_any()+hrec_tx_any())
		start_mark_lookup(f)
		for s in all_group_scalings:
			create_sub_mid(f, [grec_sw(s)], [grec_tw('nil')], [],
				aux_times(s))
		end_lookup(f)
		make_only_visible(f, shrec_tw_any()+grec_w_any()+grec_tw_any()+hrec_tx_any())
		start_mark_lookup(f)
		for w in all_glyph_sizes:
			for s in all_group_scalings:
				create_sub_mid(f, [grec_w(w)], [aux_times(s)], [],
					grec_tw(safe_size_mult_to_coord(s,w)))
		end_lookup(f)

		if None:
			make_only_visible(f, shrec_tw_any()+grec_tw_any()+hrec_tx_any())
			start_mark_lookup(f)
			for w1 in all_coords:
				for w2 in all_coords:
					create_sub_mid(f, [shrec_tw(w1),grec_tw(w2)], [shrec_tw('nil')], [],
						shrec_tw(safe_coord_minus(w1,w2)))
			end_lookup(f)
		make_only_visible(f, shrec_tw_any()+grec_tw_any()+hrec_tx_any())
		start_mark_lookup(f)
		for w2 in all_coords:
			create_sub_mid(f, [grec_tw(w2)], [shrec_tw('nil')], [],
				aux_val(w2))
		end_lookup(f)
		make_only_visible(f, shrec_tw_any()+hrec_tx_any())
		start_mark_lookup(f)
		for w1 in all_coords:
			for w2 in all_coords:
				create_sub_mid(f, [shrec_tw(w1)], [aux_val(w2)], [],
					shrec_tw(safe_coord_minus(w1,w2)))
		end_lookup(f)

		if None:
			make_only_visible(f, shrec_tx_any()+grec_tw_any()+hrec_tx_any())
			start_mark_lookup(f)
			for x in all_coords:
				for w in all_coords:
					create_sub_mid(f, [shrec_tx(x),grec_tw(w)], [shrec_tx('nil')], [],
						shrec_tx(safe_coord_plus(x,w)))
			end_lookup(f)
		make_only_visible(f, shrec_tx_any()+grec_tw_any()+hrec_tx_any())
		start_mark_lookup(f)
		for w in all_coords:
			create_sub_mid(f, [grec_tw(w)], [shrec_tx('nil')], [],
				aux_val(w))
		end_lookup(f)
		make_only_visible(f, shrec_tx_any()+hrec_tx_any())
		start_mark_lookup(f)
		for x in all_coords:
			for w in all_coords:
				create_sub_mid(f, [shrec_tx(x)], [aux_val(w)], [],
					shrec_tx(safe_coord_plus(x,w)))
		end_lookup(f)

	make_only_visible(f, shrec_tx_any()+grec_tx_any()+hrec_tx_any())
	start_mark_lookup(f)
	for x in all_coords:
		create_sub_mid(f, [shrec_tx(x)], [grec_tx('nil')], [],
			grec_tx(x))
	end_lookup(f)

def prop_hor_y(f):
	make_only_visible(f, hrec_ty_any()+shrec_ty_any())
	start_mark_lookup(f)
	for y in all_coords:
		create_sub_mid(f, [hrec_ty(y)], [shrec_ty('nil')], [],
			shrec_ty(y))
	end_lookup(f)
	
	start_reversal_mark_lookup(f)
	for y in all_coords:
		create_sub_mid(f, [shrec_ty(y)], [shrec_ty('nil')], [],
			shrec_ty(y))
	end_lookup(f)

	make_only_visible(f, grec_ty_any()+shrec_ty_any())
	start_mark_lookup(f)
	for y in all_coords:
		create_sub_mid(f, [], [grec_ty('nil')], [shrec_ty(y)],
			grec_ty(y))
	end_lookup(f)

def prop_hor_height(f):
	make_only_visible(f, hrec_th_any()+shrec_th_any())
	start_mark_lookup(f)
	for h in all_coords:
		create_sub_mid(f, [hrec_th(h)], [shrec_th('nil')], [],
			shrec_th(h))
	end_lookup(f)
	
	start_reversal_mark_lookup(f)
	for h in all_coords:
		create_sub_mid(f, [shrec_th(h)], [shrec_th('nil')], [],
			shrec_th(h))
	end_lookup(f)

	make_only_visible(f, grec_th_any()+shrec_th_any())
	start_mark_lookup(f)
	for h in all_coords:
		create_sub_mid(f, [], [grec_th('nil')], [shrec_th(h)],
			grec_th(h))
	end_lookup(f)

def increment_group(f):
	start_lookup(f)
	for w in all_coords:
		create_pos(f, [], [jump(w)], [], 0, 0, w+100, 0)
	end_lookup(f)

def make_glyph_scalings(f):
	start_lookup(f)
	for s in all_group_scalings:
		create_sub(f, [grec_sw(s,'base')], [grec_sw(min(s,unit_scale),'base')])
	end_lookup(f)

	make_only_visible(f, grec_h_any()+grec_sh_any()+grec_th_any())
	start_mark_lookup(f)
	for h1 in all_glyph_sizes:
		for h2 in all_coords:
			create_sub_mid(f, [grec_h(h1)], [grec_sh('nil')], [grec_th(h2)],
				grec_sh(min(safe_coord_size_div(h2,h1),unit_scale)))
	end_lookup(f)

	make_only_visible(f, grec_s_any()+grec_sw_any()+grec_sh_any())
	start_mark_lookup(f)
	for s1 in all_glyph_scalings:
		for s2 in all_glyph_scalings:
			create_sub_mid(f, [], [grec_s('nil')], [grec_sw(s1),grec_sh(s2)], 
				grec_s(min(s1,s2)))
	end_lookup(f)

def place_glyphs1(f):
	start_lookup(f)
	create_sub(f, [grec_anchor()], [grec_anchor_pos('nil','nil')])
	end_lookup(f)

	make_only_visible(f, grec_tx_any()+grec_ty_any())
	start_mark_lookup(f)
	for x in all_coords:
		for y in all_coords:
			create_sub_mid(f, [], [grec_anchor_pos('nil','nil')], [grec_tx(x),grec_ty(y)],
				grec_anchor_pos(x,y))
	end_lookup(f)

def place_glyphs2(f):
	start_lookup(f)
	for x in all_coords:
		for y in all_coords:
			create_pos(f, [grec_anchor_pos(x,y)], [grec_anchor()], [], x, y, -1000, 0)
	end_lookup(f)

def scale_glyphs(f):
	start_lookup(f)
	for i in range(n_glyphs):
		create_sub_mid(f, [], [glyph_base_name(i)], [grec_s(min_scale,'base')], glyph_mark_scaled_name(i))
	for i in range(n_glyphs):
		create_sub_mid(f, [], [glyph_base_name(i)], [grec_s(unit_scale,'base')], glyph_mark_unscaled_name(i))
	end_lookup(f)
	start_lookup(f)
	for i in range(n_glyphs):
		create_sub(f, [glyph_mark_scaled_name(i)], [grec_anchor(),glyph_mark_scaled_name(i)])
		create_sub(f, [glyph_mark_unscaled_name(i)], [grec_anchor(),glyph_mark_unscaled_name(i)])
	end_lookup(f)

def anchor_glyphs(f):
	start_feat(f, 'mark')
	start_lookup(f, 'mark')
	f.write('pos base ' + grec_anchor() + ' <anchor 0 0> mark ' + glyph_mark_class + ';\n')
	# f.write('pos base ' + grec_anchor() + ' <anchor 0 0> mark @TESTCLASS;\n')
	# f.write('pos base b <anchor 0 0> mark @TESTCLASS;\n')
	# f.write('pos base a <anchor 0 0> mark @TESTCLASS;\n')
	# f.write('pos base b <anchor 0 0> mark @TESTCLASS;\n')
	# f.write('pos base c <anchor 0 0> mark @TESTCLASS;\n')
	# f.write('pos base a <anchor 0 0> mark ' + glyph_mark_class + ';\n')
	# f.write('pos base b <anchor 0 0> mark ' + glyph_mark_class + ';\n')
	# f.write('pos base c <anchor 0 0> mark ' + glyph_mark_class + ';\n')
	# f.write('pos base ' + grec_anchor() + ' <anchor 0 0> mark @TESTCLASS;\n')
	end_lookup(f, 'mark')
	end_feat(f, 'mark')

# Make symbols visible. 
def test_convert(f):
	# start_lookup(f)
	# create_sub(f, [shrec_tx('nil','base')], [shrec_tx('nil','mark')])
	# create_sub(f, [grec_s('nil','base')], [grec_w(333,'mark')])
	# create_sub(f, [shrec_w(0,'base')], [shrec_w(0,'mark')])
	# create_sub(f, [shrec_w('nil','base')], [shrec_w('nil','mark')])
	# create_sub(f, [grec_w(333,'base')], [grec_w(333,'mark')])
	# create_sub(f, [grec_tx('nil','base')], [grec_tx('nil','mark')])
	# create_sub(f, [grec_h(666,'base')], [grec_h(666,'mark')])
	# end_lookup(f)
	# start_mark_lookup(f)
	# create_sub_mid(f, [hrec_bw('nil','mark')], [grec_w(333,'mark')], [], 'a')
	# create_sub_mid(f, [hrec_bw('nil','mark')], [grec_w(333,'mark')], [], 'a')
	# create_sub_mid(f, [], [grec_w(333,'mark')], [], 'e')
	# create_sub_mid(f, [grec_w(333,'mark')], [grec_h(666,'mark')], [], 'f')
	# create_sub_mid(f, [shrec_tx('nil','mark')], [grec_h(666,'mark')], [], 'f')
	# create_sub_mid(f, [], [grec_tx('nil','mark')], [], 'p')
	# create_sub_mid(f, [shrec_tx('nil','mark')], [shrec_tx('nil','mark')], [], 'q')
	# create_sub_mid(f, [], [shrec_w(0,'mark')], [], 't')
	# create_sub_mid(f, [], [shrec_w('nil','mark')], [grec_w(333,'mark'),shrec_w(0,'mark')], 'q')
	# create_sub_mid(f, [shrec_w('nil','mark')], [grec_w(333,'mark')], [], 'a')
	# end_lookup(f)

	# start_mark_lookup_xxx(f)
	# right_to_left_feature(f)
	#create_sub_mid(f, [], [vrec_h(999,'mark')], [vrec_th(1000,'mark'),hrec_s('nil','mark')], 'z')
	# create_sub_mid(f, [vrec_h(999,'mark'), vrec_th(1000,'mark')], [hrec_s('nil','mark')], [], 'z')
	# create_sub_mid(f, [vrec_h(999,'mark')], [vrec_th(1000,'mark')], [], 'z')
	# create_sub_mid(f, [vrec_th(1000,'mark')], [hrec_s('nil','mark')], [], 'z')
	# create_sub_mid(f, [], [vrec_h(999,'mark')], [vrec_th(1000,'mark'),hrec_s('nil','mark')], 'z')
	# end_lookup(f)

	start_lookup(f)
	create_sub(f, [hor_open()], ['h','o'])
	create_sub(f, [hor_close()], ['h','c'])
	create_sub(f, [vert_open()], ['v','o'])
	create_sub(f, [vert_close()], ['v','c'])
	for t in ['base','mark']:
		if True:
			create_sub(f, [hrec_ty(0,t)], ['a','a'])
			create_sub(f, [hrec_ty(200,t)], ['a','b'])
			create_sub(f, [hrec_ty(400,t)], ['a','c'])
			create_sub(f, [hrec_ty(600,t)], ['a','d'])
			create_sub(f, [hrec_ty(800,t)], ['a','e'])
			create_sub(f, [hrec_ty(1000,t)], ['a','f'])
			create_sub(f, [hrec_ty('nil',t)], ['a','x'])
		if False:
			create_sub(f, [hrec_h(0,t)], ['a','a'])
			create_sub(f, [hrec_h(333,t)], ['a','b'])
			create_sub(f, [hrec_h(2*333,t)], ['a','c'])
			create_sub(f, [hrec_h(3*333,t)], ['a','d'])
			create_sub(f, [hrec_h(4*333,t)], ['a','e'])
			create_sub(f, [hrec_h(5*333,t)], ['a','f'])
			create_sub(f, [hrec_h(6*333,t)], ['a','g'])
			create_sub(f, [hrec_h('nil',t)], ['a','x'])
		if False:
			create_sub(f, [grec_th(0,t)], ['a','a'])
			create_sub(f, [grec_th(200,t)], ['a','b'])
			create_sub(f, [grec_th(2*200,t)], ['a','c'])
			create_sub(f, [grec_th(3*200,t)], ['a','d'])
			create_sub(f, [grec_th(4*200,t)], ['a','e'])
			create_sub(f, [grec_th(5*200,t)], ['a','f'])
			create_sub(f, [grec_th(6*200,t)], ['a','g'])
			create_sub(f, [grec_th('nil',t)], ['a','x'])
		if False:
			create_sub(f, [grec_sh('nil',t)], ['a','x'])
			create_sub(f, [grec_sh(500,t)], ['a','a'])
			create_sub(f, [grec_sh(1000,t)], ['a','b'])
	end_lookup(f)
	return

	start_lookup(f)
	# create_sub(f, [shrec_w('nil','mark')], ['x'])
	# for sym in grec_s_any('base'):
		# create_sub(f, [sym], ['g','b','s'])
	# for sym in grec_w_any('base'):
		# create_sub(f, [sym], ['g','b','w'])
	# for sym in grec_h_any('base'):
		# create_sub(f, [sym], ['g','b','h'])
	# for sym in grec_sw_any('base'):
		# create_sub(f, [sym], ['g','b','s','w'])
	# for sym in grec_sh_any('base'):
		# create_sub(f, [sym], ['g','b','s','h'])
	# for sym in hrec_any('base'):
		# create_sub(f, [sym], ['h','b'])
	# for sym in shrec_any('base'):
		# create_sub(f, [sym], ['s','h','b'])
	# for sym in vrec_any('base'):
		# create_sub(f, [sym], ['v','b'])
	# for sym in svrec_any('base'):
		# create_sub(f, [sym], ['s','v','b'])
	for sym in record_symbols('base'):
		create_sub(f, [sym], ['b'])
	for sym in record_symbols('mark'):
		create_sub(f, [sym], ['m'])
	for sym in grec_aux_all():
		create_sub(f, [sym], ['g'])
	for sym in aux_all():
		create_sub(f, [sym], ['h'])
	end_lookup(f)

def test_features(f):
	return
	start_named_lookup(f, "testing")
	create_pos(f, [], [grec_tw('nil')], [], 500, 500, 0, 0)
	# f.write('position A <anchor 300 300>;')
	# f.write('pos base e <anchor 300 300>;')
	# f.write('pos e\' <0 0 0 0> f;')
	#f.write(create_sub(f, ['x\'', 'y'], ['y']))
	end_named_lookup(f, "testing")
	return

def write_features(f):
	make_mark_class(f)
	start_feat(f)
	initialize(f)
	add_brackets(f)
	remove_brackets(f)
	add_records(f)
	sum_widths(f)
	max_heights(f)
	max_widths(f)
	sum_heights(f)
	left_bottom_insert(f)
	target_x(f)
	target_y(f)
	target_width(f)
	target_height(f)
	prop_vert_x(f)
	prop_vert_width(f)
	prop_vert_y_height(f)
	prop_hor_x_width(f)
	prop_hor_y(f)
	prop_hor_height(f)
	if True:
		increment_group(f)
		make_glyph_scalings(f)
		place_glyphs1(f)
		scale_glyphs(f)
		place_glyphs2(f)
	# test_convert(f)
	end_feat(f)
	anchor_glyphs(f)

##################################################

font = fontforge.open(font_sfd)
add_aux_symbols_to(font)
make_glyphs(font)

for lookup in font.gsub_lookups:
	font.removeLookup(lookup)

f = open(feature_file_name, 'w')
write_features(f)
f.close()

font.mergeFeature(feature_file_name)

font.generate(font_otf)
