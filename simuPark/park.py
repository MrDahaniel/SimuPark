from math import ceil, gamma
from random import choice
from typing import Callable, Tuple, Union
from unicodedata import name
from simuPark.person import (
    DisneyPerson,
    FakeTimesPerson,
    Person,
    Archetype,
    SalitrePerson,
)
from simuPark.constants import ACTIVITIES, ARCHETYPES, ATTRACTIONS
from tqdm import tqdm
import numpy as np
from warnings import warn


class Queue:
    def __init__(self, type: str = "NORMAL") -> None:
        self.type: str = type
        self.wait_time: int = 0
        self.top_wait_time: int = 0
        self.in_queue: list[Person] = []
        self.fake_wait_time: int = 0

        self.max_in_queue = 0

    def serve(self, name: str, n_people: int, duration: int):
        # In this scenario, the number of people in queue is less or the same as the
        # service rate of the attraction, everyone on the queue is served.
        if n_people > len(self.in_queue):
            n_people = len(self.in_queue)

        for _i in range(n_people):
            person: Person = self.in_queue.pop(0)
            person.ride_attraction(name=name, duration=duration)

        return n_people

    def add_to_queue(self, person: Person):
        self.in_queue.append(person)

    def _update_wait_time(self, service_rate: int):
        new_wait_time = 5 * round((len(self.in_queue) / (service_rate / 60)) / 5)
        self.top_wait_time = max(new_wait_time, self.wait_time)
        self.wait_time = new_wait_time

    def _update_fake_wait_time(self, service_rate: int):
        self._update_wait_time(service_rate=service_rate)
        if 20 <= self.wait_time <= 30:
            self.fake_wait_time = self.wait_time + 10

        elif 35 <= self.wait_time <= 45:
            self.fake_wait_time = self.wait_time + 15

        elif 50 <= self.wait_time:
            self.fake_wait_time = self.wait_time + 25


class TotalQueue(Queue):
    def _update_max_in_queue(self, whole_queue: list[Person]):
        self.max_in_queue = max(self.max_in_queue, len(whole_queue))

    def _update_wait_time(self, service_rate: int, whole_queue: list[Person]):
        self._update_max_in_queue(whole_queue=whole_queue)

        new_wait_time = 5 * round((len(whole_queue) / (service_rate / 60)) / 5)
        self.top_wait_time = max(new_wait_time, self.wait_time)
        self.wait_time = new_wait_time


class FastPassMachine:
    def __init__(
        self,
        attraction_name: str,
        service_rate: int,
        hours_open: int,
        fastpass_pool_size: float = 0.3,
    ) -> None:
        self.attraction: str = attraction_name
        self.fastpass_pool: int = [
            int(service_rate * fastpass_pool_size / 4)
            for _hour in range(hours_open * 4)
        ]
        self.quarter_handouts: list[int] = [0 for _hour in range(hours_open * 4)]

    def _handout_fastpass(self, person: Person, time: int) -> bool:
        # We calculate the current hour and the minimun return window
        current_quarter: int = int(np.floor(time / 15))
        min_fastpass_quarter = current_quarter + 1

        # first we check if the person currently has a fastpass ticket
        if person.fastpass is None:
            try:
                for quarter in range(min_fastpass_quarter, len(self.fastpass_pool) - 1):
                    # if not, the person gets a fast pass with at least an hour return time
                    if self.quarter_handouts[quarter] < self.fastpass_pool[quarter]:
                        person.fastpass = (
                            self.attraction,
                            int(quarter * 15 + np.random.uniform(1, 15)),
                        )
                        self.quarter_handouts[quarter] += 1
                        return True

            # if out of bounds, all fastpass for the day have been supplied
            except IndexError:
                pass

        return False


class Activity:
    def __init__(self, name: str, popularity: int, duration: int) -> None:
        self.name: str = name
        self.duration: int = duration
        self.popularity: int = popularity


class Attraction(Activity):
    def __init__(
        self,
        name: str,
        popularity: int,
        duration: int,
        service_rate: int,
        alt_queue: str = None,
        hours_open: int = 16,
        fastpass_pool_size: float = 0.3,
        fastpass_serve_size: float = 0.6,
    ) -> None:
        super().__init__(name, popularity, duration)
        self.service_rate: int = service_rate
        self.fake_wait_time: int = 0
        self.queue: Queue = Queue()
        self.fastpass_serve_size: float = fastpass_serve_size

        self.time_until_service: int = duration

        self.total_people_served: int = 0

        if alt_queue in ["DFP", "SFP"]:
            self.alt_queue: Queue = Queue(type=alt_queue)
            self.queue: TotalQueue = TotalQueue()

            if alt_queue == "DFP":
                self.fast_pass_machine: FastPassMachine = FastPassMachine(
                    attraction_name=name,
                    service_rate=service_rate,
                    hours_open=hours_open,
                    fastpass_pool_size=fastpass_pool_size,
                )

    def serve(self):
        # We calculate the amount of people the attraction can serve each minute
        n_people_to_serve = int(self.duration * np.floor(self.service_rate / 60))
        # We tell out Queue to serve the amount of people given
        # And the duration of the ride

        if self.time_until_service != 0:
            # We decrease time left until the next cycle
            self.time_until_service -= 1

        elif self.time_until_service == 0:
            # We reset the time until the next cycle
            self.time_until_service = self.duration

            # Serve the queue
            self.total_people_served += self.queue.serve(
                name=self.name, n_people=n_people_to_serve, duration=self.duration
            )

    def add_to_queue(self, person: Person, queue: str):
        if queue == "NORMAL":
            self.queue.add_to_queue(person)
        else:  # queue in ["DFP", "SFP"]
            self.alt_queue.add_to_queue(person)

    def serve_with_fastpass(self):
        # We calculate the amount of people the attraction can serve each minute
        n_people_to_serve: int = int(self.duration * np.floor(self.service_rate / 60))

        # Then we calculate the fastpass people to serve,
        n_fastpass_serve: int = int(
            np.floor(n_people_to_serve * self.fastpass_serve_size)
        )

        # We check if the number of people in the fast pass line is lower
        # than the number of the serve size. If so, we serve all fastpass holders.
        if n_fastpass_serve > len(self.alt_queue.in_queue):
            n_fastpass_serve = len(self.alt_queue.in_queue)

        # And we calculate the number of people to serve on the normal line
        # this value is tied to the number of people being served in the fastpass
        # lane
        n_normal_serve: int = n_people_to_serve - n_fastpass_serve

        if self.time_until_service != 0:
            self.time_until_service -= 1

        elif self.time_until_service == 0:
            self.time_until_service = self.duration

            # Finally, we make both queues serve the guests
            self.total_people_served += self.queue.serve(
                name=self.name, n_people=n_normal_serve, duration=self.duration
            )
            self.total_people_served += self.alt_queue.serve(
                name=self.name, n_people=n_fastpass_serve, duration=self.duration
            )


class Park:
    def __init__(
        self,
        attraction_dict: dict[str, dict] = ATTRACTIONS,
        activities_dict: dict[str, dict] = ACTIVITIES,
        archetype_dict: dict[str, dict] = ARCHETYPES,
        fn: Callable[[float], float] = lambda x, k: k ** x * np.exp(-k) / gamma(x + 1),
        hours_open: int = 16,
        fastpass_pool_size: float = 0.3,
    ) -> None:
        self.current_time: int = 0
        self.closing_time: int = 60 * hours_open
        self.attractions: list[Attraction] = self._handle_attractions(
            attraction_dict=attraction_dict,
            alt_queue=None,
            hours_open=hours_open,
            fastpass_pool_size=fastpass_pool_size,
        )
        self.activities: list[Activity] = self._handle_activities(activities_dict)
        self.guest_archetypes: list[Archetype] = self._handle_archetypes(archetype_dict)
        self.guests: list[Union[Person, DisneyPerson]] = []
        self.function: Callable[[float], float] = fn

    def start_day(self, max_entry_rate: int, wait_time_update: int = 5) -> None:
        # First, we create the guests
        self._generate_entry_events(max_entry_rate, self.closing_time)

        # Day starts, time starts running minute per minute depending in the
        # hours open
        for minute in tqdm(range(self.closing_time)):
            # Every 5 minutes, all queue times update for the guests to check
            if minute % wait_time_update == 0:
                self._update_wait_times()

            for guest in self.guests:
                # Guest hasn't arrived to the park yet
                if guest.arrival_time > minute:
                    continue

                # print(f"Guest id : {guest.id}")
                guest.check_leave_park(minute)
                # This case is the 'left the park' state, they're skipped
                if guest.time_left_in_activity == -2:
                    # print("left park")
                    continue

                # In this case, the guest is in a queue, they're are skipped
                # as they're not able to change selections. TotalWaitTime increases.
                elif guest.time_left_in_activity == -1:
                    # print("On queue")
                    guest.total_wait_time += 1

                # On this case, the guest is currently doing an activity
                # or riding an attraction. Time passes.
                elif guest.time_left_in_activity > 0:
                    # print("Doing activity")
                    guest.time_left_in_activity -= 1

                # In this scenario, they're looking for something to do
                # They're free to choose based on their archetype
                elif guest.time_left_in_activity == 0:
                    selection = guest.choose_what_to_do(
                        self.activities,
                        self.attractions,
                    )

                    if isinstance(selection, Attraction):
                        guest.check_attraction(selection, self.closing_time - minute)
                        # guest.do_activity(selection.name, selection.duration)
                        # print("Chose attraction")
                    elif isinstance(selection, Activity):
                        # print("Chose activity")
                        guest.do_activity(selection.name, selection.duration)

                # print("")

            self._serve_guests()

    def _handle_archetypes(self, archetype_dict: dict[str, dict]) -> list[Archetype]:
        # setArchetypes handles the creation of the archetypes
        # to be used during the simulation.

        if not bool(archetype_dict):
            raise IndexError("Dictionary is Empty") from None

        archetype_list: list[Archetype] = []

        for name, details in archetype_dict.items():
            archetype: Archetype = Archetype(
                name=name,
                attraction_chance=details.get("AttractionPercentage"),
                max_stay=details.get("MaxStayTime"),
                min_stay=details.get("MinStayTime"),
                max_wait_time=details.get("MaxWaitTime"),
                min_wait_time=details.get("MinWaitTime"),
            )
            archetype_list.append(archetype)

        return archetype_list

    def _handle_activities(self, activity_dict: dict[str, dict]) -> list[Activity]:
        if not bool(activity_dict):
            raise IndexError("Dictionary is empty") from None

        activity_list: list[Archetype] = []

        for name, details in activity_dict.items():
            activity: Activity = Activity(
                name=name,
                duration=details.get("Duration"),
                popularity=details.get("Popularity"),
            )
            activity_list.append(activity)

        return activity_list

    def _handle_attractions(
        self,
        attraction_dict: dict[str, dict],
        alt_queue: str = None,
        hours_open: int = 16,
        fastpass_pool_size: float = 0.3,
    ) -> list[Attraction]:
        if not bool(attraction_dict):
            raise IndexError("Dictionary is Empty") from None

        attraction_list: list[Archetype] = []

        for name, details in attraction_dict.items():
            attraction: Attraction = Attraction(
                name=name,
                duration=details.get("Duration"),
                popularity=details.get("Popularity"),
                service_rate=details.get("ServiceRate"),
                alt_queue=alt_queue,
                hours_open=hours_open,
                fastpass_pool_size=fastpass_pool_size,
            )
            attraction_list.append(attraction)

        return attraction_list

    def _generate_entry_events(
        self,
        max_entry_rate: int,
        park_closing_time: int,
        personClass: Union[Person, DisneyPerson] = Person,
    ) -> list[float]:
        # This function generates events related to the entry of guests to the park

        print("Generating Entry Events...", flush=True)

        time = 0
        maxTime = self.closing_time
        while time < maxTime:

            #
            time -= np.log(np.random.uniform()) / max_entry_rate

            if time > maxTime:
                break

            if np.random.uniform() < self.function(time / 60, 1):
                archetype: Archetype = choice(self.guest_archetypes)
                new_guest: Person = personClass(
                    len(self.guests), int(ceil(time)), archetype, park_closing_time
                )
                self.guests.append(new_guest)

        print("Entry Events Generated\n", flush=True)

    def _update_wait_times(self):
        for attraction in self.attractions:
            attraction.queue._update_wait_time(service_rate=attraction.service_rate)

    def _serve_guests(self):
        for attraction in self.attractions:
            attraction.serve()


class DisneyPark(Park):
    def __init__(
        self,
        attraction_dict: dict[str, dict] = ATTRACTIONS,
        activities_dict: dict[str, dict] = ACTIVITIES,
        archetype_dict: dict[str, dict] = ARCHETYPES,
        fn: Callable[[float], float] = lambda x, k: k ** x * np.exp(-k) / gamma(x + 1),
        hours_open: int = 16,
        fastpass_pool_size: float = 0.3,
    ) -> None:
        super().__init__(
            attraction_dict,
            activities_dict,
            archetype_dict,
            fn,
            hours_open,
            fastpass_pool_size,
        )

        self.attractions: list[Attraction] = self._handle_attractions(
            attraction_dict=attraction_dict,
            alt_queue="DFP",
            hours_open=hours_open,
            fastpass_pool_size=fastpass_pool_size,
        )

    def start_day(self, max_entry_rate: int, wait_time_update: int = 5) -> None:
        # First, we create the guests

        self._generate_entry_events(max_entry_rate, self.closing_time, DisneyPerson)

        # Day starts, time starts running minute per minute depending in the hours open
        for minute in tqdm(range(self.closing_time)):
            # Every 5 minutes, all queue times update for the guests to check
            if minute % wait_time_update == 0:
                self._update_wait_times()

            for guest in self.guests:
                # Guest hasn't arrived to the park yet
                if guest.arrival_time > minute:
                    continue

                guest.check_leave_park(minute)
                # print(f"Guest id : {guest.id}")
                # This case is the 'left the park' state, they're skipped
                if guest.time_left_in_activity == -2:
                    # print("left park")
                    continue

                # In this case, the guest is in a queue, they're are skipped
                # as they're not able to change selections. TotalWaitTime increases.
                elif guest.time_left_in_activity == -1:
                    # print("On queue")
                    guest.total_wait_time += 1

                # On this case, the guest is currently doing an activity
                # or riding an attraction. Time passes.
                elif guest.time_left_in_activity > 0:
                    # print("Doing activity")
                    guest.time_left_in_activity -= 1

                # In this scenario, they're looking for something to do
                # They're free to choose based on their archetype
                elif guest.time_left_in_activity == 0:
                    selection = guest.choose_what_to_do(
                        self.activities, self.attractions, minute
                    )

                    if isinstance(selection, Attraction):
                        guest.check_attraction(
                            selection, self.closing_time - minute, minute
                        )
                        # guest.do_activity(selection.name, selection.duration)
                        # print("Chose attraction")
                    elif isinstance(selection, Activity):
                        # print("Chose activity")
                        guest.do_activity(selection.name, selection.duration)

            self._serve_guests()

    def _serve_guests(self):
        for attraction in self.attractions:
            attraction.serve_with_fastpass()

    def _update_wait_times(self):
        for attraction in self.attractions:
            whole_queue = attraction.queue.in_queue + attraction.alt_queue.in_queue
            attraction.queue._update_wait_time(
                service_rate=attraction.service_rate,
                whole_queue=whole_queue,
            )
            attraction.alt_queue._update_wait_time(service_rate=attraction.service_rate)


class SalitrePark(Park):
    def __init__(
        self,
        attraction_dict: dict[str, dict] = ATTRACTIONS,
        activities_dict: dict[str, dict] = ACTIVITIES,
        archetype_dict: dict[str, dict] = ARCHETYPES,
        fn: Callable[[float], float] = lambda x, k: k ** x * np.exp(-k) / gamma(x + 1),
        hours_open: int = 16,
        fastpass_pool_size: float = 0.13,
    ) -> None:
        super().__init__(
            attraction_dict,
            activities_dict,
            archetype_dict,
            fn,
            hours_open,
            fastpass_pool_size,
        )

        self.attractions: list[Attraction] = self._handle_attractions(
            attraction_dict=attraction_dict,
            alt_queue="SFP",
            hours_open=hours_open,
            fastpass_pool_size=fastpass_pool_size,
        )

        self.fastpass_pool_size: float = fastpass_pool_size

    def start_day(self, max_entry_rate: int, wait_time_update: int = 5) -> None:
        # First, we create the guests

        self._generate_entry_events(max_entry_rate, self.closing_time, SalitrePerson)

        # Day starts, time starts running minute per minute depending in the hours open
        for minute in tqdm(range(self.closing_time)):
            # Every 5 minutes, all queue times update for the guests to check
            if minute % wait_time_update == 0:
                self._update_wait_times()

            for guest in self.guests:

                if minute == 1:
                    if np.random.uniform(0, 1, 1) <= self.fastpass_pool_size:
                        guest.fastpass = True
                    else:
                        guest.fastpass = False

                # Guest hasn't arrived to the park yet
                if guest.arrival_time > minute:
                    continue

                guest.check_leave_park(minute)
                # print(f"Guest id : {guest.id}")
                # This case is the 'left the park' state, they're skipped
                if guest.time_left_in_activity == -2:
                    # print("left park")
                    continue

                # In this case, the guest is in a queue, they're are skipped
                # as they're not able to change selections. TotalWaitTime increases.
                elif guest.time_left_in_activity == -1:
                    # print("On queue")
                    guest.total_wait_time += 1

                # On this case, the guest is currently doing an activity
                # or riding an attraction. Time passes.
                elif guest.time_left_in_activity > 0:
                    # print("Doing activity")
                    guest.time_left_in_activity -= 1

                # In this scenario, they're looking for something to do
                # They're free to choose based on their archetype
                elif guest.time_left_in_activity == 0:
                    selection = guest.choose_what_to_do(
                        self.activities, self.attractions
                    )

                    if isinstance(selection, Attraction):
                        guest.check_attraction(selection)
                        # guest.do_activity(selection.name, selection.duration)
                        # print("Chose attraction")
                    elif isinstance(selection, Activity):
                        # print("Chose activity")
                        guest.do_activity(selection.name, selection.duration)

            self._serve_guests()

    def _serve_guests(self):
        for attraction in self.attractions:
            attraction.serve_with_fastpass()

    def _update_wait_times(self):
        for attraction in self.attractions:
            whole_queue = attraction.queue.in_queue + attraction.alt_queue.in_queue
            attraction.queue._update_wait_time(
                service_rate=attraction.service_rate,
                whole_queue=whole_queue,
            )
            attraction.alt_queue._update_wait_time(service_rate=attraction.service_rate)


class FakeTimesPark(Park):
    def __init__(
        self,
        attraction_dict: dict[str, dict] = ATTRACTIONS,
        activities_dict: dict[str, dict] = ACTIVITIES,
        archetype_dict: dict[str, dict] = ARCHETYPES,
        fn: Callable[[float], float] = lambda x, k: k ** x * np.exp(-k) / gamma(x + 1),
        hours_open: int = 16,
        fastpass_pool_size: float = 0.3,
    ) -> None:
        super().__init__(
            attraction_dict,
            activities_dict,
            archetype_dict,
            fn,
            hours_open,
            fastpass_pool_size,
        )

    def start_day(self, max_entry_rate: int, wait_time_update: int = 5) -> None:
        # First, we create the guests

        self._generate_entry_events(max_entry_rate, self.closing_time, FakeTimesPerson)

        # Day starts, time starts running minute per minute depending in the hours open
        for minute in tqdm(range(self.closing_time)):
            # Every 5 minutes, all queue times update for the guests to check
            if minute % wait_time_update == 0:
                self._update_wait_times()

            for guest in self.guests:
                # Guest hasn't arrived to the park yet
                if guest.arrival_time > minute:
                    continue

                guest.check_leave_park(minute)
                # print(f"Guest id : {guest.id}")
                # This case is the 'left the park' state, they're skipped
                if guest.time_left_in_activity == -2:
                    # print("left park")
                    continue

                # In this case, the guest is in a queue, they're are skipped
                # as they're not able to change selections. TotalWaitTime increases.
                elif guest.time_left_in_activity == -1:
                    # print("On queue")
                    guest.total_wait_time += 1

                # On this case, the guest is currently doing an activity
                # or riding an attraction. Time passes.
                elif guest.time_left_in_activity > 0:
                    # print("Doing activity")
                    guest.time_left_in_activity -= 1

                # In this scenario, they're looking for something to do
                # They're free to choose based on their archetype
                elif guest.time_left_in_activity == 0:
                    selection = guest.choose_what_to_do(
                        self.activities, self.attractions
                    )

                    if isinstance(selection, Attraction):
                        guest.check_attraction(selection)
                        # guest.do_activity(selection.name, selection.duration)
                        # print("Chose attraction")
                    elif isinstance(selection, Activity):
                        # print("Chose activity")
                        guest.do_activity(selection.name, selection.duration)

            self._serve_guests()

    def _update_wait_times(self):
        for attraction in self.attractions:
            attraction.queue._update_fake_wait_time(
                service_rate=attraction.service_rate
            )
