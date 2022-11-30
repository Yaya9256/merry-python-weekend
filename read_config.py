import yaml

PATH = "config/conf.yml"


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def get_redis_info(data=read_yaml(PATH)):
    redis_url = data['APP']
    return redis_url


def get_db_info(data=read_yaml(PATH)):
    db_info = data['DATABASE']
    return db_info




