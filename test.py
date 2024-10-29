import subprocess
import re
import time
import pandas as pd
import os


def run_time(file_command, file_input=None):
    start_time = time.perf_counter()
    result = subprocess.run(file_command, input=file_input, capture_output=True, text=True)
    end_time = time.perf_counter()
    match = re.search(r'Maximum resident set size \(kbytes\): (\d+)', result.stderr)
    if match:
        max_resident_size = match.group(1)
    else:
        max_resident_size = -1

    return end_time - start_time, max_resident_size


def log_results():
    command = ["/usr/bin/time", "-v", "./main.out"]
    user_input = "5\n"
    run_time_value, memory_usage = run_time(command)

    result_data = {
        "execution_time_ms": run_time_value * 1000,
        "memory_usage_kb": memory_usage
    }

    csv_file = 'c-cpp_test/test.csv'
    if os.path.exists(csv_file):
        try:
            df = pd.read_csv(csv_file)
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=["execution_time_ms", "memory_usage_kb"])
    else:
        # 创建一个新的CSV文件并添加列标题
        df = pd.DataFrame(columns=["execution_time_ms", "memory_usage_kb"])
        df.to_csv(csv_file, index=False)

    result_df = pd.DataFrame([result_data])

    # 使用 pd.concat 替代 append
    if not result_df.empty:
        df = pd.concat([df, result_df], ignore_index=True)
    # 写入CSV文件
    df.to_csv(csv_file, index=False)

    # 提交更改
    subprocess.run(["git", "config", "--local", "user.email", os.environ.get("GIT_EMAIL", "default@example.com")])
    subprocess.run(["git", "config", "--local", "user.name", os.environ.get("GIT_NAME", "default_name")])
    
    # 使用 git add . 来添加所有未跟踪的文件
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Update test.csv with results"])
    subprocess.run(["git", "push", "origin", "main"])


if __name__ == "__main__":
    log_results()
