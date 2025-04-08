# Test data for populating the octofit_db database

test_data = {
    "users": [
        {"username": "john_doe", "email": "john@example.com", "password": "password123"},
        {"username": "jane_doe", "email": "jane@example.com", "password": "password123"},
    ],
    "teams": [
        {"name": "Team Alpha", "members": ["john_doe", "jane_doe"]},
    ],
    "activities": [
        {"user": "john_doe", "activity_type": "Running", "duration": parse_duration("30 minutes")},
        {"user": "jane_doe", "activity_type": "Cycling", "duration": parse_duration("45 minutes")},
    ],
    "leaderboard": [
        {"user": "john_doe", "score": 100},
        {"user": "jane_doe", "score": 150},
    ],
    "workouts": [
        {"name": "Morning Run", "description": "A quick morning run to start the day"},
        {"name": "Evening Yoga", "description": "Relaxing yoga session in the evening"},
    ],
}
