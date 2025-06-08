import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

matches = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')

# Clean up teams list
teams = sorted(matches['team1'].dropna().unique())
seasons = sorted(matches['Season'].dropna().unique())

#team win counts
st.subheader("🏆 Total Wins by Each Team")
win_counts = matches['winner'].value_counts()
fig, ax = plt.subplots()
win_counts.plot(kind='bar', color='skyblue', ax=ax)
ax.set_ylabel("Matches Won")
st.pyplot(fig)

#Team-wise performance of the season
st.subheader("📅 Team Performance Over Seasons")
selected_team = st.selectbox("Select a team", teams)
team_wins_by_year = matches[matches['winner'] == selected_team].groupby('Season').count()['id']
fig2, ax2 = plt.subplots()
team_wins_by_year.plot(marker='o', color='orange', ax=ax2)
ax2.set_title(f"{selected_team} Wins per Season")
ax2.set_xlabel("Season")
ax2.set_ylabel("Wins")
st.pyplot(fig2)

#top batsmen of the season
st.subheader("🏏 Top Batsmen by Season")
selected_season = st.selectbox("Choose Season", seasons, key="season_batsmen")
season_matches = matches[matches['Season'] == selected_season]['id'].tolist()
season_data = deliveries[deliveries['match_id'].isin(season_matches)]
top_batsmen = season_data.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(10)

fig3, ax3 = plt.subplots()
top_batsmen.plot(kind='bar', color='green', ax=ax3)
ax3.set_title(f"Top 10 Batsmen in {selected_season}")
st.pyplot(fig3)

#top bowlers
st.subheader("🎯 Top Bowlers by Season")
selected_season_bowl = st.selectbox("Choose Season", seasons, key="season_bowlers")
season_matches_b = matches[matches['Season'] == selected_season_bowl]['id'].tolist()
season_deliveries_b = deliveries[deliveries['match_id'].isin(season_matches_b)]
# Wickets (excluding run outs and extras)
season_deliveries_b = season_deliveries_b[season_deliveries_b['dismissal_kind'].notnull()]
season_deliveries_b = season_deliveries_b[~season_deliveries_b['dismissal_kind'].isin(['run out', 'retired hurt', 'obstructing the field'])]

top_bowlers = season_deliveries_b['bowler'].value_counts().head(10)

fig4, ax4 = plt.subplots()
top_bowlers.plot(kind='bar', color='purple', ax=ax4)
ax4.set_title(f"Top 10 Bowlers in {selected_season_bowl}")
st.pyplot(fig4)

#team-vs-team
st.subheader("⚔️ Head-to-Head Team Comparison")
col1, col2 = st.columns(2)
with col1:
    team1 = st.selectbox("Team 1", teams, key="team1")
with col2:
    team2 = st.selectbox("Team 2", [t for t in teams if t != team1], key="team2")

filtered_matches = matches[((matches['team1'] == team1) & (matches['team2'] == team2)) |
                           ((matches['team1'] == team2) & (matches['team2'] == team1))]

head2head = filtered_matches['winner'].value_counts()

fig5, ax5 = plt.subplots()
head2head.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax5)
ax5.set_ylabel('')
ax5.set_title(f"{team1} vs {team2} - Win %")
st.pyplot(fig5)



