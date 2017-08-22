import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
# APP MODULES, añadimos los test de cada modulo
from user.tests import UserTest
from relationship.tests import RelationshipTest

if __name__=='__main__':
    unittest.main()