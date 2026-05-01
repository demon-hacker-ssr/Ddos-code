#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LOAD TESTING SUITE - AUTHORIZED USE ONLY
Created by: SSR Security Research Team
Version: 2.1 - Enterprise Load Tester
License: For authorized security testing only
"""

import requests
import threading
import time
import queue
import sys
import os
from datetime import datetime
import random
import hashlib

# ============================================
# SSR INTERFACE - FULL SCREEN DISPLAY
# ============================================

def clear_screen():
    """Clear terminal screen for full-screen effect"""
    os.system('cls' if os.name == 'nt' else 'clear')

def banner_display():
    """Display SSR full-screen interface"""
    clear_screen()
    
    # Calculate terminal size (approximate full screen)
    try:
        terminal_width = os.get_terminal_size().columns
        terminal_height = os.get_terminal_size().lines
    except:
        terminal_width = 120
        terminal_height = 30
    
    # ASCII Art Banner - SSR Style
    banner = f"""
{'█' * terminal_width}
{' ' * ((terminal_width - 60) // 2)}╔════════════════════════════════════════════════════╗
{' ' * ((terminal_width - 60) // 2)}║                                                            ║
{' ' * ((terminal_width - 60) // 2)}║     ███████╗███████╗██████╗     ████████╗███████╗███████╗║
{' ' * ((terminal_width - 60) // 2)}║     ██╔════╝██╔════╝██╔══██╗    ╚══██╔══╝██╔════╝██╔════╝║
{' ' * ((terminal_width - 60) // 2)}║     ███████╗███████╗██████╔╝       ██║   █████╗  ███████╗║
{' ' * ((terminal_width - 60) // 2)}║     ╚════██║╚════██║██╔══██╗       ██║   ██╔══╝  ╚════██║║
{' ' * ((terminal_width - 60) // 2)}║     ███████║███████║██║  ██║       ██║   ███████╗███████║║
{' ' * ((terminal_width - 60) // 2)}║     ╚══════╝╚══════╝╚═╝  ╚═╝       ╚═╝   ╚══════╝╚══════╝║
{' ' * ((terminal_width - 60) // 2)}║                                                            ║
{' ' * ((terminal_width - 60) // 2)}║              ENTERPRISE LOAD TESTING SUITE                  ║
{' ' * ((terminal_width - 60) // 2)}║                      AUTHORIZED USE ONLY                    ║
{' ' * ((terminal_width - 60) // 2)}║                                                            ║
{' ' * ((terminal_width - 60) // 2)}╚════════════════════════════════════════════════════╝
{'█' * terminal_width}
    """
    
    print(banner)
    
    # Developer credit with animation effect
    credits = [
        "╔════════════════════════════════════════════════════════════════╗",
        "║                    DEVELOPED WITH PRECISION BY                 ║",
        "║                      S S R  S E C U R I T Y                    ║",
        "║                                                                ║",
        "║         \"Security through testing, not through obscurity\"       ║",
        "║                                                                ║",
        "║      [ LEGITIMATE SECURITY TESTING PLATFORM v2.1 ]            ║",
        "╚════════════════════════════════════════════════════════════════╝"
    ]
    
    for line in credits:
        padding = (terminal_width - len(line)) // 2
        print(' ' * padding + line)
        time.sleep(0.1)
    
    print("\n\n")
    time.sleep(1)

def verification_screen():
    """SSR Verification and Authorization Check"""
    clear_screen()
    
    print("\n" * 5)
    print("=" * 70)
    print("🔐 SSR SECURITY VERIFICATION PORTAL 🔐")
    print("=" * 70)
    print("\n")
    print("This tool is property of SSR Security Research Team")
    print("Unauthorized use will be prosecuted to the fullest extent of law\n")
    print("-" * 70)
    
    # Developer verification
    dev_name = input("\n[SSR] Enter developer authorization key: ")
    
    # Simple verification (you can change this key)
    verification_key = hashlib.md5(f"SSR_{dev_name}_2026".encode()).hexdigest()[:8]
    
    print(f"\n[SSR] Verification ID: {verification_key}")
    print("[SSR] Validating credentials...")
    time.sleep(1.5)
    
    # Check if user entered SSR or any variation
    if dev_name.upper() in ["SSR", "S.S.R", "SSR-SECURITY", "SSR_DEVELOPER"]:
        print("\n✅ SSR DEVELOPER ACCESS GRANTED ✅")
        time.sleep(1)
        return True
    else:
        print("\n⚠️  AUTHORIZED USER VERIFIED ⚠️")
        print(f"Welcome, {dev_name.upper()} - Authorized testing personnel")
        time.sleep(1)
        
        # Legal agreement
        print("\n" + "="*70)
        print("📜 LEGAL AGREEMENT - READ CAREFULLY 📜")
        print("="*70)
        print("\nBy proceeding, you confirm that:")
        print("1. You have WRITTEN PERMISSION to test the target")
        print("2. You own the target system OR have explicit authorization")
        print("3. You understand unauthorized testing is a FEDERAL CRIME")
        print("4. You accept full legal responsibility for your actions")
        print("\n" + "="*70)
        
        agreement = input("\nType 'I AGREE' to continue: ")
        if agreement.upper() == "I AGREE":
            print("\n✅ Legal agreement accepted")
            return True
        else:
            print("\n❌ Authorization failed - Exiting")
            return False

# ============================================
# CORE TESTING ENGINE
# ============================================

class SSRLoadTester:
    """Core load testing engine - SSR Enterprise Edition"""
    
    def __init__(self, target_url, total_requests=1000000, batch_size=10000, threads=50):
        self.target = target_url
        self.total = total_requests
        self.batch = batch_size
        self.threads = threads
        self.batches = total_requests // batch_size
        self.success = 0
        self.failed = 0
        self.lock = threading.Lock()
        self.task_queue = queue.Queue()
        self.start_time = None
        self.end_time = None
        
        # Custom user agents for realistic testing
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'SSR-LoadTester/2.1 (Compatible; Security Testing)'
        ]
    
    def fire_request(self, req_id):
        """Single request execution with SSR signature"""
        ua = random.choice(self.user_agents)
        headers = {
            'User-Agent': ua,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'X-SSR-Test-ID': f"SSR-{req_id}-{int(time.time())}",
            'X-Testing-Purpose': 'Authorized Load Testing'
        }
        
        try:
            # Send request with small timeout for testing
            resp = requests.get(self.target, headers=headers, timeout=3, verify=False)
            
            if resp.status_code in [200, 201, 202, 204]:
                with self.lock:
                    self.success += 1
                return True
            else:
                with self.lock:
                    self.failed += 1
                return False
                
        except requests.Timeout:
            with self.lock:
                self.failed += 1
            return False
        except requests.ConnectionError:
            with self.lock:
                self.failed += 1
            return False
        except Exception:
            with self.lock:
                self.failed += 1
            return False
    
    def batch_strike(self, batch_id, batch_size):
        """Execute batch of requests - SSR coordinated strike"""
        local_success = 0
        local_failed = 0
        
        # Progress indicator for large batches
        if batch_id % 10 == 0:
            print(f"⚡ SSR | Executing batch {batch_id}/{self.batches}")
        
        for i in range(batch_size):
            req_id = f"{batch_id}-{i}-{int(time.time()*1000)}"
            if self.fire_request(req_id):
                local_success += 1
            else:
                local_failed += 1
        
        return local_success, local_failed
    
    def worker_agent(self, worker_id):
        """Worker thread - SSR security agent"""
        while not self.task_queue.empty():
            try:
                batch_id, batch_size = self.task_queue.get_nowait()
                
                success, failed = self.batch_strike(batch_id, batch_size)
                
                with self.lock:
                    self.success += success
                    self.failed += failed
                
                self.task_queue.task_done()
                
            except queue.Empty:
                break
            except Exception as e:
                print(f"⚠️ Worker {worker_id} error: {str(e)[:50]}")
                continue
    
    def execute_assault(self):
        """Main execution engine"""
        print("\n" + "="*70)
        print("🎯 SSR LOAD TEST INITIALIZED 🎯")
        print("="*70)
        print(f"📡 Target: {self.target}")
        print(f"💥 Total Payload: {self.total:,} requests")
        print(f"📦 Batch Size: {self.batch:,} requests/group")
        print(f"🔧 Task Forces: {self.threads} parallel workers")
        print(f"⏱️  Time Window: 60 seconds (target)")
        print(f"🎯 Request Rate: {self.total/60:,.0f} req/sec")
        print("="*70)
        
        # Final confirmation with SSR protocol
        print("\n⚠️  SSR PROTOCOL - FINAL VERIFICATION ⚠️")
        print("This test will send HTTP requests to the target system")
        print("Ensure you have proper authorization!")
        
        confirm = input("\n[SSR] Type 'EXECUTE' to start the test: ")
        if confirm.upper() != "EXECUTE":
            print("[SSR] Mission aborted - Returning to safe mode")
            return False
        
        # Load the queue with batches
        print("\n[SSR] Preparing attack vectors...")
        for batch_id in range(self.batches):
            self.task_queue.put((batch_id, self.batch))
        
        print(f"[SSR] {self.batches} batches loaded into queue")
        print("[SSR] Deploying worker threads...")
        
        self.start_time = time.time()
        
        # Launch worker threads
        workers = []
        for wid in range(self.threads):
            worker = threading.Thread(target=self.worker_agent, args=(wid,))
            worker.start()
            workers.append(worker)
        
        # Monitor progress in real-time
        start_monitor = time.time()
        last_success = 0
        
        while any(w.is_alive() for w in workers):
            time.sleep(0.5)
            elapsed = time.time() - self.start_time
            
            # Progress display every 2 seconds
            if int(elapsed * 2) > int((time.time() - start_monitor) * 2):
                current_rate = (self.success - last_success) / (time.time() - start_monitor)
                print(f"\r📊 Progress: {self.success + self.failed:,}/{self.total:,} | "
                      f"✅ {self.success:,} | ❌ {self.failed:,} | "
                      f"⚡ {current_rate:,.0f} req/s", end='', flush=True)
                last_success = self.success
                start_monitor = time.time()
        
        self.end_time = time.time()
        return True
    
    def analyze_results(self):
        """SSR Results Analysis Engine"""
        duration = self.end_time - self.start_time
        success_rate = (self.success / self.total) * 100 if self.total > 0 else 0
        
        print("\n\n" + "="*70)
        print("📊 SSR ANALYSIS REPORT 📊")
        print("="*70)
        print(f"\n⏱️  Total Time: {duration:.2f} seconds")
        print(f"📈 Requests/Second: {self.total/duration:.2f}")
        print(f"✅ Successful: {self.success:,}")
        print(f"❌ Failed: {self.failed:,}")
        print(f"📊 Success Rate: {success_rate:.2f}%")
        print(f"🎯 Target Rate: {self.total/60:,.0f} req/min")
        print(f"⚡ Actual Rate: {self.total/duration*60:,.0f} req/min")
        
        print("\n" + "-"*70)
        
        # SSR Verdict
        if success_rate >= 95:
            print("\n💥 BOOM! 💥")
            print("✅ TARGET SUCCESSFULLY HANDLED THE LOAD TEST")
            print("   The system processed all requests without significant failure")
            print("   Recommendation: Increase load for stress testing")
            return True
        elif success_rate >= 50:
            print("\n⚠️ PARTIAL SUCCESS ⚠️")
            print("   Target handled moderate load but showed degradation")
            print("   System may need optimization for high traffic")
            return False
        else:
            print("\n❌ NOT SUCCESSFUL ❌")
            print("   Target FAILED to handle the load test")
            print("   System crashed or became unresponsive under pressure")
            print("   Immediate infrastructure review recommended")
            return False

# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """SSR Main Controller"""
    try:
        # Display SSR Interface
        banner_display()
        
        # Run verification
        if not verification_screen():
            sys.exit(1)
        
        clear_screen()
        banner_display()
        
        # Configuration Section
        print("\n" + "="*70)
        print("⚙️  SSR CONFIGURATION PANEL ⚙️")
        print("="*70)
        
        target = input("\n🎯 Target URL (http://example.com): ").strip()
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
        
        print("\n⚡ SSR RECOMMENDED SETTINGS:")
        print("   • Total Requests: 1,000,000")
        print("   • Batch Size: 10,000")
        print("   • Threads: 50-100")
        
        total = int(input("\n📊 Total requests (default 1000000): ") or 1000000)
        batch = int(input("📦 Batch size (default 10000): ") or 10000)
        threads = int(input("🔧 Threads (default 50): ") or 50)
        
        # Validate configurations
        if total % batch != 0:
            total = total - (total % batch)
            print(f"⚠️ Adjusted total to {total:,} for batch alignment")
        
        # Quick connectivity test
        print("\n[SSR] Running pre-test diagnostics...")
        try:
            test_req = requests.get(target, timeout=5)
            print(f"✅ Target online - Status: {test_req.status_code}")
        except:
            print("❌ Cannot reach target - Check URL/network")
            sys.exit(1)
        
        # Initialize and execute
        tester = SSRLoadTester(target, total, batch, threads)
        
        if tester.execute_assault():
            tester.analyze_results()
        else:
            print("[SSR] Test execution cancelled")
    
    except KeyboardInterrupt:
        print("\n\n⚠️ SSR Test interrupted by operator")
        print("[SSR] Safely terminating threads...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ SSR Error: {str(e)}")
        print("[SSR] Contact support with error details")

if __name__ == "__main__":
    # Set higher recursion limit and disable SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    main()
