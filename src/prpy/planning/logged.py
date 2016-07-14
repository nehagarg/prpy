from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division
import collections
import math
import time

import openravepy
import numpy
import yaml

import prpy.planning.base
import prpy.serialization


class LoggedPlanner(prpy.planning.base.MetaPlanner):
    def __init__(self, planner):
        super(LoggedPlanner, self).__init__()
        self.planner = planner
    
    def __str__(self):
        return 'Logged({0:s})'.format(self.planner)
    
    def has_planning_method(self, method_name):
        return self.planner.has_planning_method(method_name)
    
    def get_planning_method_names(self):
        return self.planner.get_planning_method_names()
    
    def get_planners(self, method_name):
        return [self.planner]
    
    def plan(self, method, args, kw_args):
        
        # get log file name
        stamp = time.time()
        struct = time.localtime(stamp)
        fn = 'log-{}.{:06d}.yaml'.format(
            time.strftime('%Y%m%d-%H%M%S', struct),
            int(1.0e6*(stamp-math.floor(stamp))))
        
        # retrieve enviroment
        if 'robot' in kw_args:
            env = kw_args['robot'].GetEnv()
        elif len(args) > 0:
            env = args[0].GetEnv()
        else:
            raise RuntimeError('could not retrieve env from planning request!')
        
        # serialize environment
        envdict = prpy.serialization.serialize_environment(env, uri_only=True)
        
        # serialize planning request
        reqdict = {}
        reqdict['method'] = method # string
        reqdict['args'] = []
        reqdict['planner'] = str(self.planner)

        for arg in args:
            try:
                reqdict['args'].append(prpy.serialization.serialize(arg))
            except prpy.exceptions.UnsupportedTypeSerializationException as ex:
                reqdict['args'].append(str(ex))
        reqdict['kw_args'] = {}
        for key,value in kw_args.items():
            key = prpy.serialization.serialize(key)
            try:
                reqdict['kw_args'][key] = prpy.serialization.serialize(value)
            except prpy.exceptions.UnsupportedTypeSerializationException as ex:
                reqdict['kw_args'][key] = 'Error: ' + str(ex)
        
        # get ready to serialize result
        resdict = {}
        
        try:
            plan_fn = getattr(self.planner, method)
            traj = plan_fn(*args, **kw_args)

            from prpy.util import GetTrajectoryTags
            from prpy.planning.base import Tags
            tags = GetTrajectoryTags(traj)
            resdict['ok'] = True
            resdict['planner_used'] = tags[Tags.PLANNER]
            resdict['traj_first'] = list(map(float,traj.GetWaypoint(0)))
            resdict['traj_last'] = list(map(float,traj.GetWaypoint(traj.GetNumWaypoints()-1)))

            return traj
            
        except prpy.planning.PlanningError as ex:
            resdict['ok'] = False
            resdict['exception'] = str(ex)
            raise
        
        except:
            resdict['ok'] = False
            resdict['exception'] = 'unknown exception type'
            raise
        
        finally:
            # create yaml dictionary to be serialized
            yamldict = {}
            yamldict['environment'] = envdict
            yamldict['request'] = reqdict
            yamldict['result'] = resdict
            fp = open(fn,'w')
            yaml.safe_dump(yamldict, fp)
            fp.close()
        
            # save filename as tag
            if resdict['ok']:
                from prpy.util import SetTrajectoryTags
                from prpy.planning.base import Tags
                SetTrajectoryTags(traj, {Tags.LOGFILE: fn}, append=True)
        
