import time
import numpy as np
from typing import List, Optional
from statistics import mean
import matplotlib.pyplot as plt



import threading
import pandas as pd
import requests
import plotly.express as px

def generate_data() -> List[int]:
    """Generate some random data."""
    return np.random.randint(100, 10000, 1000).tolist()

def process1(data: List[int]) -> List[int]:
    """TODO: Document this function. What does it do? What are the inputs and outputs?"""
    def foo(x):
        """Find the next largest prime number."""
        while True:
            x += 1
            if all(x % i for i in range(2, x)):
                return x
    return [foo(x) for x in data]

def process2(data: List[int]) -> List[int]:
    """TODO: Document this function. What does it do? What are the inputs and outputs?"""
    def foo(x):
        """Find the next largest prime number."""
        while True:
            x += 1
            if int(np.sqrt(x)) ** 2 == x:
                return x
    return [foo(x) for x in data]

def final_process(data1: List[int], data2: List[int]) -> List[int]:
    """TODO: Document this function. What does it do? What are the inputs and outputs?"""
    return np.mean([x - y for x, y in zip(data1, data2)])

offload_url = 'http://127.0.0.1:5001' # TODO: Change this to the IP address of your server

def run(offload: Optional[str] = None) -> float:
    """Run the program, offloading the specified function(s) to the server.
    
    Args:
        offload: Which function(s) to offload to the server. Can be None, 'process1', 'process2', or 'both'.

    Returns:
        float: the final result of the program.
    """
    data = generate_data()
    if offload is None: # in this case, we run the program locally
        data1 = process1(data)
        data2 = process2(data)
    elif offload == 'process1':
        data1 = None
        def offload_process1(data):
            nonlocal data1
            url = f"{offload_url}/process1"  # URL of the process1 endpoint on the server
            data_dict = {"data": data}  # create a dictionary containing the input data
            response = requests.post(url, json=data_dict)  # send a POST request to the server with the input data
            # TODO: Send a POST request to the server with the input data
            data1 = response.json()['result']
        thread = threading.Thread(target=offload_process1, args=(data,))
        thread.start()
        data2 = process2(data)
        thread.join()
        # Question 2: Why do we need to join the thread here?
        # Question 3: Are the processing functions executing in parallel or just concurrently? What is the difference?
        #   See this article: https://oxylabs.io/blog/concurrency-vs-parallelism
        #   ChatGPT is also good at explaining the difference between parallel and concurrent execution!
        #   Make sure to cite any sources you use to answer this question.
    elif offload == 'process2':
        # TODO: Implement this case
        data2 = None
        def offload_process2(data):
            nonlocal data2
            url = f"{offload_url}/process2"  # URL of the process1 endpoint on the server
            data_dict = {"data": data}  # create a dictionary containing the input data
            response = requests.post(url, json=data_dict)  # send a POST request to the server with the input data
            # TODO: Send a POST request to the server with the input data
            data2 = response.json()['result']
        thread = threading.Thread(target=offload_process2, args=(data,))
        thread.start()
        data1 = process1(data)
        thread.join()
        pass
    elif offload == 'both':
        # TODO: Implement this case
        data1 = None
        data2 = None
        def offload_both(data):
            nonlocal data1
            nonlocal data2
            url = f"{offload_url}/process1"  # URL of the process1 endpoint on the server
            data_dict = {"data": data}  # create a dictionary containing the input data
            response = requests.post(url, json=data_dict)  # send a POST request to the server with the input data
            # TODO: Send a POST request to the server with the input data
            data1 = response.json()['result']

            url2 = f"{offload_url}/process2"  # URL of the process1 endpoint on the server
            response = requests.post(url2, json=data_dict)  # send a POST request to the server with the input data
            # TODO: Send a POST request to the server with the input data
            data2 = response.json()['result']

        thread = threading.Thread(target=offload_both, args=(data,))
        thread.start()
        thread.join()
        pass

    ans = final_process(data1, data2)
    return ans 


def main():
    modes = [None, 'process1', 'process2', 'both']

    results = []
    for mode in modes:
        execution_times = []
        for i in range(5):
            start_time = time.time()
            run(mode)
            execution_time = time.time() - start_time
            execution_times.append(execution_time)
            print(f"Mode {mode}, run {i}: {execution_time:.2f}s")
        results.append({'Mode': mode, 'Execution Time (s)': execution_times})

    data = pd.DataFrame(results)

    avg_none = mean(data.loc[1, 0], data.loc[1, 4], data.loc[1, 8], data.loc[1, 12], data.loc[1, 16])
    avg_process1 = mean(data.loc[1, 1], data.loc[1, 5], data.loc[1, 9], data.loc[1, 13], data.loc[1, 17])
    avg_process2 = mean(data.loc[1, 2], data.loc[1, 6], data.loc[1, 10], data.loc[1, 14], data.loc[1, 18])
    avg_both = mean(data.loc[1, 3], data.loc[1, 7], data.loc[1, 11], data.loc[1, 15], data.loc[1, 19])
    
    avg_values = ["avg_none", "avg_process1", "avg_process2", "avg_both"]
    column_names2 = ["none", "process1", "process2", "both"]
    
    fig = plt.figure(figsize = (10, 5))
    # creating the bar plot
    plt.bar(column_names2, avg_values, color ='maroon', width = 0.4)
    plt.xlabel("process offloaded")
    plt.ylabel("mean time to complete process")
    plt.title("Time to Complete Offloaded versus Non-Offloaded Processes")
    plt.show()
    
    # TODO: save plot to "makespan.png"
    plt.savefig("makespan.png")
def main():
    # TODO: Run the program 5 times for each offloading mode, and record the total execution time
    #   Compute the mean and standard deviation of the execution times
    #   Hint: store the results in a pandas DataFrame, use previous labs as a reference
    message = []
    offloading = [None, "process1", "process2", "both"]
    for mode in offloading:
        times = []
        for i in range(5):
            start = time.time()
            run(mode)
            end = time.time()
            times.append(end - start)
            print(f"{mode}, mean:{np.mean(times)}, standard deviation:{np.std(times)}")
        message.append([str(mode), np.mean(times), np.std(times)])
    df = pd.DataFrame(message, columns=['Mode', "Mean", "Standard Deviation"])
    # TODO: Plot makespans (total execution time) as a bar chart with error bars
    # Make sure to include a title and x and y labels
    bar = px.bar(df, x='Mode', y='Mean', error_y='Standard Deviation', title="Makespans for different offloading modes")
    

    # TODO: save plot to "makespan.png"
    bar.write_image("makespan.png")   


    # TODO: Run the program 5 times for each offloading mode, and record the total execution time
    #   Compute the mean and standard deviation of the execution times
    #   Hint: store the results in a pandas DataFrame, use previous labs as a reference


    # TODO: Plot makespans (total execution time) as a bar chart with error bars
    # Make sure to include a title and x and y labels


    # TODO: save plot to "makespan.png"


    # Question 4: What is the best offloading mode? Why do you think that is?
    # Question 5: What is the worst offloading mode? Why do you think that is?
    # Question 6: The processing functions in the example aren't very likely to be used in a real-world application. 
    #   What kind of processing functions would be more likely to be used in a real-world application?
    #   When would you want to offload these functions to a server?
    
    
if __name__ == '__main__':
    main()