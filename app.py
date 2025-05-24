"""
Twitter Thread Chunker - Streamlit UI
Clean UI layer that imports the core logic
"""

import streamlit as st
from twitter_chunker import chunk_text_for_twitter, get_thread_stats, format_thread_for_export
from twitter_auth import setup_twitter_credentials_ui, create_twitter_client
from twitter_poster import show_posting_preview, post_thread, show_posting_results


def main():
    # Page config
    st.set_page_config(
        page_title="Twitter Thread Chunker",
        page_icon="🧵",
        layout="wide"
    )
    
    # Header
    st.title("🧵 Twitter Thread Chunker")
    st.markdown("Transform your long thoughts into perfectly sized Twitter threads!")
    
    # Initialize session state for posting
    if "posting_confirmed" not in st.session_state:
        st.session_state.posting_confirmed = False
    if "current_tweets" not in st.session_state:
        st.session_state.current_tweets = []
    
    # Create three columns for better layout
    col1, col2, col3 = st.columns([1, 1, 0.8])
    
    with col1:
        st.subheader("📝 Input Your Text")
        
        # Text input methods
        input_method = st.radio(
            "Choose input method:",
            ["Type/Paste Text", "Upload File"],
            horizontal=True
        )
        
        text_input = ""
        
        if input_method == "Type/Paste Text":
            text_input = st.text_area(
                "Enter your text here:",
                height=300,
                placeholder="Paste your long text here and watch it get chunked into perfect Twitter thread format..."
            )
        else:
            uploaded_file = st.file_uploader(
                "Upload a text file",
                type=['txt'],
                help="Upload a .txt file containing your text"
            )
            
            if uploaded_file is not None:
                try:
                    text_input = str(uploaded_file.read(), "utf-8")
                    st.success(f"File uploaded successfully! ({len(text_input)} characters)")
                except Exception as e:
                    st.error(f"Error reading file: {e}")
        
        # Character count
        if text_input:
            char_count = len(text_input)
            st.info(f"📊 Character count: {char_count:,}")
    
    with col2:
        st.subheader("🧵 Generated Thread")
        
        if text_input and text_input.strip():
            # Process the text
            with st.spinner("Chunking your text..."):
                tweets, warnings = chunk_text_for_twitter(text_input)
            
            if tweets:
                # Store tweets in session state for posting
                st.session_state.current_tweets = tweets
                
                # Get and display stats
                stats = get_thread_stats(tweets)
                st.success(f"✅ Generated {stats['total_tweets']} tweets for your thread!")
                
                # Stats in expander
                with st.expander("📊 Thread Statistics", expanded=False):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Total Tweets", stats['total_tweets'])
                        st.metric("Avg Length", f"{stats['avg_length']:.1f}")
                    with col_b:
                        st.metric("Total Characters", f"{stats['total_characters']:,}")
                        st.metric("Over Limit", stats['tweets_over_limit'])
                
                # Show warnings if any
                if warnings:
                    with st.expander("⚠️ Warnings", expanded=False):
                        for warning in warnings:
                            st.warning(warning)
                
                # Display tweets
                st.markdown("### Individual Tweets")
                for i, tweet in enumerate(tweets, 1):
                    with st.container():
                        st.markdown(f"**Tweet {i} ({len(tweet)} chars)**")
                        
                        # Tweet content in a nice box
                        st.text_area(
                            f"tweet_{i}",
                            value=tweet,
                            height=100,
                            label_visibility="collapsed",
                            key=f"tweet_display_{i}"
                        )
                        
                        # Copy button for each tweet
                        if st.button(f"📋 Copy Tweet {i}", key=f"copy_{i}"):
                            st.write("Use Ctrl+C to copy the text from the box above")
                        
                        # Color code based on length
                        if len(tweet) <= 280:
                            st.success(f"✅ Perfect length ({len(tweet)}/280)")
                        else:
                            st.error(f"❌ Too long ({len(tweet)}/280)")
                        
                        st.divider()
                
                # Bulk copy option
                st.subheader("📋 Copy All Tweets")
                all_tweets_text = format_thread_for_export(tweets)
                st.text_area(
                    "All tweets (copy this):",
                    value=all_tweets_text,
                    height=200,
                    help="Copy this text and paste into your Twitter scheduling tool"
                )
                
            else:
                st.warning("No text to process. Please enter some text above.")
        
        elif not text_input:
            st.info("👆 Enter some text on the left to see the magic happen!")

    with col3:
        st.subheader("🚀 Post to Twitter")
        
        # Check if we have tweets to post
        if st.session_state.current_tweets:
            tweets = st.session_state.current_tweets
            
            # Twitter authentication setup
            twitter_configured = setup_twitter_credentials_ui()
            
            if twitter_configured:
                st.divider()
                
                # Show posting controls
                st.markdown("### Ready to Post!")
                st.info(f"📊 {len(tweets)} tweets ready")
                
                # Quick validation display
                validation_errors = []
                for i, tweet in enumerate(tweets):
                    if len(tweet) > 280:
                        validation_errors.append(f"Tweet {i+1} too long")
                
                if validation_errors:
                    st.error("❌ Issues found:")
                    for error in validation_errors:
                        st.write(f"• {error}")
                else:
                    st.success("✅ All tweets valid")
                    
                    # Posting controls
                    delay = st.slider(
                        "⏱️ Delay (seconds)",
                        min_value=1,
                        max_value=10,
                        value=3,
                        help="Time between tweets"
                    )
                    
                    # Estimate time
                    total_time = len(tweets) * delay
                    if total_time < 60:
                        time_str = f"{total_time}s"
                    else:
                        time_str = f"{total_time//60}m {total_time%60}s"
                    
                    st.caption(f"📅 Estimated time: {time_str}")
                    
                    # Post button
                    if st.button("🚀 Post Thread", type="primary", use_container_width=True):
                        st.session_state.posting_confirmed = True
                    
                    # Handle posting
                    if st.session_state.posting_confirmed:
                        st.warning("⚠️ Posting to Twitter...")
                        
                        # Post the thread
                        results = post_thread(tweets, delay)
                        
                        # Show results
                        show_posting_results(results)
                        
                        # Reset confirmation state
                        st.session_state.posting_confirmed = False
                        
                        if results["success_count"] > 0:
                            st.balloons()
            
            else:
                st.info("🔐 Configure Twitter API credentials above to enable posting")
                
        else:
            st.info("👈 Generate a thread first to enable posting")
            
            # Show Twitter setup even without tweets
            st.markdown("### Setup Twitter API")
            with st.expander("🔧 Configure Twitter Access", expanded=False):
                setup_twitter_credentials_ui()

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Built with Streamlit • Split your thoughts, not your ideas 🧵</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
