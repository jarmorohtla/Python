# uefacl.py
from cgi import parse_qs, escape
import psycopg2

def get_connection():
    dbName = "uefacldb"
    dbUser = "uefacl"
    dbPassword = "uefacl"
    return psycopg2.connect(database=dbName, user=dbUser, password=dbPassword, host="127.0.0.1", port="5432")


def create_and_fill_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS groups;")
    cur.execute("CREATE TABLE groups (groupID INT, name VARCHAR(20));")
    f = open("ucl_db/groups.txt")
    for rida in f:
        group = rida.split(',')
        cur.execute("INSERT INTO groups VALUES(" + group[0]  + ",'" + group[1].strip() + "');")
    f.close()

    cur.execute("DROP TABLE IF EXISTS clubs;")
    cur.execute("CREATE TABLE clubs (clubID INT, name VARCHAR(30), coach VARCHAR(30), groupID INT);")
    f = open("ucl_db/clubs.txt", encoding='utf-8')
    for rida in f:
        club = rida.split(',')
        cur.execute("INSERT INTO clubs VALUES(" + club[0]  + ",'" + club[1] + "','" + club[2] + "'," + club[3] + ");")
    f.close()

    cur.execute("DROP TABLE IF EXISTS players;")
    cur.execute("CREATE TABLE players (playerID INT, number INT, name VARCHAR(30), position VARCHAR(30), clubID INT);")
    f = open("ucl_db/players.txt", encoding='utf-8')
    for rida in f:
        player = rida.split(',')
        cur.execute("INSERT INTO players VALUES(" + player[0]  + "," + player[1] + ",'" + player[2] + "','" + player[3] + "'," + player[4] + ");")
    f.close()

    cur.execute("DROP TABLE IF EXISTS matches;")
    cur.execute("CREATE TABLE matches (matchID INT, groupID INT, homeClubID INT, awayClubID INT, homeGoals INT, awayGoals INT);")
    f = open("ucl_db/matches.txt")
    for rida in f:
        match = rida.split(',')
        cur.execute("INSERT INTO matches VALUES(" + match[0]  + "," + match[1] + "," + match[2] + "," + match[3] + "," + match[4] + "," + match[5] + ");")
    f.close()

    cur.execute("DROP TABLE IF EXISTS goals;")
    cur.execute("CREATE TABLE goals (goalID INT, time VARCHAR(10), playerID INT, isPenalty VARCHAR(10), isOwnGoal VARCHAR(10), matchID INT);")
    f = open("ucl_db/goals.txt")
    for rida in f:
        goal = rida.split(',')
        cur.execute("INSERT INTO goals VALUES(" + goal[0]  + ",'" + goal[1] + "'," + goal[2] + ",'" + goal[3] + "','" + goal[4] + "'," + goal[5].strip() + ");")
    f.close()

    conn.commit()
    conn.close()


def show_groups():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM groups;")
    rows = cur.fetchall()
    groups_table = "<TABLE>\n"
    for row in rows:
        groups_table += "<TR><TD><A href=\"?page=group&amp;group_id="
        groups_table += str(row[0])
        groups_table += "\">"
        groups_table += row[1]
        groups_table += "</A></TD></TR>\n"
    groups_table += "</TABLE>"
    conn.close()
    return groups_table


def show_group(group_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM groups WHERE groupID=" + str(group_id));
    row = cur.fetchone()
    group = "<H2>" + row[0] + "</H2>\n"
    
    cur.execute("SELECT matchID, hc.name as homeName, ac.name as awayName, homeGoals, awayGoals FROM matches m JOIN clubs hc ON m.homeClubID=hc.clubID JOIN clubs ac ON m.awayClubID=ac.clubID WHERE m.groupID=" + group_id + " ORDER BY matchID;")
    rows = cur.fetchall()
    for row in rows:
        group += str(row[1])
        group += "&nbsp;&nbsp;<A href=\"?page=match&amp;match_id="
        group += str(row[0])
        group += "\"><B>"
        group += str(row[3])
        group += "&nbsp;:&nbsp;"
        group += str(row[4])
        group += "</B></A>&nbsp;&nbsp;"
        group += str(row[2])
        group += "<BR>\n"
    group += "<BR>"
    return group


def show_clubs():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT clubID, clubs.name, coach, groups.name AS groupName FROM clubs JOIN groups ON clubs.groupID=groups.groupID ORDER BY name;")
    rows = cur.fetchall()
    clubs_table = "<TABLE>\n"
    clubs_table += "<TR><TH>Name</TH><TH>Coach</TH><TH>Group</TH></TR>\n"
    for row in rows:
        clubs_table += "<TR><TD><A href=\"?page=club&amp;club_id="
        clubs_table += str(row[0])
        clubs_table += "\">"
        clubs_table += row[1]
        clubs_table += "</A></TD><TD>"
        clubs_table += row[2]
        clubs_table += "</TD><TD>"
        clubs_table += row[3]
        clubs_table += "</TD></TR>\n"
    clubs_table += "</TABLE>"
    return clubs_table


def show_club(club_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM clubs WHERE clubID=" + str(club_id));
    row = cur.fetchone()
    club = "<H2>" + row[0] + "</H2>\n"
    
    club += "<H3>Goalkeepers</H3>\n"
    cur.execute("SELECT number,name FROM players WHERE clubID="+club_id+" AND position='Goalkeeper';")
    rows = cur.fetchall()
    for row in rows:
        club += "<B>"
        club += str(row[0])
        club += "</B>&nbsp;&nbsp;"
        club += row[1]
        club += "<BR>\n"
    club += "<BR>\n"
        
    club += "<H3>Defenders</H3>\n"
    cur.execute("SELECT number,name FROM players WHERE clubID="+club_id+" AND position='Defender';")
    rows = cur.fetchall()
    for row in rows:
        club += "<B>"
        club += str(row[0])
        club += "</B>&nbsp;&nbsp;"
        club += row[1]
        club += "<BR>\n"
    club += "<BR>\n"
    
    club += "<H3>Midfielders</H3>\n"
    cur.execute("SELECT number,name FROM players WHERE clubID="+club_id+" AND position='Midfielder';")
    rows = cur.fetchall()
    for row in rows:
        club += "<B>"
        club += str(row[0])
        club += "</B>&nbsp;&nbsp;"
        club += row[1]
        club += "<BR>\n"
    club += "<BR>\n"
    
    club += "<H3>Forwards</H3>\n"
    cur.execute("SELECT number,name FROM players WHERE clubID="+club_id+" AND position='Forward';")
    rows = cur.fetchall()
    for row in rows:
        club += "<B>"
        club += str(row[0])
        club += "</B>&nbsp;&nbsp;"
        club += row[1]
        club += "<BR>"
    return club


def show_match(match_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT homeClubID, hc.name as homeName, awayClubID, ac.name as awayName, homeGoals, awayGoals FROM matches m JOIN clubs hc ON m.homeClubID=hc.clubID JOIN clubs ac ON m.awayClubID=ac.clubID WHERE m.matchID=" + match_id + ";")
    row = cur.fetchone()
    match_table = "<TABLE>\n<TR><TH>" + row[1] + "</TH><TH><H1>&nbsp;&nbsp;" + str(row[4]) + " : " + str(row[5]) + "&nbsp;&nbsp;</H1></TH><TH>" + row[3] + "</TH></TR>\n"
    home_club_id = row[0]
    away_club_id = row[2]
    
    cur.execute("SELECT time,name,clubid,ispenalty,isowngoal FROM goals JOIN players ON goals.playerID=players.playerID WHERE matchID=" + match_id + " ORDER BY time;")
    rows = cur.fetchall()
    for row in rows:
        match_table += "<TR>"

        if row[2] == home_club_id and row[4] == "False" :
            match_table += "<TD>"
            match_table += str(row[0])
            match_table += ". "
            match_table += str(row[1])
            if row[3] == "True" :
                match_table += " (P)"
            match_table += "</TD><TD></TD><TD></TD></TR>\n"
        elif row[2] == away_club_id and row[4] == "False" :
            match_table += "<TD></TD><TD></TD><TD>"
            match_table += str(row[0])
            match_table += ". "
            match_table += str(row[1])
            if row[3] == "True" :
                match_table += " (P)"
            match_table += "</TD></TR>\n"
        elif row[2] == home_club_id and row[4] == "True" :
            match_table += "<TD></TD><TD></TD><TD>"
            match_table += str(row[0])
            match_table += ". "
            match_table += str(row[1])
            match_table += " (o.g.)"
            match_table += "</TD></TR>\n"
        elif row[2] == away_club_id and row[4] == "True" :
            match_table += "<TD>"
            match_table += str(row[0])
            match_table += ". "
            match_table += str(row[1])
            match_table += " (o.g.)"
            match_table += "</TD><TD></TD><TD></TD></TR>\n"
    match_table += "</TABLE>"
    return match_table


def application(environ, start_response):
    template = """<!DOCTYPE html>
<html>
<head>
<title>UEFA Champions League</title>
</head>
<body>
<h1>UEFA Champions League group stage 2012/13</h1>
{}
</body>
</html>"""

    d = parse_qs(environ['QUERY_STRING'])
    page = d.get('page', [''])[0]

    if page == "groups":
        response_body = template.format(show_groups())
    elif page == "group":
        group_id = page = d.get('group_id', [''])[0]
        response_body = template.format(show_group(group_id))
    elif page == "clubs":
        response_body = template.format(show_clubs())
    elif page == "club":
        club_id = page = d.get('club_id', [''])[0]
        response_body = template.format(show_club(club_id))
    elif page == "match":
        match_id = page = d.get('match_id', [''])[0]
        response_body = template.format(show_match(match_id))
    else:
        create_and_fill_tables()
        response_body = template.format("<h2><a href=\"?page=groups\">Groups</a></h2>\n<h2><a href=\"?page=clubs\">Clubs</a></h2>")

    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return [response_body.encode("UTF-8")]