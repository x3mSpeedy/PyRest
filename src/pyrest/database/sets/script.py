# encoding: utf-8
# author:   Jan Hybs
import time
import uuid

import persistent
from persistent.list import PersistentList

from pyrest import db
from pyrest.database.btree import BTreeEx
from pyrest.database.dbutils import DBUtils
from pyrest.database.sets.command import CommandManagementApplication


class ScriptResult (object):
    _classes = ['default', 'success', 'warning', 'danger']
    _strings = ['No results', 'Success', 'Running', 'Error']

    unknown = 0
    success = 1
    running = 2
    error = 3


class Script (persistent.Persistent):
    def __init__ (self):
        self.id = None
        self.job_id = None
        self.timestamp = None
        self.result = None
        self.commands = PersistentList ()
        self.duration = None

    def get_commands (self):
        return [db.commands.get (command_id, None) for command_id in self.commands]

    def get_result_cls (self):
        return ScriptResult._classes[self.result]

    def get_result_str (self):
        return ScriptResult._strings[self.result]

    def __repr__ (self):
        return u"<Script {self.id} '{self.timestamp}', commands=[{self.commands}]>".format (self=self)

    def __str__ (self):
        return self.__repr__ ()

    def __unicode__ (self):
        return self.__repr__ ()

    def as_dict (self):
        return dict (
            id=self.id, job_id=self.job_id,
            timestamp=int(self.timestamp) if self.timestamp else None, result=self.result,
            duration=self.duration,
            commands=[command.as_dict () for command in self.commands]
        )


class ScriptManagementApplication (BTreeEx):
    @staticmethod
    def create (*args, **kwargs):
        script = Script ()
        script.id = DBUtils.id (kwargs)
        script.job_id = kwargs.get ('job_id')
        script.timestamp = kwargs.get ('timestamp')
        script.result = kwargs.get ('result', ScriptResult.unknown)
        script.duration = kwargs.get ('duration')

        commands = kwargs.get ('commands', '').splitlines ()
        script.commands = CommandManagementApplication.create_command_list (script_id=script.id, commands=commands)
        return script

