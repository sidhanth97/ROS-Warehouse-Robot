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
        goal.target_pose.pose.orientation.x, goal.target_pose.pose.orientation.y, goal.target_pose.pose.orientation.z, goal.target_pose.pose.orientation.w = targets[idx][3:]

    return goals


def pbvs_callback(msg):
    global nav_pbvs_done
    nav_pbvs_done = msg.data



if __name__ == '__main__':
    targets = [[8.144268989562988, 1.888837218284607, 0.0, 0.0, 0.0, 0.0, 0.712946826123], [-2.0039172172546387, 4.425413608551025, 0.0, 0.0, 0.0, 1.5707, 0.712946826123]] #Goal2
    nav_pbvs_done = True
    rospy.init_node('movebase_client_py')
    nav_pbvs_pub = rospy.Publisher('/nav_pbvs_done', Bool, queue_size=10)
    rospy.Subscriber('/nav_pbvs_done', Bool, pbvs_callback)
    num_goals = 2
    goals = set_goals(targets, num_goals)

    # nav_pbvs_done = True => Navigation is in process
    # nav_pbvs_done = False => PBVS is in process

    idx = 0
    try:
        while idx < num_goals:
            if nav_pbvs_done:
                goal = goals[idx]
                result = movebase_client(goal)
                nav_pbvs_done = False
                nav_pbvs_pub.publish(nav_pbvs_done)
                print('MoveBaseClient Result: ', nav_pbvs_done)
                idx += 1
            else:
                print('PBVS is happening. Wait!')
            
        print('All goals Reached')
        rospy.signal_shutdown("Shutting down")

    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")




# Goal-1
  # x: 8.144268989562988
  # y: 1.888837218284607
  # z: -0.001434326171875


# Goal-2
#   x: -2.0039172172546387
#   y: 4.425413608551025
#   z: 0.0025634765625
# ---
