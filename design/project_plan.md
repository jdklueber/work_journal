# Project Plan

## Complete

1. Database Setup
   1. Entities created in SQLAlchemy.
   2. Alembic configured.
   3. Database created via Alembic.

2. Repositories

   1. CRUD functionality created and tested.

      * Journal

        * Create

        * Read

          * Last X entries (configured in config table)

          * Today

          * Yesterday

          * Last 2 Weeks (M-S, current week and prior.)

          * Arbitrary Time Range

          * Config
            * Create
            * Read
            * Update
            * Delete

3. UI
   1. Main Window
   2. Reports Window


Stretch Goal:  Configuration editor.  (Will use raw SQL or "autosetup" logic in the application for initial work.)