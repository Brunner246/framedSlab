"""TEMPLATE.py: foo bar does what...."""

import      utility_controller         as uc
import      element_controller         as ec
import      cadwork
import      geometry_controller        as gc
import      attribute_controller       as ac
import      visualization_controller   as vc

WIDTH = 60.
HEIGHT = 240.
ORIGIN = 0., 0., 0.

# ÄNDERN AUF BALKENLAGE !!!!!!!!!!!
def main():
    """ main function that creates a simple frame"""
    
    global ORIGIN
    
    sill = createBeam(2800., cadwork.point_3d(*ORIGIN), cadwork.point_3d(0., 1., 0.), cadwork.point_3d(1., 0., 0.), 'sill')
       
    x_dir_sill, y_dir_sill, z_dir_sill = getBeamVectors(sill)
    
    start_point_studs = cadwork.point_3d(*ORIGIN) + y_dir_sill * .5 * WIDTH + cadwork.point_3d(*ORIGIN) + x_dir_sill * .5 * WIDTH
    
    stud = createBeam(2800., start_point_studs, y_dir_sill, z_dir_sill, 'stud')
    
    
    return

#---------------------------------------------------------------

def createBeam(length, p1, x_dir, z_dir, name='beam', color=3):
    """Creates a rectangular beam with attributes: name, color

    Parameters
    ----------
    length : int
        beam length
    p1 : point_3d
        start point x, y, z
    x_dir : point_3d
        local x-vector x, y, z -> cadwork.point_3d(0., 1., 0.)
    z_dir : point_3d
        local z-vector x, y, z -> cadwork.point_3d(1., 0., 0.)
    name : str, optional
        set a name -> default = beam

    Returns
    -------
    int
        returns cadwork element ID
    """
    global WIDTH
    global HEIGHT
    beam = ec.create_rectangular_beam_vectors(WIDTH, HEIGHT, length, p1, x_dir, z_dir)
    ac.set_name([beam], name)
    vc.set_color([beam], color)
    return beam


def getBeamVectors(element_id):
    x_dir_sill = gc.get_xl(element_id)
    y_dir_sill = gc.get_yl(element_id)
    z_dir_sill = gc.get_zl(element_id)
    
    return x_dir_sill, y_dir_sill, z_dir_sill

#---------------------------------------------------------------

if __name__ == '__main__':
    main()
    
