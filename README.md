# InnoTyaga Python Bot

![InnoTyaga Logo](logo.png)

InnoTyaga is an unofficial club in Innopolis, boasting over 30 active members. This python bot was developed by @kupamonke to aid in the management of the club, particularly with handling points calculation for each member and automatically updating the leaderboard.

- [InnoTyaga Python Bot](#innotyaga-python-bot)
  - [Overview](#overview)
    - [Points Calculation](#points-calculation)
  - [Features](#features)
    - [Admin functions](#admin-functions)
  - [Install](#install)
    - [Basic install](#basic-install)
    - [Run on Docker](#run-on-docker)
  - [Future Developments](#future-developments)

## Overview

As the club grows, manually calculating points and ranking members is becoming increasingly tedious. This bot aims to simplify these tasks, allowing members to focus on their performance instead of data management.

InnoTyaga bot can display the leaderboard and automatically calculate points for members based on the weight they lift, their own weight, and their gender. Upon adding a new member or updating an existing one's details, the bot recalculates the points and updates the leaderboard.

### Points Calculation

For male members, the points are calculated using the formula `100*L/S` where `L` is the lifted weight and `S` is the self weight. For female members, the formula `164*L/S` is used. When a member's self weight is updated, it does not affect their previous results, but it is factored in for subsequent changes. However, a change in gender will recalculate the points.

## Features

- Display static information about the club.
- Display and update the leaderboard.
- Allow members to register themselves, where their Telegram name and alias are added to the leaderboard (no points information at registration).

### Admin functions

For club admins, known as "TA's" of InnoTyaga, the bot provides additional features. TA's can:

- Add new members using `/newmember`.
- Change any member's weight and self weight using `/setselfweight` and `/setweight`.
- Use `/oldmember` to add all information about a member that is currently not in the leaderboard.
- Delete members from the leaderboard.
- Change the gender and name of any member.

[Functionality demonstration video](https://youtu.be/MzXjFsMmog0)

## Install

### Basic install
```bash
git clone https://github.com/LocalT0aster/InnoTyaga.git
cd InnoTyaga
pip install -r reqirements.txt
```

### Run on Docker
```bash
docker build -t tyagabot-img .
docker run -d --name tyagabot tyagabot-img
```

## Future Developments

The current functionality of the bot meets the club's needs, but there are plans for further improvements. In the future, the `/profile` command will be added to display detailed information about a member and to show a graph of points over time.
