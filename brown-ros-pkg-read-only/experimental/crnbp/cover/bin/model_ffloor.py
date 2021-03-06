#!/usr/bin/env python
# Uses the model_create stuff to model a 1-d room with three robots in it.
#
import roslib ; roslib.load_manifest('cover')
import rospy
from geometry_msgs.msg import Twist, Quaternion, Pose
from nav_msgs.msg import Odometry
from irobot_create_2_1a.msg import SensorPacket
from model_create import CreateModel, RoomModel
from perfesser.msg import Pt
from cover.msg import Room, Room2D
import tgraph as tg
import math
import numpy as np

class TwoDRobotModel(CreateModel):
    def __init__(self, name, xpos, ypos, color, 
                 perimeter = [[0.0,0.0],[1.0,0.0],[1.0,1.0],[0.0,1.0],[0.0,0.0]],
                 radius = 0.013):
        self.name = name
        self.xpos = xpos
        self.ypos = ypos
        self.xvel = 0.0
        self.yvel = 0.0
        self.color = color
        self.radius = radius
        # Perimeters must be specified clockwise (looking down).
        self.perimeter = [(p, (q[0] - p[0], q[1] - p[1])) \
                              for p,q in zip(perimeter[0:-1],perimeter[1:]) ]

        print self.perimeter

        CreateModel.__init__(self, self.xpos, self.ypos, 3.0, name=self.name,
                             color=self.color, trails=False, 
                             nose=True, debug=False, radius = self.radius)

        self.sub = rospy.Subscriber(self.name + "/cmd_vel", Twist, self.twist)

    def cross(self, p, q):
        """
        2d cross product.
        """
        return p[0] * q[1] - p[1] * q[0]

    def intersect(self, p, r, q, s):
        """
        Intersection of two line segments in 2d.  Segment one is (p, p+r) and 
        two is (q, q+s).
        """
        c = self.cross(r,s)

        if c == 0:
            return (-1.0, -1.0)

        d = (q[0] - p[0], q[1] - p[1])
        t = self.cross(d, s) / c
        u = self.cross(d, r) / c

        return (t,u)


    # Advances the robot's position by time dt.  But asserts limits.
    def advance(self, dt):
        now = self.then + dt
        elapsed = now - self.then
        self.then = now
        if self.debug:
            print "advancing to t=%5.3f" % (self.then)

        ldist = dt * self.lwSpeed
        rdist = dt * self.rwSpeed

        d = (ldist + rdist)/2.0
        th = (rdist - ldist)/self.distanceBetweenWheels

        dx = d / dt
        dth = th / dt

        bumpLeft = False 
        bumpRight = False

        if (d != 0):
            x = math.cos(th)*d
            y = math.sin(th)*d # Does this differ from the create driver?  Should it?
            newx =  (math.cos(self.th)*x - math.sin(self.th)*y)
            newy =  (math.sin(self.th)*x + math.cos(self.th)*y)

            # Assert the limits defined by the perimeter.
            collision = False
            for p in self.perimeter:
                tu = self.intersect((self.x, self.y),(newx, newy),
                                    p[0], p[1])
                if 0.0 <= tu[0] <= 1.0 and 0.0 <= tu[1] <= 1.0:
                    collision = True
                    angleOfIncidence = math.atan2(newy,newx) - \
                        math.atan2(p[1][1],p[1][0])
                    if angleOfIncidence < 0.7 * math.pi:
                        bumpLeft = True
                    if angleOfIncidence > 0.3 * math.pi:
                        bumpRight = True
                    break


            if collision:
                # Normalize direction of change
                norm = (newx**2 + newy**2)**0.5

                self.x += tu[0] * newx - 0.01 * newx/norm
                self.y += tu[0] * newy - 0.01 * newy/norm
            else:
                self.x += newx
                self.y += newy

        if (th != 0):
            self.th += th
            self.th = self.th % (2 * math.pi)
            self.th = self.th - (2 * math.pi) if self.th > math.pi else self.th

        quaternion = Quaternion()
        quaternion.x = 0.0
        quaternion.y = 0.0
        quaternion.z = math.sin(self.th/2.0)
        quaternion.w = math.cos(self.th/2.0)

        self.odomBroadcaster.sendTransform(
            (self.x, self.y, 0),
            (quaternion.x, quaternion.y, quaternion.z, quaternion.w),
            rospy.Time.now(),
            "base_link",
            "odom"
            )

        odom = Odometry()
        odom.header.stamp = rospy.Time.now()
        odom.header.frame_id = "odom"
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0
        odom.pose.pose.orientation = quaternion

        odom.child_frame_id = "base_link"
        odom.twist.twist.linear.x = dx
        odom.twist.twist.linear.y = 0
        odom.twist.twist.angular.z = dth

        self.odomPub.publish(odom)

        if bumpLeft or bumpRight:
            print self.name, "is really at:", self.x, self.y, self.th
            self.leaveMark()
            self.detectSomething(SensorPacket(bumpLeft=bumpLeft,
                                              bumpRight=bumpRight))



class TwoDRoomModel(RoomModel):
    def __init__(self, dt, xdim, neighborDistance = 4.0,
                 perimeter = [[0,0],[1,0],[1,1],[0,1],[0,0]]):
        self.dt =  dt
        self.xdim = xdim
        self.neighborDistance = neighborDistance
        self.perimeter = perimeter

        RoomModel.__init__(self, self.dt, self.xdim, self.xdim, 
                           xscale = 10.0, yscale = 10.0, 
                           xmin = 0.0, ymin = 0.0)

        self.tg.plot_lines(np.array(self.perimeter),0,1,0,"purple")

    def dist(self, x1, y1, x2, y2):
        """ Cartesian distance """
        return ((y2 - y1)**2 + (x2 - x1)**2)**0.5

    def nearest(self):
        """
        Returns a list of robots in the room, accompanied by the names and
        locations of its neighbors.
        """
        out = Room2D()

        for rb in self.robots:
            out.names.append(rb.name)
            nr = Room()

            for rbt in self.robots:
                d = self.dist(rb.x, rb.y, rbt.x, rbt.y)
                if (d > 0.0) and (d < self.neighborDistance):
                    nr.names.append(rbt.name)
                    nr.locations.append(Pt(point=(rbt.x, rbt.y)))

            out.neighbors.append(nr)

        return out


if __name__ == '__main__':
    rospy.init_node('cover')
    import time
    import signal
    import sys
    import traceback

    def handler(signum, frame):
        print "....all right already, I'm stopping.  Jeez what a nag."
        raise

    signal.signal(signal.SIGINT, handler)

    room = TwoDRoomModel(0.1, 1000, neighborDistance=4.0,
                         perimeter = [[0.0132450331125828, 7.37748344370861],
                                      [0.582781456953642, 7.94701986754967],
                                      [0.90066225165563, 7.82781456953642],
                                      [1.28476821192053, 7.86754966887417],
                                      [1.28476821192053, 7.37748344370861],
                                      [3.44370860927152, 7.37748344370861],
                                      [3.44370860927152, 7.17880794701987],
                                      [3.82781456953642, 7.17880794701987],
                                      [3.82781456953642, 7.37748344370861],
                                      [4.17218543046358, 7.37748344370861],
                                      [4.17218543046358, 7.11258278145695],
                                      [3.96026490066225, 7.11258278145695],
                                      [3.96026490066225, 6.59602649006622],
                                      [4.17218543046358, 6.59602649006622],
                                      [4.17218543046358, 5.52317880794702],
                                      [4.7682119205298, 5.52317880794702],
                                      [4.7682119205298, 4.99337748344371],
                                      [5.54966887417219, 4.99337748344371],
                                      [5.54966887417219, 4.56953642384106],
                                      [4.19867549668874, 4.56953642384106],
                                      [4.18543046357616, 4.35761589403973],
                                      [4.18543046357616, 4.31788079470199],
                                      [4.75496688741722, 4.31788079470199],
                                      [4.75496688741722, 4.13245033112583],
                                      [5.58940397350993, 4.13245033112583],
                                      [5.58940397350993, 4.34437086092715],
                                      [5.74834437086093, 4.34437086092715],
                                      [5.74834437086093, 4.99337748344371],
                                      [6.34437086092715, 4.96688741721854],
                                      [6.33112582781457, 4.13245033112583],
                                      [8.23841059602649, 4.13245033112583],
                                      [8.23841059602649, 6.75496688741722],
                                      [7.88079470198676, 6.75496688741722],
                                      [7.88079470198676, 7.09933774834437],
                                      [7.24503311258278, 7.09933774834437],
                                      [7.24503311258278, 7.90728476821192],
                                      [7.6158940397351, 7.90728476821192],
                                      [7.6158940397351, 7.54966887417219],
                                      [8.23841059602649, 7.54966887417219],
                                      [8.23841059602649, 7.68211920529801],
                                      [7.73509933774834, 7.68211920529801],
                                      [7.73509933774834, 10.00000],
                                      [9.78807947019868, 10.00000],
                                      [9.74834437086093, 9.72185430463576],
                                      [9.90728476821192, 9.72185430463576],
                                      [9.90728476821192, 8.13245033112583],
                                      [9.68211920529801, 8.13245033112583],
                                      [9.68211920529801, 7.54966887417219],
                                      [8.7682119205298, 7.54966887417219],
                                      [8.7682119205298, 7.68211920529801],
                                      [8.63576158940397, 7.68211920529801],
                                      [8.63576158940397, 7.4569536423841],
                                      [9.96026490066225, 7.4569536423841],
                                      [9.96026490066225, 7.13907284768212],
                                      [8.72847682119205, 7.13907284768212],
                                      [8.72847682119205, 3.28476821192053],
                                      [8.52980132450331, 3.28476821192053],
                                      [8.52980132450331, 3.65562913907285],
                                      [4.59602649006623, 3.65562913907285],
                                      [4.4635761589404, 3.85430463576159],
                                      [4.19867549668874, 3.85430463576159],
                                      [4.19867549668874, 3.57615894039735],
                                      [3.50993377483444, 3.57615894039735],
                                      [3.50993377483444, 3.20529801324503],
                                      [2.92715231788079, 3.20529801324503],
                                      [2.92715231788079, 1.86754966887417],
                                      [2.47682119205298, 1.86754966887417],
                                      [2.43708609271523, 3.84105960264901],
                                      [0.370860927152318, 3.81456953642384],
                                      [0.370860927152318, 4.31788079470199],
                                      [0.649006622516556, 4.35761589403973],
                                      [0.649006622516556, 6.71523178807947],
                                      [0.132450331125828, 6.87417218543046],
                                      [0.0132450331125828, 7.37748344370861]])

    robots = []
    def addRobot(name, xloc, yloc, color, p):
        robots.append(TwoDRobotModel(name, xloc, yloc, color, 
                                     perimeter = p, radius = 0.06))
        room.addRobot(robots[-1])

    sp = lambda(x): x + (np.random.random()-0.5)/8.0

    addRobot("abel", sp(8.5), sp(6.8), 0.0, room.perimeter)
    addRobot("baker", sp(8.5), sp(6.6), 10.0, room.perimeter)
    addRobot("charlie", sp(8.5), sp(6.4), 20.0, room.perimeter)
    addRobot("dog", sp(8.5), sp(6.2), 30.0, room.perimeter)
    addRobot("easy", sp(8.6), sp(6.0), 40.0, room.perimeter)
    addRobot("fox", sp(8.5), sp(5.8), 50.0, room.perimeter)
    addRobot("george", sp(8.5), sp(5.6), 60.0, room.perimeter)
    addRobot("harold", sp(8.5), sp(5.4), 70.0, room.perimeter)
    addRobot("ivy", sp(8.5), sp(5.2), 80.0, room.perimeter)
    addRobot("joseph", sp(8.5), sp(5.0), 90.0, room.perimeter)
#    addRobot("karen", sp(8.5), sp(6.8), 50.0, room.perimeter)
#    addRobot("lulu", sp(8.5), sp(6.8), 55.0, room.perimeter)
#    addRobot("mark", sp(8.5), sp(6.8), 60.0, room.perimeter)
#    addRobot("nora", sp(8.5), sp(6.8), 65.0, room.perimeter)
#    addRobot("oswald", sp(8.5), sp(6.8), 70.0, room.perimeter)
#    addRobot("peter", sp(8.5), sp(6.8), 75.0, room.perimeter)
#    addRobot("quincy", sp(8.5), sp(6.8), 80.0, room.perimeter)
#    addRobot("roger", sp(8.5), sp(6.8), 85.0, room.perimeter)
#    addRobot("susan", sp(8.5), sp(6.8), 90.0, room.perimeter)
#    addRobot("tymon", sp(8.5), sp(6.8), 95.0, room.perimeter)
#    addRobot("umberto", sp(8.5), sp(6.8), 100.0, room.perimeter)

    locpub = rospy.Publisher("/room/locations", Room2D)

    try:

        start = rospy.Time.now().to_sec()
        startd = 91915.0
        startg = 91916.0
        starth = 91917.0
        starti = 91918.0
        startj = 91985.0


        r = rospy.Rate(4)
        while True:
            room.updateRoom()
            if start + startd < rospy.Time.now().to_sec():
                room.delRobot("dog")

            if start + startg < rospy.Time.now().to_sec():
                addRobot("george", 0.5, 0.5, 95.0, room.perimeter)
                startg = 10000000

            if start + starth < rospy.Time.now().to_sec():
                addRobot("how", 0.2, 0.5, 100.0, room.perimeter)
                starth = 10000000

            if start + starti < rospy.Time.now().to_sec():
                addRobot("ivy", 0.8, 0.5, 100.0, room.perimeter)
                addRobot("joseph", 0.81, 0.4, 100.0, room.perimeter)
                addRobot("kappa", 0.82, 0.3, 100.0, room.perimeter)
                starti = 10000000

            if start + startj < rospy.Time.now().to_sec():
                room.delRobot("george")
                room.delRobot("how")
                room.delRobot("ivy")
                room.delRobot("joseph")
                startj = 10000000

            locpub.publish(room.nearest())
            r.sleep()

    except:
        print "*************EXIT*************"
        print sys.exc_type
        print sys.exc_value
        traceback.print_tb(sys.exc_traceback)
