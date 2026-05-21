#!/usr/bin/env python3
"""
Scrum Task Manager CLI
=======================
A command-line Scrum board for managing sprints, user stories,
and backlogs. Persists data in SQLite.

User Story: As a developer practising Scrum, I want a CLI Scrum board
so that I can track sprint progress without external tools.
"""

import sqlite3
import argparse
import sys
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from datetime import date


class Status(str, Enum):
    BACKLOG = "Backlog"
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    IN_REVIEW = "In Review"
    DONE = "Done"


class Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


@dataclass
class UserStory:
    id: Optional[int]
    title: str
    description: str
    story_points: int
    priority: str
    status: str
    sprint_id: Optional[int] = None
    assignee: Optional[str] = None
    acceptance_criteria: str = ""


@dataclass
class Sprint:
    id: Optional[int]
    name: str
    goal: str
    start_date: str
    end_date: str
    is_active: bool = False


class ScrumDatabase:
    """SQLite persistence layer."""

    def __init__(self, db_path: str = "scrum_board.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS sprints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                goal TEXT,
                start_date TEXT,
                end_date TEXT,
                is_active INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS user_stories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                story_points INTEGER DEFAULT 1,
                priority TEXT DEFAULT 'Medium',
                status TEXT DEFAULT 'Backlog',
                sprint_id INTEGER REFERENCES sprints(id),
                assignee TEXT,
                acceptance_criteria TEXT
            );
        """)
        self.conn.commit()

    def add_sprint(self, sprint: Sprint) -> int:
        cur = self.conn.execute(
            "INSERT INTO sprints (name, goal, start_date, end_date, is_active) VALUES (?,?,?,?,?)",
            (sprint.name, sprint.goal, sprint.start_date, sprint.end_date, int(sprint.is_active))
        )
        self.conn.commit()
        return cur.lastrowid

    def get_active_sprint(self) -> Optional[Sprint]:
        row = self.conn.execute(
            "SELECT * FROM sprints WHERE is_active=1 LIMIT 1"
        ).fetchone()
        if row:
            return Sprint(id=row["id"], name=row["name"], goal=row["goal"],
                          start_date=row["start_date"], end_date=row["end_date"],
                          is_active=bool(row["is_active"]))
        return None

    def add_story(self, story: UserStory) -> int:
        cur = self.conn.execute(
            """INSERT INTO user_stories
               (title, description, story_points, priority, status, sprint_id, assignee, acceptance_criteria)
               VALUES (?,?,?,?,?,?,?,?)""",
            (story.title, story.description, story.story_points, story.priority,
             story.status, story.sprint_id, story.assignee, story.acceptance_criteria)
        )
        self.conn.commit()
        return cur.lastrowid

    def update_story_status(self, story_id: int, status: str) -> bool:
        cur = self.conn.execute(
            "UPDATE user_stories SET status=? WHERE id=?", (status, story_id)
        )
        self.conn.commit()
        return cur.rowcount > 0

    def get_stories_by_sprint(self, sprint_id: int) -> List[UserStory]:
        rows = self.conn.execute(
            "SELECT * FROM user_stories WHERE sprint_id=? ORDER BY priority DESC, story_points DESC",
            (sprint_id,)
        ).fetchall()
        return [self._row_to_story(r) for r in rows]

    def get_backlog(self) -> List[UserStory]:
        rows = self.conn.execute(
            "SELECT * FROM user_stories WHERE sprint_id IS NULL ORDER BY priority DESC"
        ).fetchall()
        return [self._row_to_story(r) for r in rows]

    @staticmethod
    def _row_to_story(row) -> UserStory:
        return UserStory(
            id=row["id"], title=row["title"], description=row["description"],
            story_points=row["story_points"], priority=row["priority"],
            status=row["status"], sprint_id=row["sprint_id"],
            assignee=row["assignee"], acceptance_criteria=row["acceptance_criteria"]
        )

    def sprint_velocity(self, sprint_id: int) -> dict:
        rows = self.conn.execute(
            "SELECT status, SUM(story_points) as pts FROM user_stories WHERE sprint_id=? GROUP BY status",
            (sprint_id,)
        ).fetchall()
        return {r["status"]: r["pts"] or 0 for r in rows}


class ScrumBoard:
    """Application layer — Scrum ceremonies and board operations."""

    def __init__(self, db: ScrumDatabase):
        self.db = db

    def start_sprint(self, name: str, goal: str, duration_days: int = 14) -> Sprint:
        start = date.today()
        from datetime import timedelta
        end = start + timedelta(days=duration_days)
        sprint = Sprint(id=None, name=name, goal=goal,
                        start_date=start.isoformat(), end_date=end.isoformat(), is_active=True)
        sprint.id = self.db.add_sprint(sprint)
        return sprint

    def add_to_backlog(self, title: str, description: str, points: int,
                       priority: str = "Medium", criteria: str = "") -> UserStory:
        story = UserStory(
            id=None, title=title, description=description,
            story_points=points, priority=priority,
            status=Status.BACKLOG.value, acceptance_criteria=criteria
        )
        story.id = self.db.add_story(story)
        return story

    def move_story(self, story_id: int, new_status: str) -> bool:
        return self.db.update_story_status(story_id, new_status)

    def display_board(self):
        sprint = self.db.get_active_sprint()
        if not sprint:
            print("No active sprint. Start one with: task-manager sprint start <name> <goal>")
            return

        stories = self.db.get_stories_by_sprint(sprint.id)
        velocity = self.db.sprint_velocity(sprint.id)
        done_pts = velocity.get(Status.DONE.value, 0)
        total_pts = sum(velocity.values())

        print(f"\n{'='*60}")
        print(f" 🏃 Sprint: {sprint.name}")
        print(f" 🎯 Goal:   {sprint.goal}")
        print(f" 📅 Dates:  {sprint.start_date} → {sprint.end_date}")
        print(f" 📊 Velocity: {done_pts}/{total_pts} pts done")
        print(f"{'='*60}")

        for status in Status:
            matching = [s for s in stories if s.status == status.value]
            if matching:
                print(f"\n  [{status.value.upper()}]")
                for s in matching:
                    pts_label = f"({s.story_points}pt)"
                    assignee = f"@{s.assignee}" if s.assignee else ""
                    print(f"    #{s.id:03d} {pts_label} [{s.priority}] {s.title} {assignee}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Scrum Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Sprint commands
    sprint_p = subparsers.add_parser("sprint", help="Sprint management")
    sprint_sub = sprint_p.add_subparsers(dest="sprint_cmd")
    ss = sprint_sub.add_parser("start", help="Start new sprint")
    ss.add_argument("name"); ss.add_argument("goal")
    ss.add_argument("--days", type=int, default=14)

    # Story commands
    story_p = subparsers.add_parser("story", help="User story management")
    story_sub = story_p.add_subparsers(dest="story_cmd")
    sa = story_sub.add_parser("add", help="Add user story to backlog")
    sa.add_argument("title"); sa.add_argument("--desc", default="")
    sa.add_argument("--points", type=int, default=1)
    sa.add_argument("--priority", choices=[p.value for p in Priority], default="Medium")
    sa.add_argument("--criteria", default="")

    sm = story_sub.add_parser("move", help="Move story to new status")
    sm.add_argument("story_id", type=int)
    sm.add_argument("status", choices=[s.value for s in Status])

    # Board command
    subparsers.add_parser("board", help="Display sprint board")

    args = parser.parse_args()
    db = ScrumDatabase()
    board = ScrumBoard(db)

    if args.command == "sprint" and args.sprint_cmd == "start":
        sprint = board.start_sprint(args.name, args.goal, args.days)
        print(f"✅ Sprint '{sprint.name}' started (ID: {sprint.id})")
    elif args.command == "story" and args.story_cmd == "add":
        story = board.add_to_backlog(args.title, args.desc, args.points, args.priority, args.criteria)
        print(f"✅ Story added to backlog (ID: {story.id}, {story.story_points}pts)")
    elif args.command == "story" and args.story_cmd == "move":
        ok = board.move_story(args.story_id, args.status)
        print(f"✅ Moved" if ok else "❌ Story not found")
    elif args.command == "board":
        board.display_board()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
