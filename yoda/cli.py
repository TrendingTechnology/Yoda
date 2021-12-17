import os

import click


class ComplexCLI(click.MultiCommand):
    def list_commands(self, ctx):
        commands = []
        commands_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))
        for filename in os.listdir(commands_folder):
            if filename.endswith(".py") and filename.startswith("cmd_"):
                commands.append(filename.replace("cmd_", "").replace(".py", ""))

        commands.sort()
        return commands

    def get_command(self, ctx, name):
        try:
            mod = __import__(f"yoda.commands.cmd_{name}", None, None, ["cli"])
        except ImportError:
            return
        return mod.cli


@click.command(cls=ComplexCLI)
def cli():
    """ 
...:██╗░░░██╗░█████╗░██████╗░░█████╗░:...
...:╚██╗░██╔╝██╔══██╗██╔══██╗██╔══██╗:...
...:░╚████╔╝░██║░░██║██║░░██║███████║:...
...:░░╚██╔╝░░██║░░██║██║░░██║██╔══██║:...
...:░░░██║░░░╚█████╔╝██████╔╝██║░░██║:...
...:░░░╚═╝░░░░╚════╝░╚═════╝░╚═╝░░╚═╝:...
    \n
    Hey there! 👋 Looks like you're using Yoda for the first time. Let's get you started 🚀\n
    There are three differnet OJ's from which you can get your User Statistics:\n
    Atcoder\n 
    \n
    CodeForces\n
    CodeChef\n
    For each one of the OJ's you can Download all your AC solutions ✅ as well as Submission Heatmap for each of the Website!!\n 
    \n
    🥳 You rock! We're good to go now 🥳
    """
    pass