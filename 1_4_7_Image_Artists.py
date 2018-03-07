import PIL
import os.path  
import PIL.ImageDraw            

def fillerName(original_image, logo_size, logo, st):
    """ Adds a logo to the top left of any image given.
    
    Takes 4 arguments, st being a true or false value deciding whether
    to make it transparent or not. Logo_size is the percent of the smaller
    side you want the logo to take up: 0<logo_size<1. The rest fo the arguments
    are self explanitory image files.
    """
    #set the radius of the rounded corners
    width, height = original_image.size
    position = int(logo_size * min(width, height)) # thickness in pixels
    
    ###
    #create a mask
    ###
    
    #start with transparent mask
    
    # Make the new image, starting with all transparent
    rlogo = logo.resize((position, position))
    
    if st:    
        pix = rlogo.load()
        for w in xrange(position):
            for h in xrange(position):
                r,g,b,a = pix[(w,h)]
                if a != 0:
                    pix[(w,h)] = (r,g,b,a - 50) 
                
    result = original_image.copy()
    result.paste(rlogo, (0,0), rlogo)
    return result
    
def get_images(directory=None):
    """ Returns PIL.Image objects for all the images in directory.
    
    If directory is not specified, uses current directory.
    Returns a 2-tuple containing 
    a list with a  PIL.Image object for each image file in root_directory, and
    a list with a string filename for each image file in root_directory
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    image_list = [] # Initialize aggregaotrs
    file_list = []
    
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass # do nothing with errors tying to open non-images
    return image_list, file_list

def filler_all_images(directory=None, size=0.3, st = False):
    """ Saves a modfied version of each image in directory.
    
    Uses current directory if no directory is specified. 
    Places images in subdirectory 'modified', creating it if it does not exist.
    New image files are of type PNG and have transparent rounded corners.
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    # Create a new directory 'modified'
    new_directory = os.path.join(directory, 'newEggs')
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed  
    
    #load all the images
    image_list, file_list = get_images(directory)  
    logo = PIL.Image.open('/Users/232963/WJH_147_Minh-Cole/newEgG.png')

    #go through the images and save modified versions
    for n in range(len(image_list)):
        # Parse the filename
        print n
        filename, filetype = file_list[n].split('.')
        
        # Round the corners with radius = 30% of short side
        new_image = fillerName(image_list[n], size, logo, st)
        #save the altered image, suing PNG to retain transparency
        new_image_filename = os.path.join(new_directory, filename + '.png')
        new_image.save(new_image_filename)    

