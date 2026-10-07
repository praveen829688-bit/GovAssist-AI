APPLICATION_STATUSES = [
    "Draft",
    "Submitted",
    "Under Review",
    "Documents Required",
    "Approved",
    "Rejected",
    "Completed"
]


def status_index(status):

    try:
        return APPLICATION_STATUSES.index(status)

    except ValueError:
        return 0


def progress(status):

    index = status_index(status)

    if len(APPLICATION_STATUSES) <= 1:
        return 0

    return index / (len(APPLICATION_STATUSES) - 1)


def status_message(status):

    messages = {

        "Draft":
            "Your application has not been submitted yet.",

        "Submitted":
            "Your application has been submitted.",

        "Under Review":
            "The application is currently being reviewed.",

        "Documents Required":
            "Additional documents may be required.",

        "Approved":
            "Your application has been approved.",

        "Rejected":
            "The application was rejected. Check the official authority for the reason.",

        "Completed":
            "The application process has been completed."
    }

    return messages.get(
        status,
        "Status information is unavailable."
    )
