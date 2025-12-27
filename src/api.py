"""
API module for ToBaCCo.

This module provides a unified API interface for generating CIF files programmatically.
"""

from __future__ import print_function
import os
import re
import numpy as np
import itertools
import time
from random import choice

# Import configuration
import configuration

# Import core modules
from src.core.ciftemplate2graph import ct2g
from src.core.vertex_edge_assign import vertex_assign, assign_node_vecs2edges
from src.core.cycle_cocyle import cycle_cocyle, Bstar_alpha
from src.core.SBU_geometry import SBU_coords
from src.core.scale import scale
from src.core.scaled_embedding2coords import omega2coords

# Import utility modules
from src.utils.bbcif_properties import cncalc, bbelems
from src.utils.place_bbs import scaled_node_and_edge_vectors, place_nodes, place_edges
from src.utils.remove_net_charge import fix_charges
from src.utils.remove_dummy_atoms import remove_Fr
from src.utils.adjust_edges import adjust_edges
from src.utils.charge_generator import initialize_charge_generator, generate_charge_adjustment, get_seed_from_config
from src.utils.write_cifs import (
    write_check_cif, write_cif, bond_connected_components,
    distance_search_bond, fix_bond_sym
)
from src.utils.paths import (
    get_template_path, get_node_path, get_edge_path,
    NODES_DIR, EDGES_DIR, TEMPLATES_DIR, ensure_directories
)


# Constants
pi = np.pi

# Vertex name mapping dictionary (for consistent naming with tobacco.py)
vname_dict = {'V':1,'Er':2,'Ti':3,'Ce':4,'S':5,
              'H':6,'He':7,'Li':8,'Be':9,'B':10,
              'C':11,'N':12,'O':13,'F':14,'Ne':15,
              'Na':16,'Mg':17,'Al':18,'Si':19,'P':20,
              'Cl':21,'Ar':22,'K':23,'Ca':24,'Sc':25,
              'Cr':26,'Mn':27,'Fe':28,'Co':29,'Ni':30}

metal_elements = ['Ac','Ag','Al','Am','Au','Ba','Be','Bi',
                  'Bk','Ca','Cd','Ce','Cf','Cm','Co','Cr',
                  'Cs','Cu','Dy','Er','Es','Eu','Fe','Fm',
                  'Ga','Gd','Hf','Hg','Ho','In','Ir',
                  'K','La','Li','Lr','Lu','Md','Mg','Mn',
                  'Mo','Na','Nb','Nd','Ni','No','Np','Os',
                  'Pa','Pb','Pd','Pm','Pr','Pt','Pu','Ra',
                  'Rb','Re','Rh','Ru','Sc','Sm','Sn','Sr',
                  'Ta','Tb','Tc','Th','Ti','Tl','Tm','U',
                  'V','W','Y','Yb','Zn','Zr']

vname_dict = {'V':1,'Er':2,'Ti':3,'Ce':4,'S':5,
              'H':6,'He':7,'Li':8,'Be':9,'B':10,
              'C':11,'N':12,'O':13,'F':14,'Ne':15,
              'Na':16,'Mg':17,'Al':18,'Si':19,'P':20,
              'Cl':21,'Ar':22,'K':23,'Ca':24,'Sc':24,
              'Cr':26,'Mn':27,'Fe':28,'Co':29,'Ni':30}


def _normalize_filename(filename):
    """
    Add .cif extension to filename if not present.
    
    Args:
        filename (str): Filename with or without .cif extension
        
    Returns:
        str: Filename with .cif extension
    """
    if not filename.endswith('.cif'):
        return f"{filename}.cif"
    return filename


def _validate_inputs(template_name, node_names, edge_names):
    """
    Validate input parameters using input_loader module.
    
    This function validates inputs by attempting to load them from JSON databases
    or CIF files using the input_loader module, which provides automatic fallback.
    
    Args:
        template_name (str): Template filename
        node_names (str, list, or dict): Node filename(s)
        edge_names (str or list): Edge filename(s)
        
    Raises:
        ValueError: If inputs are invalid
        FileNotFoundError: If required files don't exist in JSON database or CIF files
    """
    from src.utils.input_loader import load_building_blocks, InputValidationError
    
    # Validate template_name
    if not template_name or not isinstance(template_name, str):
        raise ValueError("template_name must be a non-empty string")
    
    # Validate node_names (can be str, list, or dict)
    if not isinstance(node_names, (str, list, dict)):
        raise ValueError(f"node_names must be str, list, or dict, got {type(node_names)}")
    
    if isinstance(node_names, str) and not node_names:
        raise ValueError("node_names string cannot be empty")
    
    if isinstance(node_names, list) and len(node_names) == 0:
        raise ValueError("node_names list cannot be empty")
    
    if isinstance(node_names, dict) and len(node_names) == 0:
        raise ValueError("node_names dict cannot be empty")
    
    # Validate edge_names (can be str or list)
    if not isinstance(edge_names, (str, list)):
        raise ValueError(f"edge_names must be str or list, got {type(edge_names)}")
    
    if isinstance(edge_names, str) and not edge_names:
        raise ValueError("edge_names string cannot be empty")
    
    if isinstance(edge_names, list) and len(edge_names) == 0:
        raise ValueError("edge_names list cannot be empty")
    
    # Validate template exists (try loading from JSON database or CIF file)
    try:
        load_building_blocks(template_name, 'template', source='auto')
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"Template '{template_name}' not found in JSON database or inputs/templates/ directory. "
            f"Details: {e}"
        )
    except InputValidationError as e:
        raise ValueError(f"Template validation error: {e}")
    
    # Validate nodes exist (try loading from JSON database or CIF file)
    try:
        load_building_blocks(node_names, 'node', source='auto')
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"One or more nodes not found in JSON database or inputs/nodes/ directory. "
            f"Details: {e}"
        )
    except InputValidationError as e:
        raise ValueError(f"Node validation error: {e}")
    
    # Validate edges exist (try loading from JSON database or CIF file)
    try:
        load_building_blocks(edge_names, 'edge', source='auto')
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"One or more edges not found in JSON database or inputs/edges/ directory. "
            f"Details: {e}"
        )
    except InputValidationError as e:
        raise ValueError(f"Edge validation error: {e}")



def _merge_config(user_config, default_config):
    """
    Merge user configuration with default configuration.
    
    Args:
        user_config (dict): User-provided configuration overrides
        default_config (dict): Default configuration
        
    Returns:
        dict: Merged configuration (user values take precedence)
    """
    if user_config is None:
        return default_config.copy()
    
    merged = default_config.copy()
    merged.update(user_config)
    return merged


def _get_default_config():
    """
    Get default configuration from configuration module.
    
    Returns:
        dict: Default configuration dictionary
    """
    return {
        'IGNORE_ALL_ERRORS': configuration.IGNORE_ALL_ERRORS,
        'PRINT': configuration.PRINT,
        'CONNECTION_SITE_BOND_LENGTH': configuration.CONNECTION_SITE_BOND_LENGTH,
        'WRITE_CHECK_FILES': configuration.WRITE_CHECK_FILES,
        'WRITE_CIF': configuration.WRITE_CIF,
        'ALL_NODE_COMBINATIONS': configuration.ALL_NODE_COMBINATIONS,
        'USER_SPECIFIED_NODE_ASSIGNMENT': configuration.USER_SPECIFIED_NODE_ASSIGNMENT,
        'COMBINATORIAL_EDGE_ASSIGNMENT': configuration.COMBINATORIAL_EDGE_ASSIGNMENT,
        'CHARGES': configuration.CHARGES,
        'SYMMETRY_TOL': configuration.SYMMETRY_TOL,
        'BOND_TOL': configuration.BOND_TOL,
        'ORIENTATION_DEPENDENT_NODES': configuration.ORIENTATION_DEPENDENT_NODES,
        'PLACE_EDGES_BETWEEN_CONNECTION_POINTS': configuration.PLACE_EDGES_BETWEEN_CONNECTION_POINTS,
        'RECORD_CALLBACK': configuration.RECORD_CALLBACK,
        'OUTPUT_SCALING_DATA': configuration.OUTPUT_SCALING_DATA,
        'FIX_UC': configuration.FIX_UC,
        'MIN_CELL_LENGTH': configuration.MIN_CELL_LENGTH,
        'OPT_METHOD': configuration.OPT_METHOD,
        'PRE_SCALE': configuration.PRE_SCALE,
        'SCALING_ITERATIONS': configuration.SCALING_ITERATIONS,
        'SINGLE_METAL_MOFS_ONLY': configuration.SINGLE_METAL_MOFS_ONLY,
        'MOFS_ONLY': configuration.MOFS_ONLY,
        'MERGE_CATENATED_NETS': configuration.MERGE_CATENATED_NETS,
        'RUN_PARALLEL': configuration.RUN_PARALLEL,
        'REMOVE_DUMMY_ATOMS': configuration.REMOVE_DUMMY_ATOMS,
        'RANDOM_SEED': configuration.RANDOM_SEED
    }


def _prepare_node_files(node_names):
    """
    Prepare node files list from input.
    
    Args:
        node_names (str, list, or dict): Node filename(s) or vertex type mapping
        
    Returns:
        list: List of node filenames with .cif extension
    """
    if isinstance(node_names, str):
        # Single string
        return [_normalize_filename(node_names)]
    elif isinstance(node_names, dict):
        # Dictionary mapping vertex types to node filenames
        return [_normalize_filename(name) for name in node_names.values()]
    else:
        # List of node filenames
        return [_normalize_filename(name) for name in node_names]


def _prepare_edge_files(edge_names):
    """
    Prepare edge files list from input.
    
    Args:
        edge_names (str or list): Edge filename(s)
        
    Returns:
        list: List of edge filenames with .cif extension
    """
    if isinstance(edge_names, str):
        # Single string
        return [_normalize_filename(edge_names)]
    else:
        # List of edge filenames
        return [_normalize_filename(name) for name in edge_names]


def generate_cif(template_name, node_names, edge_names, config=None, return_format='file', random_seed=None):
    """
    Generate CIF file content from template, nodes, and edges.
    
    This is the main API function for programmatic CIF generation.
    
    Args:
        template_name (str or list): Template filename(s) without .cif extension (e.g., "pcu")
                                     or with .cif extension (e.g., "pcu.cif")
                                     Can be single string or list of strings
        node_names (str, list, or dict): Node filename(s) or dict mapping vertex types to filenames
                                        Examples: "6c_Cu_1_Ch", ["6c_Cu_1_Ch"], or {"V": "6c_Cu_1_Ch"}
                                        Extensions (.cif) are optional
        edge_names (str or list): Edge filename(s) without .cif extension (e.g., "btc_edge" or ["btc_edge"])
                                 Extensions (.cif) are optional
                                 Can be single string or list of strings
        config (dict, optional): Configuration overrides. Any key from configuration.py
                                can be overridden here.
        return_format (str or list, optional): Output format specification. Options:
                                              - 'file': Save to file and return path (default)
                                              - 'string': Return CIF content as string
                                              - 'json': Return as JSON object
                                              - List of formats: Return dict with results for each format
        random_seed (int, optional): Seed for deterministic charge generation.
                                    If None, uses default seed from configuration.
                                    Same seed produces identical charges.
        
    Returns:
        Depends on return_format:
        - 'file': Path object or list of Path objects
        - 'string': String or list of strings (or tuples with metadata)
        - 'json': Dict with MOF names as keys
        - List of formats: Dict mapping format names to their respective outputs
        
        For backward compatibility, when return_format='file' and single result,
        returns a dict with 'file_path', 'cifname', and 'metadata' keys.
    
    Raises:
        FileNotFoundError: If template, node, or edge file not found
        ValueError: If assignments are incompatible or inputs are invalid
        
    Examples:
        >>> # Single string inputs
        >>> result = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge")
        >>> print(result["cifname"])
        pcu_v1-6c_Cu_1_Ch_1-btc_edge.cif
        
        >>> # List inputs
        >>> result = generate_cif("pcu", ["6c_Cu_1_Ch"], ["btc_edge"])
        
        >>> # With configuration override
        >>> result = generate_cif("pcu", ["6c_Cu_1_Ch"], ["btc_edge"], 
        ...                       config={"CHARGES": False})
        
        >>> # With vertex type mapping
        >>> result = generate_cif("pcu", {"V": "6c_Cu_1_Ch"}, ["btc_edge"])
        
        >>> # With deterministic charge generation
        >>> result = generate_cif("pcu", ["6c_Cu_1_Ch"], ["btc_edge"], random_seed=123)
        
        >>> # Return as string instead of file
        >>> result = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", return_format='string')
        >>> print(type(result))
        <class 'str'>
        
        >>> # Return as JSON
        >>> result = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", return_format='json')
        >>> print(result.keys())
        dict_keys(['pcu_v1-6c_Cu_1_Ch_1-btc_edge'])
    """
    start_time = time.time()
    
    # Ensure output directories exist
    ensure_directories()
    
    # Normalize inputs to lists (support single string inputs)
    from src.utils.input_loader import normalize_input_format, validate_inputs
    
    # Normalize template_name to list
    if isinstance(template_name, str):
        template_list = [template_name]
    elif isinstance(template_name, list):
        template_list = template_name
    else:
        raise ValueError(f"template_name must be str or list, got {type(template_name)}")
    
    # Normalize node_names (can be str, list, or dict)
    # Keep original format for validation
    original_node_names = node_names
    if isinstance(node_names, str):
        node_names = [node_names]
    
    # Normalize edge_names to list
    if isinstance(edge_names, str):
        edge_list = [edge_names]
    elif isinstance(edge_names, list):
        edge_list = edge_names
    else:
        raise ValueError(f"edge_names must be str or list, got {type(edge_names)}")
    
    # Validate all inputs before generation
    for template in template_list:
        valid, error_msg = validate_inputs(template, node_names, edge_list)
        if not valid:
            raise ValueError(f"Input validation failed for template '{template}': {error_msg}")
    
    # Initialize charge generator with seed
    # Get seed from config if not explicitly provided
    if random_seed is None and config is not None:
        random_seed = get_seed_from_config(config)
    elif random_seed is None:
        random_seed = get_seed_from_config(None)
    
    rng = initialize_charge_generator(random_seed)
    
    # Validate return_format
    valid_formats = {'file', 'string', 'json'}
    if isinstance(return_format, str):
        if return_format not in valid_formats:
            raise ValueError(f"Invalid return_format: '{return_format}'. Must be one of {valid_formats}")
    elif isinstance(return_format, list):
        for fmt in return_format:
            if fmt not in valid_formats:
                raise ValueError(f"Invalid return_format: '{fmt}'. Must be one of {valid_formats}")
    else:
        raise ValueError(f"return_format must be str or list, got {type(return_format)}")
    
    # Store all results from all combinations
    all_results = []
    
    # Generate MOFs for all template combinations
    for template in template_list:
        # Validate inputs for this template
        _validate_inputs(template, original_node_names, edge_list)
        
        # Normalize filenames
        template_filename = _normalize_filename(template)
        node_files = _prepare_node_files(original_node_names)
        edge_files = _prepare_edge_files(edge_list)
    
    # Merge configuration
    default_config = _get_default_config()
    merged_config = _merge_config(config, default_config)
    
    # Extract configuration values
    CHARGES = merged_config['CHARGES']
    CONNECTION_SITE_BOND_LENGTH = merged_config['CONNECTION_SITE_BOND_LENGTH']
    SYMMETRY_TOL = merged_config['SYMMETRY_TOL']
    BOND_TOL = merged_config['BOND_TOL']
    ORIENTATION_DEPENDENT_NODES = merged_config['ORIENTATION_DEPENDENT_NODES']
    PLACE_EDGES_BETWEEN_CONNECTION_POINTS = merged_config['PLACE_EDGES_BETWEEN_CONNECTION_POINTS']
    FIX_UC = merged_config['FIX_UC']
    MIN_CELL_LENGTH = merged_config['MIN_CELL_LENGTH']
    OPT_METHOD = merged_config['OPT_METHOD']
    PRE_SCALE = merged_config['PRE_SCALE']
    SCALING_ITERATIONS = merged_config['SCALING_ITERATIONS']
    SINGLE_METAL_MOFS_ONLY = merged_config['SINGLE_METAL_MOFS_ONLY']
    MOFS_ONLY = merged_config['MOFS_ONLY']
    REMOVE_DUMMY_ATOMS = merged_config['REMOVE_DUMMY_ATOMS']
    USER_SPECIFIED_NODE_ASSIGNMENT = merged_config['USER_SPECIFIED_NODE_ASSIGNMENT']
    COMBINATORIAL_EDGE_ASSIGNMENT = merged_config['COMBINATORIAL_EDGE_ASSIGNMENT']
    
    # Store results for this template
    results = []
    
    # Process template
    for net in ct2g(template_filename):
        TG, start, unit_cell, TVT, TET, TNAME, a, b, c, ang_alpha, ang_beta, ang_gamma, max_le, catenation = net
        
        TVT = sorted(TVT, key=lambda x:x[0], reverse=True)
        TET = sorted(TET, reverse=True)
        
        # Get node coordination numbers
        # For API usage, we should only use user-specified nodes, not all available nodes
        from src.utils.input_loader import load_building_blocks
        import json
        
        # Determine which nodes to consider
        if USER_SPECIFIED_NODE_ASSIGNMENT or True:  # Always use user-specified nodes in API
            # Only use the nodes specified by the user
            user_nodes = []
            for node_name in node_names:
                if not node_name.endswith('.cif'):
                    user_nodes.append(f"{node_name}.cif")
                else:
                    user_nodes.append(node_name)
            node_cns = [(cncalc(node, 'nodes'), node) for node in user_nodes]
        else:
            # Get all available nodes (legacy behavior)
            # Get nodes from directory
            node_list_from_dir = []
            if NODES_DIR.exists():
                node_list_from_dir = [node for node in os.listdir(NODES_DIR) if node.endswith('.cif')]
            
            # Get nodes from JSON database
            node_list_from_json = []
            try:
                from src.utils.paths import NODES_JSON
                if NODES_JSON.exists():
                    with open(NODES_JSON, 'r') as f:
                        nodes_db = json.load(f)
                        node_list_from_json = list(nodes_db.keys())
            except Exception:
                pass
            
            # Combine both sources (remove duplicates)
            all_nodes = list(set(node_list_from_dir + node_list_from_json))
            node_cns = [(cncalc(node, 'nodes'), node) for node in all_nodes]
        
        # Count edges by type
        edge_counts = dict((data['type'],0) for e0,e1,data in TG.edges(data=True))
        for e0,e1,data in TG.edges(data=True):
            edge_counts[data['type']] += 1
        
        # Vertex assignment
        vas = vertex_assign(TG, TVT, node_cns, unit_cell, USER_SPECIFIED_NODE_ASSIGNMENT, 
                           SYMMETRY_TOL, False)  # ALL_NODE_COMBINATIONS=False for API
        
        if len(vas) == 0 or (len(vas) > 0 and len(vas[0]) == 0):
            raise ValueError(
                "No valid vertex assignment found. "
                "At least one vertex does not have a building block with the correct number of connection sites."
            )
        
        # Cycle and cocycle basis
        CB, CO = cycle_cocyle(TG)
        
        if len(CB) != (len(TG.edges()) - len(TG.nodes()) + 1):
            raise ValueError(
                "The cycle basis is incorrect. "
                "The number of cycles in the cycle basis does not equal the rank of the cycle space."
            )
        
        num_edges = len(TG.edges())
        Bstar, alpha = Bstar_alpha(CB, CO, TG, num_edges)
        num_vertices = len(TG.nodes())
        
        # Edge assignment
        if COMBINATORIAL_EDGE_ASSIGNMENT:
            eas = list(itertools.product(edge_files, repeat=len(TET)))
        else:
            eas = []
            i = 0
            while len(eas) < len(TET):
                eas.append(edge_files[i % len(edge_files)])
                i += 1
            eas = [eas]
        
        # Process each vertex assignment
        for va in vas:
            # Check metal content
            node_elems = [bbelems(i[1], 'nodes') for i in va]
            metals = [[i for i in j if i in metal_elements] for j in node_elems]
            metals = list(set([i for j in metals for i in j]))
            
            if SINGLE_METAL_MOFS_ONLY and len(metals) != 1:
                continue
            
            if MOFS_ONLY and len(metals) < 1:
                continue
            
            # Assign node CIF names to graph vertices
            for v in va:
                for n in TG.nodes(data=True):
                    if v[0] == n[0]:
                        n[1]['cifname'] = v[1]
            
            # Process each edge assignment
            for ea in eas:
                # Assign edge CIF names to graph edges
                type_assign = dict((k,[]) for k in sorted(TET, reverse=True))
                for k, m in zip(TET, ea):
                    type_assign[k] = m
                
                for e in TG.edges(data=True):
                    ty = e[2]['type']
                    for k in type_assign:
                        if ty == k or (ty[1], ty[0]) == k:
                            e[2]['cifname'] = type_assign[k]
                
                # Calculate number of possible X-X bonds
                num_possible_XX_bonds = 0
                for edge_type, cifname in zip(TET, ea):
                    if cifname == 'ntn_edge.cif':
                        factor = 1
                    else:
                        factor = 2
                    edge_type_count = edge_counts[edge_type]
                    num_possible_XX_bonds += factor * edge_type_count
                
                # Assign node vectors to edges
                ea_dict = assign_node_vecs2edges(TG, unit_cell, SYMMETRY_TOL, template_filename)
                
                # Calculate SBU coordinates
                all_SBU_coords = SBU_coords(TG, ea_dict, CONNECTION_SITE_BOND_LENGTH)
                
                # Scale unit cell
                sc_a, sc_b, sc_c, sc_alpha, sc_beta, sc_gamma, sc_covar, Bstar_inv, max_length, callbackresults, ncra, ncca, scaling_data = scale(
                    all_SBU_coords, a, b, c, ang_alpha, ang_beta, ang_gamma, max_le, num_vertices,
                    Bstar, alpha, num_edges, FIX_UC, SCALING_ITERATIONS, PRE_SCALE, MIN_CELL_LENGTH, OPT_METHOD
                )
                
                # Check for collapsed unit cell
                for sc, name in zip((sc_a, sc_b, sc_c), ('a', 'b', 'c')):
                    if sc == MIN_CELL_LENGTH:
                        raise ValueError(
                            f"Unit cell parameter {name} collapsed during scaling! "
                            f"Try re-running with {name} fixed or a larger MIN_CELL_LENGTH"
                        )
                
                scaled_params = [sc_a, sc_b, sc_c, sc_alpha, sc_beta, sc_gamma]
                
                # Calculate scaled coordinates
                sc_Alpha = np.r_[alpha[0:num_edges-num_vertices+1,:], sc_covar]
                sc_omega_plus = np.dot(Bstar_inv, sc_Alpha)
                
                ax = sc_a
                ay = 0.0
                az = 0.0
                bx = sc_b * np.cos(sc_gamma * pi/180.0)
                by = sc_b * np.sin(sc_gamma * pi/180.0)
                bz = 0.0
                cx = sc_c * np.cos(sc_beta * pi/180.0)
                cy = (sc_c * sc_b * np.cos(sc_alpha * pi/180.0) - bx * cx) / by
                cz = (sc_c ** 2.0 - cx ** 2.0 - cy ** 2.0) ** 0.5
                sc_unit_cell = np.asarray([[ax,ay,az],[bx,by,bz],[cx,cy,cz]]).T
                
                # Convert to coordinates
                scaled_coords = omega2coords(start, TG, sc_omega_plus, 
                                            (sc_a, sc_b, sc_c, sc_alpha, sc_beta, sc_gamma),
                                            num_vertices, template_filename, 1, False)
                
                # Place nodes and edges
                nvecs, evecs = scaled_node_and_edge_vectors(scaled_coords, sc_omega_plus, 
                                                            sc_unit_cell, ea_dict)
                placed_nodes, node_bonds = place_nodes(nvecs, CHARGES, ORIENTATION_DEPENDENT_NODES)
                placed_edges, edge_bonds = place_edges(evecs, CHARGES, len(placed_nodes))
                
                # Adjust edges if needed
                if PLACE_EDGES_BETWEEN_CONNECTION_POINTS:
                    placed_edges = adjust_edges(placed_edges, placed_nodes, sc_unit_cell)
                
                # Combine nodes and edges
                placed_nodes = np.c_[placed_nodes, np.array(['node' for i in range(len(placed_nodes))])]
                placed_edges = np.c_[placed_edges, np.array(['edge' for i in range(len(placed_edges))])]
                placed_all = list(placed_nodes) + list(placed_edges)
                bonds_all = node_bonds + edge_bonds
                
                # Remove dummy atoms if needed
                nconnections = num_possible_XX_bonds
                if REMOVE_DUMMY_ATOMS:
                    placed_all, bonds_all, nconnections = remove_Fr(placed_all, bonds_all)
                
                # Form bonds
                fixed_bonds, nbcount, bond_check_passed = bond_connected_components(
                    placed_all, bonds_all, sc_unit_cell, max_length, BOND_TOL, 
                    nconnections, num_possible_XX_bonds
                )
                
                if not bond_check_passed:
                    # Attempt distance search bonding
                    fixed_bonds, nbcount = distance_search_bond(placed_all, bonds_all, sc_unit_cell, 2.5)
                    bond_check_code = '_BOND_CHECK_FAILED'
                else:
                    bond_check_code = ''
                
                # Fix charges if needed
                if CHARGES:
                    fc_placed_all, netcharge, onetcharge, rcb = fix_charges(placed_all, rng)
                    # Remove net charge from random atom using seeded RNG
                    remove_net = generate_charge_adjustment(len(fc_placed_all), rng)
                    fc_placed_all[remove_net][4] -= np.round(netcharge, 4)
                else:
                    fc_placed_all = placed_all
                
                # Fix bond symmetry
                fixed_bonds = fix_bond_sym(fixed_bonds, placed_all, sc_unit_cell)
                
                # Generate CIF filename (consistent with tobacco.py naming)
                # Convert vertex types to numbered format using vname_dict (v1, v2, v3, ...)
                v_set_for_naming = [('v' + str(vname_dict.get(re.sub('[0-9]','',i[0]), re.sub('[0-9]','',i[0]))), i[1]) for i in va]
                v_set_for_naming = sorted(list(set(v_set_for_naming)), key=lambda x: x[0])
                v_set_for_naming = [v[0] + '-' + v[1] for v in v_set_for_naming]
                
                # Generate vnames from v_set (same as tobacco.py)
                vnames = '_'.join([v.split('.')[0] for v in v_set_for_naming])
                
                # Generate enames (same as tobacco.py)
                enames_list = [e[0:-4] if e.endswith('.cif') else e for e in ea]
                enames_grouped = [list(edge_gr) for ind, edge_gr in itertools.groupby(enames_list)]
                enames_grouped = [(len(edge_gr), list(set(edge_gr))) for edge_gr in enames_grouped]
                enames_flat = [str(L) + '-' + '_'.join(names) for L, names in enames_grouped]
                enames = '_'.join(enames_flat)
                
                cifname = template_filename.replace('.cif', '') + '_' + vnames + '_' + enames + bond_check_code + '.cif'
                
                # Truncate if too long
                if len(cifname) > 255:
                    cifname = cifname[0:241] + '_truncated.cif'
                
                # Generate CIF content string (without writing to file yet)
                # We'll let format_results handle the file writing
                from io import StringIO
                import datetime
                
                sc_a, sc_b, sc_c, sc_alpha, sc_beta, sc_gamma = scaled_params
                
                # Build CIF content in memory
                cif_lines = []
                cif_lines.append('data_' + cifname[0:-4])
                cif_lines.append('_audit_creation_date              ' + datetime.datetime.today().strftime('%Y-%m-%d'))
                cif_lines.append("_audit_creation_method            'tobacco_3.0'")
                cif_lines.append("_symmetry_space_group_name_H-M    'P1'")
                cif_lines.append('_symmetry_Int_Tables_number       1')
                cif_lines.append('_symmetry_cell_setting            triclinic')
                cif_lines.append('loop_')
                cif_lines.append('_symmetry_equiv_pos_as_xyz')
                cif_lines.append('  x,y,z')
                cif_lines.append('_cell_length_a                    ' + str(sc_a))
                cif_lines.append('_cell_length_b                    ' + str(sc_b))
                cif_lines.append('_cell_length_c                    ' + str(sc_c))
                cif_lines.append('_cell_angle_alpha                 ' + str(sc_alpha))
                cif_lines.append('_cell_angle_beta                  ' + str(sc_beta))
                cif_lines.append('_cell_angle_gamma                 ' + str(sc_gamma))
                cif_lines.append('loop_')
                cif_lines.append('_atom_site_label')
                cif_lines.append('_atom_site_type_symbol')
                cif_lines.append('_atom_site_fract_x')
                cif_lines.append('_atom_site_fract_y')
                cif_lines.append('_atom_site_fract_z')
                if CHARGES:
                    cif_lines.append('_atom_site_charge')
                
                # Add atoms
                for l in fc_placed_all:
                    vec = list(map(float, l[1:4]))
                    cvec = np.dot(np.linalg.inv(sc_unit_cell), vec)
                    cvec = np.mod(cvec, 1)  # wrap coordinates to [0,1]
                    
                    if CHARGES:
                        cif_lines.append('{:7} {:>4} {:>15} {:>15} {:>15} {:>15}'.format(
                            l[0], re.sub('[0-9]','',l[0]), 
                            "%.10f" % np.round(cvec[0],10), 
                            "%.10f" % np.round(cvec[1],10), 
                            "%.10f" % np.round(cvec[2],10), 
                            l[4]))
                    else:
                        cif_lines.append('{:7} {:>4} {:>15} {:>15} {:>15}'.format(
                            l[0], re.sub('[0-9]','',l[0]), 
                            "%.10f" % np.round(cvec[0],10), 
                            "%.10f" % np.round(cvec[1],10), 
                            "%.10f" % np.round(cvec[2],10)))
                
                # Add bonds
                cif_lines.append('loop_')
                cif_lines.append('_geom_bond_atom_site_label_1')
                cif_lines.append('_geom_bond_atom_site_label_2')
                cif_lines.append('_geom_bond_distance')
                cif_lines.append('_geom_bond_site_symmetry_2')
                cif_lines.append('_ccdc_geom_bond_type')
                
                for e in fixed_bonds:
                    cif_lines.append('{:7} {:>7} {:>5} {:>7} {:>3}'.format(
                        e[0], e[1], "%.3f" % float(e[2]), e[3], e[4]))
                
                cif_content = '\n'.join(cif_lines) + '\n'
                
                # Create result dictionary
                generation_time = time.time() - start_time
                
                result = {
                    "cif_content": cif_content,
                    "cifname": cifname,
                    "metadata": {
                        "template": template_filename,
                        "nodes": [v[1] for v in va],
                        "edges": list(ea),
                        "generation_time": generation_time,
                        "random_seed": random_seed,
                        "unit_cell_params": {
                            "a": float(sc_a),
                            "b": float(sc_b),
                            "c": float(sc_c),
                            "alpha": float(sc_alpha),
                            "beta": float(sc_beta),
                            "gamma": float(sc_gamma)
                        },
                        "num_atoms": len(fc_placed_all),
                        "num_bonds": len(fixed_bonds),
                        "bond_check_passed": bond_check_passed
                    }
                }
                
                results.append(result)
        
        # Add results from this template to all_results
        all_results.extend(results)
    
    # Format results according to return_format
    from src.utils.output_formatter import format_results
    
    if return_format == 'file':
        # For backward compatibility with 'file' format, maintain old structure
        # but also save files using output_formatter
        formatted = format_results(all_results, return_format='file')
        
        # Update results with file paths
        for i, result in enumerate(all_results):
            result['file_path'] = formatted[i]
        
        # Return single result or list of results
        if len(all_results) == 1:
            return all_results[0]
        else:
            return all_results
    
    else:
        # Use output_formatter for other formats
        formatted = format_results(all_results, return_format=return_format)
        
        # For single result with string format, unwrap from list
        if return_format == 'string' and len(all_results) == 1:
            return formatted[0]
        
        # For json format or multiple results, return as is
        return formatted


def generate_multiple_mofs(combinations, config=None, return_format='file', random_seed=None):
    """
    Generate multiple MOFs from list of combinations.
    
    This function provides a convenient way to generate multiple MOFs with
    different template/node/edge combinations in a single call.
    
    Args:
        combinations (list): List of combination dictionaries, each containing:
                           - 'template': Template name (str or list)
                           - 'nodes': Node name(s) (str, list, or dict)
                           - 'edges': Edge name(s) (str or list)
                           Example: [
                               {'template': 'pcu', 'nodes': ['6c_Cu_1_Ch'], 'edges': ['btc_edge']},
                               {'template': 'dia', 'nodes': ['4c_Zn_1_Ch'], 'edges': ['bdc_edge']}
                           ]
        config (dict, optional): Configuration overrides applied to all generations
        return_format (str or list, optional): Output format specification:
                                              - 'file': Save to file and return paths (default)
                                              - 'string': Return CIF content as strings
                                              - 'json': Return as JSON object
                                              - List of formats: Return dict with results for each format
        random_seed (int, optional): Seed for deterministic charge generation.
                                    If None, uses default seed from configuration.
                                    Same seed produces identical charges across all MOFs.
    
    Returns:
        list or dict: Results for all combinations in specified format
                     - For 'file' or 'string': List of results
                     - For 'json': Single dict with all MOFs
                     - For list of formats: Dict mapping format names to their outputs
    
    Raises:
        ValueError: If combinations list is empty or has invalid structure
        FileNotFoundError: If any template, node, or edge file not found
        
    Examples:
        >>> combinations = [
        ...     {'template': 'pcu', 'nodes': ['6c_Cu_1_Ch'], 'edges': ['btc_edge']},
        ...     {'template': 'dia', 'nodes': ['4c_Zn_1_Ch'], 'edges': ['bdc_edge']}
        ... ]
        >>> results = generate_multiple_mofs(combinations)
        >>> print(len(results))
        2
        
        >>> # With JSON output
        >>> results = generate_multiple_mofs(combinations, return_format='json')
        >>> print(results.keys())
        dict_keys(['pcu_v1-6c_Cu_1_Ch_1-btc_edge', 'dia_v1-4c_Zn_1_Ch_1-bdc_edge'])
        
        >>> # With deterministic charges
        >>> results = generate_multiple_mofs(combinations, random_seed=42)
    """
    if not combinations:
        raise ValueError("combinations list cannot be empty")
    
    if not isinstance(combinations, list):
        raise ValueError(f"combinations must be a list, got {type(combinations)}")
    
    # Validate each combination
    for i, combo in enumerate(combinations):
        if not isinstance(combo, dict):
            raise ValueError(f"Combination {i} must be a dict, got {type(combo)}")
        
        required_keys = {'template', 'nodes', 'edges'}
        missing_keys = required_keys - set(combo.keys())
        if missing_keys:
            raise ValueError(f"Combination {i} missing required keys: {missing_keys}")
    
    # Collect all results
    all_results = []
    
    # Generate MOFs for each combination
    for combo in combinations:
        template = combo['template']
        nodes = combo['nodes']
        edges = combo['edges']
        
        # Generate CIF(s) for this combination
        result = generate_cif(
            template_name=template,
            node_names=nodes,
            edge_names=edges,
            config=config,
            return_format='file',  # Always use file format internally
            random_seed=random_seed
        )
        
        # Handle single result or list of results
        if isinstance(result, list):
            all_results.extend(result)
        else:
            all_results.append(result)
    
    # Format results according to return_format
    from src.utils.output_formatter import format_results
    
    if return_format == 'file':
        # Return list of results with file paths
        return all_results
    
    else:
        # Use output_formatter for other formats
        formatted = format_results(all_results, return_format=return_format)
        return formatted

