Alice & Bob - Cloud take-home assignment - BACKEND
==================================

Thanks for applying!


# Objective

The goal of this assignment is to evaluate your ability to bootstrap a project, make reasonable design choices, and effectively communicate about your work.

In short, you should feel comfortable sharing this implementation with your teammates and requesting a code review.

# Your Task

In this assignment, you will implement a Python API that receives events over the network about drone delivery missions.

Your API will ingest the events and serve basic information about the status of delivery missions based on the received events.

The delivery missions can be in the following states: `PARCEL_COLLECTED`, `TAKEN_OFF`, `LANDED`, `CRASHED`, and `PARCEL_DELIVERED`. They always start in `PARCEL_COLLECTED`. `CRASHED` and `PARCEL_DELIVERED` are final states.

A drone delivery mission is considered ongoing if it is not in a final state.

## Setup

Ensure that you have Python installed on your machine and that it is accessible in your bash environment under the name `python`.

In the `event_collector/` directory, we provide a stub of the API. For now, it only prints the received events to the standard output. To launch the API:

```bash
# From event_collector/
make run
```

Your implementation should replace the code in the `event_collector/` folder.

In the `deliveries/` directory, we provide a script that simulates delivery missions by sending events to the API. To launch the script, open another shell:

```bash
# From deliveries/
make run
```

In the API logs, you should see events being received.

You should not need to modify the content of the `deliveries/` folder.

## Requirements

The API should expose the following endpoints:

* `POST /deliveries/<delivery-id>/events`: Ingests events. It accepts a JSON payload in the request body in the form `{"type": "TAKEN_OFF"}`.
* `GET /deliveries`: Lists all currently ongoing deliveries (i.e., deliveries not in a final state).
* `GET /deliveries/<delivery-id>/events`: Returns the list of events received for a given delivery mission, whether ongoing or in a final state. Only the data of the last 1000 delivery missions should be available, and older data should be discarded.
* `GET /counts`: Returns the number of ongoing deliveries and the total number of deliveries since the beginning.

Additionally, the API must have the following properties:

* The endpoints should follow REST API best practices.
* The API should run indefinitely without running into capacity issues.
* If the API crashes and is restarted, the already ingested delivery data should not be lost. It is acceptable to lose events while the API is rebooting.

You can use any library or tool to implement your solution.

## Simplifying Assumptions

* You can assume that no events are lost over the network. The first event sent for a delivery mission is always `PARCEL_COLLECTED`, and the drone will always send a final event (`PARCEL_DELIVERED` or `CRASHED`).
* You can assume that events sent for a delivery mission are in order. For example, you will never receive `TAKEN_OFF` after `CRASHED`.
* You can assume that delivery IDs are unique, so there is no need to check for conflicts.
* You can assume that the number of ongoing delivery missions at any time is no more than 100.
* Pagination is not required for the list endpoint.

# What We'll Evaluate

Beyond correctness, we expect your code to be production-ready and include a few key unit tests. You should feel confident enough in your code to present it to your teammates and request a review.

We will pay particular attention to:

- Readability (structure, ease of use, comments, complexity management)
- Maintainability (modularity, avoiding repetition)
- Pragmatism (using existing solutions when appropriate, conciseness)
- Handling of edge cases in the API
- Quality and relevance of the unit tests provided

**Please limit your effort to half a day's work.** If you cannot finish within that time, we recommend stopping and outlining next steps in your README. We will take these into account in our evaluation!

Please submit your solution as an archive or a private Git repository. In the case of a private Git repository, please ask your Alice & Bob recruiter for the email addresses with which it should be shared.