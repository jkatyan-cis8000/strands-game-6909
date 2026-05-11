# ui layer

User-facing surfaces including CLI, web, and GUI implementations.

This layer contains all user interface code and handles user input/output.
UI code should be thin and delegate to the service layer for business logic.

May import from: `types`, `config`, `service`, `runtime`, `providers`, `ui` (self-imports allowed)
