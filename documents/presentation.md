% SmartFridge
% Christian, Jörn, Nils, Liuba
% February 17, 2018

## Agenda

- Project Management (Chris)
- Requirements (Liuba)
- System Architecture (Nils)
- Quality (Jörn)
- Live Demo (all)
- Dream (Chris)

## Project Management
### Our Software Lifecyle Model:
#### Evolutionary Prototyping (EP)
- Initial concept:
    - Module-based software system.
- Design and implementation of initial prototype:
    - Design was within 2nd meeting
- Refine prototype until acceptable:
    - Idea driven approach
- Complete and release prototype	
#### Reasons why:
- EP is a result-driven approach
- Progress is visible quickly
- Heterogenous level of programming experience before
- Gradual functionality extension facilitates orchestration of components is comprehensibly, by chosing early stages with little functionality
    - (image pipeline, ML approach) 
#### Method
- Requirements were considered for technical implementation
- Initial architecture concept was elaborated
- Idea-driven approach
- Advantage
    - Challenges were visible soon trough early implementation
    - Gruduel appearance to closer
    - Useful when requirements are unknown
    - Participatory design
### Division of tasks
- Software architecture modules defined task division
- Nils (Architect & Git advisor):
    - General python system scaffold
    - Slack chatbot integration
- Jörn (Classifai and banana showcase setup):
    - Classifai module integration
    - Banana edibility dataset
- Chris
    - Database design
    - User Interface
- Liuba
    - Data annotation
- Melanie
    - Meeting minutes
    - Architecture drawings
### Communication:
- Meeting, every Tuesday, 6pm
    - Status reports
    - Peer reviews
    - Testing
- Slack messenger channel
    - Coordination within team and external members
    - GitHub integration for automatic commit notifications
    - Notifications for our Chat-Bot solution
### Version control
- Github for version control
- One master branch
    - Subbranches for every module
    - Merging, once branches reached final states
- Kanban board for progress tracking
- Issue tracker

## Requirements

- what has been built (high level)
- what features exist (use cases)
- show possibilities to add features


## System Architecture

### Main patterns
- MVC pattern
- Client-server pattern
- Pipeline-and-filters pattern
- Minor: Reactor pattern

### MVC pattern
- Model: SQL-Database
- View: PHP website
- Controller: Python program

### Client-server pattern
- Slack
- Clarifai

### Pipeline-and-filters pattern
- Image processing pipeline
- List of processors


## Quality

### Joel Test
- source control (Git)
- bug database (issue tracker)
- fix bugs before writing new code
- schedule (Kanban board)
- spec (requirements; SDD too unspecific)
- working conditions (quiet, except in meetings)
- "continuous" testing


### misc
- refactoring
- code reviews
- coding standards (PEP8)
- training opportunities (wiki)


## Live Demo

- User Interface
- code artefacts


## dream big...

- what functionalities can be added in the future
