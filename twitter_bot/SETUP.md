# Twitter Crypto Bot - Detailed Setup Guide

This guide provides step-by-step instructions for setting up and running your Twitter Crypto Bot in a real-world environment.

## Prerequisites

- Python 3.7 or higher
- Twitter Developer Account with API access
- Twitter API credentials (API key, secret, bearer token, access token, access token secret)

## Step 1: Environment Setup

### Local Machine Setup

1. **Create a dedicated directory for your bot:**
   ```bash
   mkdir twitter_crypto_bot
   cd twitter_crypto_bot
   ```

2. **Extract the provided zip file into this directory**

3. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables with your Twitter API credentials:**

   On Windows:
   ```bash
   set TWITTER_API_KEY=your_api_key
   set TWITTER_API_SECRET=your_api_secret
   set TWITTER_BEARER_TOKEN=your_bearer_token
   set TWITTER_ACCESS_TOKEN=your_access_token
   set TWITTER_ACCESS_SECRET=your_access_secret
   ```

   On macOS/Linux:
   ```bash
   export TWITTER_API_KEY=your_api_key
   export TWITTER_API_SECRET=your_api_secret
   export TWITTER_BEARER_TOKEN=your_bearer_token
   export TWITTER_ACCESS_TOKEN=your_access_token
   export TWITTER_ACCESS_SECRET=your_access_secret
   ```

   For permanent setup, add these to your `.bashrc`, `.zshrc`, or create a `.env` file and use a package like `python-dotenv` to load them.

## Step 2: Configuration

1. **Open `twitter_bot.py` and review the following sections:**

   - `search_crypto_tweets` function: Adjust the search query to target the types of tweets you want
   - Engagement thresholds: Modify the engagement score calculation if needed
   - Reply templates: Customize the reply templates for each persona

2. **For testing purposes, you may want to reduce the `max_tweets` parameter in the `run_twitter_bot` function to 1 or 2**

## Step 3: Running the Bot

1. **Run the bot manually:**
   ```bash
   python twitter_bot.py
   ```

2. **Check the log file (`twitter_bot.log`) to see what the bot is doing:**
   ```bash
   tail -f twitter_bot.log
   ```

3. **Verify that replies are being posted to Twitter from your account**

## Step 4: Cloud Deployment Options

### Option 1: AWS Lambda

1. **Install AWS CLI and configure it with your credentials**

2. **Create a deployment package:**
   ```bash
   pip install --target ./package -r requirements.txt
   cd package
   zip -r ../lambda_function.zip .
   cd ..
   zip -g lambda_function.zip twitter_bot.py
   ```

3. **Create a Lambda function using the AWS Console or CLI**

4. **Set up environment variables in the Lambda configuration**

5. **Create a CloudWatch Events rule to trigger the Lambda function periodically**

### Option 2: Heroku

1. **Install Heroku CLI and log in**

2. **Create a new Heroku app:**
   ```bash
   heroku create twitter-crypto-bot
   ```

3. **Create a `Procfile` with the following content:**
   ```
   worker: python twitter_bot.py
   ```

4. **Set environment variables:**
   ```bash
   heroku config:set TWITTER_API_KEY=your_api_key
   heroku config:set TWITTER_API_SECRET=your_api_secret
   heroku config:set TWITTER_ACCESS_TOKEN=your_access_token
   heroku config:set TWITTER_ACCESS_SECRET=your_access_token_secret
   heroku config:set TWITTER_BEARER_TOKEN=your_bearer_token
   ```

5. **Deploy to Heroku:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku master
   ```

6. **Scale the worker dyno:**
   ```bash
   heroku ps:scale worker=1
   ```

7. **Add the Heroku Scheduler add-on and configure it to run your script periodically**

## Troubleshooting

### Common Issues:

1. **Authentication Errors:**
   - Verify that your Twitter API credentials are correct
   - Check that your app has the necessary permissions (read and write)

2. **Rate Limiting:**
   - If you see rate limit errors, reduce the frequency of bot runs
   - Ensure the bot is not running multiple instances simultaneously

3. **No Tweets Found:**
   - Adjust the search query to be less restrictive
   - Check that the engagement thresholds aren't too high

4. **Replies Not Posting:**
   - Verify that your app has write permissions
   - Check the log for specific error messages

## Security Best Practices

1. **Never commit your API credentials to version control**

2. **Regularly rotate your access tokens**

3. **Monitor your Twitter API usage**

4. **Keep your bot code in a private repository**

5. **Implement additional error handling and logging as needed**

## Next Steps

Once your bot is running successfully, consider these enhancements:

1. **Implement more sophisticated reply generation**

2. **Add more persona types**

3. **Enhance context detection**

4. **Implement analytics to track performance**

5. **Set up monitoring and alerts**

Remember that Twitter has policies about automation. Ensure your bot complies with Twitter's terms of service and developer agreement to avoid account suspension.

## Contact

For questions, customization requests, or collaboration opportunities, contact:
- Telegram: [@balcansatoshi](https://t.me/balcansatoshi)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
