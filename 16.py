import concurrent.futures
import logging
import random
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [THREAD_POOL] %(message)s")

def process_heavy_computation(job_id: int):
    logging.info(f"Worker starting job #{job_id}")
    time.sleep(random.uniform(0.5, 1.2))
    result = job_id * 42
    logging.info(f"Job #{job_id} completed. Result: {result}")
    return result

def main():
    jobs = range(1, 15)
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(process_heavy_computation, j): j for j in jobs}
        
        for future in concurrent.futures.as_completed(futures):
            job_num = futures[future]
            try:
                data = future.result()
            except Exception as exc:
                logging.error(f"Job #{job_num} generated an exception: {exc}")

    elapsed = time.time() - start_time
    logging.info(f"All 14 jobs completed across 4 threads in {elapsed:.2f} seconds.")

if __name__ == "__main__":
    main()

    