"""
Twitter Posting Module
Handles posting individual tweets and thread sequences
"""

import streamlit as st
import tweepy
import time
from typing import List, Optional, Dict, Any
from twitter_auth import create_twitter_client


def post_single_tweet(text: str, reply_to_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Post a single tweet.
    
    Args:
        text: Tweet content
        reply_to_id: Tweet ID to reply to (for threading)
        
    Returns:
        dict or None: Tweet response data or None if failed
    """
    client = create_twitter_client()
    if not client:
        return None
    
    try:
        response = client.create_tweet(
            text=text,
            in_reply_to_tweet_id=reply_to_id
        )
        
        if response and response.data:
            return {
                "id": response.data["id"],
                "text": text,
                "url": f"https://twitter.com/user/status/{response.data['id']}"
            }
        return None
        
    except Exception as e:
        st.error(f"❌ Error posting tweet: {str(e)}")
        return None


def post_thread(tweets: List[str], delay_seconds: int = 3) -> Dict[str, Any]:
    """
    Post a sequence of tweets as a thread.
    
    Args:
        tweets: List of tweet texts
        delay_seconds: Delay between posts
        
    Returns:
        dict: Results including success count, posted tweets, and errors
    """
    results = {
        "success_count": 0,
        "posted_tweets": [],
        "errors": [],
        "thread_url": None
    }
    
    if not tweets:
        results["errors"].append("No tweets to post")
        return results
    
    # Validate all tweets first
    for i, tweet in enumerate(tweets):
        if len(tweet) > 280:
            results["errors"].append(f"Tweet {i+1} exceeds 280 characters ({len(tweet)})")
    
    if results["errors"]:
        return results
    
    # Post tweets with progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    reply_to_id = None
    
    for i, tweet_text in enumerate(tweets):
        # Update progress
        progress = (i + 1) / len(tweets)
        progress_bar.progress(progress)
        status_text.text(f"Posting tweet {i+1} of {len(tweets)}...")
        
        # Post the tweet
        tweet_result = post_single_tweet(tweet_text, reply_to_id)
        
        if tweet_result:
            results["posted_tweets"].append(tweet_result)
            results["success_count"] += 1
            reply_to_id = tweet_result["id"]
            
            # Set thread URL to first tweet
            if i == 0:
                results["thread_url"] = tweet_result["url"]
            
            # Add delay between tweets (except for the last one)
            if i < len(tweets) - 1:
                time.sleep(delay_seconds)
                
        else:
            error_msg = f"Failed to post tweet {i+1}"
            results["errors"].append(error_msg)
            st.error(error_msg)
            break
    
    # Clean up progress indicators
    progress_bar.empty()
    status_text.empty()
    
    return results


def validate_thread_for_posting(tweets: List[str]) -> List[str]:
    """
    Validate a thread before posting and return any issues.
    
    Args:
        tweets: List of tweet texts
        
    Returns:
        list: List of validation error messages
    """
    errors = []
    
    if not tweets:
        errors.append("No tweets to validate")
        return errors
    
    if len(tweets) > 25:
        errors.append("Thread is too long (max 25 tweets recommended)")
    
    for i, tweet in enumerate(tweets):
        if len(tweet) > 280:
            errors.append(f"Tweet {i+1} exceeds 280 characters ({len(tweet)})")
        
        if not tweet.strip():
            errors.append(f"Tweet {i+1} is empty")
    
    return errors


def show_posting_preview(tweets: List[str]) -> bool:
    """
    Show a preview of the thread before posting with confirmation.
    
    Args:
        tweets: List of tweet texts
        
    Returns:
        bool: True if user confirms posting, False otherwise
    """
    st.subheader("🔍 Thread Preview")
    st.info(f"Ready to post {len(tweets)} tweets as a thread")
    
    # Show validation results
    validation_errors = validate_thread_for_posting(tweets)
    if validation_errors:
        st.error("❌ Thread validation failed:")
        for error in validation_errors:
            st.write(f"• {error}")
        return False
    
    st.success("✅ Thread validation passed!")
    
    # Show preview in expander
    with st.expander("📝 Preview All Tweets", expanded=False):
        for i, tweet in enumerate(tweets, 1):
            st.markdown(f"**Tweet {i}** ({len(tweet)}/280 chars)")
            st.code(tweet, language=None)
    
    # Show posting settings
    col1, col2 = st.columns(2)
    with col1:
        delay = st.slider(
            "⏱️ Delay between tweets (seconds)",
            min_value=1,
            max_value=10,
            value=3,
            help="Recommended: 2-3 seconds to avoid rate limits"
        )
    
    with col2:
        st.metric("Total Tweets", len(tweets))
        estimated_time = len(tweets) * delay
        st.metric("Estimated Time", f"{estimated_time}s")
    
    # Confirmation
    st.warning("⚠️ This will post tweets to your Twitter account immediately!")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("🚀 Post Thread Now", type="primary", use_container_width=True):
            return True
    
    return False


def show_posting_results(results: Dict[str, Any]):
    """
    Display the results of a thread posting operation.
    
    Args:
        results: Results dictionary from post_thread()
    """
    if results["success_count"] == 0:
        st.error("❌ Failed to post any tweets")
        for error in results["errors"]:
            st.error(f"• {error}")
        return
    
    if results["success_count"] == len(results["posted_tweets"]):
        st.success(f"🎉 Successfully posted all {results['success_count']} tweets!")
    else:
        st.warning(f"⚠️ Posted {results['success_count']} tweets, but some failed")
    
    # Show thread link
    if results["thread_url"]:
        st.markdown(f"🔗 **[View your thread on Twitter]({results['thread_url']})**")
    
    # Show posted tweets
    if results["posted_tweets"]:
        with st.expander("📋 Posted Tweets", expanded=False):
            for i, tweet_data in enumerate(results["posted_tweets"], 1):
                st.markdown(f"**Tweet {i}**")
                st.write(f"Text: {tweet_data['text']}")
                st.write(f"URL: {tweet_data['url']}")
                st.divider()
    
    # Show errors if any
    if results["errors"]:
        with st.expander("❌ Errors", expanded=True):
            for error in results["errors"]:
                st.error(error)


def estimate_posting_time(tweet_count: int, delay_seconds: int = 3) -> str:
    """
    Estimate the time it will take to post a thread.
    
    Args:
        tweet_count: Number of tweets in thread
        delay_seconds: Delay between posts
        
    Returns:
        str: Human-readable time estimate
    """
    total_seconds = tweet_count * delay_seconds
    
    if total_seconds < 60:
        return f"{total_seconds} seconds"
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}m {seconds}s"
    else:
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours}h {minutes}m"
