import sys
import os
import shutil
from typing import Optional
import yaml
import typer
from pydantic import ValidationError
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

from utils.schema import CDModel, MOPModel
from utils.atlassian import Atlassian
from utils.gcal import GCal


mops = typer.Typer(
    add_completion=False,
    help="""
Create MOP or Change Doc.
""",
)
ARGUMENTS = {
    "link": False,
    "render": False,
    "default": False,
    "reset": False,
}


def render_yaml(data, yaml_type: str):
    """Return rendered template."""
    env = Environment(
        loader=FileSystemLoader("renderers/"), trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template(f"{yaml_type}.j2")
    return template.render(data)


def reset_yaml(repository: str, yaml_type: str, gcal_auth_path: Optional[str]):
    """Reset MOP or CD YAML files to defaults."""
    env = Environment(
        loader=FileSystemLoader("defaults/"), trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template(f"{yaml_type}_defaults.j2")
    with open(f"{yaml_type}.yaml", "w") as f:
        f.write(template.render(repository=repository, gcal_auth_path=gcal_auth_path))


def yaml_init(yaml_type: str):
    """Return yaml file based on specified type."""
    with open(f"{yaml_type}.yaml", "r") as f:
        return yaml.safe_load(f)


def validate_yaml(data: dict, yaml_type: str):
    """Validate against schema for specified type."""
    try:
        MOPModel(**data) if yaml_type == "mop" else CDModel(**data)
    except ValidationError as e:
        sys.exit(e)


def move_yaml(*args: str):
    """Move YAML to designated repo.

    args:
      page_title: str
      repository: path
      yaml_type: str
    """
    date = datetime.today().strftime("%Y-%m-%d")
    shutil.copy(
        f"{os.path.dirname(__file__)}/{args[2]}.yaml",
        f'{args[1]}{args[2]}/{date}_{args[0].replace(" ", "_")}.yaml',
    )


def main(yaml_type: str, data: dict, **kwargs):
    """Main function for CD, MOP gen.

    Args:
      yaml_type: str = 'mop' or 'cd'
    kwargs:
      reset, default, render, link: bool
    """
    repository = data["repository"]
    gcal_auth_path = data.get("gcal_auth_path")
    if kwargs["reset"]:
        reset_yaml(repository, yaml_type, gcal_auth_path)

    else:
        atlassian = Atlassian()
        validate_yaml(data, yaml_type)
        rendered_data = render_yaml(data, yaml_type)

        if kwargs["render"]:
            print(rendered_data)
        else:
            page_title = data["page_title"]
            parent_page_id = data["parent_page_id"]
            ticket = data["ticket"]
            print(
                f"\nCreating {yaml_type.upper()}:\n\tTitle: {page_title}",
                f"\n\tParent Page ID: {parent_page_id}",
                f"\n\tTicket: {ticket}",
                f"\n\tJira Link: {kwargs['link']}\n",
            )
            atlassian.confluence_create_or_update(
                [parent_page_id, page_title, rendered_data]
            )
            print(f"\tMoving YAML to repo: {repository}\n")
            gcal_auth_path = data["gcal_auth_path"] if yaml_type == "cd" else None
            move_yaml(page_title, repository, yaml_type)
            if kwargs["default"]:
                reset_yaml(repository, yaml_type, gcal_auth_path)

            if kwargs["link"]:
                print(f"\tAdding link to {ticket}")
                page_url = (
                    "https://documentation.cenic.org/display/Core/"
                    f'{page_title.replace(" ", "+")}'
                )
                atlassian.jira_create_link([ticket, page_url, page_title])


@mops.command()
def mop() -> None:
    """Create MOP from mop.yaml"""
    data = yaml_init("mop")
    main("mop", data, **ARGUMENTS)


@mops.command()
def cd(
    calendar: bool = typer.Option(
        False,
        "--calendar",
        "-c",
        help="Create Internal Calendar Entry. Only use once, will create multiple events.",
    ),
) -> None:
    """Create Change Doc from cd.yaml"""
    data = yaml_init("cd")
    main("cd", data, **ARGUMENTS)

    if calendar:
        if not data["gcal_auth_path"]:
            raise ValueError("\n\ngcal_auth_path must be defined in cd.yaml.\n")
        start_time = str(data["start_time"])
        end_time = str(data["end_time"])
        start_day = str(data["start_day"])
        print(
            f"\tCreating Internal Change entry:\n\t\tDay: {start_day}",
            f"\n\t\tStart: {start_time}\n\t\tEnd: {end_time}\n",
        )
        gcal = GCal(data["gcal_auth_path"])
        title = data["ticket"] + data["page_title"]
        gcal.create_calendar_event(start_time, end_time, start_day, title)


@mops.callback()
def arguments(
    link: bool = typer.Option(
        False,
        "--link",
        "-l",
        help="Link to supplied Jira ticket. Only use once, will create multiple links.",
    ),
    render: bool = typer.Option(
        False, "--render", "-r", help="Print Jinja2 rendered output only."
    ),
    default: bool = typer.Option(
        False,
        "--default",
        "-d",
        help="Return YAML to default setttings after running program.",
    ),
    reset: bool = typer.Option(
        False,
        "--reset",
        "-R",
        help="Reset YAML to default settings, no other actions taken.",
    ),
):
    ARGUMENTS.update(
        {"link": link, "render": render, "default": default, "reset": reset}
    )


if __name__ == "__main__":
    mops()
