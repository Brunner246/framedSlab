"""framedSlab.py: create a simple framed slab in cadwork...."""

# import modules
import      utility_controller         as uc
import      element_controller         as ec
import      cadwork
import      geometry_controller        as gc
import      attribute_controller       as ac
import      visualization_controller   as vc


WIDTH           = 60.           # beam width
HEIGHT          = 240.          # beam height
ORIGIN          = 0., 0., 0.    # start/origin point
DIVISION        = 4             # number of divsion -> distribution (Sprungmass)
BEAM_LENGTH     = 2800.         # length (Fuss-, Kopfholz)
MEMBER_LENGTH   = 5000.         # length (Balken)


def main():
    """ main function that creates a simple framed slab"""
    
    global ORIGIN
    global BEAM_LENGTH
    global MEMBER_LENGTH
    global WIDTH
    
    beam_length = BEAM_LENGTH # uc.get_user_double('Input beam length')
    
    # Fussholz
    beam_1 = createBeam(beam_length, 
                        cadwork.point_3d(*ORIGIN), 
                        cadwork.point_3d(0., 1., 0.), 
                        cadwork.point_3d(0., 0., 1.), 
                        'beam')
    
    # get vectors (beam_1)
    x_dir_beam, y_dir_beam, z_dir_beam = getBeamVectors(beam_1)
    
    # move cadwork point -> start point for beam_2 (Kopfholz)
    start_point_beam_2 = cadwork.point_3d(*ORIGIN) + y_dir_beam * (MEMBER_LENGTH + WIDTH)
    
    # Kopfholz
    beam_2 = createBeam(beam_length, 
                        start_point_beam_2, 
                        cadwork.point_3d(0., 1., 0.), 
                        cadwork.point_3d(0., 0., 1.), 
                        'beam')
    
    # move cadwork point -> start point for members
    start_point_member = cadwork.point_3d(*ORIGIN) + y_dir_beam * .5 * WIDTH + cadwork.point_3d(*ORIGIN) + x_dir_beam * .5 * WIDTH
    
    global DIVISION
    # calculate division distance (Sprungmass)
    spacing = beamSpacing(beam_1, DIVISION)
    
    # while loop to create members -> increase spacing division
    n = 0.
    while n <= beam_length:
        member = createBeam(MEMBER_LENGTH, 
                            start_point_member + 
                            x_dir_beam * n, y_dir_beam, 
                            z_dir_beam)
        n += spacing
        
    return

#---------------------------------------------------------------

def createBeam(length, p1, x_dir, z_dir, name='member', color=3):
    """Creates a rectangular member with attributes: name, color

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
    """Returns vectors (x,y,z) 

    Parameters
    ----------
    element_id : int
        cadwork element id
        
    Returns
    -------
    point_3d
        returns cadwork point_3d / vectors
    """
    x_dir_sill = gc.get_xl(element_id)
    y_dir_sill = gc.get_yl(element_id)
    z_dir_sill = gc.get_zl(element_id)
    
    return x_dir_sill, y_dir_sill, z_dir_sill


def beamSpacing(beam, subdivisions):
    """Calculates the beam/member spacing (Sprungmass)

    Parameters
    ----------
    element_id : int
        cadwork element id
    
    subdivisions: int
        number of divisions
        
    Returns
    -------
    float
        returns divison length
    """
    global WIDTH
    beam_length = gc.get_length(beam)
    distance = (beam_length - WIDTH) / subdivisions
    
    return distance
    
    
#---------------------------------------------------------------

if __name__ == '__main__':
    main()
    
