#!/usr/bin/env python3

import numpy as np
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from aruco_detect import aruco_detect, centers, pose_align
from geometry_msgs.msg import Twist
import time
from std_msgs.msg import Bool


def cam_callback(msg):
	global theta_dot_z
	global linear_v_x
	global flag, nav_pbvs_done
	global prev_r, prev_x, prev_z
	bridge = CvBridge()
	cv_stream = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
	(corners, ids, ar) = aruco_detect(cv_stream)
	vel = Twist()

	# nav_pbvs_done = True => Navigation is in process
	# nav_pbvs_done = False => PBVS is in process

	if not nav_pbvs_done: 
		if not flag:
			if len(corners) != 0:
				centers(corners,ids,ar)
				r, t = pose_align(corners, ids)
				error_matrix = np.array([r, t[0][0], abs(0.5 - t[2][0])]) 
				error_dot_matrix = error_matrix - np.array([prev_r, prev_x, prev_z])
				prev_r, prev_x, prev_z = r, t[0][0], abs(0.5 - t[2][0])

				gain_matrix = np.array([0.1, 1.5, 1])
				gain_dot_matrix = np.array([-0.1, 0, 0])
				step = 0.005
				
				
				vc_matrix = error_matrix * gain_matrix
				vc_dot_matrix = error_dot_matrix * gain_dot_matrix
				vc = vc_matrix + vc_dot_matrix
				

				vel.angular.z = theta_dot_z - step * vc[0] if abs(vc_matrix[0]) > 1 else 0
				v_sintheta = linear_v_x / np.sin(np.radians(r)) - step * vc[1] if abs(vc_matrix[1]) > 0.05 else 0
				v_costheta = linear_v_x / np.cos(np.radians(r)) - step * vc[2] if abs(vc_matrix[2]) > 0.05 else 0
				v = np.sqrt(v_costheta**2 + v_sintheta**2)
				v = 0.5 if v > 0.5 else v
				vel.linear.x = v
				flag = False if abs(vc_matrix[2]) > 0.05 else True
				print(vc_matrix)
				print('PBVS_in_motion: {}, Odom_linear_velocity: {}, Corrected_velocity:{}'.format(flag, linear_v_x, v))
			
			else:
				print('No tag found. Rotating to find tag.')
				vel.linear.x = 0
				vel.angular.z = 0.5
			
		else: 
			vel.linear.x = 0
			vel.angular.z = 0
			nav_pbvs_done = True
			flag = False
			print("location reached")

		pub.publish(vel)

	print('Nav-PBVS-done flag: ', nav_pbvs_done)
	nav_pbvs_pub.publish(nav_pbvs_done)
    
        
def odom_callback(msg):
	global theta_dot_z
	global linear_v_x
	theta_dot_z = msg.angular.z 
	linear_v_x = msg.linear.x


def nav_callback(msg): 
	global nav_pbvs_done
	nav_pbvs_done = msg.data 


if __name__ == '__main__':
	nav_pbvs_done = True
	nav_pbvs_pub = rospy.Publisher('/nav_pbvs_done', Bool, queue_size=10)
	rospy.Subscriber('/nav_pbvs_done', Bool, nav_callback)
	theta_dot_z = 0
	linear_v_x = 0
	rospy.init_node('scan_values')
	lid_sub = rospy.Subscriber("/camera/camera", Image, cam_callback)
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	cmd_vel_sub = rospy.Subscriber('/cmd_vel', Twist, odom_callback)
	flag = False
	prev_r = 0
	prev_x = 0
	prev_z = 0
	rospy.spin()

