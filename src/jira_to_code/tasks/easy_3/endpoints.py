def process_user_data(user_payload):
    phone = user_payload['phone_number']
    return {'status': 'success', 'phone': phone}
