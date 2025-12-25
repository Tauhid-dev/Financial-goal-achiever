# Build Rules (Hard Constraints)

## Execution Rules
- NEVER run code
- NEVER start servers
- NEVER run Docker
- NEVER install packages
- ONLY create files and source code

## Safety Rules
- NEVER store raw PDFs
- NEVER log sensitive data
- NEVER use real credentials
- NEVER connect to external APIs

## Coding Rules
- Prefer dataclasses
- Prefer pure functions
- Defensive parsing
- Clear STOP conditions must be respected

## Agent Behavior Rules
- Follow tasks sequentially
- Do not skip steps
- Do not invent features
- Do not optimize prematurely