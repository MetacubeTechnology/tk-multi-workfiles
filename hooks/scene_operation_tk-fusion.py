# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os

import PeyeonScript
f_connection = PeyeonScript.scriptapp ("Fusion")

import tank
from tank import Hook
from tank import TankError


class SceneOperation(Hook):
    """
    Hook called to perform an operation with the current scene
    """

    def execute(self, operation, file_path, context, parent_action, file_version, read_only, **kwargs):
        """
        Main hook entry point
        
        :param operation:       String
                                Scene operation to perform
        
        :param file_path:       String
                                File path to use if the operation
                                requires it (e.g. open)
                    
        :param context:         Context
                                The context the file operation is being
                                performed in.
                    
        :param parent_action:   This is the action that this scene operation is
                                being executed for.  This can be one of:
                                - open_file
                                - new_file
                                - save_file_as 
                                - version_up
                        
        :param file_version:    The version/revision of the file to be opened.  If this is 'None'
                                then the latest version should be opened.
        
        :param read_only:       Specifies if the file should be opened read-only or not
                            
        :returns:               Depends on operation:
                                'current_path' - Return the current scene
                                                 file path as a String
                                'reset'        - True if scene was reset to an empty 
                                                 state, otherwise False
                                all others     - None
        """
        if operation == "current_path":
            # return the current scene path
            the_comp = f_connection.GetCurrentComp ()
            file_path = the_comp.GetAttrs ('COMPS_FileName')
            return file_path
        elif operation == "open":
            # open the specified scene
            f_connection.LoadComp (file_path)
        elif operation == "save":
            # save the current scene:
            the_comp = f_connection.GetCurrentComp ()
            file_path = the_comp.GetAttrs ('COMPS_FileName')
            the_comp.Save (file_path)
        elif operation == "save_as":
            # save the scene as file_path:
            the_comp = f_connection.GetCurrentComp ()
            the_comp.Save (file_path)
        elif operation == "reset":
            """
            Reset the scene to an empty state
            """
            the_comp = f_connection.GetCurrentComp ()
            the_comp.Close ()
            f_connection.NewComp ()
            return True
