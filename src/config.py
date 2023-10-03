class Config:
    SECRET_KEY = 'B!1weNAt1T^%kvhUI*S^'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'parking.c8ybi9whms5y.us-east-1.rds.amazonaws.com'
    MYSQL_USER = 'accelcasst'
    MYSQL_PASSWORD = 'Mugiwara0244'
    MYSQL_DB = 'parking2'

config={
    'development':DevelopmentConfig
}
