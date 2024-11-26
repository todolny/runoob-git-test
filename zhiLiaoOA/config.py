SECRET_KEY="fadsfafefsdf"

HOSTNAME = "localhost"
PORT = '5432'
DATABASE = "zhiliaooa_course"
USERNAME = "postgres"
PASSWORD = "renderg"
DB_URI = f"postgresql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
SQLALCHEMY_DATABASE_URI = DB_URI

#邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "1642992358@qq.com"
MAIL_PASSWORD="jaemxfxqwskideff"
MAIL_DEFAULT_SENDER="1642992358@qq.com"