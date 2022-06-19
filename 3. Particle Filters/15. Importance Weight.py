# Now we want to give weight to our 
# particles. This program will print a
# list of 1000 particle weights.
#
# Don't modify the code below. Please enter
# your code at the bottom.

from math import *
import random


landmarks  = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]
world_size = 100.0


class robot:
    def __init__(self):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0;
        self.turn_noise    = 0.0;
        self.sense_noise   = 0.0;
    
    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_size:
            raise ValueError, 'X coordinate out of bound'
        if new_y < 0 or new_y >= world_size:
            raise ValueError, 'Y coordinate out of bound'
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)
    
    
    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise);
        self.turn_noise    = float(new_t_noise);
        self.sense_noise   = float(new_s_noise);
    
    
    def sense(self):
        Z = []
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            Z.append(dist)
        return Z
    
    
    def move(self, turn, forward):
        if forward < 0:
            raise ValueError, 'Robot cant move backwards'         
        
        # turn, and add randomness to the turning command
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi
        
        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= world_size    # cyclic truncate
        y %= world_size
        
        # set particle
        res = robot()
        res.set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res
    
    def Gaussian(self, mu, sigma, x):
        
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))
    
    
    def measurement_prob(self, measurement):
        
        # calculates how likely a measurement should be
        
        prob = 1.0;
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        return prob
     
    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))


#myrobot = robot()
#myrobot.set_noise(5.0, 0.1, 5.0)
#myrobot.set(30.0, 50.0, pi/2)
#myrobot = myrobot.move(-pi/2, 15.0)
#print myrobot.sense()
#myrobot = myrobot.move(-pi/2, 10.0)
#print myrobot.sense()

####   DON'T MODIFY ANYTHING ABOVE HERE! ENTER CODE BELOW ####
myrobot = robot()
myrobot = myrobot.move(0.1, 5.0)
Z = myrobot.sense()

N = 1000
p = []
for i in range(N):
    x = robot()
    x.set_noise(0.05, 0.05, 5.0)
    p.append(x)

p2 = []
for i in range(N):
    p2.append(p[i].move(0.1, 5.0))
p = p2

w = []
#insert code here!
for i in range(N):
    w.append(p[i].measurement_prob(Z))
print w #Please print w for grading purposes.

# [1.3515543363201301e-33, 1.8376971060741744e-82, 6.090380035994246e-39, 1.564360347620989e-13, 4.439135026593705e-59, 1.5845431912469415e-67, 3.098965432895949e-08, 1.066003073622096e-76, 1.028750932635733e-65, 3.244514456922188e-92, 6.679501382578101e-33, 4.144461883061309e-40, 3.0774278562452356e-73, 5.058795120391478e-100, 1.2579923153696177e-12, 1.0000409701146925e-84, 4.1317787150235286e-20, 1.783624133463827e-21, 6.182240015346003e-40, 4.808038962594903e-54, 1.3405451178734102e-56, 8.285910669219975e-39, 7.134369799777452e-43, 1.5050825939579304e-23, 8.630609379842405e-55, 6.563818479824493e-18, 9.353180702208988e-18, 2.909850578595825e-42, 2.8386517543401244e-34, 2.7759312660653056e-82, 1.7891158535933513e-14, 2.3379894867602673e-94, 3.3975213114698137e-34, 2.118798577680217e-18, 1.625474433281064e-23, 6.820344681265698e-22, 1.4733128817757503e-56, 8.192375894938434e-18, 5.617324181337545e-12, 2.0255398088385195e-44, 3.3258359107733245e-08, 1.5250726033693801e-68, 2.579241407418635e-05, 6.69105851336821e-95, 1.2764233170125216e-39, 5.934934184285257e-18, 9.159109169877456e-18, 4.554823068737197e-71, 6.812010607410986e-44, 3.1419381170810287e-31, 6.414166173998387e-49, 1.9680548278072216e-46, 3.1422236066880657e-17, 4.369804708390837e-48, 1.292137669222372e-35, 2.202191759200434e-80, 4.2313646618596e-23, 3.048432234255649e-28, 3.218713064024595e-35, 1.401240475170503e-55, 2.1870780315836126e-11, 3.804694391304759e-15, 1.6637271953192717e-11, 4.4642779595518806e-39, 3.4674341176637366e-12, 2.6962588133685168e-17, 6.598359237061665e-58, 6.734325401320967e-38, 3.8504368623704224e-19, 6.980718300734927e-30, 8.674398423356972e-22, 6.147650878287446e-52, 2.1274779522714954e-61, 1.2615325222813451e-11, 7.229188578903133e-06, 1.0905868530496646e-66, 5.781332556445454e-49, 9.285994186102482e-83, 4.965074055409438e-35, 4.1805314002084963e-44, 4.2941658411501895e-68, 5.0757217280346784e-11, 3.1589978217088953e-27, 1.6087919213525746e-47, 1.3004866591917634e-102, 2.003629752391136e-12, 2.8345849546738515e-29, 1.1020070812974149e-11, 3.612122837252247e-49, 1.76857773507884e-80, 1.5540688455833613e-63, 1.7819931314580865e-59, 1.235172162193853e-07, 5.2644041039386325e-67, 1.0762341824836443e-72, 4.277169243359683e-98, 1.1669658063842253e-14, 1.3889304304453077e-50, 2.274763365947601e-81, 1.0448498012710055e-61, 7.835652030859505e-86, 4.121153366515769e-46, 9.369148507532846e-21, 4.88861968374113e-06, 4.911696223625839e-37, 3.472965950087888e-30, 1.5898477425564095e-13, 1.2796491017844807e-34, 1.1439492502186068e-60, 1.5583307533627248e-20, 3.7088119174357615e-93, 1.1570137721858641e-08, 7.802482881669483e-49, 2.1545111433885737e-76, 9.905209147559461e-22, 5.29216892445493e-07, 7.601262980494319e-98, 1.6522953125332104e-66, 7.754521271382396e-53, 2.918477826243871e-42, 4.748468583879937e-42, 6.67299236826753e-48, 1.093097035895126e-44, 1.356604726650972e-91, 6.79847510190744e-36, 5.115513607851815e-19, 1.4904765754817267e-05, 1.348098267828591e-59, 3.872377708342773e-08, 3.1771575924888203e-16, 4.066796232688708e-11, 3.4458768352615293e-22, 1.365596618298265e-13, 5.996621206532372e-41, 3.809748011316452e-46, 1.3663198345924704e-48, 3.9416906223826133e-22, 3.825604197514525e-27, 9.183069592939884e-09, 3.097308013302427e-19, 2.6732203521660106e-20, 2.539258907118722e-77, 4.306874160328335e-37, 4.340455330116221e-29, 9.705958961907031e-69, 1.4996239044963941e-30, 1.4894653736621784e-11, 6.217087094900969e-25, 7.977943822287874e-20, 2.3029370839158749e-69, 1.5738645691780345e-05, 1.1076872966030935e-29, 2.483322518635638e-20, 1.045737091974687e-56, 1.3057216813559931e-23, 3.2620966392702083e-15, 7.041556980574824e-57, 8.096196874212488e-21, 2.430770034607875e-81, 6.931306018041519e-20, 2.0171511370149245e-14, 8.158450327570612e-67, 7.487541170488175e-31, 6.959054371099162e-17, 2.349785755904575e-30, 1.6797420412073005e-17, 3.330840332934377e-14, 6.931941943865552e-26, 6.231643843373797e-17, 8.239174426258836e-41, 4.0877120322561025e-77, 3.8059585056038083e-13, 1.6906151772610488e-06, 1.9323060904713404e-06, 1.959763723236092e-46, 9.384511545541975e-73, 3.142203414023581e-77, 3.202511456732155e-05, 5.772027910912998e-68, 6.896653912442146e-63, 1.9063942141055e-36, 4.432726377086759e-57, 7.004757394579903e-11, 8.542818665012001e-60, 2.5854556937191297e-54, 2.264676937985438e-83, 1.0744941340683575e-86, 6.0110217472144164e-74, 1.3230200209314092e-65, 1.783840774846891e-96, 2.360736205417294e-40, 6.209887060201697e-70, 4.61694813116393e-74, 2.8227864179300383e-77, 2.1813195655272938e-54, 9.261593141520837e-44, 2.6619487585877004e-77, 3.6622873072827423e-37, 8.5420552826273e-69, 2.121689686589503e-79, 1.8938576475939995e-45, 1.6645600307408097e-35, 8.951026137342941e-27, 2.3603835172666163e-63, 3.8004396633533276e-06, 5.454142490661546e-24, 4.4730192853818144e-27, 2.9223196617377577e-67, 3.953023808570068e-21, 2.437683772771045e-39, 1.9260078903188396e-42, 2.1283261008057236e-47, 1.5611191987158063e-06, 3.942678021577106e-24, 2.2208530912414108e-41, 3.764446988701152e-55, 2.0284051511607281e-53, 9.86233927816832e-20, 1.0078827533656703e-07, 8.57611453992394e-62, 5.595307093928304e-29, 2.1061574436475977e-11, 1.0962681036719107e-79, 2.0263296277233254e-41, 4.020408033587568e-47, 1.9463357483102678e-46, 9.796014909693832e-17, 1.6598186813080644e-17, 9.42720498987887e-77, 3.993466979176079e-28, 3.6033218648844656e-69, 2.0520123638802382e-38, 4.663072990345224e-29, 6.38778551323046e-45, 1.7365637335858941e-15, 6.616884822457365e-23, 8.054044838693214e-99, 1.415004911721478e-54, 1.2376457982863275e-24, 6.57950092194064e-20, 4.480333328673062e-103, 1.690304874034853e-14, 1.1545336469323215e-81, 6.060053371062541e-90, 1.2735026197244669e-57, 3.4222734048651217e-71, 2.5888636463077874e-71, 7.40133807951812e-28, 2.9688835785193057e-23, 4.286367673998596e-56, 2.3253395170147123e-69, 5.229250070390874e-38, 2.930417279040876e-21, 1.1034715048169717e-13, 3.3546735486197773e-80, 6.141414027486007e-106, 3.3213988323791414e-12, 1.07940758826574e-25, 7.829687979621783e-09, 2.731957279428134e-34, 7.600422219405335e-48, 7.381525154517047e-46, 4.4911587532873707e-42, 1.6450130609842172e-22, 7.845989241234828e-38, 2.19620484470187e-46, 4.955315923814761e-28, 3.254751361015872e-19, 1.682277286055688e-62, 1.1068388634690903e-55, 7.731344856975225e-15, 5.4985332892398835e-46, 9.245049727075526e-23, 4.105024061516594e-18, 7.254845189608773e-16, 7.795760642262484e-13, 1.244865941714351e-24, 7.087483833113845e-13, 3.9669146699012796e-21, 4.0475911616215985e-65, 1.7554308134090904e-47, 1.3127774064962657e-38, 2.552284425400901e-11, 1.1496992635218264e-52, 6.455364161493871e-57, 6.046859613515125e-16, 1.3173171283587115e-16, 7.90193100674009e-40, 1.2763700876715828e-39, 5.0209166609638194e-12, 4.1716658857569e-11, 3.307936880551227e-07, 1.5364167784209924e-68, 1.7949227267791697e-23, 5.2981946585129424e-14, 6.985218093853536e-63, 6.268764149849274e-23, 1.2587288109833483e-49, 1.0793450959082055e-11, 6.253391421742922e-40, 1.703436838395928e-75, 3.5813152518918837e-54, 2.289507161575766e-23, 3.48983966450211e-41, 7.601732118340432e-25, 6.207947336304929e-11, 6.366380091590203e-22, 6.031800620399193e-17, 1.1423912335130771e-23, 2.238968452118248e-80, 4.1814407194259964e-45, 1.8652251064242698e-41, 1.6989419109233476e-12, 1.3608616310707631e-10, 3.597256735957805e-33, 4.296562531786445e-34, 1.63482481892233e-52, 1.335773655358882e-65, 3.0365699767716865e-15, 4.2631030076119515e-49, 8.156242700174345e-37, 4.284139202700865e-31, 3.5323022457087026e-51, 7.045559694797427e-47, 1.0530759190045294e-33, 2.461170458716201e-97, 4.432364960286993e-44, 3.4700230246858315e-55, 2.2598256839350441e-35, 2.5988248734258373e-54, 4.224980962707613e-74, 9.206227866482369e-41, 5.7016420904769626e-40, 5.2410669990576736e-48, 1.4810183494640392e-42, 7.506375701492119e-82, 1.9286897994806166e-43, 3.5894022052594626e-40, 4.0066513050463817e-84, 5.956800835340161e-45, 2.543186493888726e-23, 1.5465862443206764e-64, 1.673408793685248e-20, 2.8524084925146177e-41, 2.521655139162552e-12, 2.08703156156001e-11, 1.8313274466321265e-16, 1.6544909363612416e-48, 3.2510618471764584e-44, 3.438836122700288e-17, 1.7369201744324967e-39, 2.289139430144464e-33, 2.526994393322936e-13, 2.838287882373688e-38, 3.5418159940162213e-34, 3.599262862483148e-17, 1.3545491998375895e-12, 3.2319959822944644e-67, 1.9611702751613788e-43, 2.2751087066175543e-33, 6.703455041701092e-74, 1.8011924473483438e-64, 2.935892990973567e-32, 1.5175881743874328e-70, 1.1271119098453292e-21, 4.07037791685366e-24, 2.140198212136444e-07, 1.502223609867885e-27, 7.719802791318949e-07, 1.1668673711765573e-81, 2.733276371748639e-72, 2.2872289317521923e-35, 2.2434007694952555e-65, 1.1633356759828618e-48, 1.739786656213655e-47, 1.9316312406562502e-49, 9.58581809438692e-35, 2.6229232288037746e-11, 6.54438906882927e-32, 7.867126822261034e-18, 4.4168821671467245e-72, 4.4233004124347365e-07, 5.254573336798728e-17, 4.139433596070613e-06, 2.0758343945520027e-20, 1.1355974498500656e-63, 4.1358295531239115e-07, 1.2793791027184551e-52, 6.824356032522135e-11, 3.3629721013050594e-20, 3.7652744488219605e-18, 4.481687433420969e-82, 1.3025483511097392e-09, 2.190346051021684e-58, 1.1078991795246494e-20, 5.564367408130099e-95, 1.2319066976043679e-12, 4.860465814568134e-64, 4.163100965464443e-22, 2.46053774851208e-59, 1.65122638320455e-05, 5.876610134075641e-26, 7.142787291034444e-63, 1.728998631619087e-55, 1.729744412456019e-14, 5.266228881582091e-49, 1.6993980725018024e-25, 1.7397624540968327e-86, 2.988115066570484e-47, 7.683665813928825e-72, 2.5189660543051998e-26, 1.5332724617897353e-32, 3.372184100659395e-62, 8.972995584909791e-07, 2.9987119743728358e-36, 5.799206727734042e-66, 2.2364479814427528e-51, 2.68893428417257e-85, 8.861825261805569e-08, 9.790202701161247e-67, 1.0869839788133954e-74, 6.344238158975943e-57, 1.0136253421074102e-09, 2.0997729840088217e-40, 2.0462621335295776e-10, 6.396194158114086e-76, 2.7991307726890466e-59, 1.338135924939674e-70, 1.0660256350830162e-37, 9.502454991309905e-72, 1.6191684765481855e-38, 5.96667929732055e-62, 2.3363831270170715e-28, 1.2585533383437093e-59, 1.7397592424148752e-54, 3.196813577579976e-16, 1.7237920716387796e-09, 1.1767503486203176e-31, 1.0720705302320314e-29, 8.881006385015337e-106, 9.807026739384885e-20, 2.0364323579992057e-14, 9.302403374578459e-26, 6.629744456764043e-31, 6.496178096043243e-17, 9.455662519955157e-48, 1.3048380382469986e-41, 9.927964382462358e-18, 3.3826599720518613e-35, 5.171904267398794e-13, 1.5083489568861784e-32, 6.869274152993092e-30, 7.644169189155559e-47, 9.045049924201919e-41, 4.8228421119390383e-76, 6.818959346533951e-63, 4.5326488755975504e-80, 3.158242360234095e-13, 9.469301195115371e-102, 9.556017029315809e-17, 8.213019969464447e-92, 9.999012306157265e-31, 6.958515927177465e-64, 1.0344900140719414e-60, 6.894974128057409e-07, 2.1715738007109305e-80, 3.138449879543244e-98, 7.049646217302562e-07, 1.1775037201685083e-46, 1.428269464652599e-53, 1.9433894010943704e-20, 5.5034737741933995e-06, 2.102078796679623e-37, 5.2206990789925825e-58, 1.6752110201432986e-79, 2.8255219068934656e-15, 5.300232169631875e-33, 8.89895063985478e-25, 3.4028708332589573e-87, 1.8587291626161787e-16, 2.319957767738885e-33, 9.315710890743207e-25, 5.070194309194564e-28, 5.4774598217631943e-67, 3.5921410138565445e-26, 9.971969603900891e-13, 8.23046358728307e-24, 1.6950668226332022e-22, 1.0518309547479882e-06, 1.7609281656343484e-18, 1.3305169980032038e-41, 3.907514973477697e-73, 3.707858001505489e-16, 2.396836997267625e-38, 9.20584839770201e-12, 7.033800265635055e-14, 1.5362862069822368e-79, 4.29719512614382e-13, 9.394729201404002e-42, 7.326436217275106e-10, 1.2506263477024707e-19, 1.232404477356419e-44, 1.1246552527900792e-74, 6.348112591143802e-102, 5.957750942614188e-22, 2.9262609236757937e-17, 1.2828691934969386e-30, 8.238963273150413e-107, 3.694993405433537e-19, 1.821592364227709e-33, 1.1366680608646635e-93, 5.803084453758598e-14, 2.3201833256801375e-37, 1.5346896948108385e-100, 5.0042333636413924e-11, 1.560710145655797e-37, 2.446703144629902e-39, 4.403532973449589e-88, 4.937335466912524e-06, 2.5266486642619925e-58, 8.95582380307752e-46, 3.750430530538848e-10, 5.525000178098875e-08, 1.1954854403872403e-06, 1.5288158946123583e-58, 6.150605620276652e-38, 3.991994361735143e-42, 1.6131205643465788e-14, 2.0422146589138293e-38, 1.8543135898326903e-37, 6.768962720587535e-76, 1.9726295904549626e-12, 1.2991146003263788e-36, 3.640598935244036e-47, 3.0569597204215095e-56, 2.421672280427985e-32, 4.601784943204454e-16, 5.784972858655142e-13, 8.172601838145256e-73, 1.2287232264951633e-71, 5.6173861247325305e-08, 6.068011245880913e-29, 1.0927604148753416e-07, 5.0683224680089204e-15, 1.1579250402771013e-41, 4.798049385591778e-15, 6.506172793693552e-70, 1.3332317927446803e-85, 5.5810409562085634e-08, 3.4371575686587084e-45, 2.286714482603066e-08, 1.133311116148742e-06, 3.6326414174622626e-34, 5.178695685229367e-90, 5.5397972889375525e-74, 5.137522989475878e-60, 7.362144771318596e-31, 7.093970404065195e-57, 3.5595363476145285e-62, 7.244462969548957e-09, 5.162675494904249e-46, 2.18051669849464e-69, 2.444597108690473e-08, 4.422032455254162e-50, 2.68362570059804e-13, 3.280584293067322e-70, 4.612161234904855e-70, 3.497667602242799e-50, 6.994574655856735e-11, 3.3042836063858524e-26, 1.2209233458153032e-15, 3.554510271148708e-17, 1.3398762857355315e-33, 8.615887400312365e-10, 9.17864292851803e-22, 5.329476767543233e-54, 3.0236530685693146e-45, 4.7613233963979786e-54, 1.6701413093620324e-30, 1.0619057419976214e-49, 1.7332378901169997e-42, 1.6782064020980823e-50, 4.8451896348269396e-27, 1.0035498782331529e-22, 7.422717318222463e-70, 1.415880763810024e-13, 6.284462873488956e-21, 7.773644280879226e-69, 3.109555569258016e-22, 8.873830855973346e-90, 3.908212369033652e-06, 4.718521889470979e-28, 2.614577274715357e-54, 1.479974999784553e-12, 1.1184267110828272e-43, 7.851272408405793e-11, 2.1919899037885775e-21, 4.546354863498092e-58, 2.5567385706213164e-06, 2.5073226616407275e-35, 2.4698514317657257e-15, 9.133565609061345e-18, 2.6535697534202168e-37, 6.411636857967889e-41, 1.5089512758118887e-05, 1.7892008378928086e-11, 6.001133584194724e-51, 2.1321250695985576e-39, 2.473195704697545e-22, 3.328562875556791e-06, 9.519533697343876e-22, 5.574849818516838e-08, 5.026187349695465e-72, 4.866045824638528e-42, 2.348324867617655e-54, 1.1611799589593866e-23, 1.4311029352317508e-25, 5.006247699418415e-18, 5.503241084483545e-62, 7.743305764134378e-08, 9.041540394861458e-12, 1.0187440028394681e-94, 1.5917895505101764e-07, 5.581788342162642e-24, 1.5878431168999822e-52, 1.1652079963713044e-87, 3.0296413550729988e-34, 2.487641070839718e-55, 8.39826238222286e-17, 2.968706528813382e-15, 1.2740404161695817e-58, 3.234547223117508e-79, 1.4898325855993703e-23, 1.8921801161278398e-85, 1.1004650981771992e-44, 4.004587054568026e-42, 3.190317272506035e-59, 1.353744726913566e-16, 1.9106724224426836e-66, 1.3618454451439139e-71, 3.960782570474066e-53, 1.1170012617332198e-26, 2.190280531067092e-46, 4.827596425117363e-55, 2.4178300776934166e-30, 1.4947968665750788e-62, 4.758847816099893e-76, 1.0784469253304538e-12, 5.961434708894476e-26, 5.296532288619882e-06, 3.9085498902250154e-56, 7.823908590294673e-38, 5.4689470442122594e-42, 7.773966470818819e-19, 8.669601673920178e-16, 1.2791463659058984e-38, 8.649321025606776e-34, 3.12414865141518e-53, 5.635767814646002e-44, 2.2614740944603773e-11, 2.2348072289511572e-10, 2.9504782530135667e-15, 6.836626834194172e-86, 3.656597457496929e-73, 3.7748418512491165e-57, 1.2196490659935969e-61, 1.8262490156418135e-77, 7.713987137079499e-18, 4.1059621850501664e-68, 1.7385002558816267e-46, 3.797763427887535e-64, 3.885399016303718e-25, 3.6301761360839366e-29, 2.4171955751407522e-48, 2.097815384245548e-10, 1.118270133796593e-43, 1.278600728358692e-53, 1.032547112956984e-09, 9.940850654319071e-09, 2.706184012205943e-81, 1.7241646640278268e-11, 5.802229716472178e-25, 1.0817057925168885e-11, 2.162702833163462e-70, 1.5401947062118968e-10, 7.053209502994596e-48, 1.0379704416106261e-58, 2.434403436249321e-18, 3.013603976712269e-47, 4.142958280307571e-63, 9.635861325118817e-73, 3.3298830822252093e-49, 1.0043715010841625e-26, 4.415782484797286e-06, 1.3843513571584052e-84, 3.0131389752084145e-23, 1.148127554479575e-09, 2.6080851443215884e-28, 3.7372282426313236e-20, 1.2138284222013958e-64, 1.341063184969734e-16, 7.742811234738564e-68, 7.134753411406785e-52, 1.641874473992567e-92, 4.178099536166482e-31, 1.839052038726331e-67, 4.576961207747353e-30, 5.927013147678081e-28, 1.3089048989660817e-59, 1.113604348008417e-81, 5.139847365624088e-06, 1.190821727470861e-28, 1.079896511900656e-27, 8.16629730036359e-20, 2.953190909212013e-61, 4.4049250904253887e-54, 4.504966510959668e-84, 4.7740732742318e-18, 3.91721498862748e-65, 2.9068422770411777e-67, 2.3077386039041514e-29, 3.346504419677698e-17, 2.9430609543531394e-44, 3.100274507133064e-68, 2.5299799099410183e-38, 1.3842121766314782e-83, 3.4228159469952516e-58, 1.5980291837931992e-73, 2.5737738749060466e-08, 8.390091301493867e-31, 7.71617902709405e-09, 1.4689195341122942e-07, 8.204564494130933e-09, 9.181971757275433e-24, 1.2848384416184122e-11, 2.021758682205442e-21, 1.846205083032209e-12, 6.611290499911783e-74, 4.487898361685488e-18, 5.598746436472421e-53, 6.969638752941561e-70, 1.1258511886477112e-75, 1.978834200392474e-44, 1.1893691741400952e-69, 4.056775613142475e-37, 4.273371977578118e-11, 9.139422509109974e-10, 3.9551261258310304e-27, 1.1904551261149808e-20, 8.798039792176135e-93, 7.492695912622408e-12, 6.707801435397601e-30, 1.406041152548471e-30, 2.4394296594844036e-75, 8.662813594944775e-07, 6.91537575352612e-77, 1.6995183222508607e-60, 1.405041319013064e-07, 1.937830743019346e-31, 1.5121614219182737e-49, 5.198421798996738e-37, 4.657685683040685e-15, 1.7198694332331498e-30, 1.1205658593735774e-52, 5.389795760649131e-22, 7.457526871111893e-44, 7.151685609148733e-74, 3.018447444544947e-26, 7.284394564659324e-63, 4.531610543737284e-71, 2.1211634447252693e-63, 5.353394924510068e-67, 5.2574310507835083e-11, 8.32596382980818e-32, 2.105886508351151e-07, 1.8731401712978945e-52, 1.230425651844788e-88, 2.4516712078521736e-08, 7.3199087610141e-79, 2.2277268648342257e-05, 1.5630358256765e-09, 2.6183760999013804e-11, 1.9414118512439408e-37, 8.972884656463197e-06, 7.088461053496128e-19, 1.8079911415529957e-66, 2.7902375944822373e-49, 3.0466539423280876e-14, 1.9333299439843444e-49, 8.366273955799039e-07, 4.1509224421427375e-07, 2.4122856955923615e-71, 1.6324199117632322e-54, 3.176818155777589e-48, 1.7158145291558658e-48, 3.9257360429115245e-35, 1.3144596997852485e-44, 2.6767672895707928e-20, 6.845170224240417e-12, 6.74977390206199e-27, 2.1753129302599065e-108, 2.292841682768199e-13, 4.528343018260312e-44, 2.0325611761816506e-28, 4.979962666343151e-59, 1.2986797267509496e-57, 3.8363043926962726e-28, 1.357966922295837e-33, 1.3907890355326841e-32, 7.511290782561915e-66, 1.7579779677278658e-79, 2.827615203247385e-23, 1.1643682064515921e-09, 1.995135975694156e-68, 4.357373918341716e-56, 3.63141212615546e-09, 3.2265578860595955e-18, 4.4273550369259156e-21, 9.111227009277923e-29, 1.1860828883721277e-32, 3.103078204717439e-37, 1.9222654589456895e-05, 2.7860084572596477e-72, 2.147829354147594e-34, 1.8912356377439987e-16, 6.828056666710535e-39, 4.263461543317843e-44, 1.6518540673835329e-43, 4.884919920188509e-49, 2.8288395834468867e-37, 1.1506534126678644e-51, 7.015295478121229e-70, 1.0146055540136028e-60, 3.9423419050503814e-47, 2.8830617516105486e-65, 1.9967001435240774e-79, 9.149021017261994e-67, 8.732133140891924e-34, 5.834420462149605e-15, 9.661557076533036e-54, 8.958530243566484e-12, 3.4114595735574526e-79, 4.166040847005981e-75, 4.476787828283237e-19, 5.491971080480331e-20, 8.634227392256431e-43, 2.3343270912342337e-33, 6.80625933309089e-62, 6.545865578211885e-20, 4.943909830881379e-22, 4.93341788859199e-58, 6.052755700561802e-47, 1.8839904659707486e-49, 7.140337649335949e-64, 6.778492376344835e-43, 3.385996700351916e-26, 5.604429240845777e-65, 4.724787843384395e-06, 2.920666446102028e-52, 1.8880795503651734e-60, 4.8249410444669854e-54, 7.850060039368972e-26, 6.67204620758819e-17, 5.619532694920081e-54, 4.91251463069324e-20, 1.0857018031018628e-49, 6.213034006421582e-35, 1.2892232662126468e-20, 2.0582862295472417e-34, 7.066720109525975e-10, 2.0875713773948056e-16, 7.413735923886404e-49, 6.511188603456587e-44, 1.9568345388837028e-14, 3.6791484719849115e-51, 2.051075450454035e-38, 2.2931608242878658e-88, 5.899262668179513e-11, 6.594606594286786e-47, 2.004087910383361e-46, 4.593326912277407e-56, 4.0820747781433133e-10, 3.799065184498066e-41, 2.934471731146405e-19, 1.7357144418205714e-66, 5.48765599310075e-12, 2.390815749643477e-15, 9.649028000280527e-22, 1.6644025407340866e-61, 1.166021583178944e-09, 1.8520073942885778e-17, 5.853663403036754e-70, 5.626752520815997e-15, 1.784808768601167e-26, 5.469144882756238e-07, 4.085167314826322e-102, 5.479872130073514e-32, 7.98719937925505e-19, 2.945882454408142e-39, 2.3970182677989004e-07, 6.410946423001716e-13, 1.0594823321884709e-47, 3.9914040865832063e-22, 3.685683171354843e-20, 9.57362957220721e-56, 7.475815560071899e-13, 2.1089622125274055e-23, 6.515191199531666e-23, 1.5651647407975208e-42, 1.5362884400411392e-44, 3.219043466048819e-22, 3.724957462064377e-18, 3.614821613259451e-45, 1.2706100353982076e-06, 1.324773208699981e-06, 1.1379136827868558e-27, 1.1110837733623247e-45, 7.826616593750351e-45, 7.03735200165687e-36, 6.9022833218215176e-93, 7.022892236253667e-10, 2.9279451223005007e-33, 2.062408862113158e-72, 1.4609763132044578e-92, 1.7398296322405397e-66, 4.324950453310375e-46, 2.3615144865856064e-08, 3.12331697455143e-78, 1.2492141211960906e-25, 3.394844137311868e-53, 6.536428960209629e-17, 4.248426175360162e-84, 1.3200337166678684e-11, 2.1986160651755236e-06, 1.31027301309506e-19, 7.588826592903914e-47, 2.369532024092762e-64, 6.518018913006051e-07, 3.220740146833811e-43, 3.0807862762938036e-45, 7.477056258559315e-48, 6.910521619001859e-58, 2.4094930502734553e-48, 3.1591849964825414e-70, 1.3609736294142176e-24, 6.2123804783089424e-46, 2.881982899669914e-32, 9.669197728188682e-10, 3.652241142215119e-17, 4.276279524427099e-44, 1.1000054423322873e-07, 7.2661978115962045e-28, 7.929523356387636e-45, 1.868122365524443e-21, 9.887292802399783e-39, 1.1895037991930666e-30, 9.575841446789236e-37, 1.2956218321392114e-24, 7.38500203841596e-21, 1.1889745126634748e-10, 3.3009292717098e-53, 1.1170865249855465e-09, 1.0153000821567254e-76, 3.0913662374330786e-79, 3.388634736317051e-09, 1.354413645949861e-64, 1.766715880120892e-33, 1.615404326897073e-79, 4.715438051881652e-47, 1.1884286171004871e-70, 2.1092147589074185e-30, 4.903518738622916e-52, 1.3315920276191635e-47, 2.828261590950083e-49, 1.8330684387671834e-20, 3.201229277769713e-16, 3.0928606003983183e-12, 4.956710778298888e-72, 2.835398505392429e-10, 6.369276696761729e-40, 4.85152505815181e-45, 4.32859747516726e-15, 1.8751598842844234e-15, 6.3126822808876285e-83, 1.0955289355765837e-27, 4.602857267112407e-77, 1.2588990559061355e-26, 3.45341004758605e-64, 1.1557561476733645e-55, 2.907036891068397e-34, 8.330372406562738e-30, 2.3956465636685227e-14, 1.4525488305810055e-54, 1.026332837539295e-65, 5.776766859648875e-20, 4.779363081149308e-36, 8.412446769991846e-46, 1.1796083173803445e-64, 2.4097960856105437e-67, 4.560410864415207e-83]


