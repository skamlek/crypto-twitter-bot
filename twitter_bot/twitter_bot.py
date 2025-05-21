"""
Twitter Crypto Bot - Automated reply system for high-engagement crypto tweets
"""
import os
import json
import time
import logging
import requests
from datetime import datetime, timedelta
import tweepy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("twitter_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("twitter_crypto_bot")

# Twitter API Authentication
def setup_twitter_api():
    """
    Set up and authenticate with the Twitter API using environment variables
    for security.
    """
    try:
        # Get credentials from environment variables (more secure than hardcoding)
        api_key = os.environ.get("TWITTER_API_KEY")
        api_key_secret = os.environ.get("TWITTER_API_SECRET")
        access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
        access_token_secret = os.environ.get("TWITTER_ACCESS_SECRET")
        bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
        
        # Validate credentials are available
        if not all([api_key, api_key_secret, access_token, access_token_secret, bearer_token]):
            raise ValueError("Twitter API credentials not found in environment variables")
        
        # Set up authentication for v1.1 API (needed for some operations)
        auth = tweepy.OAuth1UserHandler(
            api_key, api_key_secret, access_token, access_token_secret
        )
        api_v1 = tweepy.API(auth)
        
        # Set up authentication for v2 API
        client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_key_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        
        logger.info("Twitter API authentication successful")
        return api_v1, client
    
    except Exception as e:
        logger.error(f"Twitter API authentication failed: {str(e)}")
        raise

# Tweet Search and Filtering
def search_crypto_tweets(client, max_results=10):
    """
    Search for high-engagement crypto-related tweets using Twitter API v2.
    
    Args:
        client: Authenticated Twitter API v2 client
        max_results: Maximum number of results to return
        
    Returns:
        List of tweet objects that match the criteria
    """
    try:
        # Define search query for crypto-related content
        # Note: Twitter API v2 has different query syntax than v1.1
        query = """
            (crypto OR cryptocurrency OR bitcoin OR ethereum OR blockchain OR defi OR nft OR airdrop OR staking)
            -is:retweet -is:reply has:mentions
            min_faves:50
            lang:en
        """
        
        # Get tweets from the last 24 hours
        start_time = (datetime.utcnow() - timedelta(hours=24)).isoformat() + "Z"
        
        # Search tweets with expanded user information
        response = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=["created_at", "public_metrics", "author_id", "conversation_id"],
            user_fields=["username", "name", "public_metrics"],
            expansions=["author_id"],
            start_time=start_time,
            sort_order="relevancy"
        )
        
        if not response.data:
            logger.info("No tweets found matching the criteria")
            return []
        
        # Filter tweets based on engagement metrics
        filtered_tweets = []
        users = {user.id: user for user in response.includes["users"]} if "users" in response.includes else {}
        
        for tweet in response.data:
            # Get engagement metrics
            metrics = tweet.public_metrics
            likes = metrics.get("like_count", 0)
            retweets = metrics.get("retweet_count", 0)
            replies = metrics.get("reply_count", 0)
            
            # Calculate engagement score (can be adjusted based on preferences)
            engagement_score = likes + (retweets * 2) + (replies * 1.5)
            
            # Only include tweets with sufficient engagement
            if engagement_score >= 100:  # Threshold can be adjusted
                # Add user information to tweet object
                tweet_with_user = {
                    "id": tweet.id,
                    "text": tweet.text,
                    "created_at": tweet.created_at,
                    "metrics": metrics,
                    "engagement_score": engagement_score,
                    "author_id": tweet.author_id,
                    "author_username": users.get(tweet.author_id).username if tweet.author_id in users else "unknown",
                    "conversation_id": tweet.conversation_id
                }
                filtered_tweets.append(tweet_with_user)
        
        # Sort by engagement score (highest first)
        filtered_tweets.sort(key=lambda x: x["engagement_score"], reverse=True)
        
        logger.info(f"Found {len(filtered_tweets)} high-engagement crypto tweets")
        return filtered_tweets
    
    except Exception as e:
        logger.error(f"Error searching for tweets: {str(e)}")
        return []

# Reply Generation with Manus AI
def generate_reply(tweet_text, persona="random"):
    """
    Generate a reply to a tweet using Manus AI with different character personas.
    
    Args:
        tweet_text: The text of the tweet to reply to
        persona: Which persona to use (insider, expert, friend, or random)
        
    Returns:
        Generated reply text
    """
    try:
        # Define the different personas
        personas = {
            "insider": {
                "name": "Mysterious Insider",
                "description": "You are a crypto insider replying to tweets with cryptic, professional insider hints. Use subtle reverse psychology and hints of deeper knowledge. Avoid heavy punctuation like ellipses or dashes. Keep replies under 250 characters with short, clear sentences."
            },
            "expert": {
                "name": "Low-Key Expert",
                "description": "You are a casual crypto expert replying to tweets with conversational, punchy insights. Be empathetic but hint at insider knowledge. Avoid heavy punctuation. Keep replies under 250 characters with short, clear sentences."
            },
            "friend": {
                "name": "Casual Friend",
                "description": "You are a friendly crypto enthusiast replying to tweets with relatable, light humor. Use easy language that sparks curiosity. Avoid heavy punctuation. Keep replies under 250 characters with short, clear sentences."
            }
        }
        
        # Select persona (random or specified)
        if persona == "random":
            import random
            persona = random.choice(list(personas.keys()))
        
        if persona not in personas:
            persona = "insider"  # Default to insider if invalid persona specified
        
        selected_persona = personas[persona]
        
        # Detect context from tweet text for more relevant replies
        context = detect_tweet_context(tweet_text)
        
        # In a real implementation, this would call the Manus AI API
        # For this example, we'll use a simplified approach with templates
        
        # This is where you would integrate with Manus AI
        # Example API call structure (replace with actual Manus AI API):
        """
        response = requests.post(
            "https://api.manus.ai/generate",
            headers={
                "Authorization": f"Bearer {os.environ.get('MANUS_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "prompt": f"Tweet: {tweet_text}\n\nContext: {context}\n\n{selected_persona['description']}\n\nGenerate a reply:",
                "max_tokens": 100,
                "temperature": 0.7
            }
        )
        reply = response.json().get("text", "").strip()
        """
        
        # For this example, we'll use template-based replies
        reply = generate_template_reply(tweet_text, context, persona)
        
        # Ensure reply is within character limit
        if len(reply) > 250:
            reply = reply[:247] + "..."
        
        logger.info(f"Generated reply using {selected_persona['name']} persona: {reply}")
        return reply
    
    except Exception as e:
        logger.error(f"Error generating reply: {str(e)}")
        return "Interesting perspective on crypto. The market always has more layers than most realize."

def detect_tweet_context(tweet_text):
    """
    Detect the context of a tweet to generate more relevant replies.
    
    Args:
        tweet_text: The text of the tweet
        
    Returns:
        Context category string
    """
    tweet_text = tweet_text.lower()
    
    # Define context categories and their keywords
    contexts = {
        "market_volatility": ["crash", "dip", "bear", "bull", "dump", "pump", "market", "price", "down", "up", "sell", "buy"],
        "airdrops": ["airdrop", "free", "claim", "distribution", "eligible", "snapshot"],
        "staking": ["stake", "staking", "yield", "apy", "validator", "rewards", "passive"],
        "nft": ["nft", "collection", "mint", "floor", "opensea", "art"],
        "defi": ["defi", "yield", "farm", "liquidity", "pool", "swap", "lend", "borrow"],
        "regulation": ["sec", "regulation", "compliance", "legal", "government", "ban"]
    }
    
    # Check for context matches
    for context, keywords in contexts.items():
        for keyword in keywords:
            if keyword in tweet_text:
                return context
    
    # Default context if no specific match
    return "general_crypto"

def generate_template_reply(tweet_text, context, persona):
    """
    Generate a template-based reply based on tweet context and persona.
    This is a simplified version for the example - in production, use Manus AI.
    
    Args:
        tweet_text: The text of the tweet
        context: The detected context category
        persona: The persona to use for the reply
        
    Returns:
        Generated reply text
    """
    # Template replies by context and persona
    templates = {
        "market_volatility": {
            "insider": [
                "Market moves like this separate signal from noise. Smart money positioned weeks ago.",
                "Not every dip deserves attention. This one might. The patterns are familiar to those who've seen cycles.",
                "Price action is just surface noise. The real story is in the quiet accumulation happening now."
            ],
            "expert": [
                "These market swings feel dramatic until you've seen a few cycles. Focus on fundamentals not emotions.",
                "Market psychology at work. Fear and greed playing out exactly as expected. Stay rational.",
                "Short-term volatility, long-term opportunity. The patient ones always win these games."
            ],
            "friend": [
                "Wild ride right? Remember when everyone panicked last time and missed the recovery? History rhymes.",
                "Market's just doing its thing. Deep breaths and zoom out on the chart. This too shall pass.",
                "Crypto being crypto! Perfect time to remember why you got in this space to begin with."
            ]
        },
        "airdrops": {
            "insider": [
                "The airdrop game changed months ago. The valuable ones aren't announced loudly.",
                "Real value rarely comes from what everyone's chasing. The signal is elsewhere.",
                "Interesting timing on this distribution. Watch what happens next week."
            ],
            "expert": [
                "Airdrops are marketing, not gifts. Always ask what you're giving up in return.",
                "The best airdrops come to those building value, not those hunting for free money.",
                "Quality projects don't need to give tokens away. Worth considering why this one does."
            ],
            "friend": [
                "Free tokens are fun but don't forget to check the project fundamentals too!",
                "Airdrops are like crypto lottery tickets. Enjoy the game but don't build your strategy on them.",
                "Got my popcorn ready for this airdrop season! Just remember most tokens go to zero."
            ]
        },
        # Templates for other contexts would go here
        "general_crypto": {
            "insider": [
                "The narrative shifts but the fundamentals remain. Those who know are quietly building.",
                "Interesting perspective. Though the real alpha is rarely discussed publicly.",
                "Some see volatility. Others see opportunity. The difference is experience."
            ],
            "expert": [
                "Worth considering both sides. The market rewards those who think independently.",
                "The crypto space evolves fast. Adapting your strategy is key to staying ahead.",
                "Focus on signal not noise. The best opportunities aren't the ones everyone's talking about."
            ],
            "friend": [
                "Love the energy in crypto right now! So many possibilities if you know where to look.",
                "Crypto keeps it interesting! Never a dull moment when you're building the future.",
                "This space moves so fast! Exciting to see where we'll be this time next year."
            ]
        }
    }
    
    # Get templates for the context and persona
    context_templates = templates.get(context, templates["general_crypto"])
    persona_templates = context_templates.get(persona, context_templates["insider"])
    
    # Select a random template
    import random
    reply = random.choice(persona_templates)
    
    return reply

# Post Reply to Twitter
def post_reply(client, tweet_id, reply_text):
    """
    Post a reply to a tweet using the Twitter API.
    
    Args:
        client: Authenticated Twitter API v2 client
        tweet_id: ID of the tweet to reply to
        reply_text: Text of the reply
        
    Returns:
        Boolean indicating success or failure
    """
    try:
        # Post the reply
        response = client.create_tweet(
            text=reply_text,
            in_reply_to_tweet_id=tweet_id
        )
        
        if response.data:
            logger.info(f"Successfully replied to tweet {tweet_id} with reply ID {response.data['id']}")
            return True, response.data['id']
        else:
            logger.warning(f"Failed to reply to tweet {tweet_id}: No data in response")
            return False, None
    
    except Exception as e:
        logger.error(f"Error posting reply to tweet {tweet_id}: {str(e)}")
        return False, None

# Rate Limiting and Error Handling
class RateLimitHandler:
    """
    Handler for Twitter API rate limits and errors.
    """
    def __init__(self):
        self.rate_limits = {
            "search": {"remaining": 450, "reset_time": time.time() + 900},  # 15-min window
            "post": {"remaining": 50, "reset_time": time.time() + 900}      # 15-min window
        }
    
    def update_limits(self, endpoint, response_headers):
        """Update rate limit information from response headers"""
        if 'x-rate-limit-remaining' in response_headers:
            self.rate_limits[endpoint]["remaining"] = int(response_headers['x-rate-limit-remaining'])
        
        if 'x-rate-limit-reset' in response_headers:
            self.rate_limits[endpoint]["reset_time"] = int(response_headers['x-rate-limit-reset'])
    
    def check_and_wait(self, endpoint):
        """Check if we're rate limited and wait if necessary"""
        if self.rate_limits[endpoint]["remaining"] <= 1:
            wait_time = self.rate_limits[endpoint]["reset_time"] - time.time()
            if wait_time > 0:
                logger.info(f"Rate limit reached for {endpoint}. Waiting {wait_time:.2f} seconds.")
                time.sleep(wait_time + 1)  # Add 1 second buffer
                # Reset the counter after waiting
                self.rate_limits[endpoint]["remaining"] = 450 if endpoint == "search" else 50
                self.rate_limits[endpoint]["reset_time"] = time.time() + 900
        
        # Decrement the remaining count
        self.rate_limits[endpoint]["remaining"] -= 1

# Tweet History Management
class TweetHistory:
    """
    Manage history of tweets that have been replied to.
    """
    def __init__(self, history_file="tweet_history.json"):
        self.history_file = history_file
        self.replied_tweets = self._load_history()
    
    def _load_history(self):
        """Load tweet history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error loading tweet history: {str(e)}")
            return {}
    
    def _save_history(self):
        """Save tweet history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.replied_tweets, f)
        except Exception as e:
            logger.error(f"Error saving tweet history: {str(e)}")
    
    def has_replied(self, tweet_id):
        """Check if we've already replied to a tweet"""
        return str(tweet_id) in self.replied_tweets
    
    def add_reply(self, tweet_id, reply_id, tweet_text, reply_text):
        """Add a reply to the history"""
        self.replied_tweets[str(tweet_id)] = {
            "reply_id": str(reply_id),
            "timestamp": datetime.utcnow().isoformat(),
            "tweet_text": tweet_text,
            "reply_text": reply_text
        }
        self._save_history()

# Main Bot Function
def run_twitter_bot(max_tweets=5):
    """
    Main function to run the Twitter bot.
    
    Args:
        max_tweets: Maximum number of tweets to reply to in one run
    """
    try:
        logger.info("Starting Twitter Crypto Bot")
        
        # Set up Twitter API
        api_v1, client = setup_twitter_api()
        
        # Initialize rate limit handler and tweet history
        rate_handler = RateLimitHandler()
        tweet_history = TweetHistory()
        
        # Search for crypto tweets
        rate_handler.check_and_wait("search")
        tweets = search_crypto_tweets(client, max_results=30)  # Get more than needed to filter
        
        # Counter for successful replies
        reply_count = 0
        
        # Process tweets
        for tweet in tweets:
            # Skip if we've already replied to this tweet
            if tweet_history.has_replied(tweet["id"]):
                logger.info(f"Already replied to tweet {tweet['id']} - skipping")
                continue
            
            # Generate reply with random persona
            reply_text = generate_reply(tweet["text"])
            
            # Post reply
            rate_handler.check_and_wait("post")
            success, reply_id = post_reply(client, tweet["id"], reply_text)
            
            if success:
                # Add to history
                tweet_history.add_reply(tweet["id"], reply_id, tweet["text"], reply_text)
                reply_count += 1
                
                # Log success
                logger.info(f"Reply #{reply_count}: Successfully replied to @{tweet['author_username']}")
                
                # Stop if we've reached the maximum number of replies
                if reply_count >= max_tweets:
                    break
                
                # Add a small delay between replies to avoid looking like a bot
                time.sleep(30)
            else:
                logger.warning(f"Failed to reply to tweet {tweet['id']}")
        
        logger.info(f"Bot run complete. Posted {reply_count} replies.")
    
    except Exception as e:
        logger.error(f"Error running Twitter bot: {str(e)}")

# Manual run function (for testing)
def manual_run():
    """
    Manually run the bot once for testing purposes.
    """
    run_twitter_bot(max_tweets=3)

if __name__ == "__main__":
    # For manual testing
    manual_run()
