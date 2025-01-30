"""A GitHub Python Pulumi program"""

import pulumi
import pulumi_github as github

repository = github.Repository(
    "github-pulumi",
    name="github-pulumi",
    description="srendipity-lab Pulumi project to manage org repositories",
    opts=pulumi.ResourceOptions(import_="github-pulumi"),
)
