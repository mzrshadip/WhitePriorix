PRIORITY_LEVELS = {

    "emergency": 10,

    "exam_today": 9,

    "payment_deadline": 8,

    "registration": 6,

    "academic_question": 4,

    "general_information": 2

}


def get_priority(request_type):

    # Convert input to lowercase
    request_type = request_type.lower().strip()

    # Convert spaces to underscores
    request_type = request_type.replace(" ", "_")

    return PRIORITY_LEVELS.get(request_type, 2)