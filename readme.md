# Quick start
- Rename the `config/database.ini.copy` to `config/database.ini`.
- for Conda
    - run `conda env create -f conda_freeze.yaml`
- And you are ready to go!
    - run `python main.py`
- When it's done, check the `report` folder which has the
    - `{query name}_{average query time in ms}_{is Cold or Warm}` the report folder
        - `plan` : Postgresql's `EXPLAIN ANALYZE` report in json format for each run.
        - `conf.conf` : This run's under this conf.
        - `report.csv` : every times run statics in csv format.


