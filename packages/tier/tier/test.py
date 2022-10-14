# std
import os
import sys

# internal
from tier.main import main


if __name__ == '__main__':
    os.chdir('../../../')
    sys.argv = ['tier', '-vv', 'develop']
    # sys.argv = ['tier', '-vv', 'sync']
    main()
