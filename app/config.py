#Holds structured, non-secret settings: server port, logging levels, feature flags, pool sizes, API base paths.
from fastapi import FastAPI
from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    database_hostname: str
    database_port: str 
    database_password: str 
    database_name: str
    database_username: str 
    mail_username:str
    mail_password:str
    mail_from:str
    mail_port:int
    mail_server:str
    model_config=SettingsConfigDict(env_file=".env")

settings = Settings()
