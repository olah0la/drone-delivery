from enum import Enum
from typing import Callable
from itertools import accumulate
import random
import time
import uuid
import requests
import typer


class State(Enum):
    PARCEL_COLLECTED = "PARCEL_COLLECTED"
    TAKEN_OFF = "TAKEN_OFF"
    LANDED = "LANDED"
    CRASHED = "CRASHED"
    PARCEL_DELIVERED = "PARCEL_DELIVERED"

    @property
    def is_terminal(self) -> bool:
        return self in {State.CRASHED, State.PARCEL_DELIVERED}


TRANSITIONS = {
    State.PARCEL_COLLECTED: [
        (0.8, State.TAKEN_OFF),
        (0.1, State.CRASHED),
        (0.1, State.PARCEL_DELIVERED),
    ],
    State.TAKEN_OFF: [(0.8, State.LANDED), (0.2, State.CRASHED)],
    State.LANDED: [
        (0.5, State.PARCEL_DELIVERED),
        (0.4, State.TAKEN_OFF),
        (0.1, State.CRASHED),
    ],
}


def _build_transition_function(
    transitions: dict[State, list[tuple[float, State]]]
) -> Callable[[State], State]:
    """Generate a function that randomly transitions from one state
    to the next"""
    preprocessed: dict[State, tuple[list[float], list[State]]] = {}
    for start_state, weighted_states in transitions.items():
        cumulated_weights = list(
            accumulate(prob for prob, _ in weighted_states)
        )
        destinations = [state for _, state in weighted_states]
        preprocessed[start_state] = (cumulated_weights, destinations)

    def sample_next_state(state: State):
        cum_weights, destinations = preprocessed[state]
        return random.choices(destinations, cum_weights=cum_weights)[0]

    return sample_next_state


CONSONANTS = "bcdfghjklmnprstvwz"
VOWELS = "aeuio"


def _generate_name() -> str:
    """Generate a semi-readable ID. Can be considered globally unique."""
    cs = random.choices(CONSONANTS, k=3)
    vs = random.choices(VOWELS, k=3)
    name = "".join(cs[i] + vs[i] for i in range(3))
    return name + "-" + str(uuid.uuid4())[:8]


def generate_events(
    base_url: str, num_ongoing: int = 10, wait_interval_ms: int = 10
) -> None:
    """Simulate delivery missions sending events to a provided URL.

    The simulation runs until interruption.
    An event is sent every wait_interval_ms milliseconds.
    At any moment, num_ongoing delivery missions are currently ongoing."""
    generate_next_state = _build_transition_function(TRANSITIONS)
    ongoing_deliveries: dict[str, State] = {}
    while True:
        time.sleep(wait_interval_ms / 1000)
        if len(ongoing_deliveries) < num_ongoing:
            delivery_id = _generate_name()
            new_state = State.PARCEL_COLLECTED
        else:
            delivery_id = random.choice(list(ongoing_deliveries.keys()))
            current_state = ongoing_deliveries[delivery_id]
            new_state = generate_next_state(current_state)
        r = requests.post(
            f"{base_url}/deliveries/{delivery_id}/events",
            json={"type": new_state.value},
        )
        print(f"Delivery {delivery_id} transitioned to {new_state.value}")
        if new_state.is_terminal:
            del ongoing_deliveries[delivery_id]
        else:
            ongoing_deliveries[delivery_id] = new_state


if __name__ == "__main__":
    typer.run(generate_events)
