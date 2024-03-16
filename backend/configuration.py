from backend.dao.dao import CompanyDao
from backend.service.service import CompanyService
import configparser

class AbstractFactory:
    @classmethod
    def create_company_dao(cls, config):
        raise NotImplementedError("create_company_dao method not implemented")

    @classmethod
    def create_company_service(cls, company_dao):
        raise NotImplementedError("create_company_service method not implemented")

class ConcreteFactory(AbstractFactory):
    @classmethod
    def create_company_dao(cls, config):
        return CompanyDao(
            host=config['DATABASE']['host'],
            user=config['DATABASE']['user'],
            password=config['DATABASE']['password'],
            database=config['DATABASE']['database']
        )

    @classmethod
    def create_company_service(cls, company_dao):
        return CompanyService(company_dao)

def read_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

def initialize_system(config_path="/Users/vidisha/Desktop/DESISProject/DesisSG-2/backend/config.ini"):
    config = read_config(config_path)
    factory = ConcreteFactory()

    company_dao = factory.create_company_dao(config)
    company_service = factory.create_company_service(company_dao)

    return company_service