import unittest
from unittest.mock import MagicMock, patch
from backend.configuration import AbstractFactory, ConcreteFactory, read_config, initialize_system

class TestAbstractFactory(unittest.TestCase):

    config_path="../backend/config.ini"
    config = read_config(config_path)

    def test_create_company_dao(self):
        with self.assertRaises(NotImplementedError):
            AbstractFactory.create_company_dao(self.config)

    def test_create_company_service(self):
        with self.assertRaises(NotImplementedError):
            AbstractFactory.create_company_service(None)

    def test_create_user_dao(self):
        with self.assertRaises(NotImplementedError):
            AbstractFactory.create_user_dao(self.config)

    def test_create_user_service(self):
        with self.assertRaises(NotImplementedError):
            AbstractFactory.create_user_service(None)

class TestConcreteFactory(unittest.TestCase):
    config_path="../backend/config.ini"
    config = read_config(config_path)

    @patch('backend.configuration.CompanyDao')
    def test_create_company_dao(self, mock_company_dao):
        ConcreteFactory.create_company_dao(self.config)

        mock_company_dao.assert_called_once_with(
            host='localhost',
            user='root',
            password='mysql_12#$',
            database='Securities'
        )

    @patch('backend.configuration.CompanyService')
    def test_create_company_service(self, mock_company_service):
        mock_company_dao = MagicMock()
        ConcreteFactory.create_company_service(mock_company_dao)
        mock_company_service.assert_called_once_with(mock_company_dao)

    @patch('backend.configuration.UserDao')
    def test_create_user_dao(self, mock_user_dao):
        ConcreteFactory.create_user_dao(self.config)
        mock_user_dao.assert_called_once_with(
            host='localhost',
            user='root',
            password='mysql_12#$',
            database='Securities'
        )

    @patch('backend.configuration.UserService')
    def test_create_user_service(self, mock_user_service):
        mock_user_dao = MagicMock()
        ConcreteFactory.create_user_service(mock_user_dao)
        mock_user_service.assert_called_once_with(mock_user_dao)

class TestSystemInitialization(unittest.TestCase):

    @patch('backend.configuration.read_config')
    @patch('backend.configuration.ConcreteFactory.create_company_dao')
    @patch('backend.configuration.ConcreteFactory.create_company_service')
    @patch('backend.configuration.ConcreteFactory.create_user_dao')
    @patch('backend.configuration.ConcreteFactory.create_user_service')
    def test_initialize_system(self, mock_create_user_service, mock_create_user_dao,
                               mock_create_company_service, mock_create_company_dao, mock_read_config):
        mock_read_config.return_value = {
            'DATABASE': {
                'host': 'localhost',
                'user': 'root',
                'password': 'mysql_12#$',
                'database': 'Securities'
            }
        }
        initialize_system()
        mock_read_config.assert_called_once_with("../backend/config.ini")
        mock_create_company_dao.assert_called_once()
        mock_create_company_service.assert_called_once()
        mock_create_user_dao.assert_called_once()
        mock_create_user_service.assert_called_once()

if __name__ == '__main__':
    unittest.main()
