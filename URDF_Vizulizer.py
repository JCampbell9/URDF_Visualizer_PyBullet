#!/usr/bin/python3

"""Script for testing URDFs in a simple pybullet enviroment."""

# Author: JCampbell9,
# Date: 6/17/2023

import pybullet as p
import time
import pybullet_data

import tkinter as tk

from tkinter.filedialog import askopenfile


class Vizulizer():
    """URDF Vizulizer."""

    def __init__(self, file_loc):
        """Initialize the Vizulizer class.

        Args:
            file_loc (str): path to the URDF that we want to be visualized
        """
        self.file_loc = file_loc

        self.physicsClient = p.connect(p.GUI)  # or p.DIRECT for non-graphical version
        p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
        p.setGravity(0, 0, -9.81)
        self.LinkId = {}
        self.robotStartPos = [0, 0, 1]
        self.robotStartOrientation = p.getQuaternionFromEuler([0, 0, 0])

        self.robot = p.loadURDF(self.file_loc, useFixedBase=1)
        p.resetDebugVisualizerCamera(cameraDistance=.2, cameraYaw=180, cameraPitch=-91, cameraTargetPosition=[0, 0.1, 0.4])

        self.control_gui = tk.Tk()
        self.control_gui.title("testing widget")
        self.control_gui.geometry("300x600")
        test_button = tk.Button(self.control_gui, text = "RESET", command=self.reset_button)
        test_button.pack(pady=3)

        


    def main(self):
        """Run the simulator."""           
        
        self.set_joint_sliders()

        while p.isConnected():

            p.stepSimulation()
            time.sleep(1. / 240.)
            self.control_gui.update()

            for key in self.LinkId.keys():
                linkPos = self.LinkId[key]["slider_id"].get()
                p.setJointMotorControl2(self.robot, self.LinkId[key]["joint_id"], p.POSITION_CONTROL, targetPosition=linkPos)

        p.disconnect()
    
    def reset_button(self):
        p.resetBasePositionAndOrientation(self.robot, self.robotStartPos, self.robotStartOrientation)
        for key in self.LinkId.keys():
            self.LinkId[key]["slider_id"].set(0)

    def set_joint_sliders(self):
        for i in range(0, p.getNumJoints(self.robot)):
            p.setJointMotorControl2(self.robot, i, p.POSITION_CONTROL, targetPosition=0, force=0)
            joint_info = p.getJointInfo(self.robot, i)
            linkName = joint_info[1].decode("ascii")
            # print("---------------------------------------------------------------------------------------------")
            # pprint(joint_info)

            if joint_info[2] == 4:
                continue
            else:
                if linkName not in self.LinkId:
                    
                    temp_label = tk.Label(self.control_gui, text=linkName)
                    temp_label.pack(pady=3)
                    temp_id = tk.Scale(self.control_gui, name=linkName, from_=joint_info[8], to=joint_info[9], orient=tk.HORIZONTAL, resolution=0.01)
                    temp_id.pack(pady=1)
                    temp_id.set(0)
                    self.LinkId[linkName] = {}
                    self.LinkId[linkName]["slider_id"] = temp_id
                    self.LinkId[linkName]["joint_id"] = i




if __name__ == '__main__':


    tk.Tk().withdraw()

    file = askopenfile()

    main_run = Vizulizer(file_loc=file.name)
    main_run.main()
