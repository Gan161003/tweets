# # import streamlit as st
# # import pandas as pd
# # import snscrape.modules.twitter as sntwitter
# # from textblob import TextBlob
# # from io import BytesIO

# # # =====================================================
# # # PAGE
# # # =====================================================

# # st.set_page_config(
# #     page_title="Twitter Social Listening",
# #     layout="wide"
# # )

# # st.title("🐦 Twitter/X Social Listening")

# # # =====================================================
# # # INPUTS
# # # =====================================================

# # search_query = st.text_input(
# #     "Enter Topic or Username",
# #     placeholder="Example: Karnataka Tourism OR from:KarnatakaWorld"
# # )

# # max_tweets = st.slider(
# #     "Number of Tweets",
# #     10,
# #     500,
# #     100
# # )

# # # =====================================================
# # # SESSION STATE
# # # =====================================================

# # if "df" not in st.session_state:
# #     st.session_state.df = None

# # # =====================================================
# # # BUTTON
# # # =====================================================

# # if st.button("Pull Tweets"):

# #     if not search_query:
# #         st.error("Please enter topic or username")
# #         st.stop()

# #     tweets_data = []

# #     st.info("Fetching tweets...")

# #     # =================================================
# #     # SCRAPE TWEETS
# #     # =================================================

# #     try:

# #         for i, tweet in enumerate(
# #             sntwitter.TwitterSearchScraper(
# #                 search_query
# #             ).get_items()
# #         ):

# #             if i >= max_tweets:
# #                 break

# #             text = tweet.content

# #             # =========================================
# #             # SENTIMENT
# #             # =========================================

# #             polarity = TextBlob(text).sentiment.polarity

# #             if polarity > 0:
# #                 sentiment = "Positive"

# #             elif polarity < 0:
# #                 sentiment = "Negative"

# #             else:
# #                 sentiment = "Neutral"

# #             tweets_data.append({

# #                 "Date": tweet.date,
# #                 "Username": tweet.user.username,
# #                 "Display Name": tweet.user.displayname,
# #                 "Tweet": text,

# #                 "Likes": tweet.likeCount,
# #                 "Retweets": tweet.retweetCount,
# #                 "Replies": tweet.replyCount,

# #                 "Language": tweet.lang,

# #                 "Tweet URL":
# #                 f"https://twitter.com/{tweet.user.username}/status/{tweet.id}",

# #                 "Sentiment": sentiment,
# #                 "Polarity": polarity
# #             })

# #     except Exception as e:
# #         st.error(f"Error: {e}")

# #     # =================================================
# #     # DATAFRAME
# #     # =================================================

# #     df = pd.DataFrame(tweets_data)

# #     st.session_state.df = df

# # # =====================================================
# # # DISPLAY
# # # =====================================================

# # if st.session_state.df is not None:

# #     df = st.session_state.df

# #     st.success(f"Total Tweets Pulled: {len(df)}")

# #     st.dataframe(df, use_container_width=True)

# #     # =================================================
# #     # SENTIMENT SUMMARY
# #     # =================================================

# #     st.subheader("📊 Sentiment Summary")

# #     sentiment_counts = df["Sentiment"].value_counts()

# #     st.bar_chart(sentiment_counts)

# #     # =================================================
# #     # TOP NEGATIVE
# #     # =================================================

# #     st.subheader("😡 Top Negative Tweets")

# #     negative_df = (
# #         df[df["Sentiment"] == "Negative"]
# #         .sort_values(
# #             by=["Polarity", "Likes"],
# #             ascending=[True, False]
# #         )
# #         .head(10)
# #     )

# #     st.dataframe(
# #         negative_df[
# #             [
# #                 "Username",
# #                 "Tweet",
# #                 "Likes",
# #                 "Tweet URL"
# #             ]
# #         ],
# #         use_container_width=True
# #     )

# #     # =================================================
# #     # DOWNLOAD
# #     # =================================================

# #     output = BytesIO()

# #     with pd.ExcelWriter(output, engine="openpyxl") as writer:

# #         df.to_excel(
# #             writer,
# #             index=False,
# #             sheet_name="Tweets"
# #         )

# #     output.seek(0)

# #     st.download_button(
# #         label="📥 Download Excel",
# #         data=output,
# #         file_name="twitter_social_listening.xlsx",
# #         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
# #     )




# # =====================================================
# # TWITTER/X SOCIAL LISTENING
# # =====================================================

# import streamlit as st
# import pandas as pd
# import snscrape.modules.twitter as sntwitter
# from textblob import TextBlob
# from io import BytesIO
# import time

# # =====================================================
# # PAGE CONFIG
# # =====================================================

# st.set_page_config(
#     page_title="Twitter Social Listening",
#     layout="wide"
# )

# st.title("🐦 Twitter/X Social Listening")

# # =====================================================
# # SESSION STATE
# # =====================================================

# if "df" not in st.session_state:
#     st.session_state.df = None

# if "positive_df" not in st.session_state:
#     st.session_state.positive_df = None

# if "negative_df" not in st.session_state:
#     st.session_state.negative_df = None

# # =====================================================
# # INPUTS
# # =====================================================

# search_query = st.text_input(
#     "Enter Topic or Username",
#     placeholder="Example: Karnataka Tourism OR from:KarnatakaWorld"
# )

# max_tweets = st.slider(
#     "Number of Tweets",
#     10,
#     200,
#     50
# )

# # =====================================================
# # BUTTON
# # =====================================================

# if st.button("Pull Tweets"):

#     if not search_query:
#         st.error("Please enter topic or username")
#         st.stop()

#     tweets_data = []

#     progress = st.progress(0)

#     st.info("Fetching tweets from X/Twitter...")

#     # =================================================
#     # SCRAPER
#     # =================================================

#     try:

#         scraper = sntwitter.TwitterSearchScraper(
#             f"{search_query} lang:en"
#         )

#         for i, tweet in enumerate(scraper.get_items()):

#             if i >= max_tweets:
#                 break

#             # =========================================
#             # PROGRESS BAR
#             # =========================================

#             progress.progress((i + 1) / max_tweets)

#             # =========================================
#             # SAFE TWEET TEXT
#             # =========================================

#             try:
#                 text = tweet.rawContent
#             except:
#                 try:
#                     text = tweet.content
#                 except:
#                     continue

#             # =========================================
#             # EMPTY CHECK
#             # =========================================

#             if not text:
#                 continue

#             # =========================================
#             # SENTIMENT
#             # =========================================

#             polarity = TextBlob(text).sentiment.polarity

#             if polarity > 0:
#                 sentiment = "Positive"

#             elif polarity < 0:
#                 sentiment = "Negative"

#             else:
#                 sentiment = "Neutral"

#             # =========================================
#             # SAVE DATA
#             # =========================================

#             tweets_data.append({

#                 "Date": tweet.date,

#                 "Username":
#                 getattr(tweet.user, "username", ""),

#                 "Display Name":
#                 getattr(tweet.user, "displayname", ""),

#                 "Tweet": text,

#                 "Likes":
#                 getattr(tweet, "likeCount", 0),

#                 "Retweets":
#                 getattr(tweet, "retweetCount", 0),

#                 "Replies":
#                 getattr(tweet, "replyCount", 0),

#                 "Language":
#                 getattr(tweet, "lang", ""),

#                 "Tweet URL":
#                 f"https://twitter.com/{tweet.user.username}/status/{tweet.id}",

#                 "Sentiment": sentiment,

#                 "Polarity": polarity
#             })

#             # =========================================
#             # SMALL DELAY
#             # =========================================

#             time.sleep(0.2)

#     except Exception as e:

#         st.error(
#             f"""
# Twitter blocked the request.

# Possible reasons:
# - Too many requests
# - Temporary Twitter restriction
# - snscrape limitation

# Try:
# - smaller tweet count
# - different keyword
# - retry after few minutes
#             """
#         )

#         st.code(str(e))

#     # =================================================
#     # DATAFRAME
#     # =================================================

#     df = pd.DataFrame(tweets_data)

#     if df.empty:
#         st.warning("No tweets found.")
#         st.stop()

#     # =================================================
#     # TOP POSITIVE
#     # =================================================

#     positive_df = (
#         df[df["Sentiment"] == "Positive"]
#         .sort_values(
#             by=["Polarity", "Likes"],
#             ascending=False
#         )
#         .head(10)
#     )

#     # =================================================
#     # TOP NEGATIVE
#     # =================================================

#     negative_df = (
#         df[df["Sentiment"] == "Negative"]
#         .sort_values(
#             by=["Polarity", "Likes"],
#             ascending=[True, False]
#         )
#         .head(10)
#     )

#     # =================================================
#     # SAVE SESSION
#     # =================================================

#     st.session_state.df = df
#     st.session_state.positive_df = positive_df
#     st.session_state.negative_df = negative_df

# # =====================================================
# # DISPLAY
# # =====================================================

# if st.session_state.df is not None:

#     df = st.session_state.df
#     positive_df = st.session_state.positive_df
#     negative_df = st.session_state.negative_df

#     # =================================================
#     # MAIN DATA
#     # =================================================

#     st.success(f"Total Tweets Pulled: {len(df)}")

#     st.dataframe(
#         df,
#         use_container_width=True
#     )

#     # =================================================
#     # SENTIMENT SUMMARY
#     # =================================================

#     st.subheader("📊 Sentiment Summary")

#     sentiment_counts = df["Sentiment"].value_counts()

#     st.bar_chart(sentiment_counts)

#     # =================================================
#     # TOP POSITIVE
#     # =================================================

#     st.subheader("😊 Top Positive Tweets")

#     st.dataframe(
#         positive_df[
#             [
#                 "Username",
#                 "Tweet",
#                 "Likes",
#                 "Tweet URL"
#             ]
#         ],
#         use_container_width=True
#     )

#     # =================================================
#     # TOP NEGATIVE
#     # =================================================

#     st.subheader("😡 Top Negative Tweets")

#     st.dataframe(
#         negative_df[
#             [
#                 "Username",
#                 "Tweet",
#                 "Likes",
#                 "Tweet URL"
#             ]
#         ],
#         use_container_width=True
#     )

#     # =================================================
#     # DOWNLOAD
#     # =================================================

#     output = BytesIO()

#     with pd.ExcelWriter(
#         output,
#         engine="openpyxl"
#     ) as writer:

#         df.to_excel(
#             writer,
#             index=False,
#             sheet_name="All Tweets"
#         )

#         positive_df.to_excel(
#             writer,
#             index=False,
#             sheet_name="Top Positive"
#         )

#         negative_df.to_excel(
#             writer,
#             index=False,
#             sheet_name="Top Negative"
#         )

#     output.seek(0)

#     st.download_button(
#         label="📥 Download Excel",
#         data=output,
#         file_name="twitter_social_listening.xlsx",
#         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     )



import streamlit as st
import pandas as pd
from io import BytesIO
import snscrape.modules.twitter as sntwitter

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Twitter/X Scraper",
    layout="wide"
)

st.title("🐦 Twitter/X Data Scraper")

# =========================================================
# INPUTS
# =========================================================

search_query = st.text_input(
    "Enter Search Query",
    value="karnataka tourism"
)

tweet_limit = st.number_input(
    "Number of Tweets",
    min_value=10,
    max_value=5000,
    value=100
)

search_type = st.selectbox(
    "Search Type",
    [
        "Keyword Search",
        "Hashtag Search",
        "User Tweets"
    ]
)

# =========================================================
# SCRAPE BUTTON
# =========================================================

if st.button("Fetch Tweets"):

    tweets_data = []

    try:

        # =====================================================
        # SELECT SCRAPER
        # =====================================================

        if search_type == "Keyword Search":
            scraper = sntwitter.TwitterSearchScraper(search_query)

        elif search_type == "Hashtag Search":

            hashtag = search_query.replace("#", "")
            scraper = sntwitter.TwitterHashtagScraper(hashtag)

        elif search_type == "User Tweets":

            username = search_query.replace("@", "")
            scraper = sntwitter.TwitterUserScraper(username)

        # =====================================================
        # FETCH DATA
        # =====================================================

        with st.spinner("Fetching tweets..."):

            # for i, tweet in enumerate(scraper.get_items()):

            #     if i >= tweet_limit:
            #         break

            #     tweets_data.append({

            #         "Tweet ID": tweet.id,
            #         "Date": tweet.date,
            #         "Username": tweet.user.username,
            #         "Display Name": tweet.user.displayname,
            #         "Tweet": tweet.rawContent,
            #         "Likes": tweet.likeCount,
            #         "Retweets": tweet.retweetCount,
            #         "Replies": tweet.replyCount,
            #         "Quotes": tweet.quoteCount,
            #         "Language": tweet.lang,
            #         "Source": tweet.sourceLabel,
            #         "URL": tweet.url,

            #     })
            try:
                for i, tweet in enumerate(scraper.get_items()):
            
                    if i >= tweet_limit:
                        break
            
                    tweets_data.append({
                        "Tweet ID": tweet.id,
                        "Date": tweet.date,
                        "Username": tweet.user.username,
                        "Tweet": tweet.rawContent,
                        "Likes": tweet.likeCount,
                        "Retweets": tweet.retweetCount,
                        "Replies": tweet.replyCount,
                        "URL": tweet.url
                    })
            
            except Exception as e:
                st.error(f"Twitter blocked request: {e}")

        # =====================================================
        # DATAFRAME
        # =====================================================

        df = pd.DataFrame(tweets_data)

        st.success(f"Fetched {len(df)} tweets")

        st.dataframe(df, use_container_width=True)

        # =====================================================
        # DOWNLOAD EXCEL
        # =====================================================

        output = BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

        st.download_button(
            label="📥 Download Excel",
            data=output.getvalue(),
            file_name="twitter_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Error: {str(e)}")
