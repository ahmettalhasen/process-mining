def show_event_log_details(event_logs, offset: int = 0, limit: int = 3) -> None:
    """
    Prints out the details of each trace and event in the given event log (pm4py.objects.log.log.EventLog object), 
    starting from a specific index.

    Each trace (case) and its associated events are printed, along with their respective indices.
    The details include trace ID, event activity, and event timestamp for each event in the trace.

    Args:
        event_logs (pm4py.objects.log.log.EventLog): The event logs to process, each entry in the log is considered 
                                                   as a trace (case), and each trace contains a list of events.

        offset (int, optional): The starting index from which to print the traces. Defaults to 0.
        
        limit (int, optional): The maximum number of traces to print. Defaults to 3.

    Returns:
        None
    """
    for case_index, case in enumerate(event_logs[offset:offset + limit]):
        print(f"Case index: {case_index + offset} Case ID: {case.attributes['concept:name']}")
        for event_index, event in enumerate(case):
            print(f"Event index: {event_index} Event activity: {event['concept:name']} Event time: {event['time:timestamp']}")
        print("--------------------------------------------------------------------------------------------------------")


