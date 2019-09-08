This module solves a performance problem during the closing of the POS session.
What it does is split the original "Validate Closing & Post Entries" a quick
closing process and another cron process that runs periodically doing the heavy
work.
