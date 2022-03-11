from __future__ import annotations
from random import uniform, randint, choices
from numpy import random
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from simuPark.park import Activity, Attraction


class Archetype:
    def __init__(
        self,
        name: str,
        max_wait_time: int,
        min_wait_time: int,
        max_stay: int,
        min_stay: int,
        attraction_chance: float,
    ) -> None:
        self.name: str = name
        self.max_wait_time: int = max_wait_time
        self.min_wait_time: int = min_wait_time
        self.max_stay: int = max_stay
        self.min_stay: int = min_stay
        self.attraction_chance: float = attraction_chance


class Person:
    def __init__(
        self,
        id: int,
        arrival_time: int,
        archetype: Archetype,
        park_closing_time: int = None,
    ) -> None:
        # General info
        self.id: str = id
        self.time_left_in_activity: int = 0
        self.current_activity: str = ""

        # Used for statistics
        self.attractions_experienced: int = 0
        self.total_wait_time: int = 0
        self.arrival_time: int = arrival_time
        self.things_done: list[str] = []

        # Archetype defined
        self.archetype: str = archetype.name
        self.departure_time: int = (
            randint(archetype.min_stay, archetype.max_stay) + arrival_time
        )
        self.max_wait: int = randint(archetype.min_wait_time, archetype.max_wait_time)
        self.attraction_chance: float = archetype.attraction_chance

        # Handle time after park closes
        if park_closing_time is not None and park_closing_time < self.departure_time:
            self.departure_time = park_closing_time

    # General functions, used in all scenarios

    def report(self):
        return f"id: {self.id}  arvTime: {self.arrival_time} things_done: {self.things_done} attrExp: {self.attractions_experienced} "

    def do_activity(self, name: str, duration: int):
        # Person does an activity, it gets set to idle while doing so
        self.current_activity = name
        self.time_left_in_activity = duration

    def ride_attraction(self, name: str, duration: int):
        # Person rides an attraction, it adds the activity done to the list
        # and sets it to idle for the duration of the ride
        self.things_done.append(name)
        self.current_activity = name
        self.attractions_experienced += 1
        self.time_left_in_activity = duration

    def choose_what_to_do(
        self,
        activities: list[Activity],
        attractions: list[Attraction],
    ) -> Union[Activity, Attraction]:
        # If true, person decides to do an attraction; else it's an activity
        if self.flip_weighted_coin():
            return self.spin_roulette(attractions)
        else:
            return self.spin_roulette(activities)

    def flip_weighted_coin(self) -> bool:
        # If true, person decides to do an attraction; else it's an activity
        return random.uniform(low=0, high=1) < self.attraction_chance

    def spin_roulette(
        self,
        options: list[Union[Activity, Attraction]],
    ) -> Union[Activity, Attraction]:
        # We get the sum of all popularity points in the park
        total_popularity: int = sum([activity.popularity for activity in options])

        # And we calculate the popularity of each of the attractions
        weighed_popularity: list[float] = [
            activity.popularity / total_popularity for activity in options
        ]

        # Finally the person makes a choice of what they want to do
        return choices(population=options, weights=weighed_popularity, k=1)[0]

    def check_attraction(self, attraction: Attraction):
        # This is the vanilla case, we just need to check if the wait time
        # is less than the max wait time.
        # This also can be used if the person doesn't have a turboPass
        # in the Salitre FP scenario.
        if attraction.queue.wait_time < self.max_wait:
            self.time_left_in_activity = -1
            attraction.add_to_queue(self, "NORMAL")

    def join_queue(self, attraction: Attraction, queue: str = "NORMAL"):
        # time_left_in_activity is set to -1 to indicate person being in a queue, this way
        # it can be added to the total_wait_time on the next cycle
        self.time_left_in_activity = -1
        attraction.add_to_queue(self, queue)

    def check_leave_park(self, time: int):
        # This sets the time_left_in_activity to -2
        # this scenario implies the guest left the park, they are ignored during the
        # check when time passes
        if self.time_left_in_activity == -2:
            pass
        elif self.departure_time <= time and self.time_left_in_activity != 0:
            self.time_left_in_activity = -2
            self.departure_time = time


class DisneyPerson(Person):
    def __init__(
        self, 
        id: int, 
        arrival_time: int, 
        archetype: Archetype, 
        park_closing_time: int = None, 
    ) -> None:
        super().__init__(id, arrival_time, archetype, park_closing_time)

        self.fastpass: Union[tuple[str, int], None] = None
        self.fastpass_used: int = 0

    def choose_what_to_do(
        self,
        activities: list[Activity],
        attractions: list[Attraction],
        time: int
    ) -> Union[Activity, Attraction]:
        # First, we need to check for the return window of the fastpass
        if self.fastpass is not None and self.fastpass[1] - time < 5:
            return [attraction for attraction in attractions if attraction.name == self.fastpass[0]][0]

        else:
            # If true, person decides to do an attraction; else it's an activity
            if self.flip_weighted_coin():
                return self.spin_roulette(attractions)
            else:
                return self.spin_roulette(activities)

    def check_attraction(self, attraction: Attraction, time: int):

        if (self.fastpass is not None 
            and self.fastpass[0] == attraction.name 
            and self.fastpass[1] - time < 5
        ):
            self.time_left_in_activity = -1
            self.fastpass_used += 1
            self.fastpass = None
            attraction.add_to_queue(self, "DFP")

        # Now we check the wait time for the attraction
        # if the wait time is less than 30 minutes, and lower than
        # their max wait time, they will join the normal queue
        # if the person has fastpass, they check if they still can make it in time
        elif (
            attraction.queue.wait_time <= 30
            and attraction.queue.wait_time <= self.max_wait
        ):
            if (
                self.fastpass is None 
                or (self.fastpass is not None 
                    and attraction.queue.wait_time + 5 < self.fastpass[1] - time)
                ):
                # We set the time_left_in_activity to -1 to identify as the person
                # is waiting on queue
                self.time_left_in_activity = -1
                attraction.add_to_queue(self, "NORMAL")

        # In this case, the wait time is more than 30 mins, person checks for fastpass

        elif self.fastpass is None and attraction.fast_pass_machine._handout_fastpass(
            person=self, time=time
        ):
            # If it's true, the person receives a FP, they return to the "wat do" pool
            return

        # If the return is false, it means we got no fastpass available
        # The person now checks for the normal queue, if the wait time is lower than the max wait time
        # And the wait time still let's them get in time for their return window
        elif (
            attraction.queue.wait_time <= self.max_wait
            and self.fastpass is not None
            and attraction.queue.wait_time + 5 < self.fastpass[1] - time
        ):
            self.time_left_in_activity = -1
            attraction.add_to_queue(self, "NORMAL")
        