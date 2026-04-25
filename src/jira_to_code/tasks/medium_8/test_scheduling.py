from scheduling import schedule_event

def test_timezone_aware():
    dt = schedule_event(2023, 1, 1)
    assert dt.tzinfo is not None
