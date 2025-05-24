"""
Test script for Twitter Thread Chunker functionality
Run this to validate the implementation without starting the full app
"""

def test_chunker():
    """Test the core chunking functionality"""
    print("🧵 Testing Twitter Chunker...")
    
    try:
        from twitter_chunker import chunk_text_for_twitter, get_thread_stats
        
        # Test text
        test_text = "This is a test of the Twitter Thread Chunker. " * 20
        
        # Test chunking
        tweets, warnings = chunk_text_for_twitter(test_text)
        
        print(f"✅ Chunking successful: {len(tweets)} tweets generated")
        
        # Test stats
        stats = get_thread_stats(tweets)
        print(f"✅ Stats calculation successful: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Chunker test failed: {e}")
        return False


def test_auth_import():
    """Test that authentication module imports correctly"""
    print("🔐 Testing Twitter Auth...")
    
    try:
        from twitter_auth import create_twitter_client, get_twitter_credentials
        print("✅ Auth module imports successful")
        return True
        
    except Exception as e:
        print(f"❌ Auth import failed: {e}")
        return False


def test_poster_import():
    """Test that posting module imports correctly"""
    print("🚀 Testing Twitter Poster...")
    
    try:
        from twitter_poster import validate_thread_for_posting, estimate_posting_time
        
        # Test validation
        test_tweets = ["Test tweet 1", "Test tweet 2"]
        errors = validate_thread_for_posting(test_tweets)
        print(f"✅ Validation successful: {len(errors)} errors found")
        
        # Test time estimation
        time_est = estimate_posting_time(5, 3)
        print(f"✅ Time estimation successful: {time_est}")
        
        return True
        
    except Exception as e:
        print(f"❌ Poster test failed: {e}")
        return False


def test_dependencies():
    """Test that all required dependencies are installed"""
    print("📦 Testing Dependencies...")
    
    try:
        import streamlit
        print(f"✅ Streamlit: {streamlit.__version__}")
        
        import tweepy
        print(f"✅ Tweepy: {tweepy.__version__}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Dependency missing: {e}")
        return False


def main():
    """Run all tests"""
    print("🧪 Running Twitter Thread Chunker Tests\n")
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Core Chunker", test_chunker),
        ("Auth Module", test_auth_import),
        ("Poster Module", test_poster_import)
    ]
    
    results = []
    
    for name, test_func in tests:
        print(f"\n--- {name} ---")
        result = test_func()
        results.append((name, result))
    
    print("\n" + "="*50)
    print("📊 TEST RESULTS")
    print("="*50)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:8} | {name}")
        if not passed:
            all_passed = False
    
    print("="*50)
    
    if all_passed:
        print("🎉 All tests passed! Your Twitter Thread Chunker is ready!")
        print("🚀 Run the app with: python launcher.py")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
        print("💡 Try running setup.bat to install dependencies.")


if __name__ == "__main__":
    main()
