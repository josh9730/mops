import pytest
import main


@pytest.fixture
def create_mop_dict():
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


