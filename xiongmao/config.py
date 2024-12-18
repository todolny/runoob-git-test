SECRET_KEY = "asfasfasdfageasd"#设置加密长度

#数据库配置信息
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "123456"
DATABASE = "xiongmaodd"
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI



#邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "1207840645@qq.com"
MAIL_PASSWORD="alfrskdhlxrnigej"
MAIL_DEFAULT_SENDER="1207840645@qq.com"
#alfrskdhlxrnigej