"""
Twitter Authentication Module
Handles Twitter API authentication and credential management
"""

import streamlit as st
import tweepy
from typing import Optional, Tuple


def get_twitter_credentials() -> Tuple[str, str, str, str]:
    """
    Get Twitter API credentials from Streamlit secrets or user input.
    
    Returns:
        tuple: (consumer_key, consumer_secret, access_token, access_token_secret)
    """
    # Try to get from secrets first (for deployed apps)
    try:
        if "twitter" in st.secrets:
            return (
                st.secrets["twitter"]["consumer_key"],
                st.secrets["twitter"]["consumer_secret"],
                st.secrets["twitter"]["access_token"],
                st.secrets["twitter"]["access_token_secret"]
            )
    except Exception:
        pass
    
    # Fall back to session state or user input
    if "twitter_credentials" not in st.session_state:
        st.session_state.twitter_credentials = {
            "consumer_key": "",
            "consumer_secret": "",
            "access_token": "",
            "access_token_secret": ""
        }
    
    creds = st.session_state.twitter_credentials
    return (
        creds["consumer_key"],
        creds["consumer_secret"],
        creds["access_token"],
        creds["access_token_secret"]
    )


def setup_twitter_credentials_ui() -> bool:
    """
    Display UI for setting up Twitter API credentials.
    
    Returns:
        bool: True if credentials are configured, False otherwise
    """
    st.subheader("🔐 Twitter API Setup")
    
    # Check if already configured
    consumer_key, consumer_secret, access_token, access_token_secret = get_twitter_credentials()
    
    if all([consumer_key, consumer_secret, access_token, access_token_secret]):
        st.success("✅ Twitter API credentials are configured!")
        
        # Test connection button
        if st.button("🔍 Test Connection"):
            client = create_twitter_client()
            if client and test_twitter_connection(client):
                st.success("🎉 Connection successful! You can post tweets.")
                return True
            else:
                st.error("❌ Connection failed. Please check your credentials.")
                return False
        return True
      # Show setup instructions
    st.markdown("#### 📋 How to get Twitter API credentials")
    st.markdown("""
    1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
    2. Create a new app or use an existing one
    3. Generate API keys with **Read and Write** permissions
    4. Copy the following credentials:
       - API Key (Consumer Key)
       - API Secret (Consumer Secret)
       - Access Token
       - Access Token Secret
    """)
    
    # Credential input form
    with st.form("twitter_credentials_form"):
        st.markdown("**Enter your Twitter API credentials:**")
        
        new_consumer_key = st.text_input(
            "API Key (Consumer Key)", 
            value=consumer_key,
            type="password",
            help="Your Twitter app's API Key"
        )
        
        new_consumer_secret = st.text_input(
            "API Secret (Consumer Secret)", 
            value=consumer_secret,
            type="password",
            help="Your Twitter app's API Secret"
        )
        
        new_access_token = st.text_input(
            "Access Token", 
            value=access_token,
            type="password",
            help="Your Access Token with Read and Write permissions"
        )
        
        new_access_token_secret = st.text_input(
            "Access Token Secret", 
            value=access_token_secret,
            type="password",
            help="Your Access Token Secret"
        )
        
        submitted = st.form_submit_button("💾 Save Credentials")
        
        if submitted:
            if all([new_consumer_key, new_consumer_secret, new_access_token, new_access_token_secret]):
                # Save to session state
                st.session_state.twitter_credentials = {
                    "consumer_key": new_consumer_key,
                    "consumer_secret": new_consumer_secret,
                    "access_token": new_access_token,
                    "access_token_secret": new_access_token_secret
                }
                st.success("✅ Credentials saved! Testing connection...")
                st.rerun()
            else:
                st.error("❌ Please fill in all credential fields.")
    
    return False


def create_twitter_client() -> Optional[tweepy.Client]:
    """
    Create and return a Twitter API client.
    
    Returns:
        tweepy.Client or None: Authenticated Twitter client or None if failed
    """
    try:
        consumer_key, consumer_secret, access_token, access_token_secret = get_twitter_credentials()
        
        if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
            return None
        
        client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            wait_on_rate_limit=True
        )
        
        return client
        
    except Exception as e:
        st.error(f"❌ Error creating Twitter client: {str(e)}")
        return None


def test_twitter_connection(client: tweepy.Client) -> bool:
    """
    Test the Twitter API connection.
    
    Args:
        client: Authenticated Twitter client
        
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        # Try to get user information
        user = client.get_me()
        if user and user.data:
            st.info(f"📱 Connected as: @{user.data.username}")
            return True
        return False
        
    except Exception as e:
        st.error(f"❌ Connection test failed: {str(e)}")
        return False


def clear_credentials():
    """Clear saved Twitter credentials from session state."""
    if "twitter_credentials" in st.session_state:
        del st.session_state.twitter_credentials
    st.success("🗑️ Credentials cleared!")
