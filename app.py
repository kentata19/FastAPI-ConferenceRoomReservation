import streamlit as st
import random
import requests
import json
import datetime
import pandas as pd

page = st.sidebar.selectbox('Choose your page', ['users', 'rooms', 'bookings'])

if page == 'users':
    st.title('ユーザー登録画面')
    with st.form(key='user'):
        username: str = st.text_input('ユーザー名', max_chars=12)
        data = {
            'username': username
        }
        submit_button = st.form_submit_button(label='リクエスト送信')

        if submit_button:
            url = 'http://127.0.0.1:8000/users'
            res = requests.post(
                url,
                data=json.dumps(data)
            )
            if res.status_code == 200:
                st.success('ユーザー登録完了')
            st.json(res.json())
elif page == 'rooms':
    st.title('会議室登録画面')
    with st.form(key='room'):
        room_name: str = st.text_input('会議室名', max_chars=12)
        capacity: int = st.number_input('定員', step=1)
        data = {
            'room_name': room_name,
            'capacity': capacity
        }
        submit_button = st.form_submit_button(label='リクエスト送信')

        if submit_button:
            url = 'http://127.0.0.1:8000/rooms'
            res = requests.post(
                url,
                data=json.dumps(data)
            )

            if res.status_code == 200:
                st.success('会議室登録完了')
            st.json(res.json())
elif page == 'bookings':
    st.title('会議室予約画面')

    url_users = 'http://127.0.0.1:8000/users'
    res = requests.get(url_users)
    users = res.json()
    users_dict = {}
    for user in users:
        users_dict[user['username']] = user['user_id']

    url_rooms = 'http://127.0.0.1:8000/rooms'
    res = requests.get(url_rooms)
    rooms = res.json()
    rooms_dict = {}
    for room in rooms:
        rooms_dict[room['room_name']] = {
            'room_id': room['room_id'],
            'capacity': room['capacity']
        }

    st.write('### 会議室一覧')
    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ['会議室名', '定員', '会議室ID']
    st.table(df_rooms)

    url_bookings = 'http://127.0.0.1:8000/bookings'
    res = requests.get(url_bookings)
    bookings = res.json()
    df_bookings = pd.DataFrame(bookings)

    users_id = {}
    for user in users:
        users_id[user['user_id']] = user['username']

    rooms_id = {}
    for room in rooms:
        rooms_id[room['room_id']] = {
            'room_name': room['room_name'],
            'capacity': room['capacity']
        }

    to_username = lambda x: users_id[x]
    to_roomname = lambda x: rooms_id[x]['room_name']
    to_datetime = lambda x: datetime.datetime.fromisoformat(x).strftime('%Y/%m/%d %H:%M')

    df_bookings['user_id'] = df_bookings['user_id'].map(to_username)
    df_bookings['room_id'] = df_bookings['room_id'].map(to_roomname)
    df_bookings['start_datetime'] = df_bookings['start_datetime'].map(to_datetime)
    df_bookings['end_datetime'] = df_bookings['end_datetime'].map(to_datetime)

    # 各カラム名をわかりやすく日本語に変更
    df_bookings.columns = ['ユーザー名', '会議室名', '予約人数', '開始時刻', '終了時刻', '予約ID']

    st.write('### 予約一覧')
    st.table(df_bookings)

    with st.form(key='booking'):
        username: str = st.selectbox('ユーザー名', list(users_dict.keys()))
        room_name: str = st.selectbox('会議室名', list(rooms_dict.keys()))
        booked_num: int = st.number_input('予約人数', step=1, min_value=1)
        date = st.date_input('日付:', min_value=datetime.date.today())
        start_time = st.time_input('開始時刻:', value=datetime.time(hour=9, minute=0))
        end_time = st.time_input('終了時刻:', value=datetime.time(hour=20, minute=0))
        submit_button = st.form_submit_button(label='リクエスト送信')

        if submit_button:
            user_id: int = users_dict[username]
            room_id: int = rooms_dict[room_name]['room_id']
            capacity: int = rooms_dict[room_name]['capacity']
            data = {
                'user_id': user_id,
                'room_id': room_id,
                'booked_num': booked_num,
                'start_datetime': datetime.datetime(
                    year=date.year,
                    month=date.month,
                    day=date.day,
                    hour=start_time.hour,
                    minute=start_time.minute
                ).isoformat(),
                'end_datetime': datetime.datetime(
                    year=date.year,
                    month=date.month,
                    day=date.day,
                    hour=end_time.hour,
                    minute=end_time.minute
                ).isoformat()
            }
            if booked_num <= capacity:
                url = 'http://127.0.0.1:8000/bookings'
                res = requests.post(
                    url,
                    data=json.dumps(data)
                )
                if res.status_code == 200:
                    st.success('会議室予約完了')
                st.json(res.json())
            else:
                st.error('予約人数が定員を超えています')

