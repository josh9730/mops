import re
import datetime
from enum import Enum
from typing import Optional, Union
from pydantic import (
    BaseModel,
    conint,
    validator,
    DirectoryPath,
    ConstrainedStr,
)
from .atlassian import Atlassian

JIRA_PROJECTS_LIST = Atlassian().jira_projects_list()


class SectionOptions(str, Enum):
    """Valid options for Jinja template."""

    RH = "rh"
    CORE = "core"
    NOC = "noc"
    CMD_RH = "cmd_rh"
    CMD_CORE = "cmd_core"
    CMD_NOC = "cmd_noc"
    EXPAND_CORE = "expand_core"
    EXPAND_NOC = "expand_noc"
    JUMPER = "jumper"
    NOTE = "note"

    @classmethod
    def list(cls):
        """Return list of all Enum names."""
        return list(map(lambda x: x.value, cls))

    @classmethod
    def has_member(cls, name: str):
        """Return boolean for validator for Enum names."""
        return name in cls.__members__


class Regex(ConstrainedStr):
    """Regex to prevent mypy error with pydantic constr type."""

    regex = re.compile("^(today)$")


class BaseYAML(BaseModel):
    """Base class for yaml input, should not be called directly."""

    repository: DirectoryPath
    page_title: str
    parent_page_id: int
    ticket: str
    summary: list

    @staticmethod
    def check_tickets_all(ticket):
        """Validate Jira ticket."""
        error_msg = f"{ticket} must be a valid ticket number."
        assert ticket[:3] in JIRA_PROJECTS_LIST, error_msg
        assert ticket[3] == "-", error_msg
        assert ticket[4:].isdigit(), error_msg


class CDModel(BaseYAML):
    """Change Doc validator."""

    gcal_auth_path: DirectoryPath
    start_time: datetime.time
    end_time: datetime.time
    start_day: Union[Regex, datetime.date]
    changes: dict[str, list]

    @validator("changes")
    def check_changes(cls, changes):
        """Validate changes section matches Jinja template."""
        for title, items in changes.items():
            assert isinstance(title, str)
            assert isinstance(items, list)


class MOPModel(BaseYAML):
    """MOP validator."""

    level: conint(ge=0, le=3)
    executing_dep: str
    rh: str
    approval: str
    impact: Optional[list]
    escalation: Optional[str] = "Deploying Engineer"
    partial_rollback: bool
    rollback_steps: Optional[list]
    pre_maint: Optional[list]
    rh_equip: Optional[list]
    shipping: dict[str, list]
    sections: dict[str, list]

    @validator("ticket", "approval")
    def check_tickets_model(cls, ticket):
        """Check MOP Tickets."""
        BaseYAML.check_tickets_all(ticket)

    @validator("shipping")
    def check_shipping(cls, shipping):
        """Validate shipping dict."""
        for shipping_ticket, shipping_info in shipping.items():
            BaseYAML.check_tickets_all(shipping_ticket)
            for i in shipping_info:
                assert isinstance(i, str), f"{i} must be a valid string."

    @validator("sections")
    def check_sections(cls, sections):
        """Validate that the keys of each section match the Enum model/Jinja template."""
        for section_list in sections.values():
            for i in section_list:
                section_header = list(i.keys())[0].upper()
                assert SectionOptions.has_member(
                    section_header
                ), f"Invalid section option: '{section_header.lower()}', must use one of {SectionOptions.list()}"
