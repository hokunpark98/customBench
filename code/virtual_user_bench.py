import requests
import time
import numpy as np
import argparse

def send_request(url):
    headers = {"Content-Type": "application/json"}
    start_time = time.time_ns()
    try:
        response = requests.get(url=url, headers=headers)
        end_time = time.time_ns()
        response_time_ns = end_time - start_time

        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('result') == 5:
                return response_time_ns / 1_000_000  # Convert ns to ms
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON decoding failed: {response.text} caused {e}")
    return None

def simulate_load(rate_limit, url):
    response_times = []
    for _ in range(rate_limit):
        response_time = send_request(url)
        if response_time is not None:
            response_times.append(response_time)

    successful_responses = len(response_times)
    if response_times:
        percentiles = {
            '50th': np.percentile(response_times, 50),
            '95th': np.percentile(response_times, 95),
            '99th': np.percentile(response_times, 99),
        }
    else:
        percentiles = None
    return successful_responses, response_times, percentiles

def main(rate_limit, url, duration, threshold):
    start_time = time.time()
    all_response_times = []
    total_requests = 0

    while time.time() - start_time < duration:
        successful_responses, response_times, percentiles = simulate_load(rate_limit, url)
        all_response_times.extend(response_times)
        total_requests += rate_limit
        time.sleep(1)  # Ensure we run the next batch after 1 second

    over_threshold_count = sum(1 for time in all_response_times if time > threshold)
    successful_responses = len(all_response_times)

    if all_response_times:
        percentiles = {
            '50th': np.percentile(all_response_times, 50),
            '95th': np.percentile(all_response_times, 95),
            '99th': np.percentile(all_response_times, 99),
        }
        result_str = (
            f"Total requests sent: {total_requests}, "
            f"successful responses: {successful_responses}, "
            f"over threshold {over_threshold_count} times, "
            f"50th percentile {percentiles['50th']:.0f} ms, "
            f"95th percentile {percentiles['95th']:.0f} ms, "
            f"99th percentile {percentiles['99th']:.0f} ms\n"
        )
    else:
        result_str = "No successful responses."

    print(result_str)

    with open('/home/dnc/master/customBench/code/virtual_user_result.txt', 'w') as file:
        file.write(result_str)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load testing script.')
    parser.add_argument('rate_limit', type=int, help='Number of requests per second.')
    parser.add_argument('url', type=str, help='The URL to send requests to.')
    parser.add_argument('duration', type=int, help='Duration of the test in seconds.')
    parser.add_argument('threshold', type=int, help='Threshold in ms to count response times over it.')

    args = parser.parse_args()
    
    main(args.rate_limit, args.url, args.duration, args.threshold)
