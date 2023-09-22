import logging
import logging as lg

class scrapLogger :
    """
    This is a logging class
    """
    @staticmethod
    def ineuron_scrap_logger():
        """
        Function to create custom logger, console handler and file handler
        :return: logger object
        """
        logger = lg.getLogger("SCRAP")
        logger.setLevel(lg.INFO)
        console_handler = lg.StreamHandler()
        file_handler = lg.FileHandler("log_file.log")
        formater = lg.Formatter("%(name)s - %(asctime)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formater)
        file_handler.setFormatter(formater)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        return logger
