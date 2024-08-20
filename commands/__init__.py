import os

def load_commands(bot):
    """
    Load and initialize bot commands from Python files in the commands directory.

    This function iterates through all Python files in the current directory,
    excluding __init__.py. It attempts to import each file as a module and
    call its 'setup' function, if one exists, passing the bot instance as an argument.

    Args:
        bot: The bot instance to which commands will be added.

    Raises:
        Any exceptions encountered during module import or setup are caught and printed.
    """
    commands_dir = os.path.dirname(__file__)
    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]  # Remove .py extension
            try:
                # Import the module
                module = __import__(f"commands.{module_name}", fromlist=["setup"])
                # Call the setup function if it exists
                if hasattr(module, 'setup'):
                    module.setup(bot)
                else:
                    print(f"Module {module_name} does not have a setup function.")
            except Exception as e:
                print(f"Failed to load module {module_name}: {e}")