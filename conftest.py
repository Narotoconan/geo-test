import pytest
from util.driver import base
from dotenv.main import load_dotenv
import os


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        choices=['sit', 'dev', 'prod'],
        help="sit：测试环境，dev:开发环境，prod:生产环境，默认dev"
    )


@pytest.fixture(scope='session', autouse=True)
def set_env(request):
    # 设置base_url
    load_dotenv()
    env = request.config.getoption("--env")
    base.base_url = os.environ.get(env)
