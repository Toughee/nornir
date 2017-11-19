"""
This is a simple example where we use click and brigade to build a simple CLI tool to retrieve
hosts information.

The main difference with get_facts_simple.py is that instead of calling a plugin directly
we wrap it in a function. It is not very useful or necessary here but illustrates how
tasks can be grouped.
"""
from brigade.core import Brigade
from brigade.plugins import tasks
from brigade.plugins.inventory.simple import SimpleInventory

import click


def get_facts(task, facts):
    r = tasks.napalm_get_facts(task, facts)
    print(task.host.name)
    print("============")
    print(r["result"])
    print()


@click.command()
@click.argument('site')
@click.argument('role')
@click.argument('facts')
def main(site, role, facts):
    brigade = Brigade(
        inventory=SimpleInventory("hosts.yaml", "groups.yaml"),
        dry_run=True,
    )

    filtered = brigade.filter(site=site, role=role)
    filtered.run(task=get_facts,
                 facts=facts)


if __name__ == "__main__":
    main()
