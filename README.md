# ROS-Warehouse-Robot
Course Project at UMN (CSCI5551 - Introduction to Intelligent Robots)

ROS based Volta robot equipped with Navigation and PBVS capabilities

Instructions for running the project: 

	1. Launching Simulation + robot spawner : (terminal tab-1)

			` roslaunch volta_simulation warehouse_complete.launch `


	2. Launching the navigation node: (terminal tab-2) 

			` roslaunch volta_navigation navigation.launch `
			

	3. Launching the send_goals and PBVS nodes: (terminal tab-3)

			` roslaunch vision_align align_nav.launch `

* Navigation Demo:

https://user-images.githubusercontent.com/43849409/146668619-3963d1d2-00d0-4888-80a5-8998ae149a24.mp4

* Navigation + PBVS Demo:

https://user-images.githubusercontent.com/43849409/146668833-8b49ddb9-a08a-4923-8e3d-7cb76c7153d8.mp4

