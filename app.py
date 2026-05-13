import streamlit as st
import pandas as pd
import snscrape.modules.twitter as sntwitter
from textblob import TextBlob
from io import BytesIO

# =====================================================
# PAGE
# =====================================================

st.set_page_config(
    page_title="Twitter Social Listening",
    layout="wide"
)

st.title("🐦 Twitter/X Social Listening")

# =====================================================
# INPUTS
# =====================================================

search_query = st.text_input(
    "Enter Topic or Username",
    placeholder="Example: Karnataka Tourism OR from:KarnatakaWorld"
)

max_tweets = st.slider(
    "Number of Tweets",
    10,
    500,
    100
)

# =====================================================
# SESSION STATE
# =====================================================

if "df" not in st.session_state:
    st.session_state.df = None

# =====================================================
# BUTTON
# =====================================================

if st.button("Pull Tweets"):

    if not search_query:
        st.error("Please enter topic or username")
        st.stop()

    tweets_data = []

    st.info("Fetching tweets...")

    # =================================================
    # SCRAPE TWEETS
    # =================================================

    try:

        for i, tweet in enumerate(
            sntwitter.TwitterSearchScraper(
                search_query
            ).get_items()
        ):

            if i >= max_tweets:
                break

            text = tweet.content

            # =========================================
            # SENTIMENT
            # =========================================

            polarity = TextBlob(text).sentiment.polarity

            if polarity > 0:
                sentiment = "Positive"

            elif polarity < 0:
                sentiment = "Negative"

            else:
                sentiment = "Neutral"

            tweets_data.append({

                "Date": tweet.date,
                "Username": tweet.user.username,
                "Display Name": tweet.user.displayname,
                "Tweet": text,

                "Likes": tweet.likeCount,
                "Retweets": tweet.retweetCount,
                "Replies": tweet.replyCount,

                "Language": tweet.lang,

                "Tweet URL":
                f"https://twitter.com/{tweet.user.username}/status/{tweet.id}",

                "Sentiment": sentiment,
                "Polarity": polarity
            })

    except Exception as e:
        st.error(f"Error: {e}")

    # =================================================
    # DATAFRAME
    # =================================================

    df = pd.DataFrame(tweets_data)

    st.session_state.df = df

# =====================================================
# DISPLAY
# =====================================================

if st.session_state.df is not None:

    df = st.session_state.df

    st.success(f"Total Tweets Pulled: {len(df)}")

    st.dataframe(df, use_container_width=True)

    # =================================================
    # SENTIMENT SUMMARY
    # =================================================

    st.subheader("📊 Sentiment Summary")

    sentiment_counts = df["Sentiment"].value_counts()

    st.bar_chart(sentiment_counts)

    # =================================================
    # TOP NEGATIVE
    # =================================================

    st.subheader("😡 Top Negative Tweets")

    negative_df = (
        df[df["Sentiment"] == "Negative"]
        .sort_values(
            by=["Polarity", "Likes"],
            ascending=[True, False]
        )
        .head(10)
    )

    st.dataframe(
        negative_df[
            [
                "Username",
                "Tweet",
                "Likes",
                "Tweet URL"
            ]
        ],
        use_container_width=True
    )

    # =================================================
    # DOWNLOAD
    # =================================================

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Tweets"
        )

    output.seek(0)

    st.download_button(
        label="📥 Download Excel",
        data=output,
        file_name="twitter_social_listening.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
