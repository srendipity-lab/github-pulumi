"""A GitHub Python Pulumi program."""

import pulumi_github as github

repository = github.Repository(
    "github-pulumi",
    name="github-pulumi",
    has_downloads=False,
    has_issues=True,
    has_projects=False,
    has_wiki=False,
    vulnerability_alerts=True,
    description="srendipity-lab Pulumi project to manage org repositories",
)
