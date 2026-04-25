from endpoints import process_user_data

def test_process_user_data():
    assert process_user_data({'phone_number': '123'}) == {'status': 'success', 'phone': '123'}
    assert process_user_data({}) == {'status': 'success', 'phone': None}
