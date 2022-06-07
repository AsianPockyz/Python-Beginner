from image import Image
import numpy as np

def brighten(image, factor):
    # when we brighten, we just want to make each channel higher by some amount 
    # factor is a value > 0, how much you want to brighten the image by (< 1 = darken, > 1 = brighten)
    x_pixels, y_pixels, num_channels = image.array.shape # get the x, y pixels and the # channels
    # make an empty image so we don't actually modify the base image
    new_img = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    # # the most intuitive way, non vectorized
    # for x in range(x_pixels):
    #     for y in range(y_pixels):
    #         for c in range(num_channels):
    #             new_img.array[x, y, c] = image.array[x, y, c] * factor
    # return new_img

    # vectorized version, accomplish the same as above commented for loop
    # because it is a numpy array
    new_img.array = image.array * factor

    return new_img

def adjust_contrast(image, factor, mid):
    # adjust the contrast by increasing the difference from the user-defined midpoint by factor amount
    x_pixels, y_pixels, num_channels = image.array.shape # get the x, y pixels and the # channels
    # make an empty image so we don't actually modify the base image
    new_img = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_img.array[x,y,c] = (image.array[x,y,c] - mid) * factor + mid

    # vectorized
    # new_img.array = (image.array - mid) * factor + mid

    return new_img

def blur(image, kernel_size):
    # kernel size is the number of pixels to take into account when applying the blur
    # (ie kernel_size = 3 would be neighbors to the left/right, top/bottom, and diagonals)
    # kernel size should always be an *odd* number
    x_pixels, y_pixels, num_channels = image.array.shape # get the x, y pixels and the # channels
    # make an empty image so we don't actually modify the base image
    new_img = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    neighbor_range = kernel_size // 2 # how many adjacent to one side we need to look

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                # naive implementation of iterating through each neighbor and averaging
                total = 0
                for x_i in range(max(0, x-neighbor_range), min(x_pixels - 1, x+neighbor_range) + 1):
                    for y_i in range(max(0, y-neighbor_range), min(y_pixels - 1, y+neighbor_range) + 1):
                        total += image.array [x_i, y_i, c]
                new_img.array [x,y,c] = total / (kernel_size ** 2) # average value of the pixels and it's adjacents
    
    return new_img
    # note that this blur is implemented is a kernal of size n, where each value is 1/n^2
    # for example k=3
    # [1/9 1/9 1/9]
    # [1/9 1/9 1/9]
    # [1/9 1/9 1/9]



def apply_kernel(image, kernel):
    # the kernel should be a 2D array that represents the kernel we'll use!
    # for the sake of simiplicity of this implementation, let's assume that the kernel is SQUARE
    # for example the sobel x kernel (detecting horizontal edges) is as follows:
    # [1 0 -1]
    # [2 0 -2]
    # [1 0 -1]
    x_pixels, y_pixels, num_channels = image.array.shape # get the x, y pixels and the # channels
    # make an empty image so we don't actually modify the base image
    new_img = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    kernel_size = kernel.shape[0]
    neighbor_range = kernel_size // 2

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0
                for x_i in range(max(0, x-neighbor_range), min(x_pixels - 1, x+neighbor_range) + 1):
                    for y_i in range(max(0, y-neighbor_range), min(y_pixels - 1, y+neighbor_range) + 1):
                        # here we need to find which value of the kernel corresponds to 
                        x_k = x_i + neighbor_range - x
                        y_k = y_i + neighbor_range - y
                        kernel_val = kernel[x_k, y_k]
                        total += image.array[x_i, y_i, c] * kernel_val
                new_img.array[x,y,c] = total
    return new_img

def combine_images(image1, image2):
    # let's combine two images using the squared sum of squares: value = sqrt(value_1**2, value_2**2)
    # size of image1 and image2 MUST be the same
    x_pixels, y_pixels, num_channels = image1.array.shape # get the x, y pixels and the # channels
    # make an empty image so we don't actually modify the base image
    new_img = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_img.array[x,y,c] = (image1.array[x, y, c]**2 + image2.array[x,y,c]**2)**0.5
    return new_img
    
if __name__ == '__main__':
    lake = Image(filename='lake.png')
    city = Image(filename='city.png')

    # # examples brighten the lake
    # brightened_img = brighten(lake, 4.0)
    # brightened_img.write_image('brightenedlake.png')

    # # example darken lake
    # darkened_img = brighten(lake, 0.1)
    # darkened_img.write_image('darkenedlake2.png')

    # # adjust the contrast for the lake
    # increase_contrast = adjust_contrast(lake, 2, 0.5)
    # increase_contrast.write_image('increase_contrast_lake.png')

    # # decrease contrast
    # decrease_contrast = adjust_contrast(lake, 0.5, 0.5)
    # decrease_contrast.write_image('decrease_contrast_lake.png')

    # # blur city with factor of 3
    # blur_city3 = blur(city, 3)
    # blur_city3.write_image('blur_city3.png')
    # # blur city with factor of 15
    # blur_city15 = blur(city, 15)
    # blur_city15.write_image('blur_city15.png')

    # apply a sobel edge detection kernel on x and y axis
    sobel_x_kernel = np.array([[1,2,1], [0,0,0], [-1,-2,-1]])
    sobel_y_kernel = np.array([[1,0,-1], [2,0,-2], [1, 0,-1]])

    sobel_x = apply_kernel(city, sobel_x_kernel)
    sobel_x.write_image('edge_x.png')
    sobel_y = apply_kernel(city, sobel_y_kernel)
    sobel_y.write_image('edge_y.png')

    # using the last edge detection method to combien the two images and make an edge detection filter
    sobel_xy = combine_images(sobel_x, sobel_y)
    sobel_xy.write_image('edge_xy.png')