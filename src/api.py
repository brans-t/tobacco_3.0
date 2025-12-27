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
    Validate input parameters.
    
    Args:
        template_name (str): Template filename
        node_names (list or dict): Node filenames
        edge_names (list): Edge filenames
        
    Raises:
        ValueError: If inputs are invalid
        FileNotFoundError: If required files don't exist
    """
    # Validate template_name
    if not template_name or not isinstance(template_name, str):
        raise ValueError("template_name must be a non-empty string")
    
    # Validate node_names
    if not isinstance(node_names, (list, dict)):
        raise ValueError(f"node_names must be list or dict, got {type(node_names)}")
    
    if isinstance(node_names, list) and len(node_names) == 0:
        raise ValueError("node_names list cannot be empty")
    
    if isinstance(node_names, dict) and len(node_names) == 0:
        raise ValueError("node_names dict cannot be empty")
    
    # Validate edge_names
    if not isinstance(edge_names, list):
        raise ValueError(f"edge_names must be a list, got {type(edge_names)}")
    
    if len(edge_names) == 0:
        raise ValueError("edge_names list cannot be empty")
    
    # Check if template file exists
    template_filename = _normalize_filename(template_name)
    template_path = get_template_path(template_filename)
    if not template_path.exists():
        raise FileNotFoundError(
            f"Template file '{template_filename}' not found. "
            f"Searched in: {TEMPLATES_DIR}"
        )
    
    # Check if node files exist
    node_list = []
    if isinstance(node_names, dict):
        node_list = list(node_names.values())
    else:
        node_list = node_names
    
    for node_name in node_list:
        node_filename = _normalize_filename(node_name)
        node_path = get_node_path(node_filename)
        if not node_path.exists():
            raise FileNotFoundError(
                f"Node file '{node_filename}' not found. "
                f"Searched in: {NODES_DIR}"
            )
    
    # Check if edge files exist
    for edge_name in edge_names:
        edge_filename = _normalize_filename(edge_name)
        edge_path = get_edge_path(edge_filename)
        if not edge_path.exists():
            raise FileNotFoundError(
                f"Edge file '{edge_filename}' not found. "
                f"Searched in: {EDGES_DIR}"
            )


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
        'REMOVE_DUMMY_ATOMS': configuration.REMOVE_DUMMY_ATOMS
    }


def _prepare_node_files(node_names):
    """
    Prepare node files list from input.
    
    Args:
        node_names (list or dict): Node filenames or vertex type mapping
        
    Returns:
        list: List of node filenames with .cif extension
    """
    if isinstance(node_names, dict):
        # Dictionary mapping vertex types to node filenames
        return [_normalize_filename(name) for name in node_names.values()]
    else:
        # List of node filenames
        return [_normalize_filename(name) for name in node_names]


def _prepare_edge_files(edge_names):
    """
    Prepare edge files list from input.
    
    Args:
        edge_names (list): Edge filenames
        
    Returns:
        list: List of edge filenames with .cif extension
    """
    return [_normalize_filename(name) for name in edge_names]


def generate_cif(template_name, node_names, edge_names, config=None):
    """
    Generate CIF file content from template, nodes, and edges.
    
    This is the main API function for programmatic CIF generation.
    
    Args:
        template_name (str): Template filename without .cif extension (e.g., "pcu")
                            or with .cif extension (e.g., "pcu.cif")
        node_names (list or dict): List of node filenames or dict mapping vertex types to filenames
                                   Examples: ["6c_Cu_1_Ch"] or {"V": "6c_Cu_1_Ch"}
                                   Extensions (.cif) are optional
        edge_names (list): List of edge filenames without .cif extension (e.g., ["btc_edge"])
                          Extensions (.cif) are optional
        config (dict, optional): Configuration overrides. Any key from configuration.py
                                can be overridden here.
        
    Returns:
        dict or list: Single result dict or list of dicts if multiple structures generated
                     Each dict contains:
                     - "cif_content" (str): The CIF file content
                     - "cifname" (str): Generated filename
                     - "metadata" (dict): Generation metadata (timing, parameters, etc.)
    
    Raises:
        FileNotFoundError: If template, node, or edge file not found
        ValueError: If assignments are incompatible or inputs are invalid
        
    Examples:
        >>> result = generate_cif("pcu", ["6c_Cu_1_Ch"], ["btc_edge"])
        >>> print(result["cifname"])
        pcu_v1-6c_Cu_1_Ch_1-btc_edge.cif
        
        >>> # With configuration override
        >>> result = generate_cif("pcu", ["6c_Cu_1_Ch"], ["btc_edge"], 
        ...                       config={"CHARGES": False})
        
        >>> # With vertex type mapping
        >>> result = generate_cif("pcu", {"V": "6c_Cu_1_Ch"}, ["btc_edge"])
    """
    start_time = time.time()
    
    # Ensure output directories exist
    ensure_directories()
    
    # Validate inputs
    _validate_inputs(template_name, node_names, edge_names)
    
    # Normalize filenames
    template_filename = _normalize_filename(template_name)
    node_files = _prepare_node_files(node_names)
    edge_files = _prepare_edge_files(edge_names)
    
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
    
    # Store results (may be multiple if combinatorial)
    results = []
    
    # Process template
    for net in ct2g(template_filename):
        TG, start, unit_cell, TVT, TET, TNAME, a, b, c, ang_alpha, ang_beta, ang_gamma, max_le, catenation = net
        
        TVT = sorted(TVT, key=lambda x:x[0], reverse=True)
        TET = sorted(TET, reverse=True)
        
        # Get node coordination numbers from nodes directory
        node_cns = [(cncalc(node, 'nodes'), node) for node in os.listdir(NODES_DIR)]
        
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
                    fc_placed_all, netcharge, onetcharge, rcb = fix_charges(placed_all)
                    # Remove net charge from random atom
                    remove_net = choice(range(len(fc_placed_all)))
                    fc_placed_all[remove_net][4] -= np.round(netcharge, 4)
                else:
                    fc_placed_all = placed_all
                
                # Fix bond symmetry
                fixed_bonds = fix_bond_sym(fixed_bonds, placed_all, sc_unit_cell)
                
                # Generate CIF filename
                v_set = [(re.sub('[0-9]','', i[0]), i[1]) for i in va]
                v_set = sorted(list(set(v_set)), key=lambda x: x[0])
                vnames = '_'.join([v[0] + '-' + v[1].replace('.cif', '') for v in v_set])
                
                enames_list = [e.replace('.cif', '') for e in ea]
                enames_grouped = [list(edge_gr) for ind, edge_gr in itertools.groupby(enames_list)]
                enames_grouped = [(len(edge_gr), list(set(edge_gr))) for edge_gr in enames_grouped]
                enames_flat = [str(L) + '-' + '_'.join(names) for L, names in enames_grouped]
                enames = '_'.join(enames_flat)
                
                cifname = template_filename.replace('.cif', '') + '_' + vnames + '_' + enames + bond_check_code + '.cif'
                
                # Truncate if too long
                if len(cifname) > 255:
                    cifname = cifname[0:241] + '_truncated.cif'
                
                # Generate CIF content by writing to file then reading it
                # (write_cif writes to OUTPUT_CIFS_DIR)
                write_cif(fc_placed_all, fixed_bonds, scaled_params, sc_unit_cell, cifname, CHARGES)
                
                # Read the generated CIF file
                from src.utils.paths import get_output_cif_path
                cif_path = get_output_cif_path(cifname)
                with open(cif_path, 'r') as f:
                    cif_content = f.read()
                
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
    
    # Return single result or list of results
    if len(results) == 1:
        return results[0]
    else:
        return results
