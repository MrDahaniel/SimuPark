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
        maxWaitTime: int,
        minWaitTime: int,
        maxStay: int,
        minStay: int,
        attractionChance: float,
    ) -> None:
        self.name: str = name
        self.maxWaitTime: int = maxWaitTime
        self.minWaitTime: int = minWaitTime
        self.maxStay: int = maxStay
        self.minStay: int = minStay
        self.attractionChance: float = attractionChance


class Person:
    def __init__(self, id: int, arrivalTime: int, archetype: Archetype) -> None:
        # General info
        self.id: str = id
        self.timeLeftInActivity: int = 0
        self.currentActivity: str = ""

        # Used for statistics
        self.attractionsExperienced: int = 0
        self.totalWaitTime: int = 0
        self.arrivalTime: int = arrivalTime
        self.thingsDone: list[str] = []

        # Archetype defined
        self.archetype: str = archetype.name
        self.departureTime: int = (
            randint(archetype.minStay, archetype.maxStay) + arrivalTime
        )
        self.maxWait: int = randint(archetype.minWaitTime, archetype.maxWaitTime)
        self.attractionChance: float = archetype.attractionChance

        # !!! DELETE LATER !!!
        self.choicesMade: int = 0

    # General functions, used in all scenarios

    def report(self):
        return f"id: {self.id}  arvTime: {self.arrivalTime} thingsDone: {self.thingsDone} attrExp: {self.attractionsExperienced} "

    # Person does an activity, it gets set to idle while doing so
    def doActivity(self, name: str, duration: int):
        self.currentActivity = name
        self.timeLeftInActivity = duration

        # !!!!!!!!!!!!! DELETE LATER !!!!!!!!!!!!!!!!!!
        self.thingsDone.append(name)

    # Person rides an attraction, it adds the activity done to the list
    # and sets it to idle for the duration of the ride
    def rideAttraction(self, name: str, duration: int):
        self.thingsDone.append(name)
        self.currentActivity = name
        self.attractionsExperienced += 1
        self.timeLeftInActivity = duration

    def chooseWhatToDo(
        self,
        activities: list[Activity],
        attractions: list[Attraction],
    ) -> Union[Activity, Attraction]:
        # If true, person decides to do an attraction; else it's an activity
        if self.flipWeightedCoin():
            return self.spinRoulette(attractions)
        else:
            return self.spinRoulette(activities)

    def flipWeightedCoin(self) -> bool:
        # If true, person decides to do an attraction; else it's an activity
        return random.uniform(low=0, high=1) < self.attractionChance

    def spinRoulette(
        self,
        options: list[Union[Activity, Attraction]],
    ) -> Union[Activity, Attraction]:
        totalPopularity: int = sum([activity.popularity for activity in options])
        weighedPopularity: list[float] = [
            activity.popularity / totalPopularity for activity in options
        ]
        return choices(population=options, weights=weighedPopularity, k=1)[0]

    def checkAttraction(self, attraction: Attraction):
        # This is the vanilla case, we just need to check if the wait time
        # is less than the max wait time.
        # This also can be used if the person doesn't have a turboPass
        # in the Salitre FP scenario
        if attraction.queue.waitTime < self.maxWait:
            self.timeLeftInActivity = -1
            attraction.addToQueue(self, "NORMAL")

    def joinQueue(self, attraction: Attraction, queue: str = "NORMAL"):
        # timeLeftInActivity is set to -1 to indicate person being in a queue, this way
        # it can be added to the totalWaitTime on the next cycle
        self.timeLeftInActivity = -1
        attraction.addToQueue(self, queue)

    def checkLeavePark(self, time: int):
        # This sets the timeLeftInActivity to -2
        # this scenario implies the guest left the park, they are ignored during the
        # check when time passes
        if self.timeLeftInActivity == -2:
            pass
        elif self.departureTime <= time and self.timeLeftInActivity != 0:
            self.timeLeftInActivity = -2
            self.departureTime = time

    # Disney FastPass specific
    def checkAttractionFP(self, attraction: Attraction):
        # First, we check the wait time for the attraction
        # if the wait time is less than 30 minutes, person will join
        if attraction.queue.waitTime <= 30:
            # We set the timeLeftInActivity to -1 to identify as the person
            # is waiting on queue
            self.timeLeftInActivity = -1
            attraction.addToQueue(self, "NORMAL")
