from numpy import ones, random
import scipy.signal as sg
from matplotlib import pyplot, animation
m0,kernel,fig,im=((random.randint(0,100,[256,256])<30)*1,ones([3,3]),pyplot.figure(),[])
im.append((pyplot.imshow(m0, cmap="gray", interpolation="none"),))
for i in range(0,1000):
    conv=sg.convolve2d(m0,kernel,mode='same',boundary='wrap')
    m0=(m0*((conv>2) * (conv<5)))+(1-m0)*1*(conv==3)
    im.append((pyplot.imshow(m0, cmap="gray", interpolation="none"),))
im_ani = animation.ArtistAnimation(fig, im, interval=50, repeat_delay=0, blit=True)
pyplot.show()
