import sys
sys.path.append("/Users/alexf/dev/dalle-3-optimization-framework")

from easygpt import main
from easygpt.src.utils import *
from easygpt.src import *
from easygpt.src.utils.logging import Logger

# Make your own optimization here easily
main("gpt-3.5-turbo-16k",
    0.33,
    False,
    None,
    False,
    "resources", "prompts")


