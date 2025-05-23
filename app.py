"""
Twitter Thread Chunker - Streamlit UI
Clean UI layer that imports the core logic
"""

import streamlit as st
from twitter_chunker import chunk_text_for_twitter, get_thread_stats, format_thread_for_export


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
    
    # Create two columns
    col1, col2 = st.columns([1, 1])
    
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
