# 📊 Scrum Task Manager CLI

## User Story
> *As a developer, I want a CLI Scrum board so that I can manage sprints, user stories, and track velocity without leaving the terminal.*

## Sprint Plan
| Sprint | Goal | Status |
|--------|------|--------|
| Sprint 1 | Data models + SQLite schema | ✅ Done |
| Sprint 2 | Board display + story management | ✅ Done |
| Sprint 3 | Sprint velocity + CLI polish | ✅ Done |

## Usage
```bash
# Start a sprint
python task_manager.py sprint start "Sprint 1" "Build authentication module" --days 14

# Add stories to backlog
python task_manager.py story add "Implement login" --points 5 --priority High
python task_manager.py story add "Write unit tests" --points 3 --priority Medium

# Move story through board
python task_manager.py story move 1 "In Progress"
python task_manager.py story move 1 "Done"

# View board
python task_manager.py board
```

## Definition of Done
- [x] Unit tests pass
- [x] All user stories delivered
- [x] Code reviewed
- [x] Documentation updated
