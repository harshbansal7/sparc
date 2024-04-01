def message_helper(complaint_id, receiver_details, complaint_data, user_data):
    
    formatted_string = (
    "*Complaint ID* - {}\n\n"    
    "*Complaint Category:*\n{}\n\n"
    "*Allotted To:*\n{}\n\n"
    "*Original Complaint:*\n{}\n\n"
    "*Translated Complaint:*\n{}\n\n"
    "*Complainant Name:*\n{}\n\n"
    "*Complainant Phone:*\n{}\n\n"
    # "*Entities:*\n{}"
    ).format(
        complaint_id,
        complaint_data["complaint_category"],
        receiver_details["official"],
        complaint_data["original"],
        complaint_data["description"],
        user_data["username"] if user_data else "[Not Disclosed]",
        user_data["userphone"] if user_data else "[Not Disclosed]",
        # entities,
    )

    return formatted_string