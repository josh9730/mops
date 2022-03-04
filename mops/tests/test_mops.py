import pytest
from mops import main


@pytest.fixture
def mop_dict():
    return {
        "approval": "COR-1696",
        "escalation": "Deploying Engineer",
        "executing_dep": "NOC",
        "impact": ["None"],
        "level": 0,
        "page_title": "TEST",
        "parent_page_id": 45428825,
        "partial_rollback": True,
        "pre_maint": ["STEP 1", "STEP 2"],
        "repository": "/Users/jdickman/Google Drive/My Drive/MOPs/YAML/",
        "rh": "SACR2",
        "rh_equip": ["Labeler"],
        "rollback_steps": ["STEP 1", "STEP 2"],
        "sections": {
            "TEST SECTION1": [
                {"rh": "TEST"},
                {"cmd_rh": "TEST"},
                {"noc": "TEST"},
                {"cmd_noc": ["TEST INST", "TEST MULTILINE"]},
                {"expand_noc": ["TEST INST", "TEST MULTILINE"]},
                {"core": "TEST"},
                {"cmd_core": ["TEST INST", "TEST MULTILINE"]},
                {"expand_core": ["TEST INST", "TEST MULTILINE"]},
                {"note": "TEST"},
                {
                    "jumper": [
                        "Instructions",
                        {
                            "acable": "TEST",
                            "acage": "TEST",
                            "adevice": "TEST",
                            "aport": "TEST",
                            "arack": "TEST",
                            "aterm": "Yes",
                            "zcage": "TEST",
                            "zdevice": "TEST",
                            "zport": "TEST",
                            "zrack": "TEST",
                            "zterm": "No",
                        },
                    ]
                },
            ],
            "TEST SECTION2": [
                {"rh": "TEST"},
                {"cmd_rh": "TEST"},
                {"noc": "TEST"},
                {"cmd_noc": ["TEST INST", "TEST MULTILINE"]},
                {"expand_noc": ["TEST INST", "TEST MULTILINE"]},
                {"core": "TEST"},
                {"cmd_core": ["TEST INST", "TEST MULTILINE"]},
                {"expand_core": ["TEST INST", "TEST MULTILINE"]},
                {"note": "TEST"},
                {
                    "jumper": [
                        "Instructions",
                        {
                            "acable": "TEST",
                            "acage": "TEST",
                            "adevice": "TEST",
                            "aport": "TEST",
                            "arack": "TEST",
                            "aterm": "Yes",
                            "zcage": "TEST",
                            "zdevice": "TEST",
                            "zport": "TEST",
                            "zrack": "TEST",
                            "zterm": "No",
                        },
                    ]
                },
            ],
        },
        "shipping": {
            "NOC-663883": ["7754 7528 9544", "22681004"],
            "NOC-663884": ["7754 7528 9544", "22681004"],
        },
        "summary": ["Install 48-port LC panel at SACR2"],
        "ticket": "NOC-664802",
    }


@pytest.fixture
def cd_dict():
    return {
        "changes": {
            "sut-coe-1": [
                "router isis 2152 interface te0/0/2/3 "
                "address-family ipv4 unicast metric 9999"
                "router isis 2152 interface te0/0/2/3 "
                "address-family ipv6 unicast metric 9999"
            ],
            "sut-coe-2": [
                "router isis 2152 interface te0/0/2/3 "
                "address-family ipv4 unicast metric 9999"
                "router isis 2152 interface te0/0/2/3 "
                "address-family ipv6 unicast metric 9999"
            ],
        },
        "end_time": "1500",
        "gcal_auth_path": "/Users/jdickman/Google Drive/My Drive/Scripts/",
        "page_title": "TEST",
        "parent_page_id": 8884129,
        "repository": "/Users/jdickman/Google Drive/My Drive/MOPs/YAML/",
        "start_day": "today",
        "start_time": "1740",
        "summary": ["Cost-In CLR20029"],
        "ticket": "NOC-507412",
    }


def test_mop_schema(mop_dict):
    main.validate_yaml(mop_dict, "mop")


def test_cd_schema(cd_dict):
    main.validate_yaml(cd_dict, "cd")
