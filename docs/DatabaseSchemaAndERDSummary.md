# 🗄️ Final Database Schema Summary

## 🎶 Core Music Catalog

| Table                | Description                                         |
| -------------------- | --------------------------------------------------- |
| tracks               | Track details (title, duration, ISRC, lyrics, etc.) |
| albums               | Album grouping for tracks                           |
| artists              | Individual artists and groups                       |
| artist_groups        | Defines artist groups and solo artists              |
| artist_group_members | Mapping of artists to their groups (many-to-many)   |
| track_artists        | Polymorphic: maps artists/groups to tracks          |
| audio_files          | Metadata: format, bitrate, file path                |
| fingerprints         | Audio hashes used for recognition                   |

## 📄 Ownership & Rights

| Table            | Description                               |
| ---------------- | ----------------------------------------- |
| track_ownerships | Polymorphic: who owns what % of the track |
| royalty_shares   | Revenue share among contributors          |

## 📡 Radio Detection & Monitoring

| Table              | Description                                           |
| ------------------ | ----------------------------------------------------- |
| radio_stations     | Station metadata (location, name)                     |
| radio_airplay_logs | Detected plays: station, timestamp, track, confidence |

## 🔔 Trigger Logic

- PostgreSQL AFTER INSERT trigger on radio_airplay_logs
- Sends notification via pg_notify() when a new match is detected
- Can push to:
  - Email/Slack alerts
  - Background job queues
  - Webhook listeners

## 📊 Aggregated Reports

- By Artist: Total airplays, royalties
- By Track: Play counts, exposure
- By Station: Which stations play what, when
- Available via materialized views or reporting endpoints

## 👥 System Actors & Roles

| Actor                 | Role/Responsibilities                                                                                    |
| --------------------- | -------------------------------------------------------------------------------------------------------- |
| Catalog Administrator | - Manages artist, track, and album metadata<br>- Uploads audio files and lyrics                          |
| Rights Holder         | - Assigns ownership/royalty splits<br>- Registers ISRC codes<br>- Views royalty reports                  |
| Radio Monitor         | - Monitors radio matches<br>- Investigates unlicensed usage<br>- Confirms detections                     |
| Developer/Engineer    | - Integrates audio matching engine<br>- Maintains fingerprinting system<br>- Handles backend scalability |
| Business Analyst      | - Generates reports by station/artist/region<br>- Uses aggregated insights for marketing/licensing       |
| Artist/Label          | - May access a dashboard to view plays, revenue, exposure                                                |

## 🎵 Music Catalog ERD (Simplified Overview)

```
[artists]                [artist_groups]
   │                            │
   └──< artist_group_members >──┘

[artists]
   │
   └──< track_artists >── [tracks] ──< [audio_files]
                                 │
                                 └──< [albums]

[tracks] ──< [fingerprints]
    │
    └──< [track_ownerships]
    └──< [royalty_shares]

[tracks] ──< [radio_airplay_logs] >── [radio_stations]
```

**Relationships:**

- Polymorphic Relationships: track_ownerships and royalty_shares can refer to either artists or artist_groups via owner_type / recipient_type.
- Triggers: radio_airplay_logs has a trigger that alerts when a new match is logged.

✅ The SQL schema with all required tables and triggers has been created.
