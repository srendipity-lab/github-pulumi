"""A GitHub Python Pulumi program."""

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
    name="github-pulumi",
    has_downloads=False,
    has_issues=True,
    has_projects=False,
    has_wiki=False,
    vulnerability_alerts=True,
    description="Pulumi project to manage srendipity-lab GitHub Organization",
)


class Roles(StrEnum):
    ADMIN = "maintainer"
    MEMBER = "member"


@dataclass
class Member:
    username: str
    role: Roles


class Team(pulumi.ComponentResource):
    def __init__(
        self,
        team_name: str,
        members: list[Member],
        description: str | None = "",
        opts: pulumi.ResourceOptions = None,
    ) -> None:
        self.resource_name = team_name.lower().replace(" ", "-")
        super().__init__(
            "sredipity-lab::github::TeamWithMembers",
            self.resource_name,
            {},
            opts,
        )
        self.team = github.Team(
            f"{self.resource_name}-team",
            name=team_name,
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
