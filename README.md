# group_4: NGRAM_ANALYZER

## Setup
- clone repo
- cd to ./group4
- init poetry environment ```poetry install```
- enter poetry environment ```python -m poetry shell```

## Interaction via CLI
- the following commands are run inside the poetry shell
- List command options: ```main.py -h```
- Create database: ```main.py --create-db --username username --password password --dbname database_name```
  - Alternatively, you can provide the path to a config file using the ```--config_path``` option
  - Each user can only create one database on the local machine
  - To create the database with a different name, manually delete your configuration file from the ./settings directory
      - look for config_your_username.ini
      - this will not delete the actual database
- Transfer data from ./data into the database: ```main.py --transfer path_to_data --username username --password password --dbname database_name```
  - You can specify a path to the data folder by using ```--data_path```. If not, the default path from the config file will be used
  - Alternatively, you can provide the path to a config file using the ```--config_path``` option
- Enter shell version of the CLI: ```main.py --shell``` oder ```main.py```

## Interaction via Shell
The following commands are available within the ngram_analyzer shell:
- ```help``` or ```?``` shows commands
- ```sql``` opens a sql shell
  -  Example usage for user defined functions:
    - Highest relative change
      ```sql
      select hrc['str_rep'] word, hrc['type'] type, hrc['start_year'] start, hrc['end_year'] end, hrc['result'] hrc from (select hrc(3, *) hrc from schema_f)
      ```
      - Calculates the strongest relative change between any two years that duration (3 in above example) years apart
    - Pearson correlation coefficient of two time series
      ```sql
      select pc['str_rep_1'] word_1, pc['type_1'] type_1, pc['str_rep_2'] word_2, pc['type_2'] type_2, pc['start_year'] start, pc['end_year'] end, pc['result'] pearson_corr from (select pc(1990, 2000, *) pc from schema_f a cross join schema_f b where a.str_rep != b.str_rep)
      ```
      - Calculates the Pearson correlation coefficient of two time series (limited to the time period of [start year, end year])
    - linear regression for a given time series: `select lr(*) lr from (select * from schema_f limit 1)`
      - Calculates the linear regression for a given time series from schema f
- ```plot_word_frequencies``` plotting frequency of words against each other for a set of years
- ```print_db_statistics``` prints count for each table, highest frequency and number of years
- ```print_word_frequencies``` prints a table of the word frequencies in different years for different words
    - user is prompted to give the words and years
- ```plot_scatter``` plotting the frequency as scatter of all words in certain years
- ```plot_boxplot``` plotting boxplot of all words in certain years
- ```plot_scatter_with_regression``` plotting the frequency as scatter of all words in certain years and the regression line of each word
- ```plot_kde``` plotting the Kernel Density Estimation with Gauss-Kernel of a word
