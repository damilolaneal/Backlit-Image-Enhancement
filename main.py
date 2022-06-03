#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 21:42:37 2021

This function should show all the obtained results as images. The quantitative
results will be obtained using MATLAB's built-in functions.

@author: ruwwad
"""


def main():
    print('''This function shows the qualititative results of the project.
For quantitative results, go check the MATLAB function quantitativeResults.m.
          
NOTE: This function is rather slow since we are not experts when it
comes to optimization, so give us some slack, will you :)?\n''')

    import numpy as np
    import matplotlib.pyplot as plt
    from PIL import Image
    from masatoAkaiM import masatoAkaiM
    from mAk_CLAHE import mAk_CLAHE
    from mAk_CLAHE_Fusion import mAk_CLAHE_Fusion
    from mAk_CLAHE_Fusion3 import mAk_CLAHE_Fusion3
    from imshow import imshow

    # Below, we will read all the images that we have used in this
    images = []
    inputImages = []
    for i in range(4):
        images.append('Images/r{}RGB.png'.format(i + 1))
        inputImages.append(np.array(Image.open('Images/r{}RGB.png'.format(i + 1)),
                                    dtype=float)[:, :, :3])

    # Preallocate all the results from all methods
    masatoAkai = []  # Masato Akai's method
    MAk_CLAHE = []  # Replacing global HE with CLAHE

    # Replacing global HE with CLAHE, and replacing naive blending with fusion
    MAk_CLAHE_Fusion = []

    # Replacing global HE with CLAHE, replacing naive blending with fusion, and
    # adding another input to the fusion which applies inverse gamma correction
    # to the input image
    MAk_CLAHE_Fusion3 = []

    # Find the results of all methods
    print("We will now run all 4 functions on all 4 images")
    print("Note that this will take quite a bit of time")
    print('''However, we will be updating you with the progress to assure you that
it is "doing something" :)\n''')
    print('''For the time being, let us quickly summarize what we will be doing.
We will show you the results of four methods.
1- Masato Akai's Method
2- Replacing global HE with CLAHE
3- Replacing global HE with CLAHE + Replacing naive blending with image fusion
4- The same as the last, but we will add another image to the fusion, which
   we will apply inverse gamma correction to it further reduce the artifacts
   in the bright regions
  
Now, go make yourself a cup of coffee or tea, or maybe order some food,
read the news, watch YouTube or NetFlix... We live in a day and age where
boredom is forbidden. Haven't you ever though how the current media is in a
sense, turning us all into entertainment beasts? Yeah, I probably should have
chosen another topic. Okay... ''')

    print()

    for i in range(4):
        print("Working on image {} out of 4".format(i + 1))
        print("{}%... Applying Masato Akai's method".format(int((i * 100 + 0 * 25) / 4)))
        masatoAkai.append(masatoAkaiM(images[i]))
        print("{}%... Applying Masato Akai's method + CLAHE".format(int((i * 100 + 1 * 25) / 4)))
        MAk_CLAHE.append(mAk_CLAHE(images[i]))
        print("{}%... Applying Masato Akai's method + CLAHE + Fusion".format(int((i * 100 + 2 * 25) / 4)))
        MAk_CLAHE_Fusion.append(mAk_CLAHE_Fusion(images[i]))
        print("{}%... Applying Masato Akai's method + CLAHE + Fusion3".format(int((i * 100 + 3 * 25) / 4)))
        MAk_CLAHE_Fusion3.append(mAk_CLAHE_Fusion3(images[i]))

        print("Done from image {}\n".format(i + 1))
        print('''Saving the results to folder "Results"\n''')
        print("Showing the current results")

        imshow(inputImages[i], 'Image {}'.format(i + 1), 1)
        plt.figure(dpi=300)

        plt.subplot(2, 2, 1)
        plt.title("Masato Akai's Method")
        plt.axis('off')
        plt.imshow(masatoAkai[i])

        plt.subplot(2, 2, 2)
        plt.title("MAk + CLAHE")
        plt.axis('off')
        plt.imshow(MAk_CLAHE[i])

        plt.subplot(2, 2, 3)
        plt.title("MAk + CLAHE + Fusion")
        plt.axis('off')
        plt.imshow(MAk_CLAHE_Fusion[i])

        plt.subplot(2, 2, 4)
        plt.title("MAk + CLAHE + Fusion3")
        plt.axis('off')
        plt.imshow(MAk_CLAHE_Fusion3[i])

        imshow(masatoAkai[i], "Masato Akai's Method", 1)
        imshow(MAk_CLAHE[i], "Masato Akai's Method + CLAHE", 1)
        imshow(MAk_CLAHE_Fusion[i], "MAk + CLAHE + Fusion", 1)
        imshow(MAk_CLAHE_Fusion3[i], "MAk + CLAHE + Fusion3", 1)

        plt.show()

        print('''Saving the results to folder "Results"\n''')
        Image.fromarray(np.uint8(masatoAkai[i])).save("YourResults/r{} Masato Akai's Method.png".format(i + 1))
        Image.fromarray(np.uint8(MAk_CLAHE[i])).save("YourResults/r{} MAk + CLAHE.png".format(i + 1))
        Image.fromarray(np.uint8(MAk_CLAHE_Fusion[i])).save("YourResults/r{} MAk + CLAHE + Fusion.png".format(i + 1))
        Image.fromarray(np.uint8(MAk_CLAHE_Fusion3[i])).save("YourResults/r{} MAk + CLAHE + Fusion3.png".format(i + 1))

    return [masatoAkai, MAk_CLAHE, MAk_CLAHE_Fusion, MAk_CLAHE_Fusion3]


# import numpy as np
# import matplotlib.pyplot as plt
# from PIL import Image
# from masatoAkaiM import masatoAkaiM
# from mAk_CLAHE import mAk_CLAHE
# from mAk_CLAHE_Fusion import mAk_CLAHE_Fusion
# from mAk_CLAHE_Fusion3 import mAk_CLAHE_Fusion3
# from imshow import imshow

# #Below, we will read all the images that we have used in this 
# images = []
# inputImages = []
# for i in range(4):
#     images.append('Images/r{}RGB.png'.format(i+1))
#     inputImages.append(np.array(Image.open('Images/r{}RGB.png'.format(i+1)),
#                             dtype=float)[:,:,:3])

# #Preallocate all the results from all methods
# masatoAkai = []  #Masato Akai's method
# MAk_CLAHE = []  #Replacing global HE with CLAHE

# #Replacing global HE with CLAHE, and replacing naive blending with fusion
# MAk_CLAHE_Fusion = []

# #Replacing global HE with CLAHE, replacing naive blending with fusion, and
# #adding another input to the fusion which applies inverse gamma correction
# #to the input image
# MAk_CLAHE_Fusion3 = []

# #Find the results of all methods
# print("We will now run all 4 functions on all 4 images")
# print("Note that this will take quite a bit of time")
# print('''However, we will be updating you with the progress to assure you that
# it is "doing something" :)\n''')

# for i in range(4):
#     print("Working on image {} out of 4")
#     print("{}%... Applying Masato Akai's method".format( int((i*100+0*25)/4)) )
#     masatoAkai.append(masatoAkaiM(images[i]))
#     print("{}%... Applying Masato Akai's method + CLAHE".format( int((i*100+1*25)/4)) )
#     MAk_CLAHE.append(mAk_CLAHE(images[i]))
#     print("{}%... Applying Masato Akai's method + CLAHE + Fusion".format( int((i*100+2*25)/4)) )
#     MAk_CLAHE_Fusion.append(mAk_CLAHE_Fusion(images[i]))
#     print("{}%... Applying Masato Akai's method + CLAHE + Fusion3".format( int((i*100+3*25)/4)) )
#     MAk_CLAHE_Fusion3.append(mAk_CLAHE_Fusion3(images[i]))

#     print("Done from image {}".format(i))

#     imshow(inputImages[i], 'Image {}'.format(i), 1)
#     plt.figure(dpi=300)

#     plt.subplot(2,2,1)
#     plt.title("Masato Akai's Method")
#     plt.axis('off')
#     plt.imshow(masatoAkai[i])

#     plt.subplot(2,2,2)
#     plt.title("MAk + CLAHE")
#     plt.axis('off')
#     plt.imshow(MAk_CLAHE[i])

#     plt.subplot(2,2,3)
#     plt.title("MAk + CLAHE + Fusion")
#     plt.axis('off')
#     plt.imshow(MAk_CLAHE_Fusion[i])

#     plt.subplot(2,2,3)
#     plt.title("MAk + CLAHE + Fusion3")
#     plt.axis('off')
#     plt.imshow(MAk_CLAHE_Fusion3[i])

#     imshow(masatoAkai[i], "Masato Akai's Method", 1)
#     imshow(MAk_CLAHE[i], "Masato Akai's Method + CLAHE")
#     imshow(MAk_CLAHE_Fusion[i], "MAk + CLAHE + Fusion")
#     imshow(MAk_CLAHE_Fusion3[i], "MAk + CLAHE + Fusion3")

#     plt.show()
if __name__ == '__main__':
    main()
