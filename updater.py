import os
import datetime
import random
import time
import subprocess
import yaml

def run_random_startup_commits(file_path="update.yaml"):
    """
    Executes a random number of update-and-commit cycles (1 to 5) sequentially.
    """
    # Force the working directory to be the script's actual folder
    # This prevents path resolution issues when triggered via the Windows Startup folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Determine random number of iterations between 1 and 5
    iterations = random.randint(1, 5)
    print(f"Startup triggered. Running {iterations} automated update/commit cycles...")

    for i in range(iterations):
        # Default fallback structure
        data = {
            "LAST_UPDATE": "Never",
            "UPDATE_TIMES": 0
        }

        # Step 1: Read the existing YAML file
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as file:
                    loaded_data = yaml.safe_load(file)
                    if loaded_data and isinstance(loaded_data, dict):
                        data = loaded_data
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

        # Step 2: Generate the current timestamp matching your format
        current_time = datetime.datetime.now()
        formatted_date = current_time.strftime("%A %B %d %Y at %H:%M:%S")

        # Step 3: Modify values
        data["LAST_UPDATE"] = formatted_date
        try:
            data["UPDATE_TIMES"] = int(data.get("UPDATE_TIMES", 0)) + 1
        except (ValueError, TypeError):
            data["UPDATE_TIMES"] = 1

        # Step 4: Save the updated contents back to the YAML file
        try:
            with open(file_path, "w") as file:
                yaml.dump(data, file, default_flow_style=False, sort_keys=False)
            print(f"[{i+1}/{iterations}] Updated {file_path} successfully.")
        except Exception as e:
            print(f"Error writing to {file_path}: {e}")
            continue

        # Step 5: Execute Git staging and commit actions
        try:
            subprocess.run(["git", "add", file_path], check=True)
            subprocess.run(["git", "commit", "-m", f"Auto-update {i+1}/{iterations}: {formatted_date}"], check=True)
            print(f"[{i+1}/{iterations}] Git commit completed.")
        except Exception as e:
            print(f"Git tracking/commit execution failed: {e}")

        # Add a short 1-second delay between iterations to ensure unique timestamps
        if i < iterations - 1:
            time.sleep(1)

if __name__ == "__main__":
    run_random_startup_commits()
