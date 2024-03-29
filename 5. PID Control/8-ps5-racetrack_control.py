# --------------
# User Instructions
# 
# Define a function cte in the robot class that will
# compute the crosstrack error for a robot on a
# racetrack with a shape as described in the video.
#
# You will need to base your error calculation on
# the robot's location on the track. Remember that 
# the robot will be traveling to the right on the
# upper straight segment and to the left on the lower
# straight segment.
#
# --------------
# Grading Notes
#
# We will be testing your cte function directly by
# calling it with different robot locations and making
# sure that it returns the correct crosstrack error.  
 
from math import *
import random


# ------------------------------------------------
# 
# this is the robot class
#

class robot:

    # --------
    # init: 
    #    creates robot and initializes location/orientation to 0, 0, 0
    #

    def __init__(self, length = 20.0):
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.steering_drift = 0.0

    # --------
    # set: 
    #	sets a robot coordinate
    #

    def set(self, new_x, new_y, new_orientation):

        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation) % (2.0 * pi)


    # --------
    # set_noise: 
    #	sets the noise parameters
    #

    def set_noise(self, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)

    # --------
    # set_steering_drift: 
    #	sets the systematical steering drift parameter
    #

    def set_steering_drift(self, drift):
        self.steering_drift = drift
        
    # --------
    # move: 
    #    steering = front wheel steering angle, limited by max_steering_angle
    #    distance = total distance driven, most be non-negative

    def move(self, steering, distance, 
             tolerance = 0.001, max_steering_angle = pi / 4.0):

        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        if distance < 0.0:
            distance = 0.0


        # make a new copy
        res = robot()
        res.length         = self.length
        res.steering_noise = self.steering_noise
        res.distance_noise = self.distance_noise
        res.steering_drift = self.steering_drift

        # apply noise
        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)

        # apply steering drift
        steering2 += self.steering_drift

        # Execute motion
        turn = tan(steering2) * distance2 / res.length

        if abs(turn) < tolerance:

            # approximate by straight line motion

            res.x = self.x + (distance2 * cos(self.orientation))
            res.y = self.y + (distance2 * sin(self.orientation))
            res.orientation = (self.orientation + turn) % (2.0 * pi)

        else:

            # approximate bicycle model for motion

            radius = distance2 / turn
            cx = self.x - (sin(self.orientation) * radius)
            cy = self.y + (cos(self.orientation) * radius)
            res.orientation = (self.orientation + turn) % (2.0 * pi)
            res.x = cx + (sin(res.orientation) * radius)
            res.y = cy - (cos(res.orientation) * radius)

        return res




    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]'  % (self.x, self.y, self.orientation)


############## ONLY ADD / MODIFY CODE BELOW THIS LINE ####################
   
    def cte(self, radius):
        # 
        #
        # Add code here
        #
        #
        if self.x < radius:
            cte = sqrt((self.x - radius)**2 + (self.y - radius)**2) - radius
        elif self.x > 3.0 * radius:
            cte = sqrt((self.x - 3.0 * radius)**2 + (self.y - radius)**2) - radius
        elif self.y > radius:
            cte = self.y - 2.0 * radius
        else:
            cte = -self.y 
        
        return cte
    
############## ONLY ADD / MODIFY CODE ABOVE THIS LINE ####################




# ------------------------------------------------------------------------
#
# run - does a single control run.


def run(params, radius, printflag = False):
    myrobot = robot()
    myrobot.set(0.0, radius, pi / 2.0)
    speed = 1.0 # motion distance is equal to speed (we assume time = 1)
    err = 0.0
    int_crosstrack_error = 0.0
    N = 200

    crosstrack_error = myrobot.cte(radius) # You need to define the cte function!

    for i in range(N*2):
        diff_crosstrack_error = - crosstrack_error
        crosstrack_error = myrobot.cte(radius)
        diff_crosstrack_error += crosstrack_error
        int_crosstrack_error += crosstrack_error
        steer = - params[0] * crosstrack_error \
                - params[1] * diff_crosstrack_error \
                - params[2] * int_crosstrack_error
        myrobot = myrobot.move(steer, speed)
        if i >= N:
            err += crosstrack_error ** 2
        if printflag:
            print (myrobot, err)
            print("\n")
    return err / float(N)

radius = 25.0
params = [10.0, 15.0, 0]
err = run(params, radius, True)
print '\nFinal parameters: ', params, '\n ->', err

# Output
# ([x=0.00000 y=26.00000 orient=1.57080], 0.0)

# ([x=0.01365 y=26.99988 orient=1.54349], 0.0)

# ([x=0.06592 y=27.99840 orient=1.49349], 0.0)

# ([x=0.16804 y=28.99307 orient=1.44349], 0.0)

# ([x=0.31973 y=29.98139 orient=1.39349], 0.0)

# ([x=0.52064 y=30.96090 orient=1.34349], 0.0)

# ([x=0.77025 y=31.92914 orient=1.29349], 0.0)

# ([x=1.06793 y=32.88369 orient=1.24349], 0.0)

# ([x=1.41296 y=33.82218 orient=1.19349], 0.0)

# ([x=1.80445 y=34.74224 orient=1.14349], 0.0)

# ([x=2.24145 y=35.64159 orient=1.09349], 0.0)

# ([x=2.71993 y=36.51960 orient=1.05016], 0.0)

# ([x=3.22162 y=37.38464 orient=1.04034], 0.0)

# ([x=3.72989 y=38.24584 orient=1.03489], 0.0)

# ([x=4.25610 y=39.09613 orient=0.99837], 0.0)

# ([x=4.81855 y=39.92283 orient=0.94837], 0.0)

# ([x=5.42162 y=40.72039 orient=0.89837], 0.0)

# ([x=6.06380 y=41.48681 orient=0.84837], 0.0)

# ([x=6.74348 y=42.22017 orient=0.79837], 0.0)

# ([x=7.45896 y=42.91865 orient=0.74837], 0.0)

# ([x=8.19955 y=43.59058 orient=0.72529], 0.0)

# ([x=8.95301 y=44.24807 orient=0.70967], 0.0)

# ([x=9.72345 y=44.88548 orient=0.67270], 0.0)

# ([x=10.52084 y=45.48877 orient=0.62270], 0.0)

# ([x=11.34739 y=46.05146 orient=0.57270], 0.0)

# ([x=12.20102 y=46.57213 orient=0.52270], 0.0)

# ([x=13.07810 y=47.05231 orient=0.47911], 0.0)

# ([x=13.97122 y=47.50208 orient=0.45393], 0.0)

# ([x=14.87526 y=47.92947 orient=0.42930], 0.0)

# ([x=15.79372 y=48.32476 orient=0.38354], 0.0)

# ([x=16.73003 y=48.67564 orient=0.33354], 0.0)

# ([x=17.68271 y=48.97928 orient=0.28354], 0.0)

# ([x=18.64733 y=49.24274 orient=0.24969], 0.0)

# ([x=19.61934 y=49.47756 orient=0.22440], 0.0)

# ([x=20.59811 y=49.68224 orient=0.18791], 0.0)

# ([x=21.58477 y=49.84441 orient=0.13791], 0.0)

# ([x=22.57830 y=49.95707 orient=0.08791], 0.0)

# ([x=23.57595 y=50.02443 orient=0.04694], 0.0)

# ([x=24.57538 y=50.05743 orient=0.01906], 0.0)

# ([x=25.57533 y=50.06110 orient=6.27146], 0.0)

# ([x=26.57485 y=50.03183 orient=6.23637], 0.0)

# ([x=27.57389 y=49.98806 orient=6.24243], 0.0)

# ([x=28.57366 y=49.97184 orient=0.00832], 0.0)

# ([x=29.57337 y=49.99463 orient=0.03727], 0.0)

# ([x=30.57291 y=50.02448 orient=0.02245], 0.0)

# ([x=31.57284 y=50.02619 orient=6.26415], 0.0)

# ([x=32.57248 y=49.99976 orient=6.24936], 0.0)

# ([x=33.57219 y=49.97648 orient=6.27043], 0.0)

# ([x=34.57214 y=49.98026 orient=0.02033], 0.0)

# ([x=35.57185 y=50.00413 orient=0.02740], 0.0)

# ([x=36.57169 y=50.02098 orient=0.00631], 0.0)

# ([x=37.57164 y=50.01482 orient=6.26456], 0.0)

# ([x=38.57144 y=49.99480 orient=6.26176], 0.0)

# ([x=39.57135 y=49.98257 orient=6.28015], 0.0)

# ([x=40.57132 y=49.98888 orient=0.01565], 0.0)

# ([x=41.57120 y=50.00453 orient=0.01648], 0.0)

# ([x=42.57115 y=50.01382 orient=0.00210], 0.0)

# ([x=43.57112 y=50.00880 orient=6.27104], 0.0)

# ([x=44.57105 y=49.99665 orient=6.27041], 0.0)

# ([x=45.57102 y=49.98935 orient=6.28136], 0.0)

# ([x=46.57101 y=49.99301 orient=0.00915], 0.0)

# ([x=47.57097 y=50.00216 orient=0.00990], 0.0)

# ([x=48.57095 y=50.00805 orient=0.00188], 0.0)

# ([x=49.57094 y=50.00567 orient=6.27654], 0.0)

# ([x=50.57091 y=49.99851 orient=6.27549], 0.0)

# ([x=51.57090 y=49.99389 orient=6.28164], 0.0)

# ([x=52.57090 y=49.99563 orient=0.00502], 0.0)

# ([x=53.57089 y=50.00064 orient=0.00590], 0.0)

# ([x=54.57088 y=50.00450 orient=0.00181], 0.0)

# ([x=55.57088 y=50.00373 orient=6.27984], 0.0)

# ([x=56.57087 y=49.99973 orient=6.27855], 0.0)

# ([x=57.57086 y=49.99667 orient=6.28168], 0.0)

# ([x=58.57086 y=49.99715 orient=0.00247], 0.0)

# ([x=59.57086 y=50.00015 orient=0.00353], 0.0)

# ([x=60.57086 y=50.00252 orient=0.00120], 0.0)

# ([x=61.57085 y=50.00220 orient=6.28135], 0.0)

# ([x=62.57085 y=50.00037 orient=6.28048], 0.0)

# ([x=63.57085 y=49.99826 orient=6.28168], 0.0)

# ([x=64.57085 y=49.99798 orient=0.00094], 0.0)

# ([x=65.57085 y=49.99953 orient=0.00216], 0.0)

# ([x=66.57085 y=50.00170 orient=0.00123], 0.0)

# ([x=67.57085 y=50.00169 orient=6.28194], 0.0)

# ([x=68.57085 y=50.00045 orient=6.28110], 0.0)

# ([x=69.57084 y=49.99836 orient=6.28181], 0.0)

# ([x=70.57084 y=49.99818 orient=0.00100], 0.0)

# ([x=71.57084 y=49.99971 orient=0.00206], 0.0)

# ([x=72.57084 y=50.00126 orient=0.00105], 0.0)

# ([x=73.57084 y=50.00142 orient=6.28244], 0.0)

# ([x=74.57084 y=50.00067 orient=6.28162], 0.0)

# ([x=75.57084 y=49.99910 orient=6.28184], 0.0)

# ([x=76.57083 y=49.99448 orient=6.27528], 0.0)

# ([x=77.57018 y=49.96158 orient=6.22528], 0.0)

# ([x=78.56664 y=49.87878 orient=6.17528], 0.0)

# ([x=79.55772 y=49.74628 orient=6.12528], 0.0)

# ([x=80.54094 y=49.56441 orient=6.07528], 0.0)

# ([x=81.51384 y=49.33363 orient=6.02528], 0.0)

# ([x=82.47399 y=49.05451 orient=5.97528], 0.0)

# ([x=83.41898 y=48.72776 orient=5.92528], 0.0)

# ([x=84.34647 y=48.35418 orient=5.87528], 0.0)

# ([x=85.25413 y=47.93471 orient=5.82528], 0.0)

# ([x=86.14067 y=47.47226 orient=5.77949], 0.0)

# ([x=87.01382 y=46.98482 orient=5.76855], 0.0)

# ([x=87.88309 y=46.49047 orient=5.76366], 0.0)

# ([x=88.74234 y=45.97903 orient=5.72892], 0.0)

# ([x=89.57912 y=45.43168 orient=5.67892], 0.0)

# ([x=90.38750 y=44.84319 orient=5.62892], 0.0)

# ([x=91.16545 y=44.21503 orient=5.57892], 0.0)

# ([x=91.91104 y=43.54878 orient=5.52892], 0.0)

# ([x=92.62239 y=42.84610 orient=5.47892], 0.0)

# ([x=93.30603 y=42.11631 orient=5.45137], 0.0)

# ([x=93.97320 y=41.37143 orient=5.43425], 0.0)

# ([x=94.62161 y=40.61019 orient=5.40159], 0.0)

# ([x=95.23797 y=39.82286 orient=5.35159], 0.0)

# ([x=95.81421 y=39.00571 orient=5.30159], 0.0)

# ([x=96.34889 y=38.16078 orient=5.25159], 0.0)

# ([x=96.84513 y=37.29267 orient=5.21177], 0.0)

# ([x=97.31295 y=36.40888 orient=5.18670], 0.0)

# ([x=97.75691 y=35.51287 orient=5.15814], 0.0)

# ([x=98.16532 y=34.60018 orient=5.10814], 0.0)

# ([x=98.52759 y=33.66822 orient=5.05814], 0.0)

# ([x=98.84646 y=32.72050 orient=5.01574], 0.0)

# ([x=99.13136 y=31.76198 orient=4.98688], 0.0)

# ([x=99.38779 y=30.79546 orient=4.95656], 0.0)

# ([x=99.60637 y=29.81974 orient=4.90899], 0.0)

# ([x=99.77711 y=28.83453 orient=4.85899], 0.0)

# ([x=99.90263 y=27.84251 orient=4.81751], 0.0)

# ([x=99.99307 y=26.84664 orient=4.78839], 0.0)

# ([x=100.05319 y=25.84849 orient=4.75670], 0.0)

# ([x=100.07322 y=24.84879 orient=4.70813], 0.0)

# ([x=100.04396 y=23.84932 orient=4.65813], 0.0)

# ([x=99.97059 y=22.85208 orient=4.61976], 0.0)

# ([x=99.86404 y=21.85780 orient=4.59151], 0.0)

# ([x=99.72640 y=20.86737 orient=4.55708], 0.0)

# ([x=99.54708 y=19.88369 orient=4.50708], 0.0)

# ([x=99.31882 y=18.91019 orient=4.45708], 0.0)

# ([x=99.04892 y=17.94736 orient=4.42109], 0.0)

# ([x=98.74875 y=16.99351 orient=4.39394], 0.0)

# ([x=98.41857 y=16.04965 orient=4.35781], 0.0)

# ([x=98.04808 y=15.12092 orient=4.30781], 0.0)

# ([x=97.63164 y=14.21188 orient=4.25781], 0.0)

# ([x=97.17581 y=13.32187 orient=4.22032], 0.0)

# ([x=96.69139 y=12.44708 orient=4.19301], 0.0)

# ([x=96.18024 y=11.58764 orient=4.15867], 0.0)

# ([x=95.63335 y=10.75056 orient=4.10867], 0.0)

# ([x=95.04531 y=9.94186 orient=4.05867], 0.0)

# ([x=94.42236 y=9.15967 orient=4.02101], 0.0)

# ([x=93.77424 y=8.39817 orient=3.99349], 0.0)

# ([x=93.10288 y=7.65711 orient=3.95910], 0.0)

# ([x=92.40089 y=6.94506 orient=3.90910], 0.0)

# ([x=91.66420 y=6.26900 orient=3.85910], 0.0)

# ([x=90.89867 y=5.62568 orient=3.82183], 0.0)

# ([x=90.11272 y=5.00745 orient=3.79439], 0.0)

# ([x=89.30793 y=4.41397 orient=3.75961], 0.0)

# ([x=88.47875 y=3.85516 orient=3.70961], 0.0)

# ([x=87.62269 y=3.33850 orient=3.65961], 0.0)

# ([x=86.74484 y=2.85967 orient=3.62227], 0.0)

# ([x=85.85194 y=2.40950 orient=3.59487], 0.0)

# ([x=84.94551 y=1.98726 orient=3.56019], 0.0)

# ([x=84.02207 y=1.60378 orient=3.51019], 0.0)

# ([x=83.08062 y=1.26693 orient=3.46019], 0.0)

# ([x=82.12531 y=0.97153 orient=3.42278], 0.0)

# ([x=81.16090 y=0.70724 orient=3.39535], 0.0)

# ([x=80.18878 y=0.47300 orient=3.36074], 0.0)

# ([x=79.20767 y=0.28008 orient=3.31074], 0.0)

# ([x=78.21814 y=0.13645 orient=3.26074], 0.0)

# ([x=77.22324 y=0.03616 orient=3.22337], 0.0)

# ([x=76.22559 y=-0.03184 orient=3.19593], 0.0)

# ([x=75.22632 y=-0.06885 orient=3.16128], 0.0)

# ([x=74.22644 y=-0.06354 orient=3.11128], 0.0)

# ([x=73.22750 y=-0.01824 orient=3.08128], 0.0)

# ([x=72.22863 y=0.02849 orient=3.10840], 0.0)

# ([x=71.22876 y=0.03668 orient=3.15840], 0.0)

# ([x=70.22925 y=0.00655 orient=3.18505], 0.0)

# ([x=69.22982 y=-0.02673 orient=3.16471], 0.0)

# ([x=68.22992 y=-0.02577 orient=3.11657], 0.0)

# ([x=67.23041 y=0.00545 orient=3.10415], 0.0)

# ([x=66.23071 y=0.02848 orient=3.13298], 0.0)

# ([x=65.23081 y=0.01886 orient=3.16945], 0.0)

# ([x=64.23123 y=-0.01010 orient=3.17166], 0.0)

# ([x=63.23138 y=-0.02534 orient=3.14201], 0.0)

# ([x=62.23149 y=-0.01268 orient=3.11585], 0.0)

# ([x=61.23179 y=0.01148 orient=3.11901], 0.0)

# ([x=60.23186 y=0.02114 orient=3.14487], 0.0)

# ([x=59.23195 y=0.00856 orient=3.16347], 0.0)

# ([x=58.23214 y=-0.01073 orient=3.15830], 0.0)

# ([x=57.23218 y=-0.01696 orient=3.13736], 0.0)

# ([x=56.23225 y=-0.00599 orient=3.12389], 0.0)

# ([x=55.23236 y=0.00909 orient=3.12914], 0.0)

# ([x=54.23238 y=0.01334 orient=3.14554], 0.0)

# ([x=53.23243 y=0.00439 orient=3.15553], 0.0)

# ([x=52.23249 y=-0.00728 orient=3.15101], 0.0)

# ([x=51.23251 y=-0.01037 orient=3.13835], 0.0)

# ([x=50.23253 y=-0.00335 orient=3.13079], 0.0)

# ([x=49.23257 y=0.00565 orient=3.13439], 0.0)

# ([x=48.23258 y=0.00801 orient=3.14409], 0.0)

# ([x=47.23260 y=0.00261 orient=3.14988], 0.0)

# ([x=46.23262 y=-0.00430 orient=3.14714], 0.0)

# ([x=45.23262 y=-0.00616 orient=3.13975], 0.0)

# ([x=44.23263 y=-0.00207 orient=3.13527], 0.0)

# ([x=43.23265 y=0.00324 orient=3.13730], 0.0)

# ([x=42.23265 y=0.00472 orient=3.14292], 1.0486837812317707e-05)

# ([x=41.23266 y=0.00165 orient=3.14640], 3.2775423918383636e-05)

# ([x=40.23266 y=-0.00242 orient=3.14492], 3.550525756790233e-05)

# ([x=39.23267 y=-0.00361 orient=3.14065], 4.135075138960567e-05)

# ([x=38.23267 y=-0.00132 orient=3.13795], 5.441098102154092e-05)

# ([x=37.23267 y=0.00180 orient=3.13901], 5.61556251685002e-05)

# ([x=36.23267 y=0.00276 orient=3.14225], 5.9380459334086355e-05)

# ([x=35.23268 y=0.00106 orient=3.14435], 6.70130616954712e-05)

# ([x=34.23268 y=-0.00171 orient=3.14360], 6.812778611799949e-05)

# ([x=33.23268 y=-0.00225 orient=3.14067], 7.103483492641719e-05)

# ([x=32.23268 y=-0.00057 orient=3.13914], 7.60985091777005e-05)

# ([x=31.23268 y=0.00189 orient=3.14012], 7.6417752425348e-05)

# ([x=30.23269 y=0.00197 orient=3.14291], 7.998042141214664e-05)

# ([x=29.23269 y=0.00013 orient=3.14395], 8.384347061319593e-05)

# ([x=28.23269 y=-0.00157 orient=3.14264], 8.386030302634878e-05)

# ([x=27.23269 y=-0.00158 orient=3.14058], 8.632692729204636e-05)

# ([x=26.23269 y=-0.00057 orient=3.13977], 8.883565819121282e-05)

# ([x=25.23269 y=0.00125 orient=3.14025], 8.915648610262758e-05)

# ([x=24.23269 y=0.00160 orient=3.14225], 9.0726725190792e-05)

# ([x=23.23272 y=0.00795 orient=3.12823], 0.00019429133922618325)

# ([x=22.23356 y=0.04629 orient=3.07823], 0.0031599883320024454)

# ([x=21.23756 y=0.13453 orient=3.02823], 0.01452039848682739)

# ([x=20.24722 y=0.27243 orient=2.97823], 0.03657584208908553)

# ([x=19.26501 y=0.45966 orient=2.92823], 0.06904109984162016)

# ([x=18.29339 y=0.69574 orient=2.87823], 0.10966597261317387)

# ([x=17.33477 y=0.98009 orient=2.82823], 0.1548683046632025)

# ([x=16.39157 y=1.31200 orient=2.77823], 0.20037541441968787)

# ([x=15.46614 y=1.69063 orient=2.72823], 0.2418698711786638)

# ([x=14.56078 y=2.11503 orient=2.67823], 0.27563555313908733)

# ([x=13.67777 y=2.58416 orient=2.62823], 0.29919992199525336)

# ([x=12.81386 y=3.08774 orient=2.59945], 0.3119684518819643)

# ([x=11.95891 y=3.60644 orient=2.59306], 0.317280128185806)

# ([x=11.10943 y=4.13405 orient=2.57855], 0.3203083914481547)

# ([x=10.27749 y=4.68873 orient=2.52855], 0.32474794422744413)

# ([x=9.47431 y=5.28429 orient=2.47855], 0.3321195034184527)

# ([x=8.70190 y=5.91925 orient=2.42855], 0.341134399603943)

# ([x=7.96219 y=6.59202 orient=2.37855], 0.349948856408025)

# ([x=7.25300 y=7.29696 orient=2.33986], 0.3567839698301363)

# ([x=6.56594 y=8.02352 orient=2.31666], 0.361270677125474)

# ([x=5.89748 y=8.76723 orient=2.28927], 0.3648986147384382)

# ([x=5.25833 y=9.53618 orient=2.23927], 0.3695348773635213)

# ([x=4.65842 y=10.33611 orient=2.18927], 0.3754861598036684)

# ([x=4.09760 y=11.16395 orient=2.14318], 0.3812738397470125)

# ([x=3.56835 y=12.01237 orient=2.11389], 0.3857417023187717)

# ([x=3.06312 y=12.87531 orient=2.08706], 0.38931868013536847)

# ([x=2.58864 y=13.75549 orient=2.04336], 0.3934936730997588)

# ([x=2.15592 y=14.65690 orient=1.99336], 0.39897694000932143)

# ([x=1.76879 y=15.57882 orient=1.94336], 0.40483180094799254)

# ([x=1.41990 y=16.51593 orient=1.91104], 0.4095740480429362)

# ([x=1.09806 y=17.46270 orient=1.88592], 0.4131667444091981)

# ([x=0.80649 y=18.41918 orient=1.84745], 0.41703528104673115)

# ([x=0.55751 y=19.38759 orient=1.79745], 0.4223000354568562)

# ([x=0.35725 y=20.36722 orient=1.74745], 0.42847262976406025)

# ([x=0.20157 y=21.35496 orient=1.70679], 0.4340152617129756)

# ([x=0.07972 y=22.34748 orient=1.67912], 0.4382250439074354)

# ([x=-0.01304 y=23.34313 orient=1.64826], 0.44195213101259334)

# ([x=-0.06571 y=24.34164 orient=1.59874], 0.44655643180644466)

# ([x=-0.06865 y=25.34153 orient=1.54874], 0.45208535435200836)

# ([x=-0.02724 y=26.34061 orient=1.51000], 0.4571232726031999)

# ([x=0.04757 y=27.33777 orient=1.48182], 0.4611073388847776)

# ([x=0.15330 y=28.33212 orient=1.44793], 0.46491403790781743)

# ([x=0.30061 y=29.32110 orient=1.39793], 0.46969428930094503)

# ([x=0.49717 y=30.30149 orient=1.34793], 0.4752481190288634)

# ([x=0.73581 y=31.27254 orient=1.31171], 0.4801188862152565)

# ([x=1.00515 y=32.23555 orient=1.28446], 0.48394254944351817)

# ([x=1.30478 y=33.18955 orient=1.24849], 0.4877920225409212)

# ([x=1.64511 y=34.12975 orient=1.19849], 0.49276829102808567)

# ([x=2.03201 y=35.05176 orient=1.14849], 0.4985359441123954)

# ([x=2.45881 y=35.95604 orient=1.11115], 0.5036092869888709)

# ([x=2.91462 y=36.84608 orient=1.08385], 0.5075434745673262)

# ([x=3.39770 y=37.72160 orient=1.04934], 0.5113624324486311)

# ([x=3.91731 y=38.57588 orient=0.99934], 0.5162443675605002)

# ([x=4.47896 y=39.40313 orient=0.94934], 0.5219562872521568)

# ([x=5.07634 y=40.20501 orient=0.91169], 0.527020625271313)

# ([x=5.69954 y=40.98703 orient=0.88419], 0.5309658320091147)

# ([x=6.34663 y=41.74939 orient=0.84981], 0.5347826629170169)

# ([x=7.02525 y=42.48373 orient=0.79981], 0.5396422784963871)

# ([x=7.73973 y=43.18325 orient=0.74981], 0.5453182922595353)

# ([x=8.48409 y=43.85094 orient=0.71250], 0.550337817374838)

# ([x=9.24969 y=44.49420 orient=0.68506], 0.5542549324865851)

# ([x=10.03491 y=45.11334 orient=0.65031], 0.5580797752328706)

# ([x=10.84561 y=45.69863 orient=0.60031], 0.5629669977580667)

# ([x=11.68454 y=46.24266 orient=0.55031], 0.5686650851211407)

# ([x=12.54647 y=46.74959 orient=0.51298], 0.5736980440548677)

# ([x=13.42437 y=47.22836 orient=0.48557], 0.5776196946626576)

# ([x=14.31669 y=47.67965 orient=0.45089], 0.5814430100063317)

# ([x=15.22727 y=48.09274 orient=0.40089], 0.5863284752388904)

# ([x=16.15735 y=48.45980 orient=0.35089], 0.5920293998510024)

# ([x=17.10263 y=48.78589 orient=0.31349], 0.5970694728211158)

# ([x=18.05800 y=49.08119 orient=0.28606], 0.6009965789946721)

# ([x=19.02206 y=49.34670 orient=0.25144], 0.604818423860306)

# ([x=19.99643 y=49.57119 orient=0.20144], 0.6096978683231242)

# ([x=20.98080 y=49.74670 orient=0.15144], 0.6153928996826336)

# ([x=21.97194 y=49.87905 orient=0.11406], 0.6204280146699225)

# ([x=22.96688 y=49.97922 orient=0.08663], 0.624352671026874)

# ([x=23.96443 y=50.04847 orient=0.05198], 0.6281752493392558)

# ([x=24.96396 y=50.07545 orient=0.00198], 0.633056639545544)

# ([x=25.96359 y=50.05243 orient=6.23517], 0.6387525113238088)

# ([x=26.96221 y=49.99992 orient=6.22613], 0.6415015448325846)

# ([x=27.96159 y=49.96788 orient=6.27613], 0.6415015510443942)

# ([x=28.96133 y=49.98583 orient=0.04295], 0.6425332740897846)

# ([x=29.96054 y=50.02556 orient=0.03654], 0.6427341688548053)

# ([x=30.96036 y=50.03710 orient=6.26973], 0.6433875501695702)

# ([x=31.95992 y=50.00852 orient=6.23947], 0.6447640717914792)

# ([x=32.95930 y=49.97376 orient=6.25736], 0.6448366980545158)

# ([x=33.95920 y=49.97285 orient=0.02401], 0.6455252190650335)

# ([x=34.95870 y=50.00419 orient=0.03867], 0.6462621407582032)

# ([x=35.95836 y=50.02881 orient=0.01057], 0.6462796889428699)

# ([x=36.95826 y=50.02008 orient=6.25517], 0.6471094471179465)

# ([x=37.95782 y=49.99032 orient=6.25166], 0.6475128171886927)

# ([x=38.95764 y=49.97389 orient=6.28186], 0.647606553185986)

# ([x=39.95753 y=49.98647 orient=0.02647], 0.6482880595457439)

# ([x=40.95722 y=50.01160 orient=0.02381], 0.6484712336260136)

# ([x=41.95713 y=50.02198 orient=6.28013], 0.6486058549851995)

# ([x=42.95703 y=50.00907 orient=6.26042], 0.6490887937877838)

# ([x=43.95683 y=49.98889 orient=6.26559], 0.6491709761195202)

# ([x=44.95679 y=49.98227 orient=0.00436], 0.6492944289674548)

# ([x=45.95671 y=49.99373 orient=0.01855], 0.6496086670031416)

# ([x=46.95659 y=50.00954 orient=0.01307], 0.6496479948140448)

# ([x=47.95656 y=50.01398 orient=6.27899], 0.6497389965253867)

# ([x=48.95652 y=50.00455 orient=6.26852], 0.649934361141639)

# ([x=49.95644 y=49.99229 orient=6.27334], 0.6499550438159617)

# ([x=50.95643 y=49.98912 orient=0.00350], 0.6500144571292479)

# ([x=51.95640 y=49.99656 orient=0.01139], 0.6501328865324547)

# ([x=52.95635 y=50.00601 orient=0.00752], 0.6501447116378872)

# ([x=53.95634 y=50.00841 orient=6.28047], 0.6501808637965516)

# ([x=54.95633 y=50.00268 orient=6.27443], 0.6502516168830684)

# ([x=55.95630 y=49.99541 orient=6.27740], 0.6502587791254458)

# ([x=56.95629 y=49.99353 orient=0.00203], 0.6502798705167535)

# ([x=57.95628 y=49.99788 orient=0.00668], 0.6503217669159412)

# ([x=58.95627 y=50.00346 orient=0.00448], 0.6503262518541687)

# ([x=59.95627 y=50.00497 orient=6.28172], 0.6503382426890645)

# ([x=60.95626 y=50.00169 orient=6.27810], 0.650362910536933)

# ([x=61.95625 y=49.99741 orient=6.27971], 0.6503657650070277)

# ([x=62.95625 y=49.99620 orient=0.00104], 0.6503724708994111)

# ([x=63.95625 y=49.99865 orient=0.00386], 0.65038693887493)

# ([x=64.95624 y=50.00193 orient=0.00270], 0.6503887665916835)

# ([x=65.95624 y=50.00291 orient=6.28245], 0.6503924759957501)

# ([x=66.95624 y=50.00108 orient=6.28026], 0.6504009381807457)

# ([x=67.95623 y=49.99816 orient=6.28109], 0.650402108961175)

# ([x=68.95623 y=49.99762 orient=0.00102], 0.6504055000933624)

# ([x=69.95623 y=49.99944 orient=0.00261], 0.6504111504140395)

# ([x=70.95623 y=50.00151 orient=0.00153], 0.6504114623480122)

# ([x=71.95623 y=50.00189 orient=6.28240], 0.6504137514191461)

# ([x=72.95623 y=50.00049 orient=6.28118], 0.6504173090653742)

# ([x=73.95623 y=49.99849 orient=6.28198], 0.650417551023212)

# ([x=74.95623 y=49.99841 orient=0.00106], 0.6504198432319583)

# ([x=75.95622 y=49.99947 orient=0.00191], 0.6504223668364127)

# ([x=76.95614 y=49.98875 orient=6.25985], 0.6507374056177466)

# ([x=77.95487 y=49.94044 orient=6.20985], 0.6549885348337712)

# ([x=78.94993 y=49.84227 orient=6.15985], 0.6681839710051517)

# ([x=79.93885 y=49.69449 orient=6.10985], 0.6920019770812799)

# ([x=80.91914 y=49.49747 orient=6.05985], 0.7256847158759844)

# ([x=81.88836 y=49.25170 orient=6.00985], 0.7666615706536676)

# ([x=82.84409 y=48.95780 orient=5.95985], 0.8111839533697667)

# ([x=83.78393 y=48.61650 orient=5.90985], 0.8549675451116431)

# ([x=84.70554 y=48.22866 orient=5.85985], 0.8938379082265532)

# ([x=85.60662 y=47.79523 orient=5.80985], 0.9243754073251177)

# ([x=86.48491 y=47.31732 orient=5.75985], 0.9445553768199392)

# ([x=87.34650 y=46.80974 orient=5.74176], 0.9543794758980303)

# ([x=88.20268 y=46.29306 orient=5.73868], 0.9582153673044516)

# ([x=89.05217 y=45.76550 orient=5.71623], 0.9611358687432694)

# ([x=89.88193 y=45.20757 orient=5.66623], 0.9665066963389629)

# ([x=90.68278 y=44.60887 orient=5.61623], 0.9757565129397255)

# ([x=91.45269 y=43.97089 orient=5.56623], 0.9876177030680843)

# ([x=92.18976 y=43.29523 orient=5.51623], 1.000043027418926)

# ([x=92.89214 y=42.58357 orient=5.46623], 1.010828311551177)

# ([x=93.56415 y=41.84309 orient=5.43246], 1.0182361372589814)

# ([x=94.21636 y=41.08507 orient=5.41333], 1.0226263469756016)

# ([x=94.85070 y=40.31206 orient=5.38580], 1.026212906262169)

# ([x=95.45455 y=39.51510 orient=5.33580], 1.0311250779317276)

# ([x=96.01783 y=38.68895 orient=5.28580], 1.037751867057514)

# ([x=96.53911 y=37.83569 orient=5.23580], 1.0445736325437804)

# ([x=97.02396 y=36.96115 orient=5.20142], 1.0499982519703452)

# ([x=97.48288 y=36.07270 orient=5.17695], 1.0538918839628977)

# ([x=97.91538 y=35.17112 orient=5.14241], 1.0576883100347714)

# ([x=98.30938 y=34.25213 orient=5.09241], 1.0627617924919548)

# ([x=98.65696 y=33.31459 orient=5.04241], 1.0689179557617923)

# ([x=98.96051 y=32.36185 orient=4.99924], 1.074628770488686)

# ([x=99.22981 y=31.39883 orient=4.97089], 1.078980590866292)

# ([x=99.47148 y=30.42851 orient=4.94207], 1.0826407376457903)

# ([x=99.67633 y=29.44981 orient=4.89538], 1.0870428981828648)

# ([x=99.83364 y=28.46236 orient=4.84538], 1.092567983517142)

# ([x=99.94397 y=27.46855 orient=4.80052], 1.098021454211727)

# ([x=100.01712 y=26.47127 orient=4.77070], 1.1023535610207194)

# ([x=100.06106 y=25.47227 orient=4.74198], 1.1059951203458782)

# ([x=100.06816 y=24.47238 orient=4.69701], 1.1102860543994288)

# ([x=100.02781 y=23.47330 orient=4.64701], 1.1157201397368957)

# ([x=99.93915 y=22.47733 orient=4.60021], 1.121244584705171)

# ([x=99.81215 y=21.48546 orient=4.56986], 1.1256556481428257)

# ([x=99.65662 y=20.49766 orient=4.54259], 1.129234190062467)

# ([x=99.46649 y=19.51598 orient=4.49955], 1.1333713738659839)

# ([x=99.23092 y=18.54423 orient=4.44955], 1.1387828385892536)

# ([x=98.94707 y=17.58547 orient=4.39955], 1.14458439112191)

# ([x=98.62399 y=16.63914 orient=4.36724], 1.1492975825834686)

# ([x=98.27383 y=15.70248 orient=4.34203], 1.1528817188304925)

# ([x=97.89398 y=14.77750 orient=4.30342], 1.1567535902902577)

# ([x=97.47355 y=13.87029 orient=4.25342], 1.1620201249363946)

# ([x=97.00830 y=12.98523 orient=4.20342], 1.168181461308887)

# ([x=96.50351 y=12.12207 orient=4.16299], 1.1737009625558814)

# Final parameters: [10.0, 15.0, 0] -> 0.00586850481278
