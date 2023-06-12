# Contributing to Trading Portfolio Tracker

## Reporting Issues

We use
[GitHub Projects as a Kanban board](https://github.com/users/IsaacCheng9/projects/4)
and integrate the GitHub Issues feature to track the progress of tasks and
related pull requests - remember to link the issue to the Kanban board.

Include the following information when reporting an issue (where possible):

- Breakdown of the problem
- Expected changes
- Reproducible steps (if reporting a bug)
- Prerequisite issues
  - Some issues may require another issue to be completed first.
- Related issues
  - Some issues may be related to others, but not require them to be completed
    first.
  - e.g. an issue may help provide context for another issue.

The `high priority` label should be sparingly to avoid diluting its
significance - overuse of this defeats the purpose of the label.

## Pull Requests

Include the following information when submitting a pull request:

- Overview of the changes
  - Where needed, add explanations about what the changes will effect and why
    they were made.
- Related issues
  - Using the `Fixes {link to issue}` syntax will automatically close the
    issue once merged.

## Merge Strategy

We use the _squash merging_ strategy when merging pull requests to improve the
quality of the change history and make the commit log easier to navigate.

A further explanation about the benefits of this strategy can be found
[here](https://blog.dnsimple.com/2019/01/two-years-of-squash-merge/).

## Unit Tests

Unit tests should be created and maintained as changes are made to the core
functionality to improve maintainability.

We use the _pytest_ framework for this, which has been integrated into GitHub
Actions for automated unit testing (see below).

## GitHub Actions

After pushing to the repository, the workflow in GitHub Actions includes:

- Running Python code formatting with _Black_
  - This ensures good readability and a consistent style across the codebase to
    reduce diffs for code reviews.
- Running all unit tests for Python with _Pytest_
  - This helps prevent runtime errors in production.
  - Test should be created and kept updated to facilitate this.
