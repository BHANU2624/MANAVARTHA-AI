"""
MANA VARTHA AI - Comprehensive Testing Script
Tests RAG engine with various query types
"""

import requests
import json
import time
from typing import List, Dict

# API Configuration
API_BASE_URL = "http://localhost:8000"

# ANSI color codes for pretty printing
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")

def test_health_check() -> bool:
    """Test health check endpoint"""
    print_header("Testing Health Check")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Status: {data['status']}")
            print_success(f"Message: {data['message']}")
            print_success(f"Chunks Loaded: {data['chunks_loaded']}")
            return True
        else:
            print_error(f"Health check failed: Status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {e}")
        return False

def test_query(query: str, expected_language: str = None) -> Dict:
    """Test a single query"""
    try:
        start_time = time.time()
        
        response = requests.get(
            f"{API_BASE_URL}/search",
            params={"query": query},
            timeout=10
        )
        
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n{Colors.BOLD}Query:{Colors.ENDC} {query}")
            print(f"{Colors.BOLD}Language Detected:{Colors.ENDC} {data.get('language', 'N/A')}")
            print(f"{Colors.BOLD}Response Time:{Colors.ENDC} {elapsed_time:.2f}s")
            print(f"{Colors.BOLD}Chunks Retrieved:{Colors.ENDC} {data.get('chunks_retrieved', 0)}")
            print(f"\n{Colors.BOLD}Answer:{Colors.ENDC}")
            print(f"{data['answer']}")
            
            if data.get('sources'):
                print(f"\n{Colors.BOLD}Top Source (truncated):{Colors.ENDC}")
                print(f"{data['sources'][0][:200]}...")
            
            # Validation
            if expected_language and data.get('language') != expected_language:
                print_error(f"Language mismatch: expected {expected_language}, got {data.get('language')}")
            
            if elapsed_time > 5.0:
                print_error(f"Response too slow: {elapsed_time:.2f}s")
            else:
                print_success(f"Response time OK")
            
            return data
        else:
            print_error(f"Query failed: Status {response.status_code}")
            print_error(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Query error: {e}")
        return None

def run_telugu_tests():
    """Test Telugu queries"""
    print_header("Testing Telugu Queries")
    
    telugu_queries = [
        "వాతావరణం ఎలా ఉంది?",
        "క్రికెట్ వార్తలు ఏమిటి?",
        "ఆంధ్రప్రదేశ్ లో తాజా వార్తలు",
        "రాజకీయ పరిస్థితి గురించి చెప్పండి",
        "తెలుగు సినిమా వార్తలు"
    ]
    
    results = []
    for query in telugu_queries:
        result = test_query(query, expected_language='telugu')
        results.append(result is not None)
        time.sleep(1)  # Rate limiting
    
    success_rate = sum(results) / len(results) * 100
    print_info(f"\nTelugu Queries Success Rate: {success_rate:.1f}%")
    return success_rate

def run_english_tests():
    """Test English queries"""
    print_header("Testing English Queries")
    
    english_queries = [
        "What is the weather update?",
        "Tell me about cricket news",
        "What are the latest political developments?",
        "Any news about movies?",
        "What happened in Andhra Pradesh recently?"
    ]
    
    results = []
    for query in english_queries:
        result = test_query(query, expected_language='english')
        results.append(result is not None)
        time.sleep(1)
    
    success_rate = sum(results) / len(results) * 100
    print_info(f"\nEnglish Queries Success Rate: {success_rate:.1f}%")
    return success_rate

def run_romanized_tests():
    """Test Romanized Telugu queries"""
    print_header("Testing Romanized Telugu Queries")
    
    romanized_queries = [
        "cricket news em undi?",
        "weather ela undi?",
        "politics gurinchi cheppandi",
        "cinema news enti?",
        "AP lo em jarigindi?"
    ]
    
    results = []
    for query in romanized_queries:
        result = test_query(query, expected_language='romanized')
        results.append(result is not None)
        time.sleep(1)
    
    success_rate = sum(results) / len(results) * 100
    print_info(f"\nRomanized Telugu Queries Success Rate: {success_rate:.1f}%")
    return success_rate

def run_edge_case_tests():
    """Test edge cases"""
    print_header("Testing Edge Cases")
    
    # Empty query
    print("\n--- Empty Query Test ---")
    try:
        response = requests.get(f"{API_BASE_URL}/search", params={"query": ""}, timeout=5)
        if response.status_code == 400:
            print_success("Empty query correctly rejected")
        else:
            print_error(f"Empty query not handled: Status {response.status_code}")
    except Exception as e:
        print_error(f"Error: {e}")
    
    # Very long query
    print("\n--- Long Query Test ---")
    long_query = "a" * 600
    try:
        response = requests.get(f"{API_BASE_URL}/search", params={"query": long_query}, timeout=5)
        if response.status_code == 400:
            print_success("Long query correctly rejected")
        else:
            print_error(f"Long query not handled: Status {response.status_code}")
    except Exception as e:
        print_error(f"Error: {e}")
    
    # Irrelevant query
    print("\n--- Irrelevant Query Test ---")
    test_query("What is the meaning of life?")
    
    # Mixed language query
    print("\n--- Mixed Language Query Test ---")
    test_query("cricket news ఎలా ఉంది?")

def run_performance_tests():
    """Test performance with rapid queries"""
    print_header("Testing Performance")
    
    queries = [
        "వాతావరణం ఎలా ఉంది?",
        "weather update",
        "cricket news em undi?"
    ]
    
    times = []
    for i in range(3):
        for query in queries:
            start = time.time()
            response = requests.get(
                f"{API_BASE_URL}/search",
                params={"query": query},
                timeout=10
            )
            elapsed = time.time() - start
            times.append(elapsed)
            
            if response.status_code == 200:
                print_success(f"Query {i+1} completed in {elapsed:.2f}s")
            else:
                print_error(f"Query {i+1} failed")
    
    if times:
        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)
        
        print_info(f"\nPerformance Statistics:")
        print_info(f"Average Response Time: {avg_time:.2f}s")
        print_info(f"Min Response Time: {min_time:.2f}s")
        print_info(f"Max Response Time: {max_time:.2f}s")
        
        if avg_time < 3.0:
            print_success("Performance target met (<3s average)")
        else:
            print_error(f"Performance target missed (>{avg_time:.2f}s)")

def main():
    """Main test runner"""
    print_header("MANA VARTHA AI - Comprehensive Test Suite")
    
    # Health check
    if not test_health_check():
        print_error("Backend is not healthy. Exiting tests.")
        return
    
    # Run all test suites
    telugu_rate = run_telugu_tests()
    english_rate = run_english_tests()
    romanized_rate = run_romanized_tests()
    run_edge_case_tests()
    run_performance_tests()
    
    # Final summary
    print_header("Test Summary")
    overall_rate = (telugu_rate + english_rate + romanized_rate) / 3
    
    print(f"{Colors.BOLD}Overall Success Rate:{Colors.ENDC} {overall_rate:.1f}%")
    print(f"{Colors.BOLD}Telugu Queries:{Colors.ENDC} {telugu_rate:.1f}%")
    print(f"{Colors.BOLD}English Queries:{Colors.ENDC} {english_rate:.1f}%")
    print(f"{Colors.BOLD}Romanized Telugu:{Colors.ENDC} {romanized_rate:.1f}%")
    
    if overall_rate >= 80:
        print_success("\n🎉 All tests passed! System is production ready.")
    elif overall_rate >= 60:
        print_info("\n⚠️  Most tests passed. Review failed cases.")
    else:
        print_error("\n❌ Many tests failed. System needs attention.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Tests interrupted by user{Colors.ENDC}")
    except Exception as e:
        print_error(f"Test suite error: {e}")