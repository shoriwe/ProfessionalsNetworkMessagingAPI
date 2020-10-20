from main import app
from main import configure


configure()


if __name__ == '__main__':
    app.run(port=5001)
