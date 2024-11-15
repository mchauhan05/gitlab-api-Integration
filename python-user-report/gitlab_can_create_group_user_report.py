import requests
import csv

# Configuration
GITLAB_BASE_URL = "REPLACE_WITH_YOUR_GITLAB_BASE_URL"
API_TOKEN = "REPLACE_WITH_YOUR_ADMIN_API_TOKEN"
HEADERS = {"Private-Token": API_TOKEN}
OUTPUT_FILE = "gitlab_can_create_group_user_report.csv"


def fetch_users(page=1, per_page=100):
    """Fetch users from GitLab API with pagination."""
    url = f"{GITLAB_BASE_URL}/users"
    params = {"page": page, "per_page": per_page}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()


def filter_users(users):
    """Filter users where can_create_group is True."""
    return [
        {
            "id": user["id"],
            "username": user["username"],
            "email": user.get("email", "N/A"),  # Email may not always be present
            "name": user["name"],
            "state": user["state"],
            "is_admin": user["is_admin"],
            "can_create_project": user["can_create_project"],
        }
        for user in users
        if user["can_create_group"]
    ]


def write_to_csv(data, filename):
    """Write user data to CSV."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["id", "username", "email", "name", "state", "is_admin", "can_create_project"],
        )
        writer.writeheader()
        writer.writerows(data)


def main():
    page = 1
    per_page = 100
    all_filtered_users = []

    while True:
        print(f"Fetching page {page}...")
        users = fetch_users(page=page, per_page=per_page)
        if not users:
            break
        filtered_users = filter_users(users)
        all_filtered_users.extend(filtered_users)
        page += 1

    write_to_csv(all_filtered_users, OUTPUT_FILE)
    print(f"Data written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
