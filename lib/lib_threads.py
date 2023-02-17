import concurrent.futures


def run_parallel(process_func, range_args):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_func, i) for i in range_args]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    return results