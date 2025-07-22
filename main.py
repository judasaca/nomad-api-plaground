from config import settings
import requests

api_base_path = settings.api_base_path


def main():
    response = requests.post(
        api_base_path + "/auth/token",
        data={"username": settings.username, "password": settings.password.get_secret_value()},
    )
    print(response.status_code, response.json())


if __name__ == "__main__":
    main()
