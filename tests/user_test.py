import sys

import venmo

if sys.version_info <= (3, 3):
    import mock
else:
    from unittest import mock


@mock.patch.object(venmo.user, 'search')
def test_id_from_username_case_insensitive(mock_search):
    # Mock out Venmo API response. It is case insensitive.
    mock_search.return_value = [
        {
            "id": "975376293560320029",
            "username": "zackhsi",
            "display_name": "Zack Hsi",
            "profile_picture_url": "https://venmopics.appspot.com/u/v2/f/172a1500-63f5-4d78-b15a-a06dc9c0ad82"  # noqa
        },
    ]

    ids = [
        venmo.user.id_from_username('zackhsi'),
        venmo.user.id_from_username('Zackhsi'),
        venmo.user.id_from_username('ZACKHSI'),
    ]
    # Assert that all return ids.
    assert all(ids)
    # Assert that the same id is returned.
    assert len(set(ids)) == 1
