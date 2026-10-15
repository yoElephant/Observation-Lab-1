#Liam Stone

import numpy as np
import glob
from astropy.io import fits
import matplotlib.pyplot as plt

######## OUR DATA ##########
#%%
#BIAS
def count(unfixed_image):
    actual_count = (unfixed_image/16)+1
    return actual_count

files = sorted(glob.glob(r'\Users\liamo\Astronomy\ASTR362\Lab1\BiasImages\*.fit'))

bias_images = []

for file in files:
    bias_images.append(fits.getdata(file))


bias_images = np.array(bias_images)
alt_bias = bias_images
images = count(bias_images)

mean_bias = np.mean(images, axis=0)
median_bias = np.median(mean_bias) #153.6

print(median_bias)

plt.figure(figsize=(8, 8))
plt.imshow(mean_bias, cmap='gray', origin='lower')
plt.colorbar(label='Counts')
plt.title('Mean Bias Image: CMOS')
plt.show()


#%%
#DARKS
second10_file = sorted(glob.glob(r'\Users\liamo\Astronomy\ASTR362\Lab1\darkimages\10sec\*.fit'))
images10 = []

for file in second10_file:
    images10.append(fits.getdata(file))

images10 = np.array(images10)
images10 = count(images10)
avg_10dark = np.mean(images10, axis=0)
plt.figure(figsize=(8, 8))
plt.imshow(avg_10dark, cmap='gray', origin='lower')
plt.colorbar(label='Counts')
plt.title('Mean 10 second Dark Image: CMOS')
plt.show()
#%%
#FLATS
files = sorted(glob.glob(r'\Users\liamo\Astronomy\ASTR362\Lab1\Twilight Flats\*.fit'))

flat_images = []

reduced_files = files[::5]

for file in reduced_files:
    flat_images.append(fits.getdata(file))

flats = np.array(flat_images)
flats = count(flats)

median_flats = np.median(flats, axis=0)

corrected_flats = (flats - mean_bias)/median_flats

flats = np.median(corrected_flats, axis=0)

plt.figure(figsize=(8, 8))
plt.imshow(flats, cmap='gray', origin='lower')
plt.colorbar(label='Counts')
plt.title('Normalized Flats')
plt.show()

#%%
#Difference
difference = images[1]-images[3]

difference_mean = np.mean(difference) #0.07344
plt.hist(difference)
#%%
#Science Images
deneb_images = []

deneb_files = sorted(glob.glob(r'\Users\liamo\Astronomy\ASTR362\Lab1\deneb\*.fit'))
for file in deneb_files:
    deneb_images.append(fits.getdata(file))
deneb_images = np.array(deneb_images)
deneb_images = count(deneb_images)
correct_deneb = (deneb_images - avg_10dark - mean_bias) / flats
deneb = np.median(correct_deneb, axis = 0)

vmin, vmax = np.percentile(deneb,[1,99])
plt.imshow(deneb, cmap='grey', origin='lower', vmin=vmin, vmax=vmax)
plt.title('Corrected Deneb')
plt.colorbar(label='ADU')


########## DR GOOD DATA ############
#%%
#DARKS
goodsecond10_file = sorted(glob.glob(r'\Users\liamo\Astronomy\ASTR362\Lab1\gooddarks10\*.fit'))
second30_file = sorted(glob.glob(r'\Users\liamo\Astronomy\ASTR362\Lab1\darks30\*.fit'))
goodimages10 = []
images30 = []

for file in goodsecond10_file:
    goodimages10.append(fits.getdata(file))
for file in second30_file:
    images30.append(fits.getdata(file))

goodimages10 = np.array(goodimages10)
images30 = np.array(images30)

goodimages10 = count(images10)
images30 = count(images30)

goodavg_10dark = np.mean(goodimages10, axis=0)
avg_30dark = np.mean(images30, axis=0)


plt.figure(figsize=(8, 8))
plt.imshow(goodavg_10dark, cmap='gray', origin='lower')
plt.colorbar(label='Counts')
plt.title('Mean 10 second Dark Image: CMOS (Dr Good Data)')
plt.show()

plt.figure(figsize=(8, 8))
plt.imshow(avg_30dark, cmap='gray', origin='lower')
plt.colorbar(label='Counts')
plt.title('Mean 30 second Dark Image: CMOS')
plt.show()

#%%
#Science Images

arturus_images = []
sadalsuud_images = []

arturus_files = sorted(glob.glob(r'\Users\liamo\Astronomy\ASTR362\Lab1\arcturus\*.fit'))
for file in arturus_files:
    arturus_images.append(fits.getdata(file))
arturus_images = np.array(arturus_images)
arturus_images = count(arturus_images[0:1])
correct_arturus = (arturus_images - goodavg_10dark - mean_bias) / flats
arturus = np.median(correct_arturus, axis=0)

vmin, vmax = np.percentile(arturus,[1,99])
plt.imshow(arturus, cmap='grey', origin='lower', vmin=vmin, vmax=vmax)
plt.title('Corrected Arturus')
plt.colorbar(label='ADU')
plt.show()

sadalsuud_files = sorted(glob.glob(r'\Users\liamo\Astronomy\ASTR362\Lab1\sadalsuud\*.fit'))
for file in sadalsuud_files:
    sadalsuud_images.append(fits.getdata(file))
sadalsuud_images = np.array(sadalsuud_images)
sadalsuud_images = count(sadalsuud_images[0:1])
correct_sadalsuud = (sadalsuud_images - avg_30dark - mean_bias) / flats
sadalsuud = np.median(correct_sadalsuud, axis = 0)

vmin, vmax = np.percentile(sadalsuud,[1,99])
plt.imshow(sadalsuud, cmap='grey', origin='lower', vmin=vmin, vmax=vmax)
plt.title('Corrected Sadalsuud')
plt.colorbar(label='ADU')
plt.show()
