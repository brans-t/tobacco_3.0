import re
import numpy as np
import os

PT = ['H' , 'He', 'Li', 'Be', 'B' , 'C' , 'N' , 'O' , 'F' , 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P' , 'S' , 'Cl', 'Ar',
	  'K' , 'Ca', 'Sc', 'Ti', 'V' , 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
	  'Rb', 'Sr', 'Y' , 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I' , 'Xe',
	  'Cs', 'Ba', 'Hf', 'Ta', 'W' , 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 
	  'Ra', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Ac', 'Th', 
	  'Pa', 'U' , 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'FG', 'X' ]


def _load_cif_content(cifname, direc):
	"""
	Helper function to load CIF content from JSON database or file.
	
	Args:
		cifname: CIF filename
		direc: Directory type ('nodes', 'edges', or 'templates') or full path
	
	Returns:
		str: CIF file content
	"""
	from src.utils.paths import get_node_path, get_edge_path, get_template_path, NODES_DIR, EDGES_DIR, TEMPLATES_DIR
	from src.utils.input_loader import load_building_blocks
	
	# Normalize direc parameter - convert path to type
	direc_str = str(direc)
	if 'nodes' in direc_str.lower():
		direc_type = 'nodes'
	elif 'edges' in direc_str.lower():
		direc_type = 'edges'
	elif 'templates' in direc_str.lower():
		direc_type = 'templates'
	else:
		direc_type = direc
	
	# Try to load from JSON database first
	cif_content = None
	try:
		if direc_type == 'nodes':
			blocks = load_building_blocks(cifname, 'node', source='auto')
		elif direc_type == 'edges':
			blocks = load_building_blocks(cifname, 'edge', source='auto')
		elif direc_type == 'templates':
			blocks = load_building_blocks(cifname, 'template', source='auto')
		else:
			# For custom paths, skip JSON loading
			blocks = None
		
		if blocks:
			# Normalize filename
			if not cifname.endswith('.cif'):
				cifname_with_ext = f"{cifname}.cif"
			else:
				cifname_with_ext = cifname
			cif_content = blocks.get(cifname_with_ext)
	except Exception:
		pass
	
	# Fallback to direct file reading if JSON loading failed
	if cif_content is None:
		if direc_type == 'nodes':
			path = get_node_path(cifname)
		elif direc_type == 'edges':
			path = get_edge_path(cifname)
		elif direc_type == 'templates':
			path = get_template_path(cifname)
		else:
			# Assume it's a full path or relative path
			path = os.path.join(direc, cifname)
		
		with open(path, 'r') as cif:
			cif_content = cif.read()
	
	return cif_content


def nn(string):
	return re.sub('[^a-zA-Z]','', string)

def nl(string):
	return re.sub('[^0-9]','', string)

def isfloat(value):
	"""
		determines if a value is a float
	"""
	try:
		float(value)
		return True
	except ValueError:
		return False

def iscoord(line):
	"""
		identifies coordinates in CIFs
	"""
	if nn(line[0]) in PT and line[1] in PT and False not in map(isfloat,line[2:5]):
		return True
	else:
		return False
	
def isbond(line):
	"""
		identifies bonding in cifs
	"""
	if nn(line[0]) in PT and nn(line[1]) in PT and isfloat(line[2]) and line[-1] in ('S', 'D', 'T', 'A'):
		return True
	else:
		return False

def PBC3DF(c1, c2):
    """
        c1 and c2 are coordinates, either numpy arrays or lists
    """
    diffa = c1[0] - c2[0]
    diffb = c1[1] - c2[1]
    diffc = c1[2] - c2[2]

    if diffa > 0.5:
        c2[0] = c2[0] + 1.0
    elif diffa < -0.5:
        c2[0] = c2[0] - 1.0
    
    if diffb > 0.5:
        c2[1] = c2[1] + 1.0
    elif diffb < -0.5:
        c2[1] = c2[1] - 1.0
 
    if diffc > 0.5:
        c2[2] = c2[2] + 1.0
    elif diffc < -0.5:
        c2[2] = c2[2] - 1.0
    
    return c2

def bbelems(cifname, direc):
	"""
	Get elements from building block CIF file or JSON database.
	
	Args:
		cifname: CIF filename
		direc: Directory type ('nodes', 'edges', or 'templates') or full path
	
	Returns:
		list: List of element symbols
	"""
	# Load CIF content from JSON database or file
	cif_content = _load_cif_content(cifname, direc)
	cif = filter(None, cif_content.split('\n'))

	elems = []
	elems_append = elems.append
	for line in cif:
		s = line.split()
		if '_cell_length_a' in line:
			a = s[1]
		if '_cell_length_b' in line:
			b = s[1]
		if '_cell_length_c' in line:
			c = s[1]
		if '_cell_angle_alpha' in line:
			alpha = s[1]
		if '_cell_angle_beta' in line:
			beta = s[1]
		if '_cell_angle_gamma' in line:
			gamma = s[1]
		if iscoord(s):
			elems_append(s[1])

	return elems

def bb2array(cifname, direc):
	"""
	Convert building block CIF to array format.
	
	Args:
		cifname: CIF filename
		direc: Directory type ('nodes', 'edges', or 'templates') or full path
	
	Returns:
		tuple: (fcoords, unit_cell) where fcoords is list of [atom_name, fractional_coords]
	"""
	# Load CIF content from JSON database or file
	cif_content = _load_cif_content(cifname, direc)
	cif = filter(None, cif_content.split('\n'))

	fcoords = []
	fcoords_append = fcoords.append
	for line in cif:
		s = line.split()
		if '_cell_length_a' in line:
			a = s[1]
		if '_cell_length_b' in line:
			b = s[1]
		if '_cell_length_c' in line:
			c = s[1]
		if '_cell_angle_alpha' in line:
			alpha = s[1]
		if '_cell_angle_beta' in line:
			beta = s[1]
		if '_cell_angle_gamma' in line:
			gamma = s[1]
		if iscoord(s):
			fvec = np.array([float(q) for q	 in s[2:5]])
			fcoords_append([s[0],fvec])

	pi = np.pi
	a,b,c,alpha,beta,gamma = list(map(float, (a,b,c,alpha,beta,gamma)))
	ax = a
	ay = 0.0
	az = 0.0
	bx = b * np.cos(gamma * pi / 180.0)
	by = b * np.sin(gamma * pi / 180.0)
	bz = 0.0
	cx = c * np.cos(beta * pi / 180.0)
	cy = (c * b * np.cos(alpha * pi /180.0) - bx * cx) / by
	cz = (c ** 2.0 - cx ** 2.0 - cy ** 2.0) ** 0.5
	unit_cell = np.asarray([[ax,ay,az],[bx,by,bz],[cx,cy,cz]]).T
	
	norm_vec = fcoords[0][1]
	ccoords = [[n[0],np.dot(unit_cell, PBC3DF(norm_vec, n[1]))] for n in fcoords]
	#ccoords = [[n[0],np.dot(unit_cell, n[1])] for n in fcoords]
	com = np.average(np.array([n[1] for n in ccoords if re.sub('[0-9]','',n[0]) == 'X']), axis = 0)
	sccoords = [[n[0], n[1] - com] for n in ccoords]

	return sccoords

def bbbonds(cifname, direc):
	"""
	Get bonds from building block CIF file.
	
	Args:
		cifname: CIF filename
		direc: Directory type ('nodes', 'edges', or 'templates') or full path
	
	Returns:
		list: List of bond information
	"""
def bbbonds(cifname, direc):
	"""
	Get bonds from building block CIF file or JSON database.
	
	Args:
		cifname: CIF filename
		direc: Directory type ('nodes', 'edges', or 'templates') or full path
	
	Returns:
		list: List of bond information
	"""
	# Load CIF content from JSON database or file
	cif_content = _load_cif_content(cifname, direc)
	cif = filter(None, cif_content.split('\n'))

	bonds = []
	bonds_append = bonds.append
	for line in cif:
		s = line.split()
		if isbond(s):
			bonds_append(s)
			
	return bonds

def X_vecs(cifname, direc, label):
	"""
	Get X vectors from building block CIF file or JSON database.
	
	Args:
		cifname: CIF filename
		direc: Directory type ('nodes', 'edges', or 'templates') or full path
		label: Whether to include labels
	
	Returns:
		list: List of shifted coordinate vectors
	"""
	# Load CIF content from JSON database or file
	cif_content = _load_cif_content(cifname, direc)
	cif = filter(None, cif_content.split('\n'))

	fcoords = []
	fcoords_append = fcoords.append

	for line in cif:
		s = line.split()
		if '_cell_length_a' in line:
			a = s[1]
		if '_cell_length_b' in line:
			b = s[1]
		if '_cell_length_c' in line:
			c = s[1]
		if '_cell_angle_alpha' in line:
			alpha = s[1]
		if '_cell_angle_beta' in line:
			beta = s[1]
		if '_cell_angle_gamma' in line:
			gamma = s[1]
		if iscoord(s) and 'X' in s[0]:
			fvec = np.array([float(q) for q in s[2:5]])
			fcoords_append([s[0],fvec])

	pi = np.pi
	a,b,c,alpha,beta,gamma = list(map(float, (a,b,c,alpha,beta,gamma)))
	ax = a
	ay = 0.0
	az = 0.0
	bx = b * np.cos(gamma * pi / 180.0)
	by = b * np.sin(gamma * pi / 180.0)
	bz = 0.0
	cx = c * np.cos(beta * pi / 180.0)
	cy = (c * b * np.cos(alpha * pi /180.0) - bx * cx) / by
	cz = (c ** 2.0 - cx ** 2.0 - cy ** 2.0) ** 0.5
	unit_cell = np.asarray([[ax,ay,az],[bx,by,bz],[cx,cy,cz]]).T

	mic_fcoords = [[vec[0],PBC3DF(fcoords[0][1],vec[1])] for vec in fcoords]

	if label:
		ccoords = [[vec[0],np.dot(unit_cell,vec[1])] for vec in mic_fcoords]
		com = np.average(np.asarray([vec[1] for vec in ccoords]), axis=0)
		shifted_ccoords = [[vec[0],vec[1] - com] for vec in ccoords]
	else:
		ccoords = [np.dot(unit_cell,vec[1]) for vec in mic_fcoords]
		com = np.average(ccoords, axis=0)
		shifted_ccoords = [vec - com for vec in ccoords]

	return shifted_ccoords

def bbcharges(cifname, direc):
	"""
	Get charges from building block CIF file.
	
	Args:
		cifname: CIF filename
		direc: Directory type ('nodes', 'edges', or 'templates') or full path
	
	Returns:
		tuple: (charges, elements) lists
	"""
	# Load CIF content from JSON database or file
	cif_content = _load_cif_content(cifname, direc)
	cif = filter(None, cif_content.split('\n'))

	charges = []
	charges_append = charges.append
	elements = []
	elements_append = elements.append
	for line in cif:
		s = line.split()
		if iscoord(s):
			charges_append(s[-1])
			elements_append(s[1])
				
	return charges, elements

def calc_edge_len(cifname, direc):
	"""
	Calculate edge length from CIF file or JSON database.
	
	Args:
		cifname: CIF filename
		direc: Directory type ('nodes', 'edges', or 'templates') or full path
	
	Returns:
		float: Edge length
	"""
	# Load CIF content from JSON database or file
	cif_content = _load_cif_content(cifname, direc)
	cif = filter(None, cif_content.split('\n'))

	fcoords = []
	fcoords_append = fcoords.append
	for line in cif:
		s = line.split()
		if '_cell_length_a' in line:
			a = s[1]
		if '_cell_length_b' in line:
			b = s[1]
		if '_cell_length_c' in line:
			c = s[1]
		if '_cell_angle_alpha' in line:
			alpha = s[1]
		if '_cell_angle_beta' in line:
			beta = s[1]
		if '_cell_angle_gamma' in line:
			gamma = s[1]
		if iscoord(s) and 'X' in s[0]:
			fvec = np.array([float(q) for q in s[2:5]])
			fcoords_append([s[0],fvec])

	pi = np.pi
	a,b,c,alpha,beta,gamma = list(map(float, (a,b,c,alpha,beta,gamma)))
	ax = a
	ay = 0.0
	az = 0.0
	bx = b * np.cos(gamma * pi / 180.0)
	by = b * np.sin(gamma * pi / 180.0)
	bz = 0.0
	cx = c * np.cos(beta * pi / 180.0)
	cy = (c * b * np.cos(alpha * pi /180.0) - bx * cx) / by
	cz = (c ** 2.0 - cx ** 2.0 - cy ** 2.0) ** 0.5
	unit_cell = np.asarray([[ax,ay,az],[bx,by,bz],[cx,cy,cz]]).T

	mic_fcoords = [PBC3DF(fcoords[0][1],vec[1]) for vec in fcoords]
	ccoords = [np.dot(unit_cell,vec) for vec in mic_fcoords]

	return np.linalg.norm(ccoords[0] - ccoords[1])

def cncalc(cifname, direc):
	"""
	Calculate coordination number from CIF file or JSON database.
	
	Args:
		cifname: CIF filename
		direc: Directory type ('nodes', 'edges', or 'templates') or full path
	
	Returns:
		int: Coordination number (count of 'X' atoms)
	"""
	# Import path resolution functions and loader
	from src.utils.paths import get_node_path, get_edge_path, get_template_path
	from src.utils.input_loader import load_building_blocks
	
	# Try to load from JSON database first
	cif_content = None
	try:
		if direc == 'nodes':
			blocks = load_building_blocks(cifname, 'node', source='auto')
		elif direc == 'edges':
			blocks = load_building_blocks(cifname, 'edge', source='auto')
		elif direc == 'templates':
			blocks = load_building_blocks(cifname, 'template', source='auto')
		else:
			# For custom paths, try direct file reading
			blocks = None
		
		if blocks:
			# Normalize filename
			if not cifname.endswith('.cif'):
				cifname_with_ext = f"{cifname}.cif"
			else:
				cifname_with_ext = cifname
			cif_content = blocks.get(cifname_with_ext)
	except Exception:
		pass
	
	# Fallback to direct file reading if JSON loading failed
	if cif_content is None:
		if direc == 'nodes':
			path = get_node_path(cifname)
		elif direc == 'edges':
			path = get_edge_path(cifname)
		elif direc == 'templates':
			path = get_template_path(cifname)
		else:
			# Assume it's a full path or relative path
			path = os.path.join(direc, cifname)
		
		with open(path, 'r') as cif:
			cif_content = cif.read()
	
	# Parse CIF content
	cif = filter(None, cif_content.split('\n'))
	
	cn = 0
	nc = 0
	for line in cif:
		s = line.split()
		if iscoord(s):
			nc += 1
			if re.sub('[^a-zA-Z]','',s[0]) == 'X':
				cn += 1
	return cn

	