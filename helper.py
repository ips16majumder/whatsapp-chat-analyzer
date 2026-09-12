import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji

extract = URLExtract()


def fetch_starts(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []

    for message in df['message']:
        words.extend(message.split())

    num_words = len(words)

    num_media_messages = df[
        df['message'] == '<Media omitted>\n'
    ].shape[0]

    links = []

    for message in df['message']:
        links.extend(extract.find_urls(message))

    num_links = len(links)

    return num_messages, num_words, num_media_messages, num_links


def most_busy_users(df):

    temp = df[df['user'] != 'group_notification']

    x = temp['user'].value_counts().head()

    df_percent = (
        round(
            (temp['user'].value_counts() / temp.shape[0]) * 100,
            2
        )
        .reset_index()
        .rename(
            columns={
                'user': 'name',
                'count': 'percent'
            }
        )
    )

    return x, df_percent


def create_wordcloud(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']

    temp = temp[temp['message'] != '<Media omitted>\n']

    with open(
        'stop_words_english.txt',
        'r',
        encoding='utf-8'
    ) as f:
        stop_words = set(f.read().splitlines())

    text = temp['message'].str.cat(sep=' ')

    words = []

    for word in text.lower().split():
        if word not in stop_words:
            words.append(word)

    text = ' '.join(words)

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color='white'
    )

    temp['message'] = temp['message'].apply(remove_stop_words)

    df_wc = wc.generate(text)

    return df_wc


def most_common_words(selected_user, df):

    with open(
        'stop_words_english.txt',
        'r',
        encoding='utf-8'
    ) as f:
        stop_words = set(f.read().splitlines())

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']

    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():

            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(
        Counter(words).most_common(20),
        columns=['word', 'count']
    )

    return most_common_df


def emoji_helper(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []

    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(
        Counter(emojis).most_common(),
        columns=['emoji', 'count']
    )

    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(
        index='day_name',
        columns='period',
        values='message',
        aggfunc='count'
    ).fillna(0)

    return user_heatmap
