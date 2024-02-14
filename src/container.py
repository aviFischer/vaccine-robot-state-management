from dependency_injector import containers, providers

from gantry_movement import MarlinClient
from state_machine import VaccineRobot

class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["state_machine"])

    config = providers.Configuration(yaml_files=["config.yml"])

    marlin_client = providers.Singleton(MarlinClient)

    vaccine_robot_state_machine = providers.Singleton(VaccineRobot)

