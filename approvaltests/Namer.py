import inspect
import os
import pytest


class Namer(object):
    ClassName = ''
    MethodName = ''
    Directory = ''

    APPROVED = '.approved'
    RECEIVED = '.received'

    def __init__(self, extension='.txt'):
        self.extension_with_dot = extension
        self.set_for_stack(inspect.stack(1))

    def get_class_name(self):
        return self.ClassName

    def get_method_name(self):
        return self.MethodName

    def get_directory(self):
        return self.Directory

    def get_basename(self):
        class_name = "" if (self.ClassName is None) else (self.ClassName + ".")
        return os.path.join(self.Directory, class_name + self.MethodName)

    def get_received_filename(self, basename=None):
        basename = basename or self.get_basename()
        return basename + self.RECEIVED + self.extension_with_dot

    def get_approved_filename(self, basename=None):
        basename = basename or self.get_basename()
        return basename + self.APPROVED + self.extension_with_dot

    def set_for_stack(self, caller):
        frame = self.get_test_frame(caller)
        stacktrace = caller[frame]
        self.MethodName = stacktrace[3]
        self.ClassName = self.get_class_name_for_frame(stacktrace)
        self.Directory = os.path.dirname(stacktrace[1])

    def get_class_name_for_frame(self, stacktrace):
        if "self" not in stacktrace[0].f_locals:
            return os.path.splitext(os.path.basename(stacktrace[1]))[0]
        else:
            return stacktrace[0].f_locals["self"].__class__.__name__

    def get_test_frame(self, caller):
        frameNumber = 1
        for index, frame in enumerate(caller):
            if self.is_test_method(frame):
                frameNumber = index

        return frameNumber

    def is_test_method(self, frame):
        is_unittest_test = ("self" in frame[0].f_locals
               and "_testMethodName" in frame[0].f_locals["self"].__dict__
               and frame[3] is not "__call__"
               and frame[3] is not "run")

        is_pytest_test = frame[3].startswith("test_")

        return is_unittest_test or is_pytest_test
