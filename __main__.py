"""A GitHub Python Pulumi program."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

import pulumi
import pulumi_github as github

owners = [
    "notdodo",
    "fam4r",
    "k3t4am4",
    "seintzx",
]

for user in owners:
    github.Membership(
        f"owners-{user}",
        role="admin",
        username=user,
    )

github.Repository(
    "github-pulumi",
    delete_branch_on_merge=True,
    name="github-pulumi",
    has_downloads=False,
    has_issues=True,
    has_projects=True,
    has_wiki=False,
    vulnerability_alerts=True,
    description="Pulumi project to manage srendipity-lab GitHub Organization",
)


class Roles(StrEnum):
    """GitHub roles for a team member."""

    ADMIN = "maintainer"
    MEMBER = "member"


@dataclass
class Member:
    """GitHub team's member."""

    username: str
    role: Roles


class Team(pulumi.ComponentResource):
    """
    A Pulumi component resource to create a GitHub team with customizable options.

    :param name [str]: The name of the team to create.
    :param description [str | None]: A short description of the team.
    :param members list[Member]: A list of the Members for the team.
    :param opts [pulumi.ResourceOptions | None]: Pulumi resource options for the custom resource.
    """

    def __init__(
        self,
        name: str,
        members: list[Member],
        description: str | None = "",
        opts: pulumi.ResourceOptions | None = None,
    ) -> None:
        """Initialize the Team class."""
        self.resource_name = name.lower().replace(" ", "-")
        super().__init__(
            "sredipity-lab::github::TeamWithMembers",
            self.resource_name,
            {},
            opts,
        )
        self.team = github.Team(
            f"{self.resource_name}-team",
            name=name,
            description=description,
            create_default_maintainer=False,
            privacy="closed",
            opts=opts,
        )

        github.TeamMembers(
            f"{self.resource_name}-members",
            team_id=self.team.id,
            members=[
                github.TeamMembersMemberArgs(username=member.username, role=member.role)
                for member in members
            ],
            opts=pulumi.ResourceOptions.merge(
                opts, pulumi.ResourceOptions(parent=self.team)
            ),
        )

        self.register_outputs({"team": self.team})


Team(
    "Admins",
    description="srendipty-lab Admins group",
    members=[Member(username=user, role=Roles.ADMIN) for user in owners],
)
