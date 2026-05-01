import requests
import threading
import time
import queue
from datetime import datetime
import sys

class LoadTester:
    def __init__(self, target_url, total_requests=1000000, requests_per_batch=10000, num_threads=50):
        """
        Initialize load tester
        
        Args:
            target_url: Target website URL
            total_requests: Total requests to send per minute (1,000,000)
            requests_per_batch: Requests to send in each batch (10,000)
            num_threads: Number of concurrent threads
        """
        self.target_url = target_url
        self.total_requests = total_requests
        self.requests_per_batch = requests_per_batch
        self.num_threads = num_threads
        self.total_batches = total_requests // requests_per_batch
        self.success_count = 0
        self.failure_count = 0
        self.lock = threading.Lock()
        self.task_queue = queue.Queue()
        
    def send_request(self, request_id):
        """Send a single HTTP request"""
        try:
            headers = {
                'User-Agent': f'Load-Tester-{request_id}',
                'Accept': '*/*',
                'Connection': 'keep-alive'
            }
            
            # Send request with timeout
            response = requests.get(
                self.target_url, 
                headers=headers, 
                timeout=5,
                verify=False  # Only for testing, disable SSL verification
            )
            
            # Check if request was successful
            if response.status_code == 200:
                with self.lock:
                    self.success_count += 1
                return True
            else:
                with self.lock:
                    self.failure_count += 1
                return False
                
        except requests.exceptions.RequestException as e:
            with self.lock:
                self.failure_count += 1
            return False
    
    def send_batch(self, batch_id, batch_size):
        """Send a batch of requests"""
        success = 0
        failure = 0
        
        for i in range(batch_size):
            request_id = f"{batch_id}_{i}"
            if self.send_request(request_id):
                success += 1
            else:
                failure += 1
        
        return success, failure
    
    def worker_thread(self, thread_id):
        """Worker thread to process batches"""
        while not self.task_queue.empty():
            try:
                batch_id, batch_size = self.task_queue.get_nowait()
                print(f"[Thread {thread_id}] Processing batch {batch_id}...")
                
                success, failure = self.send_batch(batch_id, batch_size)
                
                with self.lock:
                    self.success_count += success
                    self.failure_count += failure
                    
                self.task_queue.task_done()
                
            except queue.Empty:
                break
    
    def run_attack(self):
        """Run the load test"""
        print(f"\n{'='*60}")
        print(f"LOAD TEST CONFIGURATION")
        print(f"{'='*60}")
        print(f"Target URL: {self.target_url}")
        print(f"Total Requests: {self.total_requests:,}")
        print(f"Requests per Batch: {self.requests_per_batch:,}")
        print(f"Total Batches: {self.total_batches}")
        print(f"Threads: {self.num_threads}")
        print(f"Estimated Rate: {self.total_requests} requests/minute")
        print(f"{'='*60}\n")
        
        # Confirm with user
        confirm = input("⚠️  You must have WRITTEN PERMISSION to test this target!\nType 'AUTHORIZED' to continue: ")
        if confirm != "AUTHORIZED":
            print("❌ Test cancelled. Obtain written permission first.")
            return False
        
        # Prepare task queue with batches
        for batch_id in range(self.total_batches):
            self.task_queue.put((batch_id, self.requests_per_batch))
        
        start_time = time.time()
        
        # Create and start worker threads
        threads = []
        for i in range(self.num_threads):
            thread = threading.Thread(target=self.worker_thread, args=(i,))
            thread.start()
            threads.append(thread)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        duration = end_time - start_time
        
        return duration
    
    def display_results(self, duration):
        """Display test results"""
        print(f"\n{'='*60}")
        print(f"LOAD TEST RESULTS")
        print(f"{'='*60}")
        print(f"Time taken: {duration:.2f} seconds")
        print(f"Requests per second: {self.total_requests/duration:.2f}")
        print(f"Successful requests: {self.success_count:,}")
        print(f"Failed requests: {self.failure_count:,}")
        print(f"Success rate: {(self.success_count/(self.success_count+self.failure_count))*100:.2f}%")
        
        if self.success_count == self.total_requests:
            print(f"\n✅ BOOM! Website handled all {self.total_requests:,} requests successfully!")
            return True
        elif self.success_count > 0:
            print(f"\n⚠️  Partial success: Website handled {self.success_count:,} out of {self.total_requests:,} requests")
            return False
        else:
            print(f"\n❌ NOT SUCCESSFUL! Website failed to handle any requests!")
            return False

def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     LOAD TESTING TOOL - FOR AUTHORIZED USE ONLY         ║
    ║                                                          ║
    ║  WARNING: Unauthorized use is a CRIMINAL offense!      ║
    ║  Only use on systems you own or have permission for    ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Get user inputs
    target_url = input("Enter target URL (e.g., http://localhost:8000): ").strip()
    
    # Validate URL
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url
    
    try:
        total_requests = int(input("Total requests per minute (default 1000000): ") or 1000000)
        requests_per_batch = int(input("Requests per batch (default 10000): ") or 10000)
        num_threads = int(input("Number of threads (default 50): ") or 50)
        
        # Validate inputs
        if total_requests <= 0 or requests_per_batch <= 0 or num_threads <= 0:
            print("❌ Error: Values must be positive integers")
            return
        
        if total_requests % requests_per_batch != 0:
            print(f"⚠️  Warning: {total_requests} not divisible by {requests_per_batch}")
            print(f"Will send {total_requests - (total_requests % requests_per_batch)} requests")
            total_requests = total_requests - (total_requests % requests_per_batch)
        
        # Create and run load tester
        tester = LoadTester(target_url, total_requests, requests_per_batch, num_threads)
        
        # Test connection first
        print("\nTesting target connectivity...")
        try:
            test_response = requests.get(target_url, timeout=5)
            print(f"✅ Target reachable (Status: {test_response.status_code})")
        except:
            print("❌ Error: Cannot reach target. Check URL and network.")
            return
        
        # Run the test
        duration = tester.run_attack()
        
        if duration:
            tester.display_results(duration)
        
    except ValueError as e:
        print(f"❌ Error: Invalid input - {e}")
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()