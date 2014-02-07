#!/usr/bin/env python

# Copyright (c) 2013, Carnegie Mellon University
# All rights reserved.
# Authors: Michael Koval <mkoval@cs.cmu.edu>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# - Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# - Neither the name of Carnegie Mellon University nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import numpy

class MobileBase(object):
    def __init__(self, sim, robot):
        self.simulated = sim
        self.robot = robot

    def CloneBindings(self, parent):
        pass

    def Forward(self, meters, timeout=None):
        """
        Drives the robot forward the desired distance
        Note: Only implemented in simulation. Derived robots should implement this method.
        @param meters the distance to drive the robot
        @param timout duration to wait for execution
        """
        if self.simulated:
            with self.robot.GetEnv():
                current_pose = self.robot.GetTransform().copy()
                current_pose[:3,3] = current_pose[:3,3] + meters*current_pose[:3,0]
                self.robot.SetTransform(current_pose)
        else:
            raise NotImplementedError('DriveForward is not implemented')

    def Rotate(self, angle_rad, timeout=None):
        """
        Rotates the robot the desired distance
        @param angle_rad the number of radians to rotate
        @param timeout duration to wait for execution
        """
        if self.simulated:
            with self.robot.GetEnv():
                current_pose_in_world = self.robot.GetTransform().copy()
                desired_pose_in_herb = numpy.array([[numpy.cos(angle_rad), -numpy.sin(angle_rad), 0, 0],
                                                    [numpy.sin(angle_rad), numpy.cos(angle_rad), 0, 0],
                                                    [0, 0, 1, 0],
                                                    [0, 0, 0, 1]])
                desired_pose_in_world = numpy.dot(current_pose_in_world, desired_pose_in_herb)
                self.robot.SetTransform(desired_pose_in_world)
        else:
            raise NotImplementedError('Rotate is not implemented')

    def DriveStraightUntilForce(robot, direction, velocity=0.1, force_threshold=3.0,
                                max_distance=None, timeout=None, left_arm=True, right_arm=True):
        """
        Drive the base in a direction until a force/torque sensor feels a force. The
        base first turns to face the desired direction, then drives forward at the
        specified velocity. The action terminates when max_distance is reached, the
        timeout is exceeded, or if a force is felt. The maximum distance and timeout
        can be disabled by setting the corresponding parameters to None.
        @param direction forward direction of motion in the world frame
        @param velocity desired forward velocity
        @param force_threshold threshold force in Newtons
        @param max_distance maximum distance in meters
        @param timeout maximum duration in seconds
        @param left_arm flag to use the left force/torque sensor
        @param right_arm flag to use the right force/torque sensor
        @return felt_force flag indicating whether the action felt a force
        """
        if self.simulated:
            raise NotImplementedError('DriveStraightUntilForce does not work in simulation')
        else
            raise NotImplementedError('DriveStraightUntilForce is not implemented')
