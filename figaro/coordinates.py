from __future__ import division
import numpy as np

def cartesian_to_spherical(vector):
    """
    Convert the Cartesian vector [x, y, z] to spherical coordinates [r, theta, phi].
    The parameter r is the radial distance, theta is the polar angle, and phi is the azimuth.
    
    Arguments:
        :np.ndarray: cartesian vector [x, y, z]
        
    Returns:
        :np.ndarray: spherical coordinate vector [r, theta, phi]
    """
    r = np.linalg.norm(vector, axis = -1)
    unit = np.array([v/np.linalg.norm(v) for v in vector])
    theta = np.arcsin(unit[:,2])
    phi = np.arctan2(unit[:,0], unit[:,1])
    phi[phi<0] += 2*np.pi
    coord = np.array([r,theta,phi]).T
    return coord


def spherical_to_cartesian(vector):
    """
    Convert the spherical coordinate vector [r, theta, phi] to the Cartesian vector [x, y, z].
    The parameter r is the radial distance, theta is the polar angle, and phi is the azimuth
    
    Arguments:
        :np.ndarray vector: spherical coordinate vector [r, theta, phi]
        
    Returns:
        :np.ndarray: cartesian vector [x, y, z]
    """
    # Trig alias.
    cos_theta = np.cos(vector[:,1])
    # The vector.
    x = vector[:,2] * np.sin(vector[:,0]) * cos_theta
    y = vector[:,2] * np.cos(vector[:,0]) * cos_theta
    z = vector[:,2] * np.sin(vector[:,1])
    return np.array([x,y,z]).T
    
def celestial_to_cartesian(celestial_vect):
    """
    Convert the spherical coordinate vector [ra, dec, D] to the Cartesian vector [x, y, z]
    
    Arguments:
        :np.ndarray celestial_vect: celestial coordinate vector [r, dec, D]
        
    Returns:
        :np.ndarray: cartesian vector [x, y, z]
    """
    celestial_vect = np.atleast_2d(celestial_vect)
    return spherical_to_cartesian(celestial_vect)

def cartesian_to_celestial(cartesian_vect):
    """
    Convert the Cartesian vector [x, y, z] to the celestial coordinate vector [ra, dec, D]
    
    Arguments:
        :np.ndarray cartesian_vect: cartesian vector [x, y, z]
    
    Returns:
        :np.ndarray: celestial coordinate vector [ra, dec, D]
    """
    cartesian_vect = np.atleast_2d(cartesian_vect)
    spherical_vect = cartesian_to_spherical(cartesian_vect)
    D   = spherical_vect[:,0]
    dec = spherical_vect[:,1]
    ra  = spherical_vect[:,2]
    return np.array([ra, dec, D]).T

def Jacobian(cartesian_vect):
    """
    Computes the jacobian of celestial transformation for a cartesian vector
    
    Arguments:
        :np.ndarray cartesian_vect: cartesian vector [x, y, z]
    
    Returns:
        :np.ndarray: Jacobian of the transformation
    """
    return Jacobian_in_celestial(cartesian_to_celestial(np.atleast_2d(cartesian_vect)))

def inv_Jacobian(celestial_vect):
    """
    Computes the inverse jacobian of celestial transformation for a celestial vector
    
    Arguments:
        :np.ndarray cartesian_vect: cartesian vector [ra, dec, D]
    
    Returns:
        :np.ndarray: inverse Jacobian of the transformation
    """
    detJ = Jacobian_in_celestial(np.atleast_2d(celestial_vect))
    return 1/detJ
    
def Jacobian_in_celestial(celestial_vect):
    """
    Computes the jacobian of celestial transformation
    
    Arguments:
        :np.ndarray cartesian_vect: cartesian vector [ra, dec, D]
    
    Returns:
        :np.ndarray: Jacobian of the transformation
    """
    d = celestial_vect[:,2]
    theta = celestial_vect[:,1]
    return d*d*np.cos(theta)
