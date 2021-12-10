#!/usr/bin/env python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import Bool
def movebase_client(goal_position):

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()
    client.send_goal(goal_position)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

def set_goals(targets, num_goals):
    goals = [MoveBaseGoal() for _ in range(num_goals)]
    for idx, goal in enumerate(goals):
        goal.target_pose.header.seq = idx
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x, goal.target_pose.pose.position.y, goal.target_pose.pose.position.z = targets[idx][0:3]
        goal.target_pose.pose.orientation.x, goal.target_pose.pose.orientation.y, goal.target_pose.pose.orientation.z,      goal.target_pose.pose.orientation.w = targets[idx][3:]

    return goals
def pbvs_callback(msg):
	global pbvs_done
	pbvs_done = msg.data



if __name__ == '__main__':
    targets = [[7.827633380889893, 1.5852015018463135, 0.0, 0.0, 0.0, -0.701218099539, 0.712946826123]] #Goal2
    ibvs_done = False
    rospy.init_node('movebase_client_py')
    pub = rospy.Publisher('/nav_done', Bool, queue_size=10)
    rospy.Subscriber('/pbvs_done', Bool, pbvs_callback)
    num_goals = 1
    affirm = 'y'
    goals = set_goals(targets, num_goals)

    while True:

        try:
            for idx, goal in enumerate(goals):
                if affirm == 'y':
                    print(goal)
                    result = movebase_client(goal)
                    if result:
                        rospy.loginfo("Goal %d execution done!"%(idx))
                        pub.publish(True)
                        if pbvs_done:
                       	    affirm = raw_input('Continue to next goal?(y/n) ')
                else:
                    print('Exiting')
                    exit(0)

            print('All goals Reached')

        except rospy.ROSInterruptException:
            rospy.loginfo("Navigation test finished.")



# Goal-1
  # x: 7.827633380889893
  # y: 1.5852015018463135
  # z: -0.001434326171875


# Goal-2
  # x: -1.99265456199646
  # y: 3.931382417678833
  # z: -0.001434326171875
