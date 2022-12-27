""" Simple controller class for pyspark """
from typing import Dict, List, Optional

from pyspark.sql import DataFrame, SparkSession

from src.transfer import Transferer
from src.info import StatFunctions, WordFrequencies, DataBaseStatistics


class SparkController:
    """Wrapper for the pyspark class"""

    def __init__(self, config: Dict[str, str], log_level: str = "OFF") -> None:
        self.__db_url: str = config["db_url"]
        self.__properties: Dict[str, str] = {
            "user": config["user"],
            "password": config["password"],
        }
        self.__spark: Optional[SparkSession] = (
            SparkSession.builder.appName("ngram_analyzer")
            .master("local[*]")
            .config("spark.driver.extraClassPath", config["jdbc_driver"])
            .config("spark.driver.memory", "4g")
            .config("spark.executor.memory", "1g")
            .getOrCreate()
        )
        self.__spark.sparkContext.setLogLevel(log_level)

        self.__transferer: Optional[Transferer] = Transferer(
            self.__spark, self.__db_url, self.__properties
        )

        self.__wf: WordFrequencies = WordFrequencies(
            self.__spark, self.__db_url, self.__properties
        )

        self.__dbs: DataBaseStatistics = DataBaseStatistics(
            self.__spark, self.__db_url, self.__properties
        )

        self.__functions: Optional[StatFunctions] = StatFunctions(
            self.__spark, self.__db_url, self.__properties
        )

    def get_spark_session(self) -> Optional[SparkSession]:
        """Returns the spark session"""
        return self.__spark

    def close(self) -> None:
        """Closes the spark session"""
        if self.__spark is not None:
            self.__spark.stop()

    def transfer(self, paths: List[str]) -> None:
        """Transfers a list of files to the database"""
        for path in paths:
            if self.__transferer is not None:
                self.__transferer.transfer_textFile(path)

    def execute_sql(self, sql: str) -> Optional[DataFrame]:
        """Executes a SQL query"""
        if self.__spark is not None:
            word_df = self.__spark.read.jdbc(
                url=self.__db_url,
                table="word",
                properties=self.__properties,
            )
            occurence_df = self.__spark.read.jdbc(
                url=self.__db_url,
                table="occurence",
                properties=self.__properties,
            )

            word_df.createOrReplaceTempView("word")
            occurence_df.createOrReplaceTempView("occurence")
            return self.__spark.sql(sql)
        return None

    def print_word_frequencies(self, words: List[str], years: List[int]) -> None:
        self.__wf.print_word_frequencies(words, years)

    def plot_word_frequencies(self, words: List[str], years: List[int]) -> None:
        self.__wf.plot_word_frequencies(words, years)

    def print_db_statistics(self) -> None:
        self.__dbs.print_statistics()

    def hrc(self, duration: int) -> DataFrame:
        return self.__functions.hrc(duration)

    def pc(self, start_year: int, end_year: int) -> DataFrame:
        return self.__functions.pc(start_year, end_year)