import PIL
import os.path  
import PIL.ImageDraw            

def logo_function(original_image, logo_size, logo, st, location):
    """ Adds a logo to the top left of any image given.
    
    Takes 4 arguments, st being a true or false value deciding whether
    to make it transparent or not. Logo_size is the percent of the smaller
    side you want the logo to take up: 0<logo_size<=1. The rest of the arguments
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
    if location == 'tl':
        result.paste(rlogo, (0,0), rlogo)
    elif location == 'br':
        result.paste(rlogo, (width - position, height - position), rlogo)
    elif location == 'tr':
        result.paste(rlogo, (width - position,0), rlogo)
    elif location == 'bl':
        result.paste(rlogo, (0, height - position), rlogo)
    else:
        raise ValueError("Invalid position argument")
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

def logo_all_images(directory=None, size=0.3, st=False, location='tl'):
    """ 
    
    Saves a modfied version of each image in directory.
    
    No Arguments required, but you can specify the directory, size, whether
    you want it to be transparent (st), and the location.
    
     - directory takes a string. Default is None
     - size takes a float 0 < size <= 1. Default value is 0.3
     - st takes a boolean. Default value is false.
     - location takes a string:
         - 'tl' for top left of the image
         - 'tr' for top right
         - 'bl' for bottom left
         - 'br' for bottom right
         Default is 'tl'
    
    Uses current directory if no directory is specified. 
    Places images in subdirectory 'neweggs', creating it if it does not exist.
    New image files have the logo in the top left corner.
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
        new_image = logo_function(image_list[n], size, logo, st, location)
        #save the altered image, suing PNG to retain transparency
        new_image_filename = os.path.join(new_directory, filename + '.png')
        new_image.save(new_image_filename)    