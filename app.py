import streamlit as stream
import pandas as pd
import pickle

teams = ['Royal Challengers Bengaluru',
         'Gujarat Titans',
         'Lucknow Super Giants',
         'Delhi Capitals',
         'Punjab Kings','Mumbai Indians',
         'Chennai Super Kings',
         'Sunrisers Hyderabad',
         'Kolkata Knight Riders',
         'Rajasthan Royals']

cities = ['Bengaluru', 'Mumbai', 'Cape Town', 'Chennai', 'Ahmedabad',
          'Abu Dhabi', 'Kolkata', 'Jaipur', 'Hyderabad', 'Port Elizabeth',
          'Centurion', 'Chandigarh', 'Navi Mumbai', 'Pune', 'Delhi',
          'Raipur', 'Dharamsala', 'Johannesburg', 'Sharjah', 'Mohali',
          'Lucknow', 'Dubai', 'Guwahati', 'Visakhapatnam', 'Ranchi',
          'Indore', 'Cuttack', 'Kimberley', 'Durban', 'Bloemfontein',
          'Nagpur']

stream.title("Teja Vutla's Project")
stream.title('IPL WIN PROBABILITY PREDICTOR')

pipe = pickle.load(open('pipe5.pkl','rb'))

col1, col2 = stream.columns(2)

with col1:
    batting_team = stream.selectbox('Select the batting team', sorted(teams))
teams.remove(batting_team)
with col2:
    bowling_team = stream.selectbox('Select the bowling team', sorted(teams))

selected_city = stream.selectbox('select venue', sorted(cities))

target = stream.number_input('target', min_value=0, step=1, format="%d")

col3,col4,col5,col6 = stream.columns(4)
with col3:
    score = stream.number_input('Score', min_value=0, step=1, format="%d")
with col4:
    overs = stream.number_input('Overs completed', min_value=0, max_value=19, step=1, format="%d")
with col5:
    balls1 = stream.number_input('Balls bowled in current over', min_value=0, max_value=5, step=1, format="%d")
with col6:
    wickets = stream.number_input('Wickets fallen', min_value=0, max_value=10, step=1, format="%d")
teams1 =[batting_team,bowling_team]
toss_winner = stream.selectbox('select toss winner',teams1)
if stream.button('predict probability'):
    runs_left = target-score
    balls_left = 120-(overs*6)-balls1
    if(balls_left == 0):
        stream.warning("match is over")
    elif(balls_left == 120):
        stream.warning("innings did'nt start")
    else:
        x=1
        if(toss_winner==bowling_team):
            x=0
        wickets_left = 10-wickets
        crr = (6*score)/(120-balls_left)
        rrr = (6*runs_left)/balls_left
        input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'wickets':[wickets_left],'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})
        stream.title('match summary')
        stream.table(input_df)
        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]
        stream.text(batting_team+"-"+str(round(win*100))+"%")
        stream.text(bowling_team + "-" + str(round(loss*100)) + "%")