from app import init_app
from config import init_config

init_config()
app = init_app('config.Config')

if __name__ == '__main__':
    app.run()
