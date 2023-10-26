import sys
sys.path.insert(0, '/Users/alexf/dev/dalle-3-optimization-framework')  # NOTE: Correct path now

from easygpt.main import main

if __name__ == '__main__':
    main("gpt-3.5-turbo-16k",
         0.33,
         False,
         None,
         False)