from map import Containment, Space, Touching

"""
The Mental_map class is adapted from the linked_list class from
https://github.com/bfaure/Python3_Data_Structures/blob/master/Linked_List/main.py
"""


class Time_step:

    def __init__(self, containment, space, touching):
        self.containment = containment
        self.space = space
        self.touching = touching
        self.action = {"PTRANS": [], "PSTOP": [],
                       "INGEST": [], "EXPEL": [], "STATECHANGE": []}
        self.next = None


class Mental_model:
    def __init__(self, containment, space, touching):
        self.head = Time_step(containment, space, touching)

    def advance_time(self):
        """copy the current Time_step to a new Time_step"""
        cur = self.head
        while cur.next is not None:
            cur = cur.next
        new_node = Time_step(cur.containment.copy(),
                             cur.space.copy(), cur.touching.copy())
        cur.next = new_node

    # def append(self, containment, space):
    #     """add a new Time_step"""
    #     new_node = Time_step(containment, space)
    #     cur = self.head
    #     while cur.next is not None:
    #         cur = cur.next
    #     cur.next = new_node

    def length(self):
        """return the total number of Time_steps"""
        cur = self.head
        total = 1
        while cur.next is not None:
            total += 1
            cur = cur.next
        return total

    # def display(self):
    #     """print the whole linked_list"""
    #     elems = []
    #     cur_node = self.head
    #     while cur_node.next is not None:
    #         cur_node = cur_node.next
    #         elems.append(cur_node.data)
    #     print(elems)

    def get(self, index):
        """Returns the value of the Time_step at a certain index"""
        if index >= self.length() or index < 0:
            print("ERROR: Index out of range!")
            return None
        cur_idx = 0
        cur_node = self.head
        while True:
            if cur_idx == index:
                return cur_node
            cur_node = cur_node.next
            cur_idx += 1

    def get_current(self):
        """Return the current/last Time_step"""
        cur = self.head
        while cur.next is not None:
            cur = cur.next
        return cur

    def get_containment(self, index):
        """Returns the containment map of the time_stamp at index"""
        return self.get(index).containment

    def get_space(self, index):
        """Returns the space map of the time_stamp at index"""
        return self.get(index).space

    def get_touching(self, index):
        """Returns the space map of the time_stamp at index"""
        return self.get(index).touching

    def add_object(self, object):
        """add object to all maps of the last time_step"""
        cur = self.get_current()
        cur.containment.add_object(object)
        cur.space.add_object(object)
        cur.touching.add_object(object)

    def contain(self, edge):
        """add an adge to the containment map of the last time_step"""
        cur = self.get_current()

        for object in edge:
            if object not in cur.containment._graph_dict:
                cur.containment.add_object(object)
                cur.space.add_object(object)
                cur.touching.add_object(object)
        cur.containment.contain(edge)

    def x_contain(self, edge):
        """remove an adge from the containment map of the last time_step"""
        cur = self.get_current()
        cur.containment.x_contain(edge)

    def above(self, edge):
        """add an adge to the space map of the last time_step"""
        cur = self.get_current()

        for object in edge:
            if object not in cur.containment._graph_dict:
                cur.containment.add_object(object)
                cur.space.add_object(object)
                cur.touching.add_object(object)
        cur.space.above(edge)

    def x_above(self, edge):
        """remove an adge from the space map of the last time_step"""
        cur = self.get_current()
        cur.space.x_above(edge)

    def under(self, edge):
        """add an adge to the space map of the last time_step"""
        cur = self.get_current()

        for object in edge:
            if object not in cur.containment._graph_dict:
                cur.containment.add_object(object)
                cur.space.add_object(object)
                cur.touching.add_object(object)
        cur.space.under(edge)

    def x_under(self, edge):
        """remove an adge from the space map of the last time_step"""
        cur = self.get_current()
        cur.space.x_under(edge)

    def touch(self, edge):
        """add an adge to the touching map of the last time_step"""
        cur = self.get_current()

        for object in edge:
            if object not in cur.containment._graph_dict:
                cur.containment.add_object(object)
                cur.space.add_object(object)
                cur.touching.add_object(object)
        cur.touching.touch(edge)

    def x_touch(self, edge):
        """remove an adge from the touching map of the last time_step"""
        cur = self.get_current()
        cur.touching.x_touch(edge)

    def print(self, index):
        """ print the containment mape and space map
            of the Time_step at a certain index
        """
        time_step = self.get(index)

        print("\nCONTAINMENT RELATIONSHIP ---------------------")
        print(time_step.containment)

        print("\nSPATIAL RELATIONSHIP -------------------------")
        print(time_step.space)

        print("\nTOUCHING RELATIONSHIP ------------------------")
        print(time_step.touching)

        print("\nPRIMITIVE ACTIONS ----------------------------")
        for action in time_step.action:
            print(action, time_step.action[action])

    def __getitem__(self, index):
        """Allows for bracket operator syntax (i.e. a[0] = first item)"""
        return self.get(index)

    def PTRANS(self, object, to=None, From=None):
        cur = self.get_current()
        cur.action["PTRANS"].append({})
        cur.action["PTRANS"][-1]["object"] = object
        cur.action["PTRANS"][-1]["to"] = to
        cur.action["PTRANS"][-1]["from"] = From

    def PSTOP(self, object):
        cur = self.get_current()
        cur.action["PSTOP"].append({})
        cur.action["PSTOP"][-1]["object"] = object

    def INGEST(self, object, container):
        cur = self.get_current()
        cur.action["INGEST"].append({})
        cur.action["INGEST"][-1]["object"] = object
        cur.action["INGEST"][-1]["container"] = container

    def EXPEL(self, object, container):
        cur = self.get_current()
        cur.action["EXPEL"].append({})
        cur.action["EXPEL"][-1]["object"] = object
        cur.action["EXPEL"][-1]["container"] = container

    def STATECHANGE(self, object, to):
        cur = self.get_current()
        cur.action["STATECHANGE"].append({})
        cur.action["STATECHANGE"][-1]["object"] = object
        cur.action["STATECHANGE"][-1]["to"] = to