import math

#################################
# Constants.

# Maximum number of glyphs in horizontal group.
max_hor_group_len = 4
# Maximum number of subgroups of vertical group.
max_vert_group_len = 3

# Sizes expressed in 1000.
unit_glyph_size = 1000
# Minimum size of glyph.
min_glyph_size = 333
# Maximum size of glyph.
max_glyph_size = 999
# Granularity of sizes.
step_glyph_size = 333

# Coordinates expressed in 1000.
unit_coord = 1000
# Granularity of coordinates.
step_coord = 200

# Scaling expressed in 1000.
unit_scale = 1000
# Smallest scaling factor, out of 1000.
min_scale = 500
# Granularity of scaling (factor).
step_scale = 2
# Maximum number of steps in scaling.
max_steps_scale = 2
# Greatest scaling factor.
max_scale = min_scale * (step_scale ** max_steps_scale)

# Glyphs, with width and height.
glyph_dimensions = [\
(0, 999, 666),
(1, 666, 666),
(2, 999, 333),
(3, 666, 333),
(4, 666, 999),
(5, 666, 666),
(6, 999, 999),
(7, 666, 999),
(8, 999, 333)]
n_glyphs = len(glyph_dimensions)

# Areas in font.
# As in input text.
base_code_area = 65
# From source font.
source_unscaled_code_area = 256
source_scaled_code_area = 256+60
# As marks.
mark_unscaled_code_area = 65+60
mark_scaled_code_area = 65+60+60
# Auxiliary symbols.
aux_code_area = 500

#################################
# Derived lists.

# Minimum and maximum size of group of length.
def min_group_size_of_len(l):
	return min_glyph_size * l
def max_group_size_of_len(l):
	return max_glyph_size * l

# Sizes of groups of length.
def group_sizes_len(l):
	return range(min_group_size_of_len(l), max_group_size_of_len(l)+step_glyph_size, step_glyph_size)
# Sizes of possibly empty groups of up to length.
def group_sizes_len_zero_to(l):
	return range(min_group_size_of_len(0), max_group_size_of_len(l)+step_glyph_size, step_glyph_size)
# Sizes of non-empty groups of up to length.
def group_sizes_len_one_to(l):
	return range(min_group_size_of_len(1), max_group_size_of_len(l)+step_glyph_size, step_glyph_size)
# (0,1]
all_glyph_sizes = group_sizes_len(1)
# [0,1]
all_glyph_sizes_and_zero = group_sizes_len_zero_to(1)
# (0,N_h]
all_group_widths = group_sizes_len_one_to(max_hor_group_len)
# (0,N_v]
all_group_heights = group_sizes_len_one_to(max_vert_group_len)
# (0,max(N_h,N_v)]
all_group_sizes = group_sizes_len_one_to(max(max_hor_group_len,max_vert_group_len))
# [0,N_h-1]
all_suffix_group_widths = group_sizes_len_zero_to(max_hor_group_len-1)
# [0,N_v-1]
all_suffix_group_heights = group_sizes_len_zero_to(max_vert_group_len-1)

# Coordinates. 
# [0,1]
all_coords = range(0, unit_coord+step_coord, step_coord)

# All group scaling factors.
# [S_{min},S_{max}]
all_group_scalings = [min_scale * (step_scale ** e) for e in range(0,max_steps_scale+1)]
# All scaling factors for glyphs.
# [S_{min},1]
all_glyph_scalings = [s for s in all_group_scalings if s <= unit_scale]

#################################
# Operations.

# Convert multiple of unit_glyph_size to multiple of unit_coord.
def safe_size_to_coord(v):
	vf = v * 1.0 / unit_glyph_size
	step_f = step_coord * 1.0 / unit_coord
	cf =  int(math.ceil(vf / step_f)) * step_coord
	return min(max(cf,step_coord),unit_coord)

# Safe addition of sizes in coordinate system.
def safe_coord_plus(v1, v2):
	return min(v1+v2, unit_coord)

# Safe subtraction of sizes in coordinate system.
def safe_coord_minus(v1, v2):
	return max(v1-v2, 0)

# Division of value in coordinate system by glyph size.
# Outcome is scaling factor.
def safe_coord_size_div(v1, v2):
	if v1 == 0:
		return min_scale
	else:
		f1 = v1 * 1.0 / unit_coord
		f2 = v2 * 1.0 / unit_glyph_size
		s = min_scale * 1.0 / unit_scale
		q = (f1 / f2) / s
		l = int(round(math.log(q,step_scale)))
		l = min(max(l,0),max_steps_scale)
		return min_scale * (step_scale ** l)

# Safe multiplication of scaling factor and glyph size.
# The outcome is value in coordinate system.
def safe_size_mult_to_coord(s, v):
	sf = s * 1.0 / unit_scale
	vf = v * 1.0 / unit_glyph_size
	stepf = step_coord * 1.0 / unit_coord
	w = int(round(sf*vf / stepf)) * step_coord
	return min(max(w,0),unit_coord)
