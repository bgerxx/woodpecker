'''

All scheduler operations for test.

@author: quarkonics
'''

import apibinding.inventory as inventory
import apibinding.api_actions as api_actions
import zstackwoodpecker.test_util as test_util
import account_operations
import config_operations

import os
import inspect

def create_scheduler_job(name, description, target_uuid, type, parameters, session_uuid = None):
    action = api_actions.CreateSchedulerJobAction()
    action.name = name
    action.description = description
    action.targetResourceUuid = target_uuid
    action.type = type
    action.parameters = parameters
    test_util.action_logger('Create [Scheduler Job:] %s [%s] %s' % (name, target_uuid, type))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Scheduler Job:] %s is created.' % evt.inventory.uuid)
    return evt.inventory

def del_scheduler_job(uuid, session_uuid = None):
    action = api_actions.DeleteSchedulerJobAction()
    action.uuid = uuid
    test_util.action_logger('Delete [Scheduler Job:] %s' % uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Scheduler Job:] %s is deleted.' % uuid)

def create_scheduler_trigger(name, start_time, repeat_count, interval, type, session_uuid = None):
    action = api_actions.CreateSchedulerTriggerAction()
    action.name = name
    action.startTime = start_time
    action.repeatCount = repeat_count
    action.schedulerInterval = interval
    action.schedulerType = type
    test_util.action_logger('Create [Scheduler Trigger:] %s [%s] %s %s' % (name, start_time, repeat_count, interval))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Scheduler Trigger:] %s is created.' % evt.inventory.uuid)
    return evt.inventory

def del_scheduler_trigger(uuid, session_uuid = None):
    action = api_actions.DeleteSchedulerTriggerAction()
    action.uuid = uuid
    test_util.action_logger('Delete [Scheduler Trigger:] %s' % uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Scheduler Trigger:] %s is deleted.' % uuid)

def add_scheduler_job_to_trigger(trigger_uuid, job_uuid, session_uuid = None):
    action = api_actions.AddSchedulerJobToSchedulerTriggerAction()
    action.schedulerTriggerUuid = trigger_uuid
    action.schedulerJobUuid = job_uuid
    test_util.action_logger('Add [Scheduler Job:] %s to [Scheduler Trigger:] %s ' % (job_uuid, trigger_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Scheduler Job:] %s is added to [Scheduler Trigger:] %s.' % (job_uuid, trigger_uuid))

def remove_scheduler_job_from_trigger(trigger_uuid, job_uuid, session_uuid = None):
    action = api_actions.RemoveSchedulerJobFromSchedulerTriggerAction()
    action.schedulerTriggerUuid = trigger_uuid
    action.schedulerJobUuid = job_uuid
    test_util.action_logger('Remove [Scheduler Job:] %s from [Scheduler Trigger:] %s ' % (job_uuid, trigger_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 

def delete_scheduler(uuid, session_uuid = None):
    action = api_actions.DeleteSchedulerAction()
    action.uuid = uuid
    test_util.action_logger('Delete [Scheduler:] %s' % uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Scheduler:] %s is deleted.' % uuid)
    return evt

def update_scheduler(uuid, type, name, start_date=None, interval=None, repeatCount=None, cron=None, session_uuid = None):
    action = api_actions.UpdateSchedulerAction()
    action.uuid = uuid
    action.schedulerType = type
    action.schedulerName = name
    action.startTime = start_date
    action.schedulerInterval = interval
    action.repeatCount = repeatCount
    action.cronScheduler = cron

    test_util.action_logger('Update [Scheduler:] %s [schdulerType:] %s [schdulerName:] %s [startDate:] %s [interval:] %s [repeatCount:] %s [cron:] %s' \
                    % (uuid, type, name, start_date, interval, repeatCount, cron))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Scheduler:] %s is updated.' % uuid)
    return evt

def change_scheduler_state(uuid, state, session_uuid = None):
    action = api_actions.ChangeSchedulerStateAction()
    action.uuid = uuid
    action.stateEvent = state
    test_util.action_logger('Change [Scheduler:] %s' % uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid)
    test_util.test_logger('[Scheduler:] %s is changed to %s.' % (uuid, state))
    return evt

def get_current_time(session_uuid = None):
    action = api_actions.GetCurrentTimeAction()
    test_util.action_logger('GetCurrentTime')
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    return evt
