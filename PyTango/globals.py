################################################################################
##
## This file is part of PyTango, a python binding for Tango
## 
## http://www.tango-controls.org/static/PyTango/latest/doc/html/index.html
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
## 
## PyTango is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## PyTango is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
## 
## You should have received a copy of the GNU Lesser General Public License
## along with PyTango.  If not, see <http://www.gnu.org/licenses/>.
##
################################################################################

"""
This is an internal PyTango module.
"""

__all__ = [ "get_class", "get_classes", "get_cpp_class", "get_cpp_classes",
            "get_constructed_class", "get_constructed_classes",
            "class_factory", "delete_class_list",
            "class_list", "cpp_class_list", "constructed_class", "delete_class",
            "get_device_class_from_device_impl",
            "get_device_class_from_device_impl_class"]
            
__docformat__ = "restructuredtext"

# list of tuple<DeviceClass class, DeviceImpl class, tango device class name>
class_list = []

# list of tuple<DeviceClass name, tango device class name>
cpp_class_list = []

# list of DeviceClass objects, one for each registered device class
constructed_class = []

def get_classes():
    global class_list
    return class_list

def get_class(name):
    for klass_info in get_classes():
        if klass_info[2] == name:
            return klass_info
    return None

def get_class_by_class(klass):
    for klass_info in get_classes():
        if klass_info[0] == klass:
            return klass_info
    return None

def get_cpp_classes():
    global cpp_class_list
    return cpp_class_list

def get_cpp_class(name):
    for klass_info in get_cpp_classes():
        if klass_info[1] == name:
            return klass_info
    return None

def get_constructed_classes():
    global constructed_class
    return constructed_class

def get_constructed_class(name):
    for klass in get_constructed_classes():
        if klass.get_name() == name:
            return klass
    return None

def get_constructed_class_by_class(klass):
    for k in get_constructed_classes():
        if k.__class__ == klass:
            return k
    return None

def get_device_class_from_device_impl(device_impl):
    return get_device_class_from_device_impl_class(device_impl.__class__)

def get_device_class_from_device_impl_class(device_impl_class):
    for info in get_classes():
        if info[1] == device_impl_class:
            return get_constructed_class_by_class(info[0])

#
# A method to delete Tango classes from Python
#

def delete_class_list():
    global constructed_class
    if len(constructed_class) != 0:
        del(constructed_class[:])

def delete_class(device_class):
    constructed_classes = get_constructed_classes()
    try:
        constructed_classes.remove(device_class)
    except ValueError:
        pass

#
# A generic class_factory method
#

def class_factory():
    local_class_list = get_classes()
    local_cpp_class_list = get_cpp_classes()

    if ((len(local_class_list) + len(local_cpp_class_list)) == 0):
        print('Oups, no Tango class defined within this device server !!!')
        print('Sorry, but I exit')
        import sys
        sys.exit()

    # Call the delete_class_list function in order to clear the global
    # constructed class Python list. This is necessary only in case of
    # ServerRestart command
    delete_class_list()

    local_constructed_class = get_constructed_classes()
    for class_info in local_class_list:
        device_class_class = class_info[0]
        tango_device_class_name = class_info[2]
        device_class = device_class_class(tango_device_class_name)
        local_constructed_class.append(device_class)

