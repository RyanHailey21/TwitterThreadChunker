"""
Twitter Thread Chunker - Core Logic
Contains the main chunking functionality separate from UI
"""

def chunk_text_for_twitter(text):
    """
    Splits a large string of text into chunks suitable for a Twitter thread.

    Each chunk is kept within Twitter's character limit (280) and includes
    a thread indicator (e.g., "1/5"). The function attempts to split at
    word boundaries.

    Args:
        text: The input string to be chunked.

    Returns:
        tuple: (formatted_tweets, warnings)
            - formatted_tweets: List of strings, each a formatted tweet chunk
            - warnings: List of warning messages
    """
    if not text or not text.strip():
        return [], []

    MAX_TWEET_LENGTH = 280
    INDICATOR_RESERVE = 15
    content_limit = MAX_TWEET_LENGTH - INDICATOR_RESERVE

    words = text.split()
    chunks = []
    current_chunk_words = []
    warnings = []

    for word in words:
        potential_chunk_content = " ".join(current_chunk_words + [word])
        potential_chunk_length = len(potential_chunk_content)

        if potential_chunk_length > content_limit:
            if current_chunk_words:
                chunks.append(" ".join(current_chunk_words))
            current_chunk_words = [word]
            
            if len(word) > content_limit:
                warnings.append(f"Warning: Word '{word[:20]}...' is longer than content limit ({content_limit})")
        else:
            current_chunk_words.append(word)

    if current_chunk_words:
        chunks.append(" ".join(current_chunk_words))

    total_chunks = len(chunks)
    formatted_tweets = []

    if total_chunks == 0:
        return [], warnings

    for i, chunk in enumerate(chunks):
        indicator = f"{i+1}/{total_chunks}"
        formatted_tweet = f"{chunk} {indicator}"
        
        if len(formatted_tweet) > MAX_TWEET_LENGTH:
            warnings.append(f"Tweet {i+1}/{total_chunks} exceeds {MAX_TWEET_LENGTH} characters ({len(formatted_tweet)})")
        
        formatted_tweets.append(formatted_tweet)

    return formatted_tweets, warnings


def get_thread_stats(tweets):
    """
    Calculate statistics about the generated thread.
    
    Args:
        tweets: List of tweet strings
        
    Returns:
        dict: Statistics about the thread
    """
    if not tweets:
        return {}
    
    lengths = [len(tweet) for tweet in tweets]
    
    return {
        'total_tweets': len(tweets),
        'total_characters': sum(lengths),
        'avg_length': sum(lengths) / len(lengths),
        'max_length': max(lengths),
        'min_length': min(lengths),
        'tweets_over_limit': len([l for l in lengths if l > 280])
    }


def format_thread_for_export(tweets, separator="\n\n---\n\n"):
    """
    Format the entire thread for easy copying/exporting.
    
    Args:
        tweets: List of tweet strings
        separator: String to use between tweets
        
    Returns:
        str: Formatted thread ready for export
    """
    return separator.join(tweets)
